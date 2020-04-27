import gspread
import datetime
import json
from os import path
from tempfile import TemporaryDirectory as TempD
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
googleapi = {
    "type": "service_account",
    "project_id": settings.PROJECT_ID,
    "private_key_id": settings.PRIVATE_KEY_ID,
    "private_key": settings.PRIVATE_KEY,
    "client_email": settings.CLIENT_EMAIL,
    "client_id": settings.CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": settings.CLIENT_X509_CART_URL
}

with TempD() as tmpdir:
    file_path = path.join(tmpdir, "googleapi.json")
    with open(file_path, 'w') as f:
        json.dump(googleapi, f)
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_api/cursounam.json', scope)
    client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

def existe_cuenta(cuenta):
    """"""
    # Check if is a test
    if cuenta in ['miguel', 'pablo', 'panta', 'haydee', 'fernanda']:
        return True

    sheet = client.open("curso_test").worksheet("Cuentas")
    cuentas = sheet.get_all_values()
    cuentas = [str(cuenta)[2:-2] for cuenta in cuentas]
    if cuenta in cuentas:
        return True
    else:
        return False

def google_cuentas():
    """"""
    sheet = client.open("curso_test").worksheet("Cuentas")
    cuentas = sheet.col_values(1)
    # Add names to test
    for name in ['miguel', 'pablo', 'panta', 'haydee', 'fernanda']:
        cuentas.append(name)

    return cuentas

def google_cuentas_tema(tema):
    """"""
    sheet = client.open("curso_test").worksheet(tema)
    cuentas = sheet.col_values(1)
    return cuentas[1:]

def existe_calificacion(cuenta, tema):
    """"""
    cuentas = google_cuentas_tema(tema)
    if cuenta in cuentas:
        return True
    else:
        return False

def agregar_calificacion(tema, cuenta, calif, tiempo, preguntas):
    """"""
    # Check if is a test
    if cuenta in ['miguel', 'pablo', 'panta', 'haydee', 'fernanda']:
        tema = 'test'

    sheet = client.open("curso_test").worksheet(tema)
    cuentas = sheet.col_values(1)
    ctas_ultima_posicion = len(cuentas[1:]) # Quitamos cabezeras
    for i in range(1, 25):#[1,2,3,4,5,6,7,8,9,10,11,12,13]:  #,13,14,15,16,17,18,19]:
        if i == 1:
            # Cuenta
            sheet.update_cell(ctas_ultima_posicion + 2, i, cuenta)
        elif i == 2:
            # Calificacion
            sheet.update_cell(ctas_ultima_posicion + 2, i, str(calif))
        elif i == 3:
            # Fecha
            date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            sheet.update_cell(ctas_ultima_posicion + 2, i, date)
        elif i == 4:
            # Tiempo
            sheet.update_cell(ctas_ultima_posicion + 2, i, str(tiempo))
        else:
            index = i - 5
            # Preguntas
            sheet.update_cell(ctas_ultima_posicion + 2, i, str(preguntas[index]))
