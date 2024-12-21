
#base alternativa creada con ia que usa main.py como base para guradar la info.
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

# Configuración
intervalo = 20
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
archivo_csv = "datos_acciones.csv"

# Crear el archivo CSV con encabezados
with open(archivo_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Fecha y Hora", "Acción", "Precio (CLP)", "Volumen", "Monto"])

while True:
    driver.get("https://www.bolsadesantiago.com/principales_acciones")
    time.sleep(10)  # esperar a que cargue la página

    acciones = driver.find_elements(By.CSS_SELECTOR, "div.card.mb-4.animated.fadeIn.ng-scope")
    for accion in acciones:
        try:
            nombre = accion.find_element(By.CSS_SELECTOR, "h3.text-uppercase.text-secondary.font-weight-bold.f-20.ng-binding").text
            precio = accion.find_element(By.CSS_SELECTOR, "h4.text-muted.mb-0.ng-binding").text
            volumen = accion.find_elements(By.CSS_SELECTOR, "div.card-body .text-muted.mb-0.ng-binding")

            fecha_hora = time.strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actuales
            volumen_text = volumen[1].text if len(volumen) > 1 else "N/A"
            monto_text = volumen[2].text if len(volumen) > 2 else "N/A"

            # Guardar en CSV
            with open(archivo_csv, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([fecha_hora, nombre, precio, volumen_text, monto_text])
            
            print(f"Guardado: {fecha_hora} | Acción: {nombre} | Precio: {precio} CLP | Volumen: {volumen_text} | Monto: {monto_text}")

        except Exception as e:
            print(f"Error al extraer información de una acción: {e}")

    time.sleep(intervalo)
