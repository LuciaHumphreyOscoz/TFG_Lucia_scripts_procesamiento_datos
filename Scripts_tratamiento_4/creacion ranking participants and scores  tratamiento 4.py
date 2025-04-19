import pandas as pd
from fpdf import FPDF
import os
import re

# -------- CARGA Y FILTRADO --------
file_path = r"C:\Users\lucia\Downloads\asignacion_tratamiento_4_2025-04-15.csv".replace("\\", "/")
df = pd.read_csv(file_path)

# Filtrar solo IDs personalizados válidos (3 dígitos exactos)
df = df[df["player.custom_participant_id"].notna()].copy()
df["custom_id"] = df["player.custom_participant_id"].astype(int).astype(str)
df = df[df["custom_id"].str.match(r"^\d{3}$")]

# Volver a int para cálculos
df["custom_id"] = df["custom_id"].astype(int)

# Calcular puntuación máxima y total de rondas por ID
df_scores = df.groupby("custom_id").agg(
    final_score=("player.score", "max"),
    total_rounds_played=("player.score", lambda x: x.notna().sum())
).reset_index()


# Ordenar ranking
df_scores = df_scores.sort_values(by=["final_score", "total_rounds_played"], ascending=[False, True])

# -------- GUARDAR CSV --------
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
desktop_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 4")
os.makedirs(desktop_folder, exist_ok=True)

csv_path_downloads = os.path.join(downloads_path, "resultscompetitivetask_tratamiento_4.csv")
csv_path_desktop = os.path.join(desktop_folder, "resultscompetitivetask_tratamiento_4.csv")

df_scores.to_csv(csv_path_downloads, index=False, sep=";")
df_scores.to_csv(csv_path_desktop, index=False, sep=";")

# -------- GENERAR PDF --------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Título
pdf.set_font("Arial", style='B', size=14)
pdf.cell(0, 10, "Ranking - Tarea Competitiva Tratamiento 4", ln=True, align='C')
pdf.ln(10)

# Encabezados
pdf.set_font("Arial", style='B', size=11)
pdf.set_fill_color(220, 220, 220)
pdf.cell(40, 10, "Custom ID", 1, 0, 'C', True)
pdf.cell(40, 10, "Puntuación", 1, 0, 'C', True)
pdf.cell(50, 10, "Rondas Jugadas", 1, 1, 'C', True)

# Filas del ranking
pdf.set_font("Arial", size=10)
for _, row in df_scores.iterrows():
    pdf.cell(40, 10, str(int(row["custom_id"])), 1, 0, 'C')
    pdf.cell(40, 10, str(int(row["final_score"])), 1, 0, 'C')
    pdf.cell(50, 10, str(int(row["total_rounds_played"])), 1, 1, 'C')


# Guardar PDF
pdf_path_downloads = os.path.join(downloads_path, "ranking_tarea_competitiva_tratamiento_4.pdf")
pdf_path_desktop = os.path.join(desktop_folder, "ranking_tarea_competitiva_tratamiento_4.pdf")
pdf.output(pdf_path_downloads)
pdf.output(pdf_path_desktop)

# -------- MENSAJE FINAL --------
print("\n✅ Resultados ordenados y guardados.")
print(f"📁 CSV: {csv_path_downloads}")
print(f"📁 PDF: {pdf_path_downloads}")
print(f"📁 Copias en escritorio: {desktop_folder}")