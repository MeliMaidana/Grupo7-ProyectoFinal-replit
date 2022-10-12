from flask import Flask, render_template, request, jsonify, session , current_app
import sqlite3, os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './media'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
path = './media'
path2 = 'img'

app = Flask(__name__)

# Define the application directory
# BASE_DIR = dirname(dirname(abspath(__file__)))
# Media dir
# MEDIA_DIR = join(BASE_DIR, 'media')
# POSTS_IMAGES_DIR = join(MEDIA_DIR, 'posts')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'esto-es-una-clave-muy-secreta'


@app.route('/')
def index():
    return render_template('probandoPerfiles.html')

@app.route('/celes')
def celes():
    return render_template('home.html')
@app.route('/celes2')
def Inicio():
    return render_template('inicio.html')
@app.route('/celes3')
def mision():
    return render_template('mision.html')
@app.route('/celes4')
def AdoptaGatos():
    return render_template('AdoptaGatos2.html')
@app.route('/celes5')
def AdoptaPerros():
    return render_template('AdoptaPerros.html')
@app.route('/celes6')
def adoptame():
    return render_template('adoptame.html')
@app.route('/celes7')
def Refugio():
    return render_template('Refugio.html')


@app.route('/meli')
def meli():
  return render_template('probando.html')
  
@app.route('/formulario', methods=["GET", "POST"])
def formulario():
  if request.method == "POST":
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    dni = request.form["dni"]
    mail = request.form["mail"]
    telefono = request.form["telefono"]
    direccion = request.form["direccion"]
    hogar = request.form["hogar"]
    mascotas = request.form["mascotas"]
    convivientes = request.form["convivientes"]

    print('Formulario enviado')
    return render_template('inicio.html')

@app.route('/meli2')
def meli2():
    return render_template('probandoPerfiles.html')

@app.route('/cargarPerfiles', methods=["GET", "POST"])
def cargarPerfiles():
  if (request.method == "POST"):
    nombre = request.form["nombre"]
    sexo = request.form["sexo"]
    edad = request.form["edad"]
    raza = request.form["raza"]
    tamaño = request.form["tamaño"]
    informacion = request.form["informacion"]
    file = request.files['imagen']

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    print(file_path)

    print(request.form.get('animal'))
    
    if request.form.get('animal') == 'perro':
      animal = "Perros"
    elif request.form.get('animal') == 'gato':
      animal = "Gatos"
    else:
      mensaje = "¡Elija un checkbox!"
      print(mensaje)
      return render_template('probandoPerfiles.html',
                             mensaje = mensaje)
    
    
    
    conn = sqlite3.connect('tabla.db')
    q = f"""SELECT imagen FROM Gatos WHERE imagen = '{file_path}'"""
    resu = conn.execute(q)
    p = f"""SELECT imagen FROM Perros WHERE imagen = '{file_path}'"""
    resuP = conn.execute(p)

    if resu.fetchone():
      print('Por favor renombre el archivo, el anterior ya existe.')
      return render_template('probandoPerfiles.html')
    elif resuP.fetchone():
      print('Por favor renombre el archivo, el anterior ya existe.')
      return render_template('probandoPerfiles.html')
    else:  
      r = f"""INSERT INTO '{animal}' (nombre, sexo, edad, raza, tamaño, informacion, imagen) VALUES ('{nombre}', '{sexo}', '{edad}', '{raza}', '{tamaño}', '{informacion}', '{file_path}');"""
      conn.execute(r)
      conn.commit()
      conn.close()
    
    return render_template('base.html')

@app.route('/saludo', methods=["GET", "POST"])
def irAHome():
  return render_template('home.html')
  
@app.route('/refugio', methods=["GET", "POST"])
def refugio():
  if request.method == "POST":
    if (request.form["usuario"] != "" and request.form["password"] != ""):
      session['usuario'] = request.form["usuario"]
      session['contraseña'] = request.form["password"]
      conn = sqlite3.connect('tabla.db')
      q = f"""SELECT * FROM Refugio WHERE usuario = '{session['usuario']}' and contraseña = '{session['contraseña']}'"""
      resu = conn.execute(q)
      lista = resu.fetchall()
      if lista[0] != session['usuario'] or lista[1] != session['contraseña']:
        mensaje = 'Los datos ingresados son incorrectos'
        return render_template('probandoFormulario.html', mensaje = mensaje)
      conn.commit()      
      conn.close()
      print(session['usuario'])
      print(session['contraseña'])
      print("Funciona el formulario refugio")
  else:
    return render_template('home2.html')

@app.route('/tha')
def borrarPerfil():
  return render_template('borrarPerfil.html')

"""
    sexo = request.form["sexo"]
    edad = request.form["edad"]
    raza = request.form["raza"]
    tamaño = request.form["tamaño"]
    informacion = request.form["informacion"]



    q = fSELECT imagen FROM Gatos WHERE imagen = '{file_path}'
    resu = conn.execute(q)
    p = fSELECT imagen FROM Perros WHERE imagen = '{file_path}'
    resuP = conn.execute(p)

    if resu.fetchone():
      print('Por favor renombre el archivo, el anterior ya existe.')
      return render_template('probandoPerfiles.html')
    elif resuP.fetchone():
      print('Por favor renombre el archivo, el anterior ya existe.')
      return render_template('probandoPerfiles.html')
    else:  
      r = f INSERT INTO Perros (imagen) VALUES ('{file_path}');
      conn.execute(r)
      conn.commit()
      conn.close()
"""
app.run(host='0.0.0.0', port=81)


