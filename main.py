from flask import Flask, render_template, request, jsonify, session
import sqlite3

app = Flask(__name__)

app.secret_key = 'esto-es-una-clave-muy-secreta'

@app.route('/')
def index():
    return render_template('probandoFormulario.html')

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
    return ("Funciono")

@app.route('/meli2')
def meli2():
    return render_template('probandoPerfiles.html')

@app.route('/cargarPerfiles', methods=["GET", "POST"])
def cargarPerfiles():
  if request.method == "POST":
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    raza = request.form["raza"]
    tamaño = request.form["tamaño"]
    informacion = request.form["informacion"]
    imagen = request.form["imagen"]
    return ("Funciono")

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
      
      if lista[0] != session['usuario']  or lista[1] != session['contraseña']:
        mensaje = 'Los datos ingresados son incorrectos'
        return render_template('probandoFormulario.html', mensaje = mensaje)
      conn.commit()      
      conn.close()
      print(session['usuario'])
      print(session['contraseña'])
      print("Funciona el formulario refugio")
      return render_template('home.html')
  else:
    return render_template('home2.html')



"""
"""
app.run(host='0.0.0.0', port=81)
