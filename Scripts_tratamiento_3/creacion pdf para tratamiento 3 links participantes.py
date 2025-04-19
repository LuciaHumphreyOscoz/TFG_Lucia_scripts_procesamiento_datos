import pandas as pd
from fpdf import FPDF
import os

# -------- CONFIGURACIÓN --------
file_path = r"C:\Users\lucia\Downloads\asignacion_tratamiento_3_2025-04-15.csv".replace("\\", "/")

winner_links = [
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/ffqbehtv',  # P1
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/ld3ilf13',  # P3
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/oveudoim',  # P5
]

loser_links = [
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/t3kat0my',  # P2
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/s9bq7er4',  # P4
    'https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/y63jc2jq',  # P6
]


# -------- CARGA Y UNIÓN DE DATOS --------
df = pd.read_csv(file_path)

# Ronda 1 → custom_id
df_r1 = df[df["subsession.round_number"] == 1]
df_r1 = df_r1[df_r1["player.custom_participant_id"].notna()]
df_r1["custom_id"] = df_r1["player.custom_participant_id"].astype(int)

# Ronda 10 → puntuación
df_r10 = df[df["subsession.round_number"] == 10]
df_merged = df_r10.merge(
    df_r1[["participant.id_in_session", "custom_id"]],
    on="participant.id_in_session",
    how="left"
)

df_merged = df_merged[df_merged["custom_id"].notna()]
df_merged["final_score"] = df_merged["player.score"].astype(int)

# -------- RANKEAR Y ASIGNAR LINKS --------
df_final = df_merged[["custom_id", "final_score"]].copy()
df_final["rank"] = df_final["final_score"].rank(ascending=False, method="first")
cutoff = len(df_final) / 2
df_final["status"] = df_final["rank"].apply(lambda x: "winner" if x <= cutoff else "loser")

# Asignar links
i_win = i_lose = 0
assigned_links = []
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

pdf.set_font("Arial", style='B', size=12)
pdf.multi_cell(0, 10, "INSTRUCCIONES IMPORTANTES\n", align='C')
pdf.ln(5)

pdf.set_font("Arial", size=12)
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

pdf.set_font("Arial", size=11)
pdf.set_fill_color(220, 220, 220)
pdf.cell(50, 10, "ID", 1, 0, 'C', True)
pdf.cell(0, 10, "ENLACE ASIGNADO", 1, 1, 'C', True)

for _, row in df_final.iterrows():
    pdf.cell(50, 10, str(int(row['custom_id'])), 1, 0, 'C')
    link_original = str(row['assigned_link'])
    link_seguro = link_original.replace("://", "[:]//")
    pdf.set_font("Arial", size=10)
    enlace_formateado = 'COPIA EL ENLACE Y REEMPLAZA "[ : ]" POR ":"\n' + link_seguro
    pdf.multi_cell(0, 10, enlace_formateado, border=1)
    pdf.set_font("Arial", size=11)

# -------- GUARDAR PDF --------
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
desktop_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 3")
os.makedirs(desktop_folder, exist_ok=True)

pdf_path = os.path.join(downloads_path, "participant_links_tratamiento_3.pdf")
desktop_pdf_path = os.path.join(desktop_folder, "participant_links_tratamiento_3.pdf")

pdf.output(pdf_path)
pdf.output(desktop_pdf_path)

print(f"✅ PDF creado correctamente en: {pdf_path}")
print(f"✅ Copia también guardada en: {desktop_pdf_path}")
