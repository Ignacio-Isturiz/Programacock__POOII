from src.db.conexion import get_connection
from src.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class ModeloUsuario:

    @staticmethod
    def registrar_usuario(username, email, password, token):
        password_hash = generate_password_hash(password)
        expiracion = datetime.utcnow() + timedelta(hours=1)
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (username, email, password_hash, is_active, recovery_token, token_expiration)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
        """
        cursor.execute(query, (username, email, password_hash, False, token, expiracion))
        data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return ModeloUsuario.convertir_a_clase(data)

    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return ModeloUsuario.convertir_a_clase(data)

    @staticmethod
    def validar_credenciales(email, password):
        usuario = ModeloUsuario.buscar_por_email(email)
        if usuario and check_password_hash(usuario.password_hash, password):
            return usuario
        return None

    @staticmethod
    def actualizar_token_recuperacion(email, token):
        conn = get_connection()
        cursor = conn.cursor()
        expiracion = datetime.utcnow() + timedelta(hours=1)
        cursor.execute("""
            UPDATE users SET recovery_token = %s, token_expiration = %s WHERE email = %s
        """, (token, expiracion, email))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def validar_token(token):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE recovery_token = %s AND token_expiration >= %s
        """, (token, datetime.utcnow()))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return ModeloUsuario.convertir_a_clase(data)

    @staticmethod
    def activar_usuario_por_token(token):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET is_active = TRUE, recovery_token = NULL, token_expiration = NULL
            WHERE recovery_token = %s AND token_expiration >= %s
        """, (token, datetime.utcnow()))
        actualizado = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return actualizado

    @staticmethod
    def actualizar_contraseña(email, nueva_contraseña):
        conn = get_connection()
        cursor = conn.cursor()
        password_hash = generate_password_hash(nueva_contraseña)
        cursor.execute("""
            UPDATE users SET password_hash = %s, recovery_token = NULL, token_expiration = NULL WHERE email = %s
        """, (password_hash, email))
        conn.commit()
        cursor.close()
        conn.close()
        return True

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
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT id, username, email, password_hash, is_active, recovery_token, token_expiration
                    FROM users WHERE email = %s
                """, (email,))
                fila = cursor.fetchone()
                if fila:
                    # ✅ Utiliza el mismo método que el resto
                    return cls.convertir_a_clase(fila)
                return None
        finally:
            conexion.close()
