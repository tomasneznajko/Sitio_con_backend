from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory 
from datetime import datetime
import os

#Request: Recibe peticiones del usuario y las deja disponibles en objetos para ser utilizadas
#Redirect y url_for: Me redirecciona a una url creada por url_for
#datetime: Acceso a diferentes formatos de tiempo correlacionados con el envío de información
#send_from_directory: Enviar objeto que esté en un directorio
#os: Funcionalidad del SO => Leer rutas


from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor #Para configurar el cursor usado para las consultas SQL como tipo diccionario


app = Flask(__name__)
mysql = MySQL() #Instanciar objeto a utilizar en la conexion de base de datos


#Configurar conexion a la base de datos

app.config['MYSQL_DATABASE_HOST'] = 'localhost' #Servidor utilizado  
app.config['MYSQL_DATABASE_USER'] = 'root' #Usuario
app.config['MYSQL_DATABASE_PASSWORD'] = 'Biancaduarte777' #Contraseña del usuario
app.config['MYSQL_DATABASE_DB'] = 'usuarios_neznajko' #Mi base de datos

#Podria configurar el puerto, pero, por defecto, ya es 3306


mysql.init_app(app) #Inicializar la base de datos, usando los datos de app.config recibidos en app

@app.route('/uploads/<path:imagen>')
def uploads(imagen):
    return send_from_directory(os.path.join('../uploads'), imagen) #Indico el directorio donde están las imagenes, para que las lea

@app.route('/') #Conectarse con mi sitio de nombre '(ip)+/'

def index(): #Responder a lo conectado en route

    
        # Crear conexion de mysql a la base de datos en vista (dentro de variable conn)
    conn = mysql.connect()
    cursor = conn.cursor(DictCursor) #Crear cursor => Realizo consultas en la base de datos

    cursor.execute('SELECT * FROM usuario') #Ejecuto consulta con cursor
    usuarios = cursor.fetchall() #Traer todos los registros asociados a esa consulta que realiza el cursor en formato de "tupla de tuplas"

    print(usuarios) #Muestro en consola los registros de la vista obtenida 

    return render_template('index.html', usuarios = usuarios) #Mi sitio muestra este codigo html, ya que reconoce todo archivo desde templates

@app.route('/registrarse') 
def create(): #Nombre de funcion suele coincidir con el conectado con route desde template
    return render_template('registrarse.html') #Vista de registrarse (su HTML con contenido)

# En route del create:
# GET: Obtener información cuando entro a la URL -> Por defecto
# POST: Se envía por formulario
# PUT: Modificar todo el registro completo
# PATCH: Modificar partes especificas del registro
# DELETE: Avisar que se va a borrar registro
# Usados con API o servicios

#Conexion con las vistas:
@app.route('/origenes')
def origenes():
    return render_template('origenes.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/leyendas')
def leyendas():
    return render_template('leyendas.html')

@app.route('/momentazos')
def momentazos():
    return render_template('momentazos.html')



# def conectarPagina(nombre):
#     @app.route('/' + nombre)
#     def funcion():
#         return render_template(nombre + '.html')

# conectarPagina('origenes')

# conectarPagina('leyendas')
# conectarPagina('momentazos')


@app.route('/store', methods=['POST'])
def store():
    print(request.form)
    print(request.files) #Archivos por separado

    conn = mysql.connect()
    cursor = conn.cursor()

    nombre = request.form['nombre'] #Recibo el valor del name del formulario
    apellido = request.form['apellido']
    fecha = request.form['fecha']
    sexo = request.form['sexo']
    doc = request.form['doc']
    identificacion = request.form['identificacion']
    telefono = request.form['telefono']
    email = request.form['email'] 

    if request.files['foto'].filename != '': #Se sube el archivo, porque tiene un nombre
        foto = request.files['foto']
        tiempo_foto = datetime.now().strftime('%Y%m%d%H%M%S') #Obtengo el momento en que se envía la imagen, indicando el formato del tiempo que se muestre
        nombre_foto = tiempo_foto + '_' + foto.filename #Nombre con el que se guardará en la carpeta
        foto.save('uploads/' + nombre_foto)#Indicar guardado fisico de la imagen/archivo

        sql = 'INSERT INTO usuario (nombre, apellido, fecha, sexo, tipo_doc, num_doc, telefono, email, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)' #Evita inyeccion de sql el uso de %s + values
        values = [nombre, apellido, fecha, sexo, doc, identificacion, telefono, email, nombre_foto]
    else: #No se envía el archivo
        sql = 'INSERT INTO usuario (nombre, apellido, fecha, sexo, tipo_doc, num_doc, telefono, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' #Evita inyeccion de sql el uso de %s + values
        values = [nombre, apellido, fecha, sexo, doc, identificacion, telefono, email] 

    #Realizar insercion de datos del formulario
    


    #Establecer consulta en sql
    cursor.execute(sql, values)
    conn.commit() 

    return redirect(url_for('index')) #Obtengo URL de la función, si no está a simple vista

