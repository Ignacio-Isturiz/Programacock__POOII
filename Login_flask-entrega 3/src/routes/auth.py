from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from src.models.modelusuario import ModeloUsuario
from src.utils.email import send_email
from functools import wraps
import secrets
import re
from datetime import datetime 

auth_bp = Blueprint('auth', __name__)

# Decorador para proteger rutas
def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorada

# Función para validar seguridad de la contraseña
def validar_contraseña(password):
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r"[a-z]", password):
        return "La contraseña debe contener al menos una letra minúscula."
    if not re.search(r"[0-9]", password):
        return "La contraseña debe contener al menos un número."
    return None

# Registro
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('auth.registro'))

        error = validar_contraseña(password)
        if error:
            flash(error, 'danger')
            return redirect(url_for('auth.registro'))

        modelo = ModeloUsuario()
        usuario_existente = modelo.buscar_por_email(email)
        if usuario_existente:
            flash('El email ya está registrado.', 'warning')
            return redirect(url_for('auth.registro'))

        token = secrets.token_urlsafe(32)
        modelo = ModeloUsuario()
        modelo.registrar_usuario(username, email, password, token)

        activation_url = url_for('auth.activar_cuenta', token=token, _external=True)
        html = render_template('email/activar_cuenta.html', username=username, activation_url=activation_url)
        send_email("Activa tu cuenta", [email], html)

        flash('Cuenta creada con éxito. Revisa tu correo para activarla.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

# Activación
@auth_bp.route('/activar/<token>')
def activar_cuenta(token):
    modelo = ModeloUsuario()
    usuario = modelo.validar_token(token)
    if usuario:
        modelo = ModeloUsuario()
        if modelo.activar_usuario_por_token(token):
            flash("Cuenta activada con éxito. Ya puedes iniciar sesión.", 'success')
        else:
            flash("Error al activar tu cuenta.", 'danger')
    else:
        flash("Token inválido o expirado.", 'danger')
    return redirect(url_for('auth.login'))

# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        modelo = ModeloUsuario()
        user = modelo.buscar_por_email(email)

        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('Tu cuenta no está activada. Revisa tu correo.', 'warning')
                return redirect(url_for('auth.login'))

            session['user_id'] = user.id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('auth.base'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('login.html')

# Vista protegida
@auth_bp.route('/base')
@login_requerido
def base():
    return render_template('base.html')

# Logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))

# Recuperar contraseña
@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        email = request.form['email']
        modelo = ModeloUsuario()
        usuario = modelo.buscar_por_email(email)

        if usuario:
            token = secrets.token_urlsafe(32)
            modelo = ModeloUsuario()
            modelo.actualizar_token_recuperacion(email, token)

            reset_url = url_for('auth.reestablecer_contraseña', token=token, _external=True)
            html = render_template(
                'email/reestablecer_cuenta.html',
                usuario=usuario,
                reset_url=reset_url,
                current_year=datetime.now().year
            )
            send_email("Recuperación de contraseña", [email], html)
            flash('Revisa tu correo para continuar con la recuperación.', 'info')
        else:
            flash('No se encontró una cuenta con ese correo.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('recuperar.html')

# Reestablecer contraseña
@auth_bp.route('/reestablecer/<token>', methods=['GET', 'POST'])
def reestablecer_contraseña(token):
    modelo = ModeloUsuario()
    usuario = modelo.validar_token(token)
    if not usuario:
        flash("Token inválido o expirado.", 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nueva_contraseña = request.form['password']

        error = validar_contraseña(nueva_contraseña)
        if error:
            flash(error, 'danger')
            return redirect(url_for('auth.reestablecer_contraseña', token=token))

        modelo = ModeloUsuario()
        modelo.actualizar_contraseña(usuario.email, nueva_contraseña)
        flash('Contraseña actualizada. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reestablecer.html', token=token)
