
const toggle = document.querySelector('.toggle')
const links = document.querySelector('.links')

toggle.addEventListener('click', () => {
    toggle.classList.toggle('rotate')
    links.classList.toggle('active')
})


function formulario() {
  var name = document.getElementById("nombre").value 
  var apellido = document.getElementById("apellido").value 
  var dni = document.getElementById("dni").value
  var correo = document.getElementById("mail").value 
  var telefono = document.getElementById("telefono").value 
  var direccion = document.getElementById("direccion").value 
  var hogar = document.getElementById("hogar").value 
  var mascotas = document.getElementById("mascotas").value 
  var convivientes = document.getElementById("convivientes").value 

  var contieneArroba = false
  if (correo.includes('@')){
    contieneArroba = true
  }
  if (name.length == 0 || apellido.length == 0 || dni.length == 0 || correo.length == 0 || telefono.length == 0 || direccion.length == 0 || hogar.length == 0 || mascotas.length  == 0 || convivientes.length == 0 || contieneArroba == false)  {
    alert("Faltan ingresar datos")
  }
  
  $.ajax({ 
    url:"/formulario", 
    type:"POST", 
    data: {"nombre":name,
          "apellido": apellido,
          "dni": dni,
          "mail": correo,
          "telefono": telefono,
          "direccion": direccion,
          "hogar": hogar,
          "mascotas": mascotas,
          "convivientes": convivientes
          }, 

    success: function(response){  
      datos = response
      //if(datos == true) {
        alert(`Se registro su respuesta`)
      //}
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}

function formularioRefugio() {
  var usuario = document.getElementById("usuario").value 
  var password = document.getElementById("password").value 
  console.log(password)
if (usuario.length == 0 || password.length == 0)  {
    alert("Faltan ingresar datos")
  }
  
  $.ajax({ 
    url:"/refugio", 
    type:"POST", 
    data: {"usuario":usuario,
          "password": password,
          }, 

    success: function(response){  
      datos = response
      //console.log(datos)
      location.href= '/saludo'
      if(datos == true) {
        alert(`Se registro su respuesta`)
      }
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}


function cargarPerfiles() {
  var name = document.getElementById("nombre").value 
  var sexo = document.getElementById("sexo").value 
  var edad = document.getElementById("edad").value
  var raza = document.getElementById("raza").value 
  var tamaño = document.getElementById("tamaño").value 
  var informacion = document.getElementById("informacion").value 
  var imagen = document.getElementById("imagen").value 
  let formData = new FormData($("#form1")[0])
  console.log(formData)

  if (name.length == 0 || sexo.length == 0 || edad.length == 0 || raza.length == 0 || tamaño.length == 0 || informacion.length == 0 || imagen.length == 0)  {
    alert("Faltan ingresar datos")
  }

  let sarasa = {"nombre":name,
          "sexo": sexo,
          "edad": edad,
          "raza": raza,
          "tamaño": tamaño,
          "informacion": informacion,
          "imagen": imagen
          };
  console.log(sarasa);
  $.ajax({ 
    url:"/cargarPerfiles", 
    type:"POST", 
    data: {"nombre":name,
          "sexo": sexo,
          "edad": edad,
          "raza": raza,
          "tamaño": tamaño,
          "informacion": informacion,
          "imagen": imagen
          }, 

    success: function(response){  
      datos = response
      if(datos == true) {
        alert(`Se registro su respuesta`)
      }
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}
