import os
import shutil
import sys
import argparse
from typing import List, Union
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tqdm import tqdm
import face_recognition
import numpy as np

def validate_paths(paths: List[str]) -> List[str]:
    """
    Validate and normalize file paths.

    Args:
        paths (List[str]): List of file paths to validate

    Returns:
        List[str]: List of validated, absolute paths
    """
    valid_paths = []
    for path in paths:
        # Expand user home directory and get absolute path
        expanded_path = os.path.expanduser(path)
        abs_path = os.path.abspath(expanded_path)

        if not os.path.exists(abs_path):
            print(f"Warning: Path does not exist - {abs_path}")
            continue

        valid_paths.append(abs_path)

    return valid_paths

def load_reference_faces(reference_image_paths: List[str]) -> List[np.ndarray]:
    """
    Load reference face encodings from given image paths with user-friendly error handling.

    Args:
        reference_image_paths (List[str]): Paths to reference images

    Returns:
        List[np.ndarray]: List of face encodings for reference faces
    """
    reference_encodings = []
    for ref_path in reference_image_paths:
        try:
            ref_image = face_recognition.load_image_file(ref_path)
            ref_encoding = face_recognition.face_encodings(ref_image)

            if ref_encoding:
                reference_encodings.append(ref_encoding[0])
                print(f"Successfully loaded reference face from: {ref_path}")
            else:
                print(f"⚠️ No face detected in reference image: {ref_path}")
        except Exception as e:
            print(f"❌ Error processing reference image {ref_path}: {e}")

    return reference_encodings

def find_and_save_matching_faces(
        album_path: str,
        output_folder: str,
        reference_image_paths: List[str],
        tolerance: float = 0.6,
        file_extensions: Union[List[str], None] = None
) -> int:
    """
    Find and save images containing faces matching reference faces with enhanced user feedback.

    Args:
        album_path (str): Path to the folder containing images to search
        output_folder (str): Path to save matched images
        reference_image_paths (List[str]): Paths to reference images
        tolerance (float, optional): Face matching tolerance. Defaults to 0.6.
        file_extensions (List[str], optional): Allowed file extensions. Defaults to image extensions.

    Returns:
        int: Number of matched images
    """
    # Validate and create output folder
    output_folder = os.path.abspath(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    # Load reference face encodings
    reference_encodings = load_reference_faces(reference_image_paths)

    if not reference_encodings:
        print("❌ No valid reference faces found. Cannot proceed.")
        return 0

    # Default file extensions if not provided
    if file_extensions is None:
        file_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    # Normalize extensions to lowercase
    file_extensions = [ext.lower() for ext in file_extensions]

    # Find image files
    try:
        image_files = [
            f for f in os.listdir(album_path)
            if os.path.splitext(f.lower())[1] in file_extensions
        ]
    except PermissionError:
        print(f"❌ Permission denied. Cannot access directory: {album_path}")
        return 0

    if not image_files:
        print(f"❌ No images found in {album_path} with specified extensions.")
        return 0

    print(f"📸 Searching through {len(image_files)} images...")

    matched_images = 0
    skipped_images = 0

    # Search for matching faces
    for filename in tqdm(image_files, desc="🔍 Searching for faces"):
        img_path = os.path.join(album_path, filename)

        try:
            # Load image and find face locations
            image = face_recognition.load_image_file(img_path)
            face_locations = face_recognition.face_locations(image)

            if face_locations:
                # Compute face encodings for detected faces
                face_encodings = face_recognition.face_encodings(image, face_locations)

                # Compare each detected face with reference faces
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        reference_encodings,
                        face_encoding,
                        tolerance=tolerance
                    )

                    if any(matches):
                        output_path = os.path.join(output_folder, filename)
                        shutil.copy2(img_path, output_path)
                        matched_images += 1
                        break  # Move to next image after finding a match
            else:
                skipped_images += 1

        except Exception as e:
            print(f"❌ Error processing image {filename}: {e}")
            skipped_images += 1

    # Print comprehensive results
    print("\n📊 Search Results:")
    print(f"✅ Found {matched_images} images with matching faces")
    print(f"⏩ Skipped {skipped_images} images with no detectable faces")
    print(f"📁 Matched images saved to: {output_folder}")

    return matched_images

