from flask import Flask, render_template, request, jsonify, session, current_app, redirect
import sqlite3, os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/media'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'esto-es-una-clave-muy-secreta'

@app.route('/')
def Index():
  session['perro'] = "."
  session['gato'] = "."
  session['sesion'] = False
  return render_template('inicio.html')
  
@app.route('/formularioAdopcion')
def formularioParaAdoptar():
    return render_template('formularioAdopcion.html')
  
@app.route('/nuestraMision')
def mision():
    return render_template('mision2.html')
  
@app.route('/adoptame')
def adoptame():
    return render_template('adoptame.html')

  
# CAMBIAR LOS NOMBRES DE LAS VARIABLES Y LAS RUTAS.
# BORRAR LAS RUTAS INECESARIAS.

  
@app.route('/maca1')
def maca():
  return render_template('Refugio.html')

@app.route('/maca2')
def meli():
  return render_template('formularioAdopcion.html')

@app.route('/maca3')
def maca3():
  return render_template('borrar.html')
  
@app.route('/formulario', methods=["GET", "POST"])
def formulario():
  if (request.method == "POST"):
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
  else:
    return render_template('formularioAdopcion.html')
    

@app.route('/cargarPerfiles', methods=["GET", "POST"])
def cargarPerfiles():
  if (request.method == "POST"):
    if session['sesion'] == True:
      nombre = request.form["nombre"]
      nombre = nombre.capitalize()
      sexo = request.form["sexo"]
      edad = request.form["edad"]
      raza = request.form["raza"]
      tamaño = request.form["tamaño"]
      informacion = request.form["informacion"]
      file = request.files['imagen']
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      print(file_path)
      file.save(file_path)
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
        mensaje2 = "Por favor renombre el archivo, el anterior ya existe."
        return render_template('probandoPerfiles.html', mensaje2 = mensaje2)
      elif resuP.fetchone():
        mensaje2 = "Por favor renombre el archivo, el anterior ya existe."
        return render_template('probandoPerfiles.html', mensaje2 = mensaje2)
      else:  
        r = f"""INSERT INTO '{animal}' (nombre, sexo, edad, raza, tamaño, informacion, imagen) VALUES ('{nombre}', '{sexo}', '{edad}', '{raza}', '{tamaño}', '{informacion}', '{file_path}');"""
        conn.execute(r)
        conn.commit()
        conn.close()
      
      return render_template('probandoPerfiles.html')
    else:
      return redirect('/formularioRefugio')
    
  else:
    return render_template('probandoPerfiles.html')
    
@app.route('/saludo', methods=["GET", "POST"])
def irAHome():
  return render_template('home.html')

@app.route('/formularioRefugio', methods=["GET", "POST"])
def Refugio():
  if session['sesion'] == True:
    return redirect('/opcionesAdmin')
  else:
    return render_template('Refugio.html')

@app.route('/refugio', methods=["GET", "POST"])
def refugio():
  if (request.method == "POST"):
    if (request.form["usuario"] != "" or request.form["password"] != ""):
      session['sesion'] = True
      session['usuario'] = request.form["usuario"]
      session['contraseña'] = request.form["password"]
      conn = sqlite3.connect('tabla.db')
      q = f"""SELECT * FROM Refugio WHERE usuario = '{session['usuario']}' and contraseña = '{session['contraseña']}'"""
      resu = conn.execute(q)
      lista = resu.fetchall()
      if len(lista) != 0:
        if lista[0][0] != session['usuario'] or lista[0][1] != session['contraseña']:
          mensaje = 'Los datos ingresados son incorrectos'
          print('llega a formulario refugio 5')
          return render_template('Refugio.html', mensaje = mensaje)
      else:
        mensaje = 'Los datos ingresados son incorrectos'
        return render_template('Refugio.html', mensaje = mensaje)
      conn.commit()      
      conn.close()
      return render_template('opcionesAdministrador.html')
    else:
      mensaje = "Por favor rellene todos los campos"
      return render_template('Refugio.html', mensaje = mensaje)
      
  else:
    return render_template('Refugio.html')

@app.route('/borrar')
def borrar():
  
  if session['sesion'] == True:
    largoP = 0
    largo = 0
    return render_template('borrar.html', largo = largo, largoP = largoP)
  else:
    return redirect('/formularioRefugio')

@app.route('/opcionesBorrarGato',  methods=["GET", "POST"])
def opcionesBorrarGato():
  if (request.method == "POST"):
    if session['sesion'] == True:
      if (request.form["nombreGato"] != "" and session['perro'] == "."):
        animal = request.form["nombreGato"]
        conn = sqlite3.connect('tabla.db')
        animal = animal.capitalize()
        r = f"""SELECT nombre, imagen FROM Gatos where nombre = '{animal}'"""
        print(animal)
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreGatos = []
        imagenGatos = []
        for i in lista:
          nombreGatos.append(i[0])
        print(nombreGatos)
        for i in lista:
          imagenGatos.append(i[-1])
        print(imagenGatos)
        largo = len(nombreGatos)
        largoP = 0
        conn.commit()      
        conn.close()
        
        return render_template('borrar.html', gatos = nombreGatos, imagenGatos = imagenGatos, largo = largo, largoP = largoP)
  
      else:
        largo = 0
        largoP = 0
        mensajeG = "Ingrese un nombre"
        return render_template('borrar.html', mensajeG = mensajeG, largo = largo, largoP = largoP)
    else:
      return redirect('/formularioRefugio')  
  else:
    largoP = 0
    return redirect('/borrar', largo = largo, largoP = largoP)

