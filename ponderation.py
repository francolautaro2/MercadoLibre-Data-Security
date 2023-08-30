from database import update_criticality, update_visibility

# Pondera las respuestas asignando un puntaje, las respuestas estan en una lista de tipo ["Si", "No", "No", "Si"]
async def asignar_clasificacion_ponderada(respuestas, file_id):
    
    num_respuestas_si = respuestas.count("Si")

    if num_respuestas_si >= 4:
        await update_criticality("CRITICO", file_id)
        await update_visibility("Privado", file_id)
    elif num_respuestas_si >= 3:
        await update_criticality("ALTO", file_id)
        await update_visibility("Privado", file_id)
    elif num_respuestas_si >= 2:
        await update_criticality("MEDIO", file_id)
    else:
        await update_criticality("BAJO", file_id)
