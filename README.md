# FacialRecognitionApp

This project utilizes the RetinaFace model for face detection and the face_recognition library for face recognition. It can be used to identify faces in an input image and match them with known individuals from a set of sample images.

Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/face-recognition-project.git
cd face-recognition-project
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Usage
Place the input image for face recognition in the /content directory.
Create a folder named sample_images and add sample images of known individuals to this folder.
Run the script:
bash
Copy code
python face_recognition_script.py
The script will detect faces, save cropped faces, and match them with sample images, printing the results to the console.

For detailed documentation, refer to Documentation.

Contributing
Contributions are welcome. Fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
