## Project Description

The **"Find Images with My Face"** project is a computer vision application that detects and saves images from a given album that contain a specific face (e.g., your own face). Using the **face_recognition** library, the project compares face encodings between a reference image and images in the album. If a match is found, the image is copied to a specified output folder.

This project utilizes several powerful Python libraries including **OpenCV**, **face_recognition**, and **tqdm** to efficiently handle and process images for face detection and matching.

### Key Features:
- Detects faces in images using face recognition models.
- Compares detected faces with a reference face (such as your own face).
- Saves matching images to a specified folder.
- Supports multiple image formats (JPG, PNG, BMP, GIF, etc.).
- Provides real-time progress updates via `tqdm` while processing multiple images.

### Use Cases:
- Organize and collect images with specific people (e.g., finding pictures of you from a photo album).
- Face detection for any personalized computer vision task.
- Easy setup and integration for future applications involving face recognition.
# Find Images with My Face

This project detects and saves images from an album that contain a specific face (e.g., your face) by comparing face encodings.

## Requirements

- Python 3.x
- `face_recognition`
- `opencv-python`
- `numpy`
- `tqdm`
- `Pillow`

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/username/find-images-with-my-face.git
    cd find-images-with-my-face
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Prepare a folder of images you want to search for the reference face in.
2. Provide a path to the reference face image (e.g., your own image).
3. Run the script:
    ```bash
    python test.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
