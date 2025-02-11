class Carrito:
    def __init__(self):
        self.productos = []
        self.total = 0.0

    def agregar_producto(self, nombre, precio):
        self.productos.append((nombre, precio))
        self.total += precio
        print(f"Producto '{nombre}' añadido al carrito.")

    def eliminar_producto(self, nombre):
        for producto in self.productos:
            if producto[0] == nombre:
                self.total -= producto[1]
                self.productos.remove(producto)
                print(f"Producto '{nombre}' eliminado del carrito.")
                return
        print(f"Producto '{nombre}' no encontrado en el carrito.")

    def ver_carrito(self):
        if not self.productos:
            print("El carrito está vacío.")
        else:
            print("Productos en el carrito:")
            for producto in self.productos:
                print(f"- {producto[0]}: ${producto[1]:.2f}")
            print(f"Total: ${self.total:.2f}")
    
    def vaciar_carrito(self):
        self.productos = []
        self.total = 0.0
        print("El carrito ha sido vaciado.")

    def aplicar_descuento(self, edad):
        if edad < 25:
            descuento = 0.10
        elif 26 <= edad <= 40:
            descuento = 0.15
        elif 41 <= edad <= 60:
            descuento = 0.0
        else:
            descuento = 0.30

        total_con_descuento = self.total * (1 - descuento)
        print(f"Descuento aplicado: {descuento * 100}%")
        print(f"Total con descuento: ${total_con_descuento:.2f}")

def mostrar_productos_disponibles(productos):
    print("\nProductos disponibles:")
    for idx, (nombre, precio) in enumerate(productos, start=1):
        print(f"{idx}. {nombre}: ${precio:.2f}")

def main():
    carrito = Carrito()
    
    # Lista de productos predefinidos
    productos_disponibles = [
        ("Ron", 80000),
        ("Aguardiente", 70000),
        ("Vodka", 100000),
        ("Whisky", 175000),
        ("FourLoko", 25000),
        ("Cerveza", 5000)
    ]
    
    edad = int(input("Por favor, ingrese su edad para aplicar el descuento: "))
    
    while True:
        print("\n--- Menú ---")
        print("1. Ver carrito")
        print("2. Añadir producto al carrito")
        print("3. Eliminar producto del carrito")
        print("4. Calcular total con descuento")
        print("5. Pagar")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            carrito.ver_carrito()
        elif opcion == "2":
            mostrar_productos_disponibles(productos_disponibles)
            try:
                seleccion = int(input("Seleccione el número del producto que desea añadir: "))
                if 1 <= seleccion <= len(productos_disponibles):            
                    nombre, precio = productos_disponibles[seleccion - 1]
                    carrito.agregar_producto(nombre, precio)
                else:
                    print("Selección no válida. Intente de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")
        elif opcion == "3":
            nombre = input("Ingrese el nombre del producto a eliminar: ")
            carrito.eliminar_producto(nombre)
        elif opcion == "4":
            carrito.aplicar_descuento(edad)
        elif opcion == "5":
            if not carrito.productos:
                print("El carrito está vacío. No hay nada que pagar.")
            else:
                total_con_descuento = carrito.aplicar_descuento(edad)
                print(f"\n¡Gracias por su compra! Total a pagar: ${total_con_descuento:.2f}")
                carrito.vaciar_carrito()
        elif opcion == "6":
            print("Gracias por usar el carrito de compras. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()