@app.route('/eliminar',  methods=["POST"])
def eliminar():
  if (request.method == "POST"):
    if session['sesion'] == True:
      print("hla")
      nombre = request.form["nombre"]
      mascota = request.form["mascota"]
      print(mascota)
      conn = sqlite3.connect('tabla.db')
      if mascota == "gato":
        print("gato")
        q = f"""DELETE FROM Gatos WHERE nombre = '{nombre}'"""
      else:
        print("perro")
        q = f"""DELETE FROM Perros WHERE nombre = '{nombre}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      print(nombre)
      return jsonify(nombre)
    else:
      return redirect('/formularioRefugio')

@app.route('/opcionesBorrarPerro',  methods=["GET", "POST"])
def opcionesBorrarPerro():
  if (request.method == "POST"):
    if session['sesion'] == True:
      if (request.form["nombrePerro"] != "" and session['gato'] == "."):
        animal = request.form["nombrePerro"]
        conn = sqlite3.connect('tabla.db')
        animal = animal.capitalize()
        r = f"""SELECT nombre, imagen FROM Perros where nombre = '{animal}'"""
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombrePerros = []
        imagenPerro = []
        for i in lista:
          nombrePerros.append(i[0])
        print(nombrePerros)
        for i in lista:
          imagenPerro.append(i[-1])
        print(imagenPerro)
        largoP = len(nombrePerros)
        largo = 0
        conn.commit()      
        conn.close()
        
        return render_template('borrar.html', perros = nombrePerros, imagenPerro = imagenPerro, largo = largo, largoP = largoP)
  
      else:
        largo = 0
        largoP = 0
        mensajeP = "Ingrese un nombre"
        return render_template('borrar.html', mensajeP = mensajeP, largo = largo, largoP = largoP)
    else:
      return redirect('/formularioRefugio')  
  else:
    largo = 0
    return redirect('/borrar', largo = largo, largoP = largoP)
'''
@app.route('/eliminarPerro',  methods=["POST"])
def eliminarPerro():
  if (request.method == "POST"):
    if session['sesion'] == True:
      nombre = request.form["nombre"]
      conn = sqlite3.connect('tabla.db')
      q = f"""DELETE FROM Gatos WHERE nombre = '{nombre}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      return jsonify(nombre)
    else:
      return redirect('/formularioRefugio')
    '''
@app.route('/opcionesAdmin')
def opcionesAdmin():
  if session['sesion'] == True:
    return render_template('opcionesAdministrador.html')
  else:
    return redirect('/formularioRefugio')
  
@app.route('/seleccionarGato', methods=["GET", "POST"])
def perfilGato():
  if (request.method == "POST"):
    animal = request.form["gatoSeleccionado"]
    conn = sqlite3.connect('tabla.db')
    q = f"""SELECT * FROM Gatos WHERE imagen = '{animal}'"""
    resu = conn.execute(q)   
    gato = []
    for i in resu:
      gato.append(i)
    print(gato)
    nombre = gato[0][1]
    print(gato[0][1] )
    print(nombre)
    conn.commit()      
    conn.close()
    return jsonify(nombre) 

@app.route('/mostrarGatos',  methods=["GET", "POST"])
def mostrarGatos():
  conn = sqlite3.connect('tabla.db')
  q = f"""SELECT * FROM Gatos"""
  resu = conn.execute(q)

  gatos = []
  imagenGatos = []
  for i in resu:
    gatos.append(i)
  for i in gatos:
    imagenGatos.append(i[-1])
    
  largo = len(gatos)
  #lista = resu.fetchall()
  conn.commit()      
  conn.close()
  
  
  return render_template('mostrarGatos.html', gatos = gatos, largo = largo, imagenGatos = imagenGatos)

@app.route('/mostrarPerros',  methods=["GET", "POST"])
def mostrarPerros():
  conn = sqlite3.connect('tabla.db')
  q = f"""SELECT * FROM Perros"""
  resu = conn.execute(q)

  perros = []
  imagenPerros = []
  for i in resu:
    perros.append(i)
  for i in perros:
    imagenPerros.append(i[-1])
    
  largo = len(perros)
  #lista = resu.fetchall()
  conn.commit()      
  conn.close()
  
  
  return render_template('mostrarPerros.html', perros = perros, largo = largo, imagenPerros = imagenPerros)


@app.route('/redirigir',  methods=["GET", "POST"])
def formularioAdopcion():
  if (request.method == "GET"):
    return render_template('formulario.html')
    
"""
  
"""
app.run(host='0.0.0.0', port=81)


