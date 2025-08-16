import pandas as pd
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