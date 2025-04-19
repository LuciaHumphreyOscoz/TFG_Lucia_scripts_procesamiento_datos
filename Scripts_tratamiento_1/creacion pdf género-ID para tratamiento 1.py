import pandas as pd
from fpdf import FPDF
import os

# ----------- CONFIGURACIÓN -----------
file_path = r"C:\Users\lucia\Downloads\asignacion_tratamiento_1_2025-04-14.csv"
file_path = file_path.replace("\\", "/")

# ----------- CARGA Y LIMPIEZA DE DATOS -----------
df = pd.read_csv(file_path)

# Seleccionar columnas limpias directamente
df = df[[
    'player.custom_participant_id',
    'player.gender'
]].copy()

# Renombrar para que se vean más limpias en el PDF
df.columns = ['custom_id', 'gender']
df = df.sort_values(by='custom_id')
df = df[df['custom_id'].notna() & (df['custom_id'].astype(str).str.strip() != "")]

# ----------- GENERAR PDF -----------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", style='B', size=14)
pdf.cell(0, 10, "Listado de Participantes - Custom ID y Género", ln=True, align='C')
pdf.ln(10)

# Encabezados
pdf.set_font("Arial", style='B', size=11)
pdf.set_fill_color(220, 220, 220)
pdf.cell(60, 10, "Custom ID", 1, 0, 'C', True)
pdf.cell(60, 10, "Género", 1, 1, 'C', True)

# Filas
pdf.set_font("Arial", size=11)
for _, row in df.iterrows():
    pdf.cell(60, 10, str(int(row["custom_id"])), 1, 0, 'C')
    pdf.cell(60, 10, str(row["gender"]), 1, 1, 'C')

# Rutas de guardado
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
pdf_download_path = os.path.join(downloads_folder, "participantes_genero_tratamiento_1.pdf")

desktop_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 1")
os.makedirs(desktop_folder, exist_ok=True)
pdf_desktop_path = os.path.join(desktop_folder, "participantes_genero_tratamiento_1.pdf")

# Guardar PDF en ambas rutas
pdf.output(pdf_download_path)
pdf.output(pdf_desktop_path)

print(f"✅ PDF creado: {pdf_download_path}")
print(f"✅ Copia en escritorio: {pdf_desktop_path}")
