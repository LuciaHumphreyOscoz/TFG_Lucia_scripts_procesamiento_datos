import pandas as pd
import os

# Ruta del archivo CSV
ruta_csv = r"C:\Users\lucia\Downloads\emails_2025-04-14 (1).csv".replace("\\", "/")

# Carpeta de destino y nombre del archivo .txt
carpeta_destino = r"C:\Users\lucia\OneDrive\Desktop\Scripts tratamiento 1".replace("\\", "/")
archivo_salida = os.path.join(carpeta_destino, "lista_emails_para_pegar.txt")

# Leer el archivo CSV
df = pd.read_csv(ruta_csv)

# Filtrar por la etiqueta deseada en session.label
df_filtrado = df[df["session.label"] == "correos tratamiento 1"]

# Usar la columna correcta: 'player.email'
emails = df_filtrado["player.email"].dropna().astype(str)

# Crear cadena de texto con emails separados por coma
texto_emails = ", ".join(emails)

# Guardar en .txt
with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write(texto_emails)

print(f"✅ {len(emails)} correos guardados en:\n{archivo_salida}")


