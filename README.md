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
