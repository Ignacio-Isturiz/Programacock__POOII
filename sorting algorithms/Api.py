import requests
import tkinter as tk
from tkinter import ttk

def obtener_datos_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Función para procesar los datos
def procesar_datos(data):
    data_cleaned = []
    for item in data:
        # Obtener el peso y talla
        peso = item.get("peso", None)
        talla = item.get("talla", None)
        
        # Añadir los datos procesados
        data_cleaned.append({
            "peso": peso,
            "talla": talla
        })
    
    columns = list(data_cleaned[0].keys()) if data_cleaned else []
    return data_cleaned, columns

def actualizar_tabla(datos):
    for row in tabla.get_children():
        tabla.delete(row)
    for item in datos:
        tabla.insert("", "end", values=(item["peso"], item["talla"]))

def ordenar_por(columna):
    global datos_procesados
    datos_procesados.sort(key=lambda x: x[columna] if isinstance(x[columna], (int, float)) else float('inf'))
    actualizar_tabla(datos_procesados)

# Configuración de la interfaz
root = tk.Tk()
root.title("Datos API")

frame = ttk.Frame(root)
frame.pack(pady=10)

columnas = ["peso", "talla"]
tabla = ttk.Treeview(frame, columns=columnas, show="headings")

for col in columnas:
    tabla.heading(col, text=col, command=lambda c=col: ordenar_por(c))
    tabla.column(col, width=150)

tabla.pack()

url = "https://www.datos.gov.co/resource/ttnc-9dzn.json"
datos = obtener_datos_api(url)
datos_procesados, columnas = procesar_datos(datos)
actualizar_tabla(datos_procesados)

root.mainloop()
