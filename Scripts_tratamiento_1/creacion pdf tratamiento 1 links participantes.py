import pandas as pd
import random
from fpdf import FPDF
import os
from itertools import zip_longest

# -------- CONFIGURACIÓN --------
file_path = r"C:\Users\lucia\Downloads\asignacion_tratamiento_1_2025-04-14.csv".replace("\\", "/")

# ENLACES SESIÓN 1: hombres asignadores
sesion_1_asignador_links = [
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/rk2wmg7j",	
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/tt9a9bx8",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/uzai9oyj"
]

sesion_1_receptor_links = [
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/437gzwry",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/pdvbkyk4",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/n3bqdnbt",
]

# ENLACES SESIÓN 2: mujeres asignadoras
sesion_2_asignador_links = [
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/od9khyyu",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/qtp3rk0y",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/cvzt6t8c",
]

sesion_2_receptor_links = [
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/8ycmqrck",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/pi7co8sf",
    "https://game-experiments-d8f8ab596e55.herokuapp.com/InitializeParticipant/fjkp4avh",
]

# -------- ELECCIÓN DE SESIÓN --------
sesion_elegida = random.choice([1, 2])
asignador_genero = "Hombre" if sesion_elegida == 1 else "Mujer"

if sesion_elegida == 1:
    links_asignador = sesion_1_asignador_links.copy()
    links_receptor = sesion_1_receptor_links.copy()
else:
    links_asignador = sesion_2_asignador_links.copy()
    links_receptor = sesion_2_receptor_links.copy()

# -------- CARGA Y FILTRO --------
df = pd.read_csv(file_path)
df = df[['player.custom_participant_id', 'player.gender']].copy()
df = df.rename(columns={'player.custom_participant_id': 'custom_id', 'player.gender': 'gender'})

# Eliminar incompletos y dejar solo IDs de 3 cifras
df = df[df['custom_id'].notna() & df['gender'].notna()]
df = df[df['custom_id'].astype(str).str.match(r'^\d{3}$')]
df['custom_id'] = df['custom_id'].astype(int)

print(f"✅ Total participantes válidos: {len(df)}")

# -------- SEPARACIÓN POR GÉNERO --------
hombres = df[df['gender'] == 'Hombre'].copy()
mujeres = df[df['gender'] == 'Mujer'].copy()
nobinarios = df[df['gender'] == 'No binario'].copy()

# -------- EMPAREJAMIENTO HOMBRE-MUJER --------
parejas = []
for h, m in zip(hombres.itertuples(index=False), mujeres.itertuples(index=False)):
    parejas.append((h, m))

used_hombres = set(p.custom_id for p, _ in parejas)
used_mujeres = set(p.custom_id for _, p in parejas)

sobrantes_h = hombres[~hombres['custom_id'].isin(used_hombres)].itertuples(index=False)
sobrantes_m = mujeres[~mujeres['custom_id'].isin(used_mujeres)].itertuples(index=False)
sobrantes = list(sobrantes_h) + list(sobrantes_m) + list(nobinarios.itertuples(index=False))

# -------- EMPAREJAMIENTO RESTANTE --------
for a, b in zip_longest(sobrantes[::2], sobrantes[1::2]):
    if b is None:
        continue
    parejas.append((a, b))

# -------- ASIGNACIÓN DE LINKS --------
resultados = []
i_asig = 0
i_recep = 0

for p1, p2 in parejas:
    try:
        # CASO 1: Uno es hombre o mujer y el otro no binario
        if "No binario" in (p1.gender, p2.gender):
            if p1.gender != "No binario":
                asignador = p1 if p1.gender == asignador_genero else p2
                receptor = p2 if p1.gender == asignador_genero else p1
            else:
                asignador = p2 if p2.gender == asignador_genero else p1
                receptor = p1 if p2.gender == asignador_genero else p2

        # CASO 2: Hombre + Mujer → asignar según género asignador
        elif p1.gender != p2.gender:
            asignador = p1 if p1.gender == asignador_genero else p2
            receptor = p2 if p1.gender == asignador_genero else p1

        # CASO 3: Mismo género → asignación aleatoria
        else:
            pareja = [p1, p2]
            random.shuffle(pareja)
            asignador, receptor = pareja

        link_asig = links_asignador[i_asig] if i_asig < len(links_asignador) else 'NO LINK'
        link_recep = links_receptor[i_recep] if i_recep < len(links_receptor) else 'NO LINK'

        resultados.append({'custom_id': int(asignador.custom_id), 'link': link_asig})
        resultados.append({'custom_id': int(receptor.custom_id), 'link': link_recep})

        i_asig += 1
        i_recep += 1

    except Exception as e:
        print("⚠️ Error al procesar pareja:", e)
        continue
    
df_final = pd.DataFrame(resultados)

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
    pdf.cell(50, 10, str(row['custom_id']), 1, 0, 'C')
    link_seguro = str(row['link']).replace("://", "[:]//")
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, 'COPIA EL ENLACE Y REEMPLAZA "[ : ]" POR ":"\n' + link_seguro, border=1)
    pdf.set_font("Arial", size=11)

# -------- GUARDAR PDF --------
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 1")
os.makedirs(desktop_path, exist_ok=True)

filename = f"participant_links_tratamiento_1_sesion_{sesion_elegida}.pdf"
pdf_path_downloads = os.path.join(downloads_path, filename)
pdf_path_desktop = os.path.join(desktop_path, filename)

pdf.output(pdf_path_downloads)
pdf.output(pdf_path_desktop)

print(f"✅ PDF creado correctamente en: {pdf_path_downloads}")
print(f"✅ Copia también guardada en: {pdf_path_desktop}")

