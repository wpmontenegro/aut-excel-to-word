import pandas as pd
import csv, html, os, re
from pathlib import Path
from datetime import date

FIRST_HEADER_EXCEL = "ID del caso"
CUSTOM_FIELDS = {
    "id": "ID del caso",
    "requirement": "HU",
    "steps": "Pasos",
    "currentDate": "Fecha actual",
}
MONTHS_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

def load_clean_excel(path):
    # Verificamos si existe el archivo
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    # Leer sin cabecera para buscar la fila real
    tmp = pd.read_excel(path, header=None)

    # Buscar fila con el nombre de columna clave
    header_row = tmp[tmp.eq(FIRST_HEADER_EXCEL).any(axis=1)].first_valid_index()
    if header_row is None:
        raise ValueError(f"No se encontró la cabecera con '{FIRST_HEADER_EXCEL}' en el Excel: {path}")

    # Volver a leer con la cabecera correcta
    df = pd.read_excel(path, header=header_row)

    # Eliminar columnas vacías
    df = df.dropna(axis=1, how="all")

    # Eliminar filas vacías
    df = df.dropna(how="all")

    return df

def current_date_format(fecha: date) -> str:
    return f"{fecha.day} de {MONTHS_ES[fecha.month - 1]} del {fecha.year}"

def is_integer(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

def sanitize_text(text):
    if pd.isna(text):
        return ""
      # Convierte < > & en &lt; &gt; &amp;
    return html.escape(str(text))

def normalize_header(header: str) -> str:
    return header.strip().replace(" ", "_")

def clear_numeration(str: str) -> str:
    # Quita el patrón tipo "1) " al inicio
    return re.sub(r'^\s*\d+\)\s*', '', str).strip()

def separate_steps(texto):
    # Dividir con regex que detecta "número)"
    partes = re.split(r'(?=\d+\))', texto.strip())
    # Limpiar y quitar vacíos
    pasos = [clear_numeration(p.strip()) for p in partes if p.strip()]
    return pasos

def export_to_word(df, template, userStory, output_folder):
    today = current_date_format(date.today())
    # Recorrer cada fila del Excel
    for _, row in df.iterrows():
     # Procesar pasos: separarlos por salto de línea y crear lista de dicts
        pasos_lista = []
        # Primero filtras pasos vacíos
        pasos_filtrados = separate_steps(row[CUSTOM_FIELDS["steps"]])

        # Luego se enumera ya filtrados
        pasos_lista = [{"num": i, "desc": paso} for i, paso in enumerate(pasos_filtrados, start=1)]

        # Convertir la fila en diccionario
        contexto = {
            normalize_header(col): sanitize_text(row[col]) if isinstance(row[col], str) else row[col]
            for col in df.columns
        }
        
        # Campos adicionales
        contexto.update({
            normalize_header(CUSTOM_FIELDS["requirement"]): userStory,
            normalize_header(CUSTOM_FIELDS["currentDate"]): today,
            normalize_header(CUSTOM_FIELDS["steps"]): pasos_lista
        })

        # Renderizar plantilla con los datos
        template.render(contexto)

        # Guardar documento
        output_path = os.path.join(output_folder, f"{userStory}_{row[CUSTOM_FIELDS["id"]]} - Evidencia de Pruebas.docx")
        template.save(output_path)

        print(f"✅ Archivo generado: {output_path}")

def export_to_xray_csv(df, user_story, output_folder):
    id_col = CUSTOM_FIELDS["id"]
    steps_col = CUSTOM_FIELDS["steps"]

    filas = []
    for _, row in df.iterrows():
        case_id = row.get(id_col, "")
        steps_raw = row.get(steps_col, "")

        # dividir pasos por salto de línea y limpiar vacíos
        pasos = separate_steps(steps_raw)

        for i, paso in enumerate(pasos):
            nueva_fila = {}
            for col in df.columns:
                if col == steps_col:
                    nueva_fila[col] = paso
                elif col == id_col:
                    nueva_fila[col] = case_id
                else:
                    # solo en la primera fila se pone valor, después vacío
                    nueva_fila[col] = row[col] if i == 0 else ""
            filas.append(nueva_fila)

    df_out = pd.DataFrame(filas, columns=df.columns)

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{user_story} - Casos para Xray.csv")

    df_out.to_csv(output_path, sep=";", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
    print(f"✅ CSV generado: {output_path}")