from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from src.models.modelusuario import ModeloUsuario
from src.utils.email import send_email
from functools import wraps
import secrets

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

        usuario_existente = ModeloUsuario.buscar_por_email(email)
        if usuario_existente:
            flash('El email ya está registrado.', 'warning')
            return redirect(url_for('auth.registro'))

        token = secrets.token_urlsafe(32)
        ModeloUsuario.registrar_usuario(username, email, password, token)

        activation_url = url_for('auth.activar_cuenta', token=token, _external=True)
        html = f"""
        <h3>¡Bienvenido, {username}!</h3>
        <p>Gracias por registrarte. Haz clic en el siguiente enlace para activar tu cuenta:</p>
        <a href="{activation_url}">Activar cuenta</a>
        <p>Si no te registraste, puedes ignorar este correo.</p>
        """

        send_email("Activa tu cuenta", [email], html)
        flash('Cuenta creada con éxito. Revisa tu correo para activarla.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

# Activación
@auth_bp.route('/activar/<token>')
def activar_cuenta(token):
    usuario = ModeloUsuario.validar_token(token)
    if usuario:
        if ModeloUsuario.activar_usuario_por_token(token):
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
        user = ModeloUsuario.obtener_por_email(email)

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
        usuario = ModeloUsuario.buscar_por_email(email)

        if usuario:
            token = secrets.token_urlsafe(32)
            ModeloUsuario.actualizar_token_recuperacion(email, token)

            reset_url = url_for('auth.reestablecer_contraseña', token=token, _external=True)
            html = f"""
            <h3>Hola, {usuario.username}</h3>
            <p>Haz clic en el siguiente enlace para restablecer tu contraseña:</p>
            <a href="{reset_url}">Restablecer contraseña</a>
            <p>Si no solicitaste esto, puedes ignorar este correo.</p>
            """
            send_email("Recuperación de contraseña", [email], html)
            flash('Revisa tu correo para continuar con la recuperación.', 'info')
        else:
            flash('No se encontró una cuenta con ese correo.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('recuperar.html')

# Reestablecer contraseña
@auth_bp.route('/reestablecer/<token>', methods=['GET', 'POST'])
def reestablecer_contraseña(token):
    usuario = ModeloUsuario.validar_token(token)
    if not usuario:
        flash("Token inválido o expirado.", 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nueva_contraseña = request.form['password']
        ModeloUsuario.actualizar_contraseña(usuario.email, nueva_contraseña)
        flash('Contraseña actualizada. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reestablecer.html', token=token)
