from src.db.conexion import get_connection
from src.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import text

class ModeloUsuario:

    def __init__(self):
        self.conn = get_connection()

    def registrar_usuario(self, username, email, password, token):
        password_hash = generate_password_hash(password)
        expiracion = datetime.utcnow() + timedelta(hours=1)
        try:
            with self.conn.begin():
                query = text("""
                    INSERT INTO users (username, email, password_hash, is_active, recovery_token, token_expiration)
                    VALUES (:username, :email, :password_hash, :is_active, :recovery_token, :token_expiration)
                    RETURNING id, username, email, password_hash, is_active, recovery_token, token_expiration;
                """)
                result = self.conn.execute(query, {
                    "username": username,
                    "email": email,
                    "password_hash": password_hash,
                    "is_active": False,
                    "recovery_token": token,
                    "token_expiration": expiracion
                })
                data = result.mappings().fetchone()
                return self.convertir_a_clase(data)
        finally:
            self.conn.close()

    def buscar_por_email(self, email):
        try:
            with self.conn:
                result = self.conn.execute(
                    text("SELECT * FROM users WHERE email = :email"),
                    {"email": email}
                )
                data = result.mappings().fetchone()
                return self.convertir_a_clase(data)
        finally:
            self.conn.close()

    def validar_credenciales(self, email, password):
        usuario = self.buscar_por_email(email)
        if usuario and check_password_hash(usuario.password_hash, password):
            return usuario
        return None

    def actualizar_token_recuperacion(self, email, token):
        expiracion = datetime.utcnow() + timedelta(hours=1)
        try:
            with self.conn.begin():
                self.conn.execute(
                    text("""
                        UPDATE users
                        SET recovery_token = :token, token_expiration = :exp
                        WHERE email = :email
                    """),
                    {
                        "token": token,
                        "exp": expiracion,
                        "email": email
                    }
                )
        finally:
            self.conn.close()

    def validar_token(self, token):
        try:
            with self.conn:
                result = self.conn.execute(
                    text("""
                        SELECT * FROM users
                        WHERE recovery_token = :token AND token_expiration >= :now
                    """),
                    {
                        "token": token,
                        "now": datetime.utcnow()
                    }
                )
                data = result.mappings().fetchone()
                return self.convertir_a_clase(data)
        finally:
            self.conn.close()

    def activar_usuario_por_token(self, token):
        try:
            with self.conn.begin():
                result = self.conn.execute(
                    text("""
                        UPDATE users
                        SET is_active = TRUE, recovery_token = NULL, token_expiration = NULL
                        WHERE recovery_token = :token AND token_expiration >= :now
                    """),
                    {
                        "token": token,
                        "now": datetime.utcnow()
                    }
                )
                return result.rowcount > 0
        finally:
            self.conn.close()

    def actualizar_contraseña(self, email, nueva_contraseña):
        password_hash = generate_password_hash(nueva_contraseña)
        try:
            with self.conn.begin():
                self.conn.execute(
                    text("""
                        UPDATE users
                        SET password_hash = :password_hash,
                            recovery_token = NULL,
                            token_expiration = NULL
                        WHERE email = :email
                    """),
                    {
                        "password_hash": password_hash,
                        "email": email
                    }
                )
                return True
        finally:
            self.conn.close()

    def convertir_a_clase(self, data):
        if not data:
            return None
        return User(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            is_active=data['is_active'],
            recovery_token=data['recovery_token'],
            token_expiration=data['token_expiration']
        )
