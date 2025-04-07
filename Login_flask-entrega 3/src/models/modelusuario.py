from src.db.conexion import get_connection
from src.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import text

class ModeloUsuario:

    @staticmethod
    def registrar_usuario(username, email, password, token):
        password_hash = generate_password_hash(password)
        expiracion = datetime.utcnow() + timedelta(hours=1)
        conn = get_connection()
        try:
            with conn.begin():
                query = text("""
                    INSERT INTO users (username, email, password_hash, is_active, recovery_token, token_expiration)
                    VALUES (:username, :email, :password_hash, :is_active, :recovery_token, :token_expiration)
                    RETURNING id, username, email, password_hash, is_active, recovery_token, token_expiration;
                """)
                result = conn.execute(query, {
                    "username": username,
                    "email": email,
                    "password_hash": password_hash,
                    "is_active": False,
                    "recovery_token": token,
                    "token_expiration": expiracion
                })
                data = result.mappings().fetchone()
                return ModeloUsuario.convertir_a_clase(data)
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        try:
            with conn:
                result = conn.execute(
                    text("SELECT * FROM users WHERE email = :email"),
                    {"email": email}
                )
                data = result.mappings().fetchone()
                return ModeloUsuario.convertir_a_clase(data)
        finally:
            conn.close()

    @staticmethod
    def validar_credenciales(email, password):
        usuario = ModeloUsuario.buscar_por_email(email)
        if usuario and check_password_hash(usuario.password_hash, password):
            return usuario
        return None

    @staticmethod
    def actualizar_token_recuperacion(email, token):
        expiracion = datetime.utcnow() + timedelta(hours=1)
        conn = get_connection()
        try:
            with conn.begin():
                conn.execute(
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
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def validar_token(token):
        conn = get_connection()
        try:
            with conn:
                result = conn.execute(
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
                return ModeloUsuario.convertir_a_clase(data)
        finally:
            conn.close()

    @staticmethod
    def activar_usuario_por_token(token):
        conn = get_connection()
        try:
            with conn.begin():
                result = conn.execute(
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
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def actualizar_contraseña(email, nueva_contraseña):
        password_hash = generate_password_hash(nueva_contraseña)
        conn = get_connection()
        try:
            with conn.begin():
                conn.execute(
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
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def convertir_a_clase(data):
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

    @classmethod
    def obtener_por_email(cls, email):
        return cls.buscar_por_email(email)
