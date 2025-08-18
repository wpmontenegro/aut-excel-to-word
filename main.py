import os
import re
from docxtpl import DocxTemplate
from datetime import date
from utils import load_clean_excel, current_date_format, export_to_xray_csv
from pathlib import Path

# Datos de entrada
patron = r"^HU-\d{3}$"
while True:
    userStory = input('Ingrese el nombre de la HU con el formato HU-XXX: ').upper().strip()
    if re.match(patron, userStory):
        break
    else:
        print("Por favor ingrese nuevamente con el formato correcto (Ej. HU-123)")

# Rutas de los archivos y nombre primera cabecera
EXCEL_FILE = f"input/{userStory} - Matriz de Casos.xlsx"
ID_HEADER = "ID de caso de prueba"
TEMPLATE_FILE = "format/Evidencia de Pruebas Template.docx"
OUTPUT_FOLDER = "output_cases"

# Crear carpeta de salida si no existe
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Leer el Excel
df = load_clean_excel(EXCEL_FILE, ID_HEADER)

# Cargar la plantilla de Word
path = Path(TEMPLATE_FILE)
if not path.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {path}")

template = DocxTemplate(path)

# Genera fecha actual
today = current_date_format(date.today())

# Exportar casos a CSV
output_path_csv = os.path.join(OUTPUT_FOLDER, f"{userStory} - Test Case Export.csv")
export_to_xray_csv(df, output_path_csv)

# Recorrer cada fila del Excel
for index, row in df.iterrows():
     # Procesar pasos: separarlos por salto de línea y crear lista de dicts
    pasos_lista = []
    if isinstance(row["Pasos"], str):
        # Primero filtras pasos vacíos
        pasos_filtrados = [p.strip() for p in row["Pasos"].split("\n") if p.strip()]

        # Luego se enumera ya filtrados
        for i, paso in enumerate(pasos_filtrados, start=1):
            pasos_lista.append({"num": i, "desc": paso})

    # Convertir la fila en diccionario
    contexto = {
        "userStory": userStory,
        "currentDate": today,
        "id": row[ID_HEADER].strip(),
        "title": row["Descripción de la prueba"],
        "preconditions": row["Prerrequisitos"],
        "steps": pasos_lista,
        "expectedResult": row["Resultado esperado"]
    }

    # Renderizar plantilla con los datos
    template.render(contexto)

    # Guardar documento
    output_path = os.path.join(OUTPUT_FOLDER, f"{userStory}_{row[ID_HEADER]} - Evidencia de Pruebas.docx")
    template.save(output_path)

    print(f"✅ Archivo generado: {output_path}")