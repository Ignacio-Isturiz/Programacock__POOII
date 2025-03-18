import requests
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

# Importar los algoritmos de ordenamiento
from bucket_sort import BucketSort
from bubble_sort import BubbleSort
from counting_sort import CountingSort
from heap_sort import HeapSort
from insertion_sort import InsertionSort
from merge_sort import MergeSort
from quick_sort import QuickSort
from selection_sort import SelectionSort

# Definición de la interfaz para los algoritmos de ordenamiento
class SortingAlgorithm(ABC):
    @abstractmethod
    def sort(self, arr, ascending=True):
        pass

# Función para obtener y limpiar los datos desde la API
def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            return []

        # Convertir datos numéricos
        for item in data:
            for key in item.keys():
                if isinstance(item[key], str) and item[key].isdigit():
                    item[key] = int(item[key])  # Convertir a entero si es posible

        return data
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error al consumir la API: {e}")
        return []

# Función para actualizar la tabla con los datos
def update_table(data, tree):
    tree.delete(*tree.get_children())
    for item in data:
        values = [item.get(col, "") for col in columns]
        tree.insert("", "end", values=values)

# Función para ordenar los datos
def sort_data():
    selected_column = column_selector.get()
    method = sorting_method.get()
    ascending = order_direction.get() == "Ascendente"

    if not selected_column or method not in sort_algorithms:
        messagebox.showerror("Error", "Seleccione una columna y un método válido")
        return

    try:
        # Filtrar solo los valores numéricos
        sortable_data = [item for item in dataset if isinstance(item.get(selected_column), (int, float))]

        if not sortable_data:
            messagebox.showerror("Error", f"No hay datos numéricos en la columna '{selected_column}'")
            return

        # Extraer valores para ordenar
        values_to_sort = [item[selected_column] for item in sortable_data]

        # Aplicar el algoritmo de ordenamiento
        sorted_values = sort_algorithms[method].sort(values_to_sort, ascending)

        # Ordenar dataset basado en los valores ordenados
        sorted_dataset = sorted(dataset, key=lambda x: sorted_values.index(x[selected_column]) if x[selected_column] in sorted_values else float('inf'))

        update_table(sorted_dataset, sorted_data_tree)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Configuración de la ventana
root = tk.Tk()
root.title("Ordenamiento de Dataset desde API")
root.geometry("800x600")

# URL de la API
api_url = "https://www.datos.gov.co/resource/sgf4-8tf8.json"
dataset = fetch_data(api_url)
columns = list(dataset[0].keys()) if dataset else []

# Incluir "edad fallecido" y "codigo institucion" si están presentes en los datos
# Incluir "edad fallecido" y "codigo institucion" si están en los datos
if any("edad_fallecido" in item for item in dataset) and "edad_fallecido" not in columns:
    columns.append("edad_fallecido")
    
if any("codigo_institucion" in item for item in dataset) and "codigo_institucion" not in columns:
    columns.append("codigo_institucion")


# Filtrar solo columnas con valores numéricos

# Filtrar solo columnas con valores numéricos
numeric_columns = [
    col for col in columns 
    if any(isinstance(item.get(col), (int, float)) for item in dataset)
]
# Diccionario de algoritmos de ordenamiento
sort_algorithms = {
    "Bubble Sort": BubbleSort(),
    "Counting Sort": CountingSort(),
    "Heap Sort": HeapSort(),
    "Insertion Sort": InsertionSort(),
    "Merge Sort": MergeSort(),
    "Quick Sort": QuickSort(),
    "Radix Sort": BucketSort(),
    "Selection Sort": SelectionSort(),
    "Bucket Sort": BucketSort()
}

# Marco para mostrar datos originales
frame_data = tk.Frame(root)
frame_data.pack(pady=10)

tk.Label(frame_data, text="Dataset Original", font=("Arial", 12, "bold")).pack()
columns_display = columns if columns else ["No Data"]
original_data_tree = ttk.Treeview(frame_data, columns=columns_display, show="headings")
for col in columns_display:
    original_data_tree.heading(col, text=col)
    original_data_tree.column(col, width=100)
original_data_tree.pack()

update_table(dataset, original_data_tree)

# Marco de controles
frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

tk.Label(frame_controls, text="Seleccionar Columna:").grid(row=0, column=0, padx=5, pady=5)
column_selector = ttk.Combobox(frame_controls, values=numeric_columns)
column_selector.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_controls, text="Método de ordenamiento:").grid(row=1, column=0, padx=5, pady=5)
sorting_method = tk.StringVar(value="Bubble Sort")
ttk.Combobox(frame_controls, textvariable=sorting_method, values=list(sort_algorithms.keys())).grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_controls, text="Orden:").grid(row=2, column=0, padx=5, pady=5)
order_direction = tk.StringVar(value="Ascendente")
ttk.Combobox(frame_controls, textvariable=order_direction, values=["Ascendente", "Descendente"]).grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_controls, text="Ordenar", command=sort_data).grid(row=3, column=0, columnspan=2, pady=10)

# Marco para mostrar datos ordenados
frame_sorted = tk.Frame(root)
frame_sorted.pack(pady=10)

tk.Label(frame_sorted, text="Dataset Ordenado", font=("Arial", 12, "bold")).pack()
sorted_data_tree = ttk.Treeview(frame_sorted, columns=columns_display, show="headings")
for col in columns_display:
    sorted_data_tree.heading(col, text=col)
    sorted_data_tree.column(col, width=100)
sorted_data_tree.pack()

# Cargar datos en la tabla
update_table(dataset, original_data_tree)

root.mainloop()
