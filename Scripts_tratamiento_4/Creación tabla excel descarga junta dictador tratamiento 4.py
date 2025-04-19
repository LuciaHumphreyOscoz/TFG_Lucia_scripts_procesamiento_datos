import pandas as pd
import os

# -------- CARGA --------
input_csv_path = os.path.join(os.path.expanduser("~"), "Downloads", "ultimatum_tratamiento_4_2025-04-15.csv")

# Leer CSV con codificación adecuada para caracteres especiales
df = pd.read_csv(input_csv_path, encoding='utf-8')

# Columnas a conservar
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
    "player.class_level",
    "player.talent_vs_effort",
]
# Filtrar las columnas que realmente existen
existing_cols = [col for col in selected_columns if col in df.columns]
df_filtered = df[existing_cols]

# Redondear valores numéricos excepto el pago total
for col in df_filtered.select_dtypes(include=["float", "int"]).columns:
    if col != "player.total_payment_euros":
        df_filtered[col] = df_filtered[col].round(0).astype("Int64")  # valores sin decimales
    else:
        df_filtered[col] = df_filtered[col].round(1)  # solo 1 decimal

# Reordenar columnas
prioritarias = ["player.custom_participant_id", "player.id_in_group", "player.assigned_role"]
ordered_cols = prioritarias + [col for col in df_filtered.columns if col not in prioritarias]
df_filtered = df_filtered[ordered_cols]

# -------- EXPORTACIÓN --------
output_name = "data_dictador_tratamiento_4.csv"
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", output_name)
desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Scripts tratamiento 4", output_name)

os.makedirs(os.path.dirname(desktop_path), exist_ok=True)

# Guardar CSVs con codificación utf-8-sig (Excel friendly)
df_filtered.to_csv(downloads_path, index=False, sep=";", encoding='utf-8-sig')
df_filtered.to_csv(desktop_path, index=False, sep=";", encoding='utf-8-sig')

print(f"✅ CSV actualizado en Descargas: {downloads_path}")
print(f"✅ Copia también en Escritorio: {desktop_path}")


