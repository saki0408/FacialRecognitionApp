# FacialRecognitionApp

This project is a Python script that performs face recognition using the RetinaFace model for face detection and the face_recognition library for encoding and comparing faces. The script detects faces in an input image, extracts them, and matches them with known individuals from a set of sample images.

Features

Face Detection: Utilizes the RetinaFace model to accurately detect faces in the input image.
Face Recognition: Matches the detected faces with known individuals from a set of sample images using cosine similarity.
Cropped Faces: Saves the extracted faces as individual images for further analysis or visualization.
Customizable: The script can be customized for specific use cases, such as incorporating ground truth information for evaluation.
Installation

Clone the repository:

git clone https://github.com/your-username/face-recognition-project.git

cd face-recognition-project

Install dependencies:

pip install -r requirements.txt

Usage

Place the input image for face recognition in the /content directory.

Create a folder named sample_images and add sample images of known individuals to this folder.

Run the script:

python face_recognition_script.py

The script will detect faces, save cropped faces, and match them with sample images, printing the results to the console.

Documentation

For detailed documentation, including algorithm overview, code structure, customization options, and performance considerations, refer to Documentation.
