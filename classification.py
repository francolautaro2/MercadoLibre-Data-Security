from database import update_criticality

def classification_response(name, conn):

    classification = input(f"Ingrese la criticidad de {name} (CRITICO/ALTO/MEDIO/BAJO): ")
    classification = classification.upper()  # Convertir a mayúsculas para hacer la comparación insensible a mayúsculas y minúsculas
    
    if classification == "CRITICO":
        update_criticality(classification, name, conn)
        # Maneja los cambios para cambiar la visibilidad del archivo

    elif classification == "ALTO":
        update_criticality(classification, name, conn)
        # Maneja los cambios para cambiar la visibilidad del archivo

    elif classification == "MEDIO":
        update_criticality(classification, name, conn)
        # Maneja los cambios para cambiar la visibilidad del archivo

    elif classification == "BAJO":
        update_criticality(classification, name, conn)
        # Maneja los cambios para cambiar la visibilidad del archivo

    else:
        print("Por favor ingrese una criticidad correcta.")

