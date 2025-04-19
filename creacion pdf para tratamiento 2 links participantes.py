import pandas as pd
from fpdf import FPDF
import os
import re

# -------- CONFIGURACIÓN --------
file_path = r"C:\Users\lucia\Downloads\asignacion_tratamiento_2_2025-04-15.csv".replace("\\", "/")

winner_links = [
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/74kz5gia",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/hqz0xb37",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/s9rtn7qr"

]

loser_links = [
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/65c3x99w',  # P2
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/9hjn15do',  # P4
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/0xyofhre',  # P6
]


# -------- PROCESAMIENTO DE DATOS --------
df = pd.read_csv(file_path)

# Filtrar y limpiar IDs personalizados válidos
df = df[df["player.custom_participant_id"].notna()].copy()
df["custom_id"] = df["player.custom_participant_id"].astype(int).astype(str)
df = df[df["custom_id"].str.match(r"^\d{3}$")]

# Obtener score máximo por participante
df_final = df.groupby("custom_id").agg({
    "player.score": "max",
    "player.id_in_group": "first"
}).reset_index().rename(columns={
    "player.score": "final_score",
    "player.id_in_group": "id_in_group"
})

# Rankeo y clasificación
df_final["rank"] = df_final["final_score"].rank(ascending=False, method="first")
cutoff = len(df_final) / 2
df_final["status"] = df_final["rank"].apply(lambda x: "winner" if x <= cutoff else "loser")

# Asignar enlaces personalizados
assigned_links = []
i_win = 0
i_lose = 0

for _, row in df_final.iterrows():
    if row["status"] == "winner" and i_win < len(winner_links):
        assigned_links.append(winner_links[i_win])
        i_win += 1
    elif row["status"] == "loser" and i_lose < len(loser_links):
        assigned_links.append(loser_links[i_lose])
        i_lose += 1
    else:
        assigned_links.append("NO LINK - not enough")

df_final["assigned_link"] = assigned_links
df_final = df_final.sort_values(by="custom_id")

# -------- GENERAR PDF --------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Título
pdf.set_font("Arial", style='B', size=12)
pdf.multi_cell(0, 10, "INSTRUCCIONES IMPORTANTES\n", align='C')
pdf.ln(5)

pdf.set_font("Arial", style='', size=12)
pdf.multi_cell(0, 10,
    "Por favor, copia y pega manualmente el enlace asignado en tu navegador. NO hagas clic directamente.\n"
    "Tendrás que quitar el paréntesis y dejar solo los dos puntos después del 'http'.\n"
    "Asegúrate de que tu ID coincide exactamente con el enlace asignado.\n"
    "Si introduces un enlace incorrecto, tu participación será INVÁLIDA y NO recibirás pago.\n"
    "No compartas este documento ni tu enlace con nadie.\n"
)

pdf.ln(5)
pdf.cell(0, 5, "-" * 80, ln=True)
pdf.ln(5)

# Tabla
pdf.set_font("Arial", size=11)
pdf.set_fill_color(220, 220, 220)
pdf.cell(50, 10, "ID", 1, 0, 'C', True)
pdf.cell(0, 10, "ENLACE ASIGNADO", 1, 1, 'C', True)

for _, row in df_final.iterrows():
    pdf.cell(50, 10, row['custom_id'], 1, 0, 'C')
    link_original = str(row['assigned_link'])
    link_seguro = link_original.replace("://", "[:]//")
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, 'COPIA EL ENLACE Y REEMPLAZA "[ : ]" POR ":"\n' + link_seguro, border=1)
    pdf.set_font("Arial", size=11)

# Guardar en Descargas
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
pdf_path = os.path.join(downloads_path, "participant_links_tratamiento_2.pdf")
pdf.output(pdf_path)

# Guardar también en Escritorio
desktop_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 2")
os.makedirs(desktop_folder, exist_ok=True)
desktop_pdf_path = os.path.join(desktop_folder, "participant_links_tratamiento_2.pdf")
pdf.output(desktop_pdf_path)

print(f"✅ PDF creado correctamente en: {pdf_path}")
print(f"✅ Copia también guardada en: {desktop_pdf_path}")
