import tkinter as tk
from tkinter import messagebox, scrolledtext
from Api import fetch_data
from sorting_algorithms import (
    bubble_sort, counting_sort, heap_sort, insertion_sort,
    merge_sort, quick_sort, radix_sort, selection_sort, bucket_sort
)

def show_sorted_data():
    try:
        api_url = "https://www.datos.gov.co/resource/sgf4-8tf8.json"
        data = fetch_data(api_url)
        
        if not data:
            messagebox.showerror("Error", "No se pudieron obtener datos de la API.")
            return

        # Diccionario de algoritmos
        sort_algorithms = {
            "Bubble Sort": bubble_sort,
            "Counting Sort": counting_sort,
            "Heap Sort": heap_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort,
            "Radix Sort": radix_sort,
            "Selection Sort": selection_sort,
            "Bucket Sort": bucket_sort
        }

        # Obtener método y dirección de ordenamiento
        method = sorting_method.get()
        ascending = order_direction.get() == "Ascendente"
        sorted_data = sort_algorithms[method](data.copy(), ascending)

        # Mostrar datos originales
        original_data_text.config(state=tk.NORMAL)
        original_data_text.delete(1.0, tk.END)
        original_data_text.insert(tk.END, "Datos originales (edades):\n")
        original_data_text.insert(tk.END, ", ".join(map(str, data)))
        original_data_text.config(state=tk.DISABLED)

        # Mostrar datos ordenados
        sorted_data_text.config(state=tk.NORMAL)
        sorted_data_text.delete(1.0, tk.END)
        sorted_data_text.insert(tk.END, "Datos ordenados (edades):\n")
        sorted_data_text.insert(tk.END, ", ".join(map(str, sorted_data)))
        sorted_data_text.config(state=tk.DISABLED)
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Configuración de la ventana
root = tk.Tk()
root.title("Ordenamiento de Edades desde API")
root.geometry("600x500")

# Marco para datos originales
frame_original = tk.Frame(root)
frame_original.pack(pady=10)

tk.Label(frame_original, text="Datos Originales", font=("Arial", 12, "bold")).pack()
original_data_text = scrolledtext.ScrolledText(frame_original, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
original_data_text.pack()

# Marco para datos ordenados
frame_sorted = tk.Frame(root)
frame_sorted.pack(pady=10)

tk.Label(frame_sorted, text="Datos Ordenados", font=("Arial", 12, "bold")).pack()
sorted_data_text = scrolledtext.ScrolledText(frame_sorted, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
sorted_data_text.pack()

# Controles
frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

# Selección de método
tk.Label(frame_controls, text="Método de ordenamiento:").grid(row=0, column=0, padx=5, pady=5)
sorting_method = tk.StringVar(value="Burbuja")
tk.OptionMenu(frame_controls, sorting_method, 
            "Bubble Sort", "Counting Sort", "Heap Sort", "Insertion Sort", 
            "Merge Sort", "Quick Sort", "Radix Sort", "Selection Sort", "Bucket Sort").grid(row=0, column=1, padx=5, pady=5)


# Selección de dirección
tk.Label(frame_controls, text="Ordenamiento:").grid(row=1, column=0, padx=5, pady=5)
order_direction = tk.StringVar(value="Ascendente")
tk.OptionMenu(frame_controls, order_direction, "Ascendente", "Descendente").grid(row=1, column=1, padx=5, pady=5)

# Botón para ordenar
tk.Button(frame_controls, text="Ordenar Edades", command=show_sorted_data).grid(row=2, column=0, columnspan=2, pady=10)

# Ejecutar la interfaz
root.mainloop()
