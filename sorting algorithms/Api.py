import requests

def fetch_data(api_url):
    try:
        print(f"Intentando consumir la API: {api_url}")
        response = requests.get(api_url)
        print(f"Respuesta de la API: {response.status_code}")

        response.raise_for_status()  # Lanza una excepción si la respuesta no es 200
        data = response.json()
        print(f"Datos obtenidos de la API: {data}")

        # Verifica si la respuesta es una lista
        if isinstance(data, list) and len(data) > 0:
            ages = []
            for item in data:
                if 'edad_fallecido' in item:
                    try:
                        age = int(item['edad_fallecido'])  # Convierte a entero
                        ages.append(age)
                    except ValueError:
                        print(f"Advertencia: No se pudo convertir 'edad_fallecido' en: {item}")

            print(f"Edades extraídas: {ages}")
            return ages if ages else None  # Retorna None si no hay edades válidas
        else:
            print("La API no devolvió datos válidos o no contiene el campo 'edad_fallecido'.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al consumir la API: {e}")
        return None
