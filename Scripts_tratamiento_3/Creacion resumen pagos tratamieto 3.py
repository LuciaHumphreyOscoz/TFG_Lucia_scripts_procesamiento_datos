import pandas as pd
import os
from fpdf import FPDF

# -------- CONFIGURACIÓN --------
file_path = r"C:\Users\lucia\Downloads\ultimatum_tratamiento_3_2025-04-15.csv".replace("\\", "/")

downloads = os.path.join(os.path.expanduser("~"), "Downloads")
desktop_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 3")
os.makedirs(desktop_folder, exist_ok=True)

output_excel = os.path.join(downloads, "resumen_pagos_tratamiento_3.xlsx")
desktop_output_excel = os.path.join(desktop_folder, "resumen_pagos_tratamiento_3.xlsx")
pdf_path_downloads = os.path.join(downloads, "resumen_pagos_tratamiento_3.pdf")
pdf_path_desktop = os.path.join(desktop_folder, "resumen_pagos_tratamiento_3.pdf")

# -------- CARGA Y PROCESAMIENTO DE DATOS --------
df = pd.read_csv(file_path)

# Usar la columna correcta de pago total
columns_needed = ["player.custom_participant_id", "player.total_payment_euros"]
df = df[columns_needed].rename(columns={
    "player.custom_participant_id": "custom_id",
    "player.total_payment_euros": "pago_euros"
})

# Filtrar solo IDs válidos de 3 dígitos
df = df[df["custom_id"].notna()].copy()
df["custom_id_str"] = df["custom_id"].astype(int).astype(str)
df = df[df["custom_id_str"].str.match(r"^\d{3}$")]
df["custom_id"] = df["custom_id_str"].astype(int)
df.drop(columns="custom_id_str", inplace=True)

# Conversión y orden
df["pago_euros"] = df["pago_euros"].astype(float)
df = df.sort_values(by="custom_id")

# -------- GUARDAR EXCEL --------
df.to_excel(output_excel, index=False)
df.to_excel(desktop_output_excel, index=False)

# -------- GENERAR PDF --------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", style='B', size=14)
pdf.cell(0, 10, "Resumen de Pagos - Tratamiento 3", ln=True, align='C')
pdf.ln(10)

# Configuración tabla centrada
table_width = 100  # total width of table (2 columns: 50 + 50)
page_width = 210  # A4 width in mm
x_start = (page_width - table_width) / 2
pdf.set_x(x_start)

# Encabezados
pdf.set_font("Arial", style='B', size=11)
pdf.set_fill_color(220, 220, 220)
pdf.cell(50, 10, "Custom ID", 1, 0, 'C', True)
pdf.cell(50, 10, "Pago (EUR)", 1, 1, 'C', True)

# Filas con alineación centrada
pdf.set_font("Arial", size=10)
for _, row in df.iterrows():
    pdf.set_x(x_start)
    pdf.cell(50, 10, str(int(row["custom_id"])), 1, 0, 'C')
    pdf.cell(50, 10, f'{row["pago_euros"]:.1f} EUR', 1, 1, 'C')

# Guardar PDF
pdf.output(pdf_path_downloads)
pdf.output(pdf_path_desktop)

# -------- MENSAJE FINAL --------
print(f"✅ Excel creado: {output_excel}")
print(f"✅ PDF creado: {pdf_path_downloads}")
print(f"✅ Copias también en: {desktop_folder}")