@app.route('/edit/<int:id>') #int: id sera el valor dinamico a enviar a la URL /edit/ + (id)
def edit(id): #id ya indicado en la barra se recibe por parametro
    sql = 'SELECT * FROM usuario WHERE id_usuario = %s' #Si el id no existe, traerá un none
    values = [id] #Usamos el id a modificar

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor) 

    cursor.execute(sql, values)
    usuario = cursor.fetchone() #Me trae un único elemento, un id


    return render_template('edit.html', usuario = usuario)


@app.route('/update', methods = ['POST'])
def update():
    print(request.form)
    print(request.files)

    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)


    id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha = request.form['fecha']
    sexo = request.form['sexo']
    doc = request.form['doc']
    identificacion = request.form['identificacion']
    telefono = request.form['telefono']
    email = request.form['email']

    if request.files['foto'].filename != '': #Se sube el archivo, porque tiene un nombre
        sql = 'SELECT foto FROM usuario WHERE id_usuario = %s' 
        values = [id]

        cursor.execute(sql, values)
        usuario = cursor.fetchone()

        if request.files['foto'] != None: #Se pregunta si el archivo subido no es NULO => se guardó correctamente
            try:
                os.remove(os.path.join('uploads', usuario['foto'])) #Elimino el archivo que se tiene actualmente en uploads
            except: #Evitar problema de que se haya borrado la imagen de uploads, existiendo en la base de datos
                pass

            foto = request.files['foto']
            tiempo_foto = datetime.now().strftime('%Y%m%d%H%M%S') #Obtengo el momento en que se envía la imagen, indicando el formato del tiempo que se muestre
            nombre_foto = tiempo_foto + '_' + foto.filename #Nombre con el que se guardará en la carpeta
            foto.save('uploads/' + nombre_foto)#Indicar guardado fisico de la imagen/archivo

            sql = 'UPDATE usuario SET nombre = %s, apellido = %s, fecha = %s, sexo = %s, tipo_doc = %s, num_doc = %s, telefono = %s, email = %s, foto = %s WHERE id_usuario=%s'
            values = [nombre, apellido, fecha, sexo, doc, identificacion, telefono, email, nombre_foto, id]
    else: #No se envía el archivo => Se modifica todo lo demás, menos el archivo, ya que no está
        sql = 'UPDATE usuario SET nombre = %s, apellido = %s, fecha = %s, sexo = %s, tipo_doc = %s, num_doc = %s, telefono = %s, email = %s WHERE id_usuario=%s'
        values = [nombre, apellido, fecha, sexo, doc, identificacion, telefono, email, id]

    cursor.execute(sql, values)
    conn.commit()  #Guardo datos en el motor de base de datos
 

    return redirect(url_for('index')) 

@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor(DictCursor)

    sql = 'SELECT foto FROM usuario WHERE id_usuario = %s' #Evita inyeccion de sql el uso de %s + values
    values = [id]
    cursor.execute(sql, values)
    usuario = cursor.fetchone()

    print(usuario)

    if usuario['foto'] != None: #Se pregunta si el archivo subido no es NULO, se guardó correctamente
        try:
            os.remove(os.path.join('uploads', usuario['foto'])) #Elimino el archivo que se tiene actualmente en uploads
        except: #Evitar problema de que se haya borrado la imagen de uploads, existiendo en la base de datos
            pass    

    sql = 'DELETE FROM usuario WHERE id_usuario = %s'
    values = [id]
    cursor.execute(sql, values)
    conn.commit()

    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run( debug = True ) #Registra cambios sin reiniciar el servidor, solo ejecuto el codigo nuevo
