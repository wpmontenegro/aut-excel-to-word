import os
import re
from docxtpl import DocxTemplate

from utils import load_clean_excel, export_to_xray_csv, export_to_word
from pathlib import Path

# Datos de entrada
PATTERN = r"^HU-\d{3,}$"
while True:
    requirement = input('Ingrese el nombre de la HU con el formato HU-XXX: ').upper().strip()
    if re.match(PATTERN, requirement):
        break
    else:
        print("Por favor ingrese nuevamente con el formato correcto (Ej. HU-123)")

# Rutas de los archivos y nombre primera cabecera
EXCEL_FILE = f"input/{requirement} - Matriz de Casos.xlsx"
TEMPLATE_FILE = "format/Evidencia de Pruebas Template.docx"
OUTPUT_FOLDER = "output_cases"

# Crear carpeta de salida si no existe
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Leer el Excel y remplazar espacios en los nombres de las columnas
df = load_clean_excel(EXCEL_FILE)

# Cargar la plantilla de Word
path = Path(TEMPLATE_FILE)
if not path.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {path}")

template = DocxTemplate(path)

# Exportar casos como evidencia a Word
export_to_word(df, template, requirement, OUTPUT_FOLDER)

# Exportar casos a CSV
export_to_xray_csv(df, requirement, OUTPUT_FOLDER)