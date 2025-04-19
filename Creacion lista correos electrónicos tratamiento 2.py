import pandas as pd
import os

# Ruta del nuevo archivo CSV (ajústala si cambia de nombre o ubicación)
ruta_csv = r"C:\Users\lucia\Downloads\emails_2025-04-11.csv".replace("\\", "/")

# Carpeta de destino y nombre del archivo .txt
carpeta_destino = r"C:\Users\lucia\OneDrive\Desktop\Scripts tratamiento 2".replace("\\", "/")
archivo_salida = os.path.join(carpeta_destino, "lista_emails_para_pegar.txt")

# Leer el archivo CSV
df = pd.read_csv(ruta_csv)

# Filtrar por la etiqueta deseada en session.label
df_filtrado = df[df["session.label"] == "Correos tratamiento 2"]

# Usar la columna correcta: 'player.email'
emails = df_filtrado["player.email"].dropna().astype(str)

# Crear cadena de texto con emails separados por coma
texto_emails = ", ".join(emails)

# Guardar en .txt
with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write(texto_emails)

print(f"✅ {len(emails)} correos guardados en:\n{archivo_salida}")




# Carpeta de destino y nombre del archivo .txt
carpeta_destino = r"C:\Users\lucia\OneDrive\Desktop\Scripts tratamiento 2".replace("\\", "/")
archivo_salida = os.path.join(carpeta_destino, "lista_emails_para_pegar.txt")

# Leer el archivo CSV
df = pd.read_csv(ruta_csv)

# Usar la columna correcta: 'player.email'
emails = df["player.email"].dropna().astype(str)
emails_limpios = [e.strip() for e in emails if "@" in e]

# Crear cadena de texto con emails separados por coma
texto_emails = ", ".join(emails_limpios)

# Guardar en .txt
with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write(texto_emails)

print(f"✅ {len(emails_limpios)} correos guardados en:\n{archivo_salida}")

