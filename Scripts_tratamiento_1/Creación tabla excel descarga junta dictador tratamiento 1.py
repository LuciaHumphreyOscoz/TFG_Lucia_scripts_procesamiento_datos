import pandas as pd
import os

# Ruta al archivo CSV descargado
input_csv_path = r"C:\Users\lucia\Downloads\ultimatum_tratamiento_1_H_2025-04-14.csv".replace("\\", "/")

# Leer CSV
df = pd.read_csv(input_csv_path)

# Columnas a conservar, ya limpias
selected_columns = [
    "player.custom_participant_id",
    "session.code",
    "session.config.name",
    "player.id_in_group",
    "player.group.id_in_subsession",
    "player.assigned_role",
    "group.offer",
    "group.offer_accepted",
    "player.final_payment",
    "player.total_payment_euros",
    "player.explanation1",
    "player.explanation2",
    "player.hypothetical_offer",
    "player.perception_others_proposers",
    "player.perception_proposers",
    "player.group.offer_accepted",
    "player.perception_others_allocators",
    "player.perception_allocators",
    "player.gender",
    "player.age",
    "player.studies",
    "player.socialcapital",
    "player.football_team",
    "player.becaMEC",
    "player.payoff_satisfaction",
    "player.role_fairness",
    "player.discrimiation_level"
]

# Filtrar columnas que existan
existing_cols = [col for col in selected_columns if col in df.columns]
df_filtered = df[existing_cols]

# Reordenar columnas principales
prioritarias = ["player.custom_participant_id", "player.assigned_role"]
ordered_cols = [col for col in prioritarias if col in df_filtered.columns]
ordered_cols += [col for col in df_filtered.columns if col not in ordered_cols]
df_filtered = df_filtered[ordered_cols]

# Rutas de salida
output_name = "data_dictador_tratamiento_1.csv"
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", output_name)
desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 1", output_name)

os.makedirs(os.path.dirname(desktop_path), exist_ok=True)

# Guardar en ambas ubicaciones
df_filtered.to_csv(downloads_path, index=False, sep=";")
df_filtered.to_csv(desktop_path, index=False, sep=";")

print(f"✅ CSV actualizado en Descargas: {downloads_path}")
print(f"✅ Copia también en Escritorio: {desktop_path}")

