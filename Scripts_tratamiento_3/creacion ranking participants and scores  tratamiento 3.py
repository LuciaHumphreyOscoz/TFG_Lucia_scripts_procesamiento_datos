import pandas as pd
import os
from fpdf import FPDF

# -------- CARGA --------
file_path = r"C:\Users\lucia\Downloads\asignacion_tratamiento_3_2025-04-15.csv".replace("\\", "/")
df = pd.read_csv(file_path)

# -------- FILTRAR RONDA 1 Y 10 --------
df_ronda1 = df[df["subsession.round_number"] == 1]
df_ronda10 = df[df["subsession.round_number"] == 10]

# Asegurarse de que los ID sean enteros
df_ronda1 = df_ronda1[df_ronda1["player.custom_participant_id"].notna()]
df_ronda1["custom_id"] = df_ronda1["player.custom_participant_id"].astype(int)

# Combinar usando el identificador de sesión
merged = df_ronda10.merge(
    df_ronda1[["participant.id_in_session", "custom_id"]],
    on="participant.id_in_session",
    how="left"
)

# Limpiar y preparar columnas finales
merged = merged[merged["custom_id"].notna()]
merged["final_score"] = merged["player.score"].astype(int)
merged["total_rounds_played"] = 10

df_final_sorted = merged[["custom_id", "final_score", "total_rounds_played"]].copy()
df_final_sorted = df_final_sorted.sort_values(by=["final_score", "custom_id"], ascending=[False, True])

# -------- GUARDAR CSV --------
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
desktop_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 3")
os.makedirs(desktop_folder, exist_ok=True)

csv_path_downloads = os.path.join(downloads_path, "resultscompetitivetask_tratamiento_3.csv")
csv_path_desktop = os.path.join(desktop_folder, "resultscompetitivetask_tratamiento_3.csv")

df_final_sorted.to_csv(csv_path_downloads, index=False, sep=";")
df_final_sorted.to_csv(csv_path_desktop, index=False, sep=";")

# -------- GENERAR PDF --------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Título
pdf.set_font("Arial", style='B', size=14)
pdf.cell(0, 10, "Ranking - Tarea Competitiva Tratamiento 3", ln=True, align='C')
pdf.ln(10)

# Encabezados
pdf.set_font("Arial", style='B', size=11)
pdf.set_fill_color(220, 220, 220)
pdf.cell(40, 10, "Custom ID", 1, 0, 'C', True)
pdf.cell(40, 10, "Puntuación", 1, 0, 'C', True)
pdf.cell(50, 10, "Rondas Jugadas", 1, 1, 'C', True)

# Filas del ranking
pdf.set_font("Arial", size=10)
for _, row in df_final_sorted.iterrows():
    pdf.cell(40, 10, str(int(row["custom_id"])), 1, 0, 'C')
    pdf.cell(40, 10, str(int(row["final_score"])), 1, 0, 'C')
    pdf.cell(50, 10, str(int(row["total_rounds_played"])), 1, 1, 'C')

# Guardar PDF
pdf_path_downloads = os.path.join(downloads_path, "ranking_tarea_competitiva_tratamiento_3.pdf")
pdf_path_desktop = os.path.join(desktop_folder, "ranking_tarea_competitiva_tratamiento_3.pdf")
pdf.output(pdf_path_downloads)
pdf.output(pdf_path_desktop)

# -------- FIN --------
print("\n✅ ¡Listo! Datos de la ronda 10 con IDs de la ronda 1 combinados correctamente.")
print(f"📁 CSV: {csv_path_downloads}")
print(f"📁 PDF: {pdf_path_downloads}")