def gui_select_folder(prompt: str) -> str:
    """
    Open a file dialog to select a folder with a custom prompt.

    Args:
        prompt (str): Dialog prompt text

    Returns:
        str: Selected folder path
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title=prompt)
    return folder_path

def gui_select_files(prompt: str) -> List[str]:
    """
    Open a file dialog to select multiple image files.

    Args:
        prompt (str): Dialog prompt text

    Returns:
        List[str]: List of selected file paths
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(
        title=prompt,
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
    )
    return list(file_paths)

def interactive_mode():
    """
    Interactive mode for user-friendly face matching process.
    """
    print("🕵️ Face Matching Image Finder 🖼️")
    print("----------------------------")

    # Select album folder
    print("\n1. Select Album Folder")
    album_path = gui_select_folder("Select folder with images to search")
    if not album_path:
        print("❌ No folder selected. Exiting.")
        return

    # Select output folder
    print("\n2. Select Output Folder")
    output_folder = gui_select_folder("Select folder to save matched images")
    if not output_folder:
        print("❌ No output folder selected. Exiting.")
        return

    # Select reference images
    print("\n3. Select Reference Images")
    reference_images = gui_select_files("Select reference images with faces")
    if not reference_images:
        print("❌ No reference images selected. Exiting.")
        return

    # Ask for tolerance
    tolerance = simpledialog.askfloat(
        "Matching Tolerance",
        "Enter face matching tolerance (0.4-1.0, lower is stricter):",
        initialvalue=0.6,
        minvalue=0.4,
        maxvalue=1.0
    ) or 0.6

    # Perform face matching
    matched_count = find_and_save_matching_faces(
        album_path,
        output_folder,
        reference_images,
        tolerance=tolerance
    )

    # Show completion message
    if matched_count > 0:
        tk.messagebox.showinfo(
            "Search Complete",
            f"Found {matched_count} images with matching faces!\n"
            f"Saved to: {output_folder}"
        )
    else:
        tk.messagebox.showwarning(
            "Search Complete",
            "No matching faces were found in the album."
        )

def main():
    """
    Main entry point with support for both CLI and interactive modes.
    """
    if len(sys.argv) > 1:
        # Command-line mode
        parser = argparse.ArgumentParser(description='Find images with specific faces')
        parser.add_argument('album_path', help='Path to the folder containing images to search')
        parser.add_argument('output_folder', help='Path to save matched images')
        parser.add_argument('reference_images', nargs='+', help='Paths to reference images')
        parser.add_argument('--tolerance', type=float, default=0.6,
                            help='Face matching tolerance (lower is stricter, default: 0.6)')
        parser.add_argument('--extensions', nargs='+',
                            default=['.jpg', '.jpeg', '.png', '.bmp', '.gif'],
                            help='Allowed file extensions (with dot)')

        args = parser.parse_args()

        # Validate paths before processing
        album_path = validate_paths([args.album_path])[0]
        output_folder = validate_paths([args.output_folder])[0]
        reference_images = validate_paths(args.reference_images)

        find_and_save_matching_faces(
            album_path,
            output_folder,
            reference_images,
            tolerance=args.tolerance,
            file_extensions=args.extensions
        )
    else:
        # Interactive mode
        interactive_mode()

if __name__ == '__main__':
    main()

# Optional dependencies note
print("Note: Ensure you have the following libraries installed:")
print("pip install face_recognition tqdm")
print("\nOptional ways to run:")
print("1. CLI Mode: python script.py /album/path /output/path /ref1.jpg /ref2.jpg")
print("2. Interactive Mode: python script.py")