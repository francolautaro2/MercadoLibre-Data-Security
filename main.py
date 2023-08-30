
import asyncio

from google_drive import get_drive, get_files
from formularios import read_responses, get_forms_service, create_forms
from database import obtener_datos_no_clasificados, guardar_datos
from email_form import enviar_correos

    
async def main():
    print("Inicio del programa")
    form_service = await get_forms_service()
    drive = await get_drive()
    
    while True:
        files = await get_files(drive)
        await guardar_datos(files)
        archivos_no_clasificados = await obtener_datos_no_clasificados()
        formularios = await create_forms(form_service, drive, archivos_no_clasificados)
        await enviar_correos(drive,formularios)
        await read_responses(form_service, drive, formularios)
        await asyncio.sleep(10)
        print("Proceso terminado")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
