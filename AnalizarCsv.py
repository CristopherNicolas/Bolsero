import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Configuración
periodo_media_movil = 5  # Días para la media móvil
periodo_rsi = 14  # Días para calcular el RSI

# Función para calcular el RSI
def calcular_rsi(series, periodo=14):
    delta = series.diff()
    ganancias = delta.where(delta > 0, 0)
    perdidas = -delta.where(delta < 0, 0)
    
    avg_ganancias = ganancias.rolling(window=periodo).mean()
    avg_perdidas = perdidas.rolling(window=periodo).mean()
    
    rs = avg_ganancias / avg_perdidas
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Función para graficar los resultados
def graficar(df_accion, nombre_accion):
    # Limpiar la figura actual para evitar que se dibujen varios gráficos
    plt.clf()  

    # Crear los subgráficos con plt.subplots
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    # Subgráfico 1: Precio y Media Móvil
    axes[0].plot(df_accion["Fecha y Hora"], df_accion["Precio (CLP)"], label="Precio (CLP)", color="blue")
    axes[0].plot(df_accion["Fecha y Hora"], df_accion["Media Móvil"], label=f"Media Móvil ({periodo_media_movil} días)", color="orange")
    axes[0].set_title(f"{nombre_accion} - Precio y Media Móvil")
    axes[0].set_xlabel("Fecha y Hora")
    axes[0].set_ylabel("Precio (CLP)")
    axes[0].legend()
    axes[0].grid(True)

    # Subgráfico 2: RSI
    axes[1].plot(df_accion["Fecha y Hora"], df_accion["RSI"], label=f"RSI ({periodo_rsi} días)", color="green")
    axes[1].axhline(y=30, color='red', linestyle='--', label="Sobreventa (RSI 30)")
    axes[1].axhline(y=70, color='red', linestyle='--', label="Sobrecompra (RSI 70)")
    axes[1].set_title(f"{nombre_accion} - RSI")
    axes[1].set_xlabel("Fecha y Hora")
    axes[1].set_ylabel("RSI")
    axes[1].legend()
    axes[1].grid(True)

    # Ajustar el diseño y mostrar
    plt.tight_layout(h_pad=900, w_pad=900)
    plt.draw()  # Evitar cerrar la ventana al actualizar
    plt.show()


# Función de análisis por acción
def analizar_accion(df_accion, nombre_accion):
    df_accion["Precio (CLP)"] = df_accion["Precio (CLP)"].str.replace(',', '.').apply(limpiar_valor).astype(float)
    df_accion["Volumen"] = df_accion["Volumen"].str.replace(',', '.').apply(limpiar_valor).astype(float)

    # Ordenar por fecha
    df_accion = df_accion.sort_values("Fecha y Hora")

    # Calcular indicadores
    df_accion["Media Móvil"] = df_accion["Precio (CLP)"].rolling(window=periodo_media_movil).mean()
    df_accion["RSI"] = calcular_rsi(df_accion["Precio (CLP)"], periodo_rsi)

    # Seleccionar última fila para análisis actual
    ultima_fila = df_accion.iloc[-1]
    precio_actual = ultima_fila["Precio (CLP)"]
    media_movil = ultima_fila["Media Móvil"]
    rsi_actual = ultima_fila["RSI"]
    volumen_actual = ultima_fila["Volumen"]
    promedio_volumen = df_accion["Volumen"].mean()

    # Determinar tendencia
    precios_recientes = df_accion["Precio (CLP)"].tail(periodo_media_movil).tolist()
    if len(precios_recientes) == periodo_media_movil:
        if precios_recientes == sorted(precios_recientes):
            tendencia = "Al alza"
        elif precios_recientes == sorted(precios_recientes, reverse=True):
            tendencia = "A la baja"
        else:
            tendencia = "Estable"
    else:
        tendencia = "Datos insuficientes"

    # Evaluar volumen
    volumen_alto = volumen_actual > promedio_volumen

    # Generar recomendación
    if rsi_actual < 30:
        decision = "Comprar (Sobreventa detectada)"
    elif rsi_actual > 70:
        decision = "Vender (Sobrecompra detectada)"
    elif precio_actual > media_movil:
        decision = "Comprar"
    elif precio_actual < media_movil:
        decision = "Vender"
    else:
        decision = "Mantener"

    # Generar reporte
    print(f"--- Análisis para {nombre_accion} ---")
    print(f"Precio actual: {precio_actual}")
    print(f"Media móvil ({periodo_media_movil} días): {media_movil:.2f}")
    print(f"RSI actual: {rsi_actual:.2f}")
    print(f"Tendencia: {tendencia}")
    print(f"Volumen actual: {volumen_actual} (Promedio: {promedio_volumen:.2f})")
    print(f"Recomendación: {decision} {'(Volumen alto)' if volumen_alto else ''}")
    print("---------------------------\n")

    # Llamar a la función de graficar
    graficar(df_accion, nombre_accion)
# Función para limpiar los valores y dejar solo el último punto como separador decimal
def limpiar_valor(valor):
    # Reemplazar todos los puntos excepto el último con una cadena vacía
    return re.sub(r'(?<=\d)\.(?=\d)', '', valor)

