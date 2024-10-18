from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aquí'  

usuarios = {
    'wilder': '1234',
    'ali': '12345',
}

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'usuario' not in session:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorador

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['username']
        contraseña = request.form['password']
        if nombre_usuario in usuarios and usuarios[nombre_usuario] == contraseña:
            session['usuario'] = nombre_usuario
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('bienvenida'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/bienvenida')
@login_requerido
def bienvenida():
    usuario = session['usuario']
    return render_template('Bienvenido.html', usuario=usuario)

@app.route('/logout')
@login_requerido
def logout():
    session.pop('usuario', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
