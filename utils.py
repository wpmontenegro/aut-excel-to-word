import pandas as pd
import csv
from pathlib import Path

def load_clean_excel(path, search_header="ID"):
    # Verificamos si existe el archivo
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    # Leer sin cabecera para buscar la fila real
    tmp = pd.read_excel(path, header=None)

    # Buscar fila con el nombre de columna clave
    header_row = tmp[tmp.eq(search_header).any(axis=1)].index[0]

    # Volver a leer con la cabecera correcta
    df = pd.read_excel(path, header=header_row)

    # Eliminar columnas vacías
    df = df.dropna(axis=1, how="all")

    # Eliminar filas vacías
    df = df.dropna(how="all")

    return df

def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)

    return messsage

def is_integer(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False
    

def export_to_xray_csv(df, output_csv):
    filas = []

    for _, row in df.iterrows():
        case_id = row["ID de caso de prueba"]
        summary = row.get("Descripción de la prueba", "")
        preconditions = row.get("Prerrequisitos", "")
        expectedResult = row.get("Resultado esperado", "")
        
        # Dividir pasos (uno por línea) y limpiar espacios
        pasos = [p.strip() for p in str(row.get("Pasos", "")).split("\n") if p.strip()]
        
        for i, paso in enumerate(pasos):
            if i == 0:
                # Primera fila del caso: incluye toda la información
                filas.append({
                    "TCID": case_id,
                    "Test Summary": summary,
                    "Test Type": "Manual",
                    "Preconditions": preconditions,
                    "Action": paso,
                    "Result": expectedResult
                })
            else:
                # Filas siguientes solo con el paso
                filas.append({
                    "TCID": case_id,
                    "Test Summary": "",
                    "Test Type": "",
                    "Test Summary": "",
                    "Action": paso,
                    "Result": ""
                })
    
    # Convertir a DataFrame final y exportar a CSV
    df_out = pd.DataFrame(filas)
    df_out.to_csv(output_csv, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)
    print(f"✅ Archivo CSV generado en: {output_csv}")