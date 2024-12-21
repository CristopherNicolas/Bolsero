#Hecho por Cristopher Faundez para obtner informacion de la bolsa de santiago 
#de forma automatica dado un intervalo de tiempo.
#ideas para desarrollar : 

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

intervalo = 20
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

while True:
    driver.get("https://www.bolsadesantiago.com/principales_acciones")
    time.sleep(10) # esperar a que cargue la página
    
    acciones = driver.find_elements(By.CSS_SELECTOR, "div.card.mb-4.animated.fadeIn.ng-scope")
    for accion in acciones:
        try:
            nombre = accion.find_element(By.CSS_SELECTOR, "h3.text-uppercase.text-secondary.font-weight-bold.f-20.ng-binding").text
            precio = accion.find_element(By.CSS_SELECTOR, "h4.text-muted.mb-0.ng-binding").text
            volumen = accion.find_elements(By.CSS_SELECTOR, "div.card-body .text-muted.mb-0.ng-binding")
            
            print(f"Acción: {nombre} | Precio: {precio} CLP | Volumen: {volumen[1].text} | Monto: {volumen[2].text}")
            
        except Exception as e:
            print(f"Error al extraer información de una acción: {e}")
    
    time.sleep(intervalo) 
