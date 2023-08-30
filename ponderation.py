from database import update_criticality, update_visibility
from google_drive import change_public_access
# Pondera las respuestas asignando un puntaje, las respuestas estan en una lista de tipo ["Si", "No", "No", "Si"]
async def asignar_clasificacion_ponderada(drive, respuestas, file_id):
    
    num_respuestas_si = respuestas.count("Si")

    if num_respuestas_si >= 4:
        await update_criticality("CRITICO", file_id)
        # Cambia la visibilidad en la base de datos
        await update_visibility("Privado", file_id)
        # Cambia la visibilidad en google drive
        await change_public_access(drive, file_id)
    elif num_respuestas_si >= 3:
        await update_criticality("ALTO", file_id)
        await update_visibility("Privado", file_id)
        # Cambia la visibilidad en google drive
        await change_public_access(drive, file_id)
    elif num_respuestas_si >= 2:
        # Cambia la visibilidad en la base de datos
        await update_criticality("MEDIO", file_id)
    else:
        # Cambia la visibilidad en la base de datos
        await update_criticality("BAJO", file_id)
