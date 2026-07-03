# PROYECTO DE INVESTIGACIÓN FORMATIVA - PROGRAMACIÓN | UNACH 2026
# Sistema de Control de Gastos Personales utilizando Vectores y Matrices
# Integrantes: Gonzales Diego, Picausi Shirley, Pérez Mateo, Poaquiza Analy, Valverde Ashley
# ==============================================================================

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# ------------------------------------------------------------------------------
# 1. DEFINICIÓN DE CONSTANTES Y ESTRUCTURAS DE DATOS GLOBALES
# ------------------------------------------------------------------------------

# Vector global que define las categorías de gastos disponibles en el sistema
CATEGORIAS = ["Alimentación", "Transporte", "Educación", "Salud", "Entretenimiento", "Servicios", "Ropa", "Gastos Hormiga"]

# Vector global con los meses del año para mapeo de índices (0 = Enero, 11 = Diciembre)
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# ------------------------------------------------------------------------------
# 2. INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (PERSISTENCIA DE DATOS EN STREAMLIT)
# ------------------------------------------------------------------------------

# Inicializamos la matriz principal de gastos (12 meses x 8 categorías) si no existe
if "matriz_gastos" not in st.session_state:
    # Creamos una matriz de 12 filas (meses) y len(CATEGORIAS) columnas llena de ceros (0.0)
    st.session_state.matriz_gastos = [[0.0 for _ in range(len(CATEGORIAS))] for _ in range(12)]

# Inicializamos un vector dinámico para almacenar el historial de transacciones detalladas
if "historial_gastos" not in st.session_state:
    st.session_state.historial_gastos = []

# Inicializamos el fondo de ahorro acumulado por el usuario
if "ahorro_total" not in st.session_state:
    st.session_state.ahorro_total = 0.0

# ------------------------------------------------------------------------------
# 3. MÓDULO DE LÓGICA ALGORÍTMICA (FUNCIONES RECURSIVAS Y OPERACIONES)
# ------------------------------------------------------------------------------

def registrar_gasto_matriz(mes_nombre, categoria_nombre, valor):
    """Mapea directamente el mes y la categoría a índices numéricos para actualizar la matriz."""
    # Obtenemos el índice de la fila (mes) buscando en nuestro vector de MESES
    fila_mes = MESES.index(mes_nombre)
    # Obtenemos el índice de la columna (categoría) buscando en nuestro vector de CATEGORIAS
    columna_cat = CATEGORIAS.index(categoria_nombre)
    # Sumamos el valor directamente en la celda correspondiente de la matriz bidimensional
    st.session_state.matriz_gastos[fila_mes][columna_cat] += valor

def suma_recursiva_vector(vector, n):
    """Calcula la suma total de un vector numérico utilizando el principio de recursividad."""
    # Caso base: si el tamaño a evaluar es 0 o menor, la suma es 0
    if n <= 0:
        return 0.0
    # Caso recursivo: suma el último elemento actual más la llamada recursiva del subvector anterior
    return vector[n - 1] + suma_recursiva_vector(vector, n - 1)

def obtener_gasto_total_anual():
    """Calcula el gasto de todo el año a partir de la matriz usando la función recursiva."""
    vector_totales_mensuales = []
    # Recorremos cada fila (mes) de la matriz de gastos
    for fila in st.session_state.matriz_gastos:
        # Sumamos recursivamente los gastos de las categorías de ese mes
        total_mes = suma_recursiva_vector(fila, len(fila))
        # Agregamos el resultado al vector de totales mensuales
        vector_totales_mensuales.append(total_mes)
    # Retornamos la suma recursiva total de todo el vector de meses
    return suma_recursiva_vector(vector_totales_mensuales, len(vector_totales_mensuales))

def ordenar_gastos_recursivo(lista_pares):
    """Ordena una lista de pares [categoría, total] de mayor a menor usando QuickSort recursivo."""
    # Caso base: si la lista tiene 0 o 1 elemento, ya está perfectamente ordenada
    if len(lista_pares) <= 1:
        return lista_pares
    else:
        # Elegimos el primer elemento como pivote para la partición
        pivote = lista_pares[0]
        # Elementos con un valor de gasto mayor o igual al pivote (van a la izquierda)
        mayores = [x for x in lista_pares[1:] if x[1] >= pivote[1]]
        # Elementos con un valor de gasto menor al pivote (van a la derecha)
        menores = [x for x in lista_pares[1:] if x[1] < pivote[1]]
        # Combinación recursiva: mayores ordenados + pivote + menores ordenados
        return ordenar_gastos_recursivo(mayores) + [pivote] + ordenar_gastos_recursivo(menores)

# ------------------------------------------------------------------------------
# 4. INTERFAZ GRÁFICA DE USUARIO (MODULARIZADA EN STREAMLIT)
# ------------------------------------------------------------------------------

# Configuración básica de la ventana de la aplicación web
st.set_page_config(page_title="Control de Gastos Personales", page_icon="💰", layout="wide")

# Encabezado principal del proyecto con estilos HTML personalizados
st.markdown("""
    <h1 style='text-align: center; color: #1a73e8;'>💰 Sistema de Control de Gastos Personales</h1>
    <h4 style='text-align: center; color: gray;'>Facultad de Ingeniería – Ciencia de Datos e Inteligencia Artificial</h4>
    <hr>
""", unsafe_allow_html=True)

# Creación de la barra lateral izquierda para la navegación del menú principal
st.sidebar.header("📋 Menú Principal")
opcion = st.sidebar.radio(
    "Selecciona una opción:",
    ["1️⃣ Agregar Gasto / Ahorro", "2️⃣ Mostrar Historial Detallado", "3️⃣ Análisis Anual y Mensual (Matriz)", "4️⃣ Análisis por Categoría y Gastos Hormiga"]
)

# ------------------------------------------------------------------------------
# MÓDULO 4.1: REGISTRO DE GASTOS Y AHORROS
# ------------------------------------------------------------------------------
if opcion == "1️⃣ Agregar Gasto / Ahorro":
    st.subheader("➕ Registrar Nuevo Movimiento Financiero")
    st.markdown("Ingresa los datos correspondientes para mapearlos en las estructuras matriciales.")
    
    # Dividimos la pantalla en dos columnas para los formularios
    col_gasto, col_ahorro = st.columns(2)
    
    with col_gasto:
        st.write("### 📌 Registrar un Gasto")
        # Campos de entrada de datos indexados por vectores
        mes_g = st.selectbox("Selecciona el Mes del Gasto:", MESES, key="mes_gasto")
        cat_g = st.selectbox("Categoría del Gasto:", CATEGORIAS, key="cat_gasto")
        val_g = st.number_input("Valor ($):", min_value=0.01, step=0.01, format="%.2f", key="val_gasto")
        
        # Botón para procesar y guardar el gasto ingresado
        if st.button("💾 Grabar Gasto", use_container_width=True):
            # Invocamos el módulo para mapear y actualizar la matriz bidimensional
            registrar_gasto_matriz(mes_g, cat_g, val_g)
            # Guardamos el registro en el vector de historial detallado
            st.session_state.historial_gastos.append({"Mes": mes_g, "Categoría": cat_g, "Valor": val_g})
            st.success(f"✔️ Gasto de ${val_g:.2f} registrado con éxito en {mes_g} para la categoría {cat_g}.")
            
    with col_ahorro:
        st.write("### 🐷 Registrar un Ahorro")
        val_a = st.number_input("Monto a destinar a ahorros ($):", min_value=0.01, step=0.01, format="%.2f", key="val_ahorro")
        
        # Botón para actualizar el acumulador de ahorros
        if st.button("💾 Guardar Ahorro", use_container_width=True):
            st.session_state.ahorro_total += val_a
            st.success(f"✔️ ¡Excelente! Has sumado ${val_a:.2f} a tu fondo de ahorros.")

# ------------------------------------------------------------------------------
# MÓDULO 4.2: HISTORIAL DE TRANSACCIONES DETALLADAS (VECTORES)
# ------------------------------------------------------------------------------
elif opcion == "2️⃣ Mostrar Historial Detallado":
    st.subheader("📜 Lista de Gastos Registrados en el Vector Histórico")
    
    # Verificamos si existen datos guardados en el vector dinámico
    if len(st.session_state.historial_gastos) == 0:
        st.info("Aún no has registrado transacciones en el sistema.")
    else:
        # Convertimos el vector de diccionarios a un DataFrame de Pandas para visualización tabular rápida
        df_historial = pd.DataFrame(st.session_state.historial_gastos)
        st.dataframe(df_historial, use_container_width=True)
        
        # Caja de métricas rápidas de control
        total_historico = obtener_gasto_total_anual()
        st.metric(label="Total Acumulado en Gastos", value=f"${total_historico:.2f}")

# ------------------------------------------------------------------------------
# MÓDULO 4.3: ANÁLISIS ANUAL Y MENSUAL (REPRESENTACIÓN DE LA MATRIZ DE GASTOS)
# ------------------------------------------------------------------------------
elif opcion == "3️⃣ Análisis Anual y Mensual (Matriz)":
    st.subheader("📊 Matriz de Distribución Financiera Mensual")
    st.markdown("Visualización completa de la matriz bidimensional de datos (Meses x Categorías).")
    
    # Renderizamos la matriz de gastos en formato de tabla interactiva
    df_matriz = pd.DataFrame(st.session_state.matriz_gastos, index=MESES, columns=CATEGORIAS)
    st.dataframe(df_matriz, use_container_width=True)
    
    # Mostramos balances estratégicos combinando funciones recursivas
    total_anual = obtener_gasto_total_anual()
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Gasto Consolidado Anual", f"${total_anual:.2f}")
    with col_m2:
        st.metric("Fondo de Ahorro Neto", f"${st.session_state.ahorro_total:.2f}")
    with col_m3:
        # Cálculo de balance básico (Ahorro - Gastos)
        balance = st.session_state.ahorro_total - total_anual
