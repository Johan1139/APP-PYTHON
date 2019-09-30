from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Conexion a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db'
mysql = MySQL(app)

#Configuraciones
app.secret_key = 'key' #Como va a ir protegida la sesión

@app.route('/home')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas')
    personas = cur.fetchall()
    return jsonify(personas)

@app.route('/add', methods=['POST'])
def add_persona():
    if request.method == 'POST':
        perid = request.get_json()['perid']
        nombre = request.get_json()['pernombre']
        apellido = request.get_json()['perapellido']
        telefono = request.get_json()['pertelefono']
        fechanac = request.get_json()['perfechanac']
        cedula = request.get_json()['percedula']

        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM personas p JOIN linea l ON p.perid=l.perid 
        WHERE l.linumerolinea = """, (str(telefono)))
        dato = cursor.fetchall()

        if (len(dato) < 0):
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO personas VALUES (%s, %s, %s, %s, %s, %s)', 
            (int(perid), str(nombre), str(apellido), str(telefono), str(fechanac), str(cedula)))
            mysql.connection.commit()

            resultado = {'msj':'PERSONA REGISTRADA SATISFACTORIAMENTE'}
        else:
            resultado = {'mjs':'YA EXISTE UNA PERSONA CON ESTA LINEA'}

    return jsonify({'resultado': resultado})

@app.route('/registrarlinea', methods=['POST'])
def reg_linea():
    if request.method == 'POST':
        linumerolinea = request.get_json()['linumerolinea']
        perid = request.get_json()['perid']
        linestado = request.get_json()['linestado']
        equserial = request.get_json()['equserial']
        equmarca = request.get_json()['equmarca']
        equdescripcion = request.get_json()['equdescripcion']
        equestado = request.get_json()['equestado']
        facnumero = request.get_json()['facnumero']
        facfechaemision = request.get_json()['facfechaemision']
        facvalor = request.get_json()['facvalor']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO linea VALUES(%s,%s,%s)',(str(linumerolinea), int(perid), str(linestado)))
        mysql.connection.commit()

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO equipo VALUES(%s,%s,%s,%s,%s)',(int(equserial),str(linumerolinea),str(equmarca),str(equdescripcion),str(equestado)))
        mysql.connection.commit()

        curs = mysql.connection.cursor()
        curs.execute('INSERT INTO factura VALUES(%s,%s,%s,%s)',(int(facnumero), str(linumerolinea),str(facfechaemision), int(facvalor)))
        mysql.connection.commit()

        resultado = {'msj':'Registro Exitoso'}
        return jsonify({'resultado':resultado})

@app.route('/consultarfacturas/<string:fecha>/<int:cedula>')
def consultarfacturas(fecha,cedula):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("""SELECT p.pernombre, p.perapellido, p.percedula, f.facnumero, f.facfechaemision, f.facvalor
            FROM (personas p JOIN linea li ON p.perid=li.perid)
                JOIN factura f ON f.linumerolinea= li.linumerolinea   
            WHERE p.percedula=%s OR f.facfechaemision=%s """,(int(cedula), str(fecha)))
        datos = cur.fetchall()
        return jsonify(datos)

@app.route('/eliminarfactura/<int:numero>', methods=['DELETE'])
def delete(numero):
    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        respuesta = cur.execute('DELETE FROM factura WHERE facnumero=%s' % (numero)) # % funcion sleep pausa las funciones que realizan las demas consultas 
        mysql.connection.commit()

        if respuesta>0:
            resultado = {'msj':'Factura Eliminada'}
        else:
            resultado = {'msj':'Factura No Encontrada'}

        return jsonify({"resultado":resultado})

@app.route('/updatelinea/<string:cedula>/<string:telefono>', methods=['PUT'])
def update_linea(cedula,telefono):
    if request.method == 'PUT':
        linestado = request.get_json()['linestado']

        cur =mysql.connection.cursor()
        cur.execute("""UPDATE personas p 
        JOIN linea li ON p.perid=li.perid
        SET linestado=%s 
        WHERE li.linumerolinea=%s AND p.percedula=%s""", 
        (str(linestado), str(telefono), str(cedula)))
        mysql.connection.commit()
        
        resultado = {'msj':'LINEA ACTUALIZADA'}

        return jsonify({"resultado":resultado})

if __name__ == '__main__':
    app.run(debug = True)