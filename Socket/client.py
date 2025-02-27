import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Conectado al servidor de Node.js")
    sio.emit("mensaje_desde_python", "¡Hola desde otra computadora!")

@sio.on("respuesta")
def recibir_respuesta(data):
    print("Respuesta de Node.js:", data)

@sio.event
def disconnect():
    print("Desconectado del servidor")

# 🔹 Reemplaza '192.168.1.X' con la IP de la computadora que tiene el servidor
sio.connect("http://172.30.3.213:3000")  # 🔹 Sin ".X"
# ⚠ CAMBIA ESTA IP
sio.wait()
