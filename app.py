from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
import face_recognition
import numpy as np
import time  # Para generar nombres únicos

app = Flask(__name__)
app.secret_key = "12345"
app.config["UPLOAD_FOLDER"] = "static/uploads"

# 🧩 Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'face_recognition_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Crear carpeta de uploads si no existe
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ==========================
# Función para detectar duplicados
# ==========================
def is_duplicate(unknown_image_path, known_faces, known_names, tolerance=0.5):
    unknown_img = face_recognition.load_image_file(unknown_image_path)
    unknown_encodings = face_recognition.face_encodings(unknown_img)

    if len(unknown_encodings) == 0:
        return None  # no hay rostro

    unknown_encoding = unknown_encodings[0]

    if known_faces:
        distances = face_recognition.face_distance(known_faces, unknown_encoding)
        min_distance_index = np.argmin(distances)
        if distances[min_distance_index] <= tolerance:
            return known_names[min_distance_index]  # ya existe

    return None  # no duplicado

# ==========================
# Rutas de la app
# ==========================
@app.route("/")
def index():
    return render_template("index.html")

# 🧍 Registrar usuario con foto
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["nombre"]
        email = request.form.get("email", "")
        foto = request.files["foto"]

        # Guardar temporalmente la foto
        temp_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp_" + foto.filename)
        foto.save(temp_path)

        # Cargar rostros conocidos desde la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, image_path FROM users")
        empleados = cur.fetchall()
        cur.close()

        known_faces = []
        known_names = []
        for empleado in empleados:
            try:
                face_img = face_recognition.load_image_file(empleado["image_path"])
                encoding = face_recognition.face_encodings(face_img)[0]
                known_faces.append(encoding)
                known_names.append(empleado["name"])
            except:
                continue

        # Verificar duplicados
        existing_name = is_duplicate(temp_path, known_faces, known_names, tolerance=0.5)
        if existing_name:
            os.remove(temp_path)
            flash(f"Esta persona ya está registrada como: {existing_name}", "warning")
            return redirect(url_for("register"))

        # Guardar foto final con nombre único
        name_file, ext = os.path.splitext(foto.filename)
        final_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{name_file}_{int(time.time())}{ext}")
        os.rename(temp_path, final_path)

        # Guardar en MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, image_path) VALUES (%s, %s, %s)", (name, email, final_path))
        mysql.connection.commit()
        cur.close()

        flash("Empleado registrado correctamente ✅", "success")
        return redirect(url_for("register"))

    return render_template("register.html")

# 🧠 Reconocer rostro
@app.route("/recognize", methods=["POST"])
def recognize():
    foto = request.files.get("foto")
    if not foto:
        flash("Debes subir una foto", "danger")
        return redirect(url_for("index"))

    path = os.path.join(app.config["UPLOAD_FOLDER"], foto.filename)
    foto.save(path)

    # Cargar empleados registrados
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, image_path FROM users")
    empleados = cur.fetchall()
    cur.close()

    known_faces = []
    known_names = []

    for empleado in empleados:
        try:
            face_img = face_recognition.load_image_file(empleado["image_path"])
            encoding = face_recognition.face_encodings(face_img)[0]
            known_faces.append(encoding)
            known_names.append(empleado["name"])
        except:
            continue

    # Comparar rostro
    nombre_reconocido = is_duplicate(path, known_faces, known_names, tolerance=0.5)
    if not nombre_reconocido:
        nombre_reconocido = "No encontrado 😕"

    return render_template("result.html", nombre=nombre_reconocido)

# 👀 Ver empleados registrados
@app.route("/empleados")
def empleados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    empleados = cur.fetchall()
    cur.close()
    return render_template("empleados.html", empleados=empleados)

# ==========================
# Ejecutar app
# ==========================
if __name__ == "__main__":
    app.run(debug=True)
