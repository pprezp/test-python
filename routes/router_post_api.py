from models.db_config import db
from datetime import datetime
from fastapi import APIRouter, Response, status, File, UploadFile, responses, Form
from functions import AuthHandler
from models.file_base_model import FileModel
from dotenv import load_dotenv
import base64
load_dotenv()

router = APIRouter()

@router.post('/files')
async def create_file(fileModel: FileModel, response: Response):

    try:

        file_extension_list = ['jpeg', 'gif', 'pdf']
        file_name = fileModel.file_name
        file_extension = file_name.split('.')[-1]
        aprobado = fileModel.aprobado
        file_size = (len(fileModel.file_content) * 3) / 4 - fileModel.file_content.count('=', -2)
        now_date = datetime.now().strftime("%Y-%m-%d")

        if fileModel.category not in (1, 2, 3, 4, 5, 6, 7):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                'error': 'Ingresa una categoria valida'
            }

        if file_size > 200000:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                'error': 'El archivo pesa más de 200KB, debes de reducirlo antes de subirlo'
            }

        if (aprobado > 1 or aprobado < 0):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                'error': 'El estado de aprobado es diferente de 0 o 1, colocar un valor correcto'
            }

        aprobado = 2 if aprobado == 1 else 0

        if file_extension in file_extension_list:
            
            file_content = base64.b64decode(fileModel.file_content).hex()

            insert_query = f"""
                INSERT INTO ArchivosPorUsuario(
                    estafeta,
                    id_NombreCarpeta,
                    nombreArchivo,
                    aprobado,
                    documento,
                    tamanio,
                    fecha_escaneo,
                    fecha_carga,
                    usuario_subio
                )
                VALUES(
                    {fileModel.estafeta},
                    {fileModel.category},
                    '{file_name}',
                    {aprobado},
                    0x{file_content},
                    {file_size},
                    CONVERT(datetime, '{now_date}', 102),
                    CONVERT(datetime, '{now_date}', 102),
                    1
                )
            """

            conn = db.get_connection()
            print(conn)
            cursor = conn.cursor()
            cursor.execute(insert_query)
            conn.commit()
            conn.close()

            return { 
                'success':True
            }
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "error": f"El formato de archivo {file_name}, (.{file_extension}) no es compatible."
            }
        
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "error": str(e)
        }
