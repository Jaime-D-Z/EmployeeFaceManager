import face_recognition
import os
import numpy as np

def load_known_faces(folder="static/uploads"):
    known_faces = []
    known_names = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(folder, filename))
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                known_faces.append(encoding[0])
                known_names.append(filename.split(".")[0])
    return known_faces, known_names


def recognize_face(unknown_image_path, known_faces, known_names):
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if len(unknown_encodings) == 0:
        return "No se detectó ningún rostro."

    results = face_recognition.compare_faces(known_faces, unknown_encodings[0])
    if True in results:
        match_index = results.index(True)
        return known_names[match_index]
    else:
        return "Desconocido"
