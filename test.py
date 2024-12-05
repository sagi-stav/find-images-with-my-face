import cv2
import os
import shutil
from tqdm import tqdm
import face_recognition
import numpy as np

def find_and_save_specific_face(album_path, output_folder, reference_image_paths):
    os.makedirs(output_folder, exist_ok=True)

    # Load reference face(s) and compute embeddings
    reference_encodings = []
    for ref_path in reference_image_paths:
        ref_image = face_recognition.load_image_file(ref_path)
        ref_encoding = face_recognition.face_encodings(ref_image)
        if ref_encoding:
            reference_encodings.append(ref_encoding[0])
        else:
            print(f"No face found in reference image: {ref_path}")

    if not reference_encodings:
        print("No valid reference faces found")
        return

    matched_images = 0
    image_files = [f for f in os.listdir(album_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]

    for filename in tqdm(image_files, desc="Searching for faces"):
        img_path = os.path.join(album_path, filename)

        # Load image and find face locations
        image = face_recognition.load_image_file(img_path)
        face_locations = face_recognition.face_locations(image)

        if face_locations:
            # Compute face encodings for detected faces
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Compare each detected face with reference faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(reference_encodings, face_encoding, tolerance=0.6)

                if any(matches):
                    output_path = os.path.join(output_folder, filename)
                    shutil.copy2(img_path, output_path)
                    matched_images += 1
                    break  # Move to next image after finding a match

    print(f"\nFound {matched_images} images with matching faces")

# Set paths
album_path = r"C:\Users\97255\PycharmProjects\find_images_with_my_face\reception"
output_folder = r"C:\Users\97255\PycharmProjects\find_images_with_my_face\my_faces"
reference_image_paths = ["test.jpggit "]

# Run the function
find_and_save_specific_face(album_path, output_folder, reference_image_paths)