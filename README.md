# Sistema de Reconocimiento Facial con Flask 🎯

Sistema web de reconocimiento facial desarrollado con Flask, MySQL y la librería `face-recognition`. Permite registrar empleados con sus fotografías y reconocerlos posteriormente mediante comparación de encodings faciales.

## 📋 Características

- ✅ Registro de empleados con foto, nombre y email
- 🔍 Reconocimiento facial en tiempo real
- 🚫 Detección automática de duplicados al registrar
- 📊 Visualización de empleados registrados
- 💾 Almacenamiento en MySQL
- 🎨 Interfaz Bootstrap responsiva
- 🔔 Alertas con SweetAlert2

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask, Flask-MySQLdb
- **Reconocimiento Facial**: face_recognition, dlib
- **Base de Datos**: MySQL
- **Frontend**: HTML5, Bootstrap 5, SweetAlert2
- **Procesamiento**: NumPy, OpenCV

## 📦 Requisitos Previos

- Python 3.7+
- MySQL Server
- CMake (requerido para dlib)
- Visual Studio Build Tools (en Windows)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd face-recognition-system
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**
```
Flask==2.3.0
Flask-MySQLdb==1.0.1
face-recognition==1.3.0
numpy==1.24.0
Pillow==10.0.0
```

### 4. Configurar MySQL

Crea la base de datos y tabla:

```sql
CREATE DATABASE face_recognition_db;

USE face_recognition_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    image_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Configurar la aplicación

Edita `app.py` con tus credenciales de MySQL:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña'
app.config['MYSQL_DB'] = 'face_recognition_db'
```

## 🎮 Uso

### Iniciar el servidor

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

### Funcionalidades

#### 1️⃣ **Registrar Empleado**
- Accede a `/register`
- Completa el formulario con nombre, email y foto
- El sistema detectará automáticamente si la persona ya está registrada
- Tolerancia de similitud: 0.5 (ajustable)

#### 2️⃣ **Reconocer Rostro**
- Desde la página principal, sube una foto
- El sistema comparará con todos los rostros registrados
- Mostrará el nombre del empleado o "No encontrado"

#### 3️⃣ **Ver Empleados**
- Accede a `/empleados`
- Visualiza la lista completa con fotos

## 📁 Estructura del Proyecto

```
face-recognition-system/
│
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias
│
├── static/
│   └── uploads/               # Imágenes de empleados
│       ├── prueba1.jpg
│       ├── prueba2.jpeg
│       └── ...
│
├── templates/
│   ├── index.html             # Página principal
│   ├── register.html          # Formulario de registro
│   ├── empleados.html         # Lista de empleados
│   └── result.html            # Resultado del reconocimiento
│
└── models/
    └── face_utils.py          # Funciones auxiliares (opcional)
```

## 🔧 Funciones Principales

### `is_duplicate()`
Verifica si un rostro ya está registrado en la base de datos.

```python
def is_duplicate(unknown_image_path, known_faces, known_names, tolerance=0.5):
    # Compara el encoding facial con los registrados
    # Retorna el nombre si existe, None si no
```

**Parámetros:**
- `tolerance`: Umbral de similitud (menor = más estricto)
  - 0.4: Muy estricto
  - 0.5: Recomendado (por defecto)
  - 0.6: Más permisivo

### `load_known_faces()`
Carga todos los rostros desde una carpeta.

```python
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
```

### `recognize_face()`
Reconoce un rostro desconocido comparándolo con los conocidos.

```python
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
```

## ⚙️ Configuración Avanzada

### Ajustar precisión del reconocimiento

En `app.py`, modifica el parámetro `tolerance`:

```python
# Más estricto (menos falsos positivos)
is_duplicate(temp_path, known_faces, known_names, tolerance=0.4)

# Más permisivo (menos falsos negativos)
is_duplicate(temp_path, known_faces, known_names, tolerance=0.6)
```

### Cambiar carpeta de uploads

```python
app.config["UPLOAD_FOLDER"] = "ruta/personalizada"
```

## 🐛 Solución de Problemas

### Error al instalar `face_recognition`

**Windows:**
```bash
pip install cmake
pip install dlib
pip install face_recognition
```

**Linux/Mac:**
```bash
sudo apt-get install cmake
pip install dlib
pip install face_recognition
```

### Error de conexión MySQL

Verifica que MySQL esté corriendo:
```bash
# Windows
net start mysql

# Linux/Mac
sudo service mysql start
```

### No detecta rostros

- Asegúrate de que la imagen tenga buena iluminación
- La cara debe estar visible y no muy inclinada
- Usa imágenes con resolución mínima de 640x480

## 📊 Base de Datos

### Esquema de la tabla `users`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT | ID único (auto-increment) |
| name | VARCHAR(255) | Nombre del empleado |
| email | VARCHAR(255) | Email (opcional) |
| image_path | VARCHAR(500) | Ruta de la imagen |
| created_at | TIMESTAMP | Fecha de registro |

## 🔒 Seguridad

- **Cambiar `secret_key`**: Usa una clave segura en producción
- **Validación de archivos**: Solo permite imágenes (jpg, png)
- **Sanitización**: Nombres de archivo únicos con timestamp

## 🚀 Despliegue en Producción

1. Desactiva el modo debug:
```python
app.run(debug=False)
```

2. Usa un servidor WSGI como Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

3. Configura variables de entorno para credenciales sensibles

## 📝 Licencia

Este proyecto es de código abierto. Siéntete libre de usarlo y modificarlo.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando Flask y Face Recognition**
