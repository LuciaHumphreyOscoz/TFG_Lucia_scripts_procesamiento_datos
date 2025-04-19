import pandas as pd
import os
from fpdf import FPDF

# -------- CONFIGURACIÓN --------
file_path = r"C:\Users\lucia\Downloads\ultimatum_tratamiento_1_M_2025-04-14.csv".replace("\\", "/")

downloads = os.path.join(os.path.expanduser("~"), "Downloads")
desktop_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 1")
os.makedirs(desktop_folder, exist_ok=True)

# Rutas de salida
xlsx_path_downloads = os.path.join(downloads, "resumen_pagos_tratamiento_1.xlsx")
xlsx_path_desktop = os.path.join(desktop_folder, "resumen_pagos_tratamiento_1.xlsx")
csv_path_downloads = os.path.join(downloads, "resumen_pagos_tratamiento_1.csv")
csv_path_desktop = os.path.join(desktop_folder, "resumen_pagos_tratamiento_1.csv")
pdf_path_downloads = os.path.join(downloads, "resumen_pagos_tratamiento_1.pdf")
pdf_path_desktop = os.path.join(desktop_folder, "resumen_pagos_tratamiento_1.pdf")

# -------- CARGA Y PROCESAMIENTO --------
df = pd.read_csv(file_path)

columns_needed = ["session.code", "player.custom_participant_id", "player.total_payment_euros"]
df = df[columns_needed].rename(columns={
    "player.custom_participant_id": "custom_id",
    "player.total_payment_euros": "pago_euros",
    "session.code": "session_code"
})

df = df[df["custom_id"].notna()].copy()
df["custom_id"] = df["custom_id"].astype(int)
df["pago_euros"] = df["pago_euros"].astype(float)
df = df.sort_values(by="custom_id")

# -------- GUARDAR ARCHIVOS --------
df.to_excel(xlsx_path_downloads, index=False)
df.to_excel(xlsx_path_desktop, index=False)
df.to_csv(csv_path_downloads, index=False, sep=";")
df.to_csv(csv_path_desktop, index=False, sep=";")

# -------- PDF --------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", style='B', size=14)
pdf.cell(0, 10, "Resumen de Pagos - Tratamiento 1", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", style='B', size=11)
pdf.set_fill_color(220, 220, 220)
pdf.cell(40, 10, "Custom ID", 1, 0, 'C', True)
pdf.cell(50, 10, "Pago (EUR)", 1, 0, 'C', True)
pdf.cell(60, 10, "Código de Sesión", 1, 1, 'C', True)

pdf.set_font("Arial", size=10)
for _, row in df.iterrows():
    pdf.cell(40, 10, str(row["custom_id"]), 1, 0, 'C')
    pdf.cell(50, 10, f'{row["pago_euros"]:.2f} EUR', 1, 0, 'C')
    pdf.cell(60, 10, str(row["session_code"]), 1, 1, 'C')

pdf.output(pdf_path_downloads)
pdf.output(pdf_path_desktop)

# -------- MENSAJE FINAL --------
print(f"✅ Excel creado: {xlsx_path_downloads}")
print(f"✅ CSV creado: {csv_path_downloads}")
print(f"✅ PDF creado: {pdf_path_downloads}")
print(f"📁 Copias también guardadas en: {desktop_folder}")
