from database import update_criticality, get_id_file, connect_database
from google_drive import change_public_access


def classification_response(name, visibility, conn, service):
    while True:
        classification = input(f"Ingrese la criticidad de {name} (CRITICO/ALTO/MEDIO/BAJO): ")
        classification = classification.upper()  # Convertir a mayúsculas para hacer la comparación insensible a mayúsculas y minúsculas
        
        if classification == "CRITICO":
            update_criticality(classification, name, conn)
            # Maneja los cambios para cambiar la visibilidad del archivo si este es publico
            if visibility == "Publico":
                print("El file es publico, se cambiara su visibilidad a privado.")
                file_id = get_id_file(name,conn)
                change_public_access(file_id[0], service)
                break
            break
        elif classification == "ALTO":
            update_criticality(classification, name, conn)
            # Maneja los cambios para cambiar la visibilidad del archivo
            if visibility == "Publico":
                print("El file es publico, se cambiara su visibilidad a privado.")
                file_id = get_id_file(name,conn)
                change_public_access(file_id[0], service)
                break
            break
        elif classification == "MEDIO":
            update_criticality(classification, name, conn)
            break
        elif classification == "BAJO":
            update_criticality(classification, name, conn)
            break
        else:
            print("Por favor ingrese una criticidad correcta.")

