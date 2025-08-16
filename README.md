# Generador de Evidencias de Casos de Prueba

Este proyecto automatiza la conversión de casos de prueba documentados en un archivo Excel a un documento Word listo para ser utilizado como evidencia.  
Su objetivo es **reducir el tiempo manual** de copiar y dar formato, permitiendo que cualquier persona genere documentación profesional con unos pocos pasos.

## 🚀 Características
- Lee casos de prueba desde un archivo Excel.
- Genera automáticamente un documento Word con formato estándar.
- No requiere conocimientos técnicos avanzados para usarlo.

## 📋 Requisitos
- Python 3.9 o superior
- Librerías:
  - `pandas`
  - `openpyxl`
  - `python-docx`

Puedes instalarlas ejecutando:
```bash
pip install pandas openpyxl docxtpl
```

## 📥 Datos de entrada

Cuando el programa se ejecuta, solicitará:

### 1. Nombre del requerimiento
Debe tener la siguiente nomenclatura: HU-XXX (Ejemplo: HU-123)

## 💻 Ejecución

En la consola:
```bash
python main.py
```
Luego, el programa te pedirá cada dato de entrada uno por uno.
```yml
Ingrese el nombre de la HU con el formato HU-XXX: HU-123

✅ Documento generado: output_cases\HU-123_TC_001- Evidencia de Pruebas.docx
```

## 🎯 Beneficios

- Ahorra horas de trabajo manual.
- Estandariza la documentación.
- Fácil de usar para cualquier miembro del equipo.