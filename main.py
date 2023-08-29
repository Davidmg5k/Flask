from flask import Flask, render_template, request, redirect, flash
from base_datos import Contacto

app = Flask(__name__)
contacto=Contacto()
app.secret_key='esLaContraseña'

@app.route('/')
def inicio():
    contactos=contacto.listar_contactos()
    return render_template('index.html', contactos=contactos)

@app.route('/agregarContacto', methods=['POST'])
def agregar_contacto():
    if request.method == 'POST':
        contacto.agregar(nombre=request.form['nombreCompleto'],celular=request.form['celular'],correo=request.form['correo_electronico'])
        flash('Se ha agregado el contacto correctamente')
    return redirect('/')

@app.route('/editarContacto/<string:nombre>/<string:celular>')
def editar_contacto(nombre, celular):
    cnt=contacto.buscar(nombre=nombre, celular=celular)
    return render_template('editar.html', contactos=cnt)

@app.route('/actualizarContacto/<string:nombre>/<string:celular>', methods=['POST'])
def actualizar_contacto(nombre, celular):
    if request.method == 'POST':
        contacto.editar(nombre=request.form['nombreCompleto'],celular=request.form['celular'],correo=request.form['correo_electronico'], b_nombre=nombre, b_celular=celular)
    flash("Se han actualizado los datos correctamente")
    return redirect('/')

@app.route('/eliminarContacto/<string:nombre>/<string:celular>')
def eliminar_contacto(nombre, celular):
    contacto.eliminar(nombre=nombre, celular=celular)
    return redirect('/')

@app.route('/buscarContacto',methods=['POST'])
def buscar_contact():
    if request.method == 'POST':
        cnt=contacto.buscar(nombre=request.form['nombreCompleto'],celular=request.form['celular'])
        flash('El contacto es: {}'.format(cnt))
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)