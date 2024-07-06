from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.utils import secure_filename
from retinaface import RetinaFace
from PIL import Image
import face_recognition
import os
from scipy.spatial.distance import cosine
import cv2
import math
import csv
import pandas as pd

app = Flask(__name__)

app.secret_key = 'thisissecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '9619528836'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)

app.config['UPLOAD_FOLDER'] = 'content/test_image/'

def process_uploaded_image(file_path):
    resp = RetinaFace.detect_faces("content/test_image/testimage.jpg")
    faces = RetinaFace.extract_faces(img_path="content/test_image/testimage.jpg", align=True)

    output_directory = "content/cropped_faces"
    os.makedirs(output_directory, exist_ok=True)

    matches = []

    for i, face in enumerate(faces):
        output_path = os.path.join(output_directory, f"face_{i}.jpg")
        cv2.imwrite(output_path, cv2.cvtColor(face, cv2.COLOR_RGB2BGR))

    # Load the face encodings from the sample_images folder
    sample_images_encodings = []
    sample_images_filenames = []

    sample_images_folder = "content/sample_images/"
    for filename in os.listdir(sample_images_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(sample_images_folder, filename)
            img = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(img)
            if len(encoding) > 0:
                sample_images_encodings.append(encoding[0])
                sample_images_filenames.append(filename)

    # Load the face images from the cropped_faces folder
    cropped_faces_folder = "content/cropped_faces/"
    matched_samples = set()

    # Display the number of detected faces
    print(f"Number of detected faces: {len(faces)}")

    # Remove the code for displaying cropped faces

    total_faces = len(faces)
    correct_matches = 0

    for i, face in enumerate(faces):
        # Face recognition and accuracy calculation
        filename = f"face_{i}.jpg"
        image_path = os.path.join(cropped_faces_folder, filename)
        img = face_recognition.load_image_file(image_path)
        unknown_encoding = face_recognition.face_encodings(img)

        if len(unknown_encoding) == 0:
            # matches.append(f"No face found in face_{i}.jpg")
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

            if os.path.exists('content/test_image/testimage.jpg'):
                os.remove('content/test_image/testimage.jpg')

        if best_match_index is not None:
            matched_samples.add(best_match_index)
            matches.append(f"{sample_images_filenames[best_match_index]}")
        # else:
        #     matches.append(f"No match found for {filename}")

    return matches

@app.route('/', methods =['GET', 'POST'])
@app.route('/login', methods =['GET', 'POST'])
def  login():
     message=''
     if request.method == 'POST' and 'username' in request.form and 'phone' in request.form and 'password_' in request.form:
        username = request.form['username']
        phone = request.form['phone']
        password_ = request.form['password_']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND phone = %s AND password_ = %s', (username, phone, password_))
        user = cursor.fetchone()
        if user:
            if user['password_']==password_:
                return render_template('admin-home.html', message = message)
        else:
            message =  "Incorrect username/password!"
     return render_template('login.html', message=message)

@app.route('/signup', methods =['GET', 'POST'])
def  signup():
     message = ''
     if request.method == 'POST' and 'username' in request.form and 'phone' in request.form and 'password_' in request.form:
        username = request.form['username']
        phone = request.form['phone']
        password_ = request.form['password_']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username LIKE %s", [username])
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not username or not password_ or not phone:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, phone, password_))
            mysql.connection.commit()
            message = 'You have successfully registered! '
            return render_template('login.html', message = message)
     elif request.method == 'POST':
        message = "Please fill out the form!"
     return render_template('signup.html', title="Sign Up")

# @app.route('/')
# def upload_file():
#     return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_filename = 'testimage.jpg'
        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        
        # Process the uploaded image
        matches = process_uploaded_image(file_path)
        # matches=['220001001.png','220001066.png']
        for i in range(len(matches)):
            matches[i]=matches[i][0:-4]

            print(matches)

    csv_filename = r'content\matches.csv'  # Name for the CSV file
    csv_file_path = r'content\matches.csv'  # Path for the CSV file

    print(csv_filename)
    print(csv_file_path)

    # present_students_file = 'present_students.csv'  # File containing present students
    attendance_register_file = 'attendance_register.csv'  # Attendance register file to create
    attendance_register_file_path = f'content/{attendance_register_file}'

    # Load the present students from present_students.csv
    present_students = set()
    with open(r'content\matches.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            present_students.add(row[0])  # Assuming the first column contains student names

    # All students' names
    all_students = [
    '220001001', '220001002', '220001003', '220001004', '220001005',
    '220001006', '220001007', '220001008', '220001009', '220001010',
    '220001011', '220001012', '220001013', '220001014', '220001015',
    '220001016', '220001017', '220001018', '220001019', '220001020',
    '220001021', '220001022', '220001023', '220001024', '220001025',
    '220001026', '220001027', '220001028', '220001029', '220001030',
    '220001031', '220001032', '220001033', '220001034', '220001035',
    '220001036', '220001037', '220001038', '220001039', '220001040',
    '220001041', '220001042', '220001043', '220001044', '220001045',
    '220001046', '220001047', '220001048', '220001049', '220001050',
    '220001051', '220001052', '220001053', '220001054', '220001055',
    '220001056', '220001057', '220001058', '220001059', '220001060',
    '220001061', '220001062', '220001063', '220001064', '220001065',
    '220001066', '220001067', '220001068', '220001069', '220001070',
    '220001071', '220001072', '220001073', '220001074', '220001075',
    '220001076', '220001077', '220001078', '220001079', '220001080',
    '220001081', '220001082', '220002018', '220002029', '220002063',
    '220002081']

  # Replace with your student names

    # Create attendance register and mark 'Present' for present students
    with open(r'content\attendance_register.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Student Name', 'Status'])  # Header
        for student in all_students:
            status = 'Present' if student in present_students else 'Absent'  # Mark 'Present' if student is present
            writer.writerow([student, status])

    l=[None]*len(all_students)

    for i in range(len(all_students)):
        if all_students[i] in matches:
            l[i]="Present"
        else:
            l[i]="Absent"
    
    print(l)

    d=pd.DataFrame(
        {
            "Students":all_students,
            "Attendance":l
        }
    )

    d.to_csv('z.csv')

    # Send the created attendance register as a response for download
    return send_file(r'z.csv', as_attachment=True)

# csv_filename = 'matches.csv'  # Name for the CSV file
# csv_file_path = f'content/{csv_filename}'

# attendance_register_file = 'attendance_register.csv'  # Attendance register file to create
# attendance_register_file_path = f'content/{attendance_register_file}'

# with open(csv_file_path, 'w', newline='') as file:
#     pass

# with open(attendance_register_file_path, 'w', newline='') as file:
#     pass

if __name__ == '__main__':
    app.run(debug=True)

