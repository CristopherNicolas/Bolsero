import time
import os
import csv
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from collections import defaultdict
from AnalizarCsv import analizar_accion  # Importar la función de análisis

# Configuración
intervalo = 20
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# Directorios para guardar los archivos
directorio_csv = "datos_csv"
directorio_json = "datos_json"

# Crear directorios si no existen
os.makedirs(directorio_csv, exist_ok=True)
os.makedirs(directorio_json, exist_ok=True)

# Flujo principal de scraping y análisis
while True:
    driver.get("https://www.bolsadesantiago.com/principales_acciones")
    time.sleep(10)  # esperar a que cargue la página

    acciones_dict = defaultdict(list)  # Resetear el diccionario por cada iteración

    acciones = driver.find_elements(By.CSS_SELECTOR, "div.card.mb-4.animated.fadeIn.ng-scope")
    for accion in acciones:
        try:
            nombre = accion.find_element(By.CSS_SELECTOR, "h3.text-uppercase.text-secondary.font-weight-bold.f-20.ng-binding").text
            precio = accion.find_element(By.CSS_SELECTOR, "h4.text-muted.mb-0.ng-binding").text
            volumen = accion.find_elements(By.CSS_SELECTOR, "div.card-body .text-muted.mb-0.ng-binding")

            # el formato de guardado es de 
            fecha_hora = time.strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actuales
            volumen_text = volumen[1].text if len(volumen) > 1 else "N/A"
            monto_text = volumen[2].text if len(volumen) > 2 else "N/A"

            # Guardar en el diccionario por acción para JSON
            acciones_dict[nombre].append({
                "Fecha y Hora": fecha_hora,
                "Precio (CLP)": precio,
                "Volumen": volumen_text,
                "Monto": monto_text
            })

            print(f"Guardado: {fecha_hora} | Acción: {nombre} | Precio: {precio} CLP | Volumen: {volumen_text} | Monto: {monto_text}")

        except Exception as e:
            print(f"Error al extraer información de una acción: {e}")

    # Generar nombres de archivos basados en la fecha y hora
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    archivo_csv = os.path.join(directorio_csv, f"acciones_{timestamp}.csv")
    archivo_json = os.path.join(directorio_json, f"acciones_{timestamp}.json")

    # Guardar en CSV
    with open(archivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha y Hora", "Acción", "Precio (CLP)", "Volumen", "Monto"])
        for accion, datos in acciones_dict.items():
            for dato in datos:
                writer.writerow([dato["Fecha y Hora"], accion, dato["Precio (CLP)"], dato["Volumen"], dato["Monto"]])

    # Guardar en JSON
    with open(archivo_json, mode="w", encoding="utf-8") as json_file:
        json.dump(acciones_dict, json_file, ensure_ascii=False, indent=4)

    print(f"Archivos guardados: {archivo_csv}, {archivo_json}")

    # Cargar los datos del archivo CSV recién creado
    df = pd.read_csv(archivo_csv, encoding="utf-8")
    
    # Filtrar y analizar por cada acción
    acciones = df["Acción"].unique()
    for accion in acciones:
        df_accion = df[df["Acción"] == accion]
        analizar_accion(df_accion, accion)  # Llamar a la función de análisis y graficado

    # Esperar antes de la siguiente iteración
    time.sleep(intervalo)
