from retinaface import RetinaFace
from PIL import Image
import face_recognition
import os
import cv2
from scipy.spatial.distance import cosine
from matplotlib import pyplot as plt
import math

def get_ground_truth(filename):
    # Replace this function with your logic to get ground truth for each face in the test image
    # For example, you might have a mapping of filenames to ground truth identities
    # Return None if ground truth is not available for a particular face
    pass

resp = RetinaFace.detect_faces("/content/test_5.jpg")
faces = RetinaFace.extract_faces(img_path="/content/test_5.jpg", align=True)

output_directory = "/content/cropped_faces"
os.makedirs(output_directory, exist_ok=True)
for i, face in enumerate(faces):
    output_path = os.path.join(output_directory, f"face_{i}.jpg")
    cv2.imwrite(output_path, cv2.cvtColor(face, cv2.COLOR_RGB2BGR))

# Load the face encodings from the sample_images folder
sample_images_encodings = []
sample_images_filenames = []

sample_images_folder = "/content/sample_images/"
for filename in os.listdir(sample_images_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(sample_images_folder, filename)
        img = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(img)
        if len(encoding) > 0:
            sample_images_encodings.append(encoding[0])
            sample_images_filenames.append(filename)

# Load the face images from the cropped_faces folder
cropped_faces_folder = "/content/cropped_faces/"
matched_samples = set()

# Display the number of detected faces
print(f"Number of detected faces: {len(faces)}")
plt.tight_layout()
plt.show()

# Display each cropped face in rows of three
num_cols = 3
num_rows = math.ceil(len(faces) / num_cols)

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

total_faces = len(faces)
correct_matches = 0

for i, face in enumerate(faces):
    row = i // num_cols
    col = i % num_cols
    ax = axes[row, col] if num_rows > 1 else axes[col]
    ax.imshow(face)
    ax.axis("off")
    ax.set_title(f"Face {i+1}")

    # Face recognition and accuracy calculation
    filename = f"face_{i}.jpg"
    image_path = os.path.join(cropped_faces_folder, filename)
    img = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(img)

    if len(unknown_encoding) == 0:
        print(f"No face found in {filename}")
        continue

    # Compare the unknown face encoding with the encodings from the sample_images using cosine distance
    best_similarity = 0.0  # Initialize with the lowest possible similarity
    best_match_index = None

    for j, sample_encoding in enumerate(sample_images_encodings):
        if j in matched_samples:
            continue  # Skip already matched samples
        similarity = 1 - cosine(sample_encoding, unknown_encoding[0])
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_index = j

    if best_match_index is not None:
        matched_samples.add(best_match_index)
        print(f"Face in {filename} matches with {sample_images_filenames[best_match_index]} (Cosine Similarity: {best_similarity})")
    else:
        print(f"No match found for {filename}")
