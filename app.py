# ==============================================================================
# PROYECTO DE INVESTIGACIÓN FORMATIVA - PROGRAMACIÓN | UNACH 2026
# Sistema de Control de Gastos Personales utilizando Vectores y Matrices
# Integrantes: Gonzales Diego, Picausi Shirley, Pérez Mateo, Poaquiza Analy, Valverde Ashley
# ==============================================================================

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os

# ------------------------------------------------------------------------------
# 1. DEFINICIÓN DE CONSTANTES Y ESTRUCTURAS DE DATOS GLOBALES
# ------------------------------------------------------------------------------

CATEGORIAS = ["Alimentación", "Transporte", "Educación", "Salud", "Entretenimiento", "Servicios", "Ropa", "Gastos Hormiga"]
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# ------------------------------------------------------------------------------
# 2. INICIALIZACIÓN DEL ESTADO DE LA SESIÓN
# ------------------------------------------------------------------------------

if "matriz_gastos" not in st.session_state:
    st.session_state.matriz_gastos = [[0.0 for _ in range(len(CATEGORIAS))] for _ in range(12)]

if "historial_gastos" not in st.session_state:
    st.session_state.historial_gastos = []

if "ahorro_total" not in st.session_state:
    st.session_state.ahorro_total = 0.0

# ------------------------------------------------------------------------------
# 3. MÓDULO DE LÓGICA ALGORÍTMICA
# ------------------------------------------------------------------------------

def registrar_gasto_matriz(mes_nombre, categoria_nombre, valor):
    fila_mes = MESES.index(mes_nombre)
    columna_cat = CATEGORIAS.index(categoria_nombre)
    st.session_state.matriz_gastos[fila_mes][columna_cat] += valor

def suma_recursiva_vector(vector, n):
    if n <= 0:
        return 0.0
    return vector[n - 1] + suma_recursiva_vector(vector, n - 1)

def obtener_gasto_total_anual():
    vector_totales_mensuales = []
    for fila in st.session_state.matriz_gastos:
        total_mes = suma_recursiva_vector(fila, len(fila))
        vector_totales_mensuales.append(total_mes)
    return suma_recursiva_vector(vector_totales_mensuales, len(vector_totales_mensuales))

def ordenar_gastos_recursivo(lista_pares):
    if len(lista_pares) <= 1:
        return lista_pares
    else:
        pivote = lista_pares[0]
        mayores = [x for x in lista_pares[1:] if x[1] >= pivote[1]]
        menores = [x for x in lista_pares[1:] if x[1] < pivote[1]]
        return ordenar_gastos_recursivo(mayores) + [pivote] + ordenar_gastos_recursivo(menores)

# ------------------------------------------------------------------------------
# 4. CONFIGURACIÓN DE PÁGINA Y TRATAMIENTO DE IMAGEN DE FONDO
# ------------------------------------------------------------------------------

st.set_page_config(page_title="Control de Gastos Personales", layout="wide")

# Función para convertir la imagen local a código Base64 incrustable
def obtener_base64_de_imagen(ruta_archivo):
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "rb") as image_file:
            data = image_file.read()
            return base64.b64encode(data).decode()
    return ""

# Intentamos cargar el archivo exacto de tu carpeta
nombre_imagen = "6273ac59-25a1-4ac6-939f-5ff9e44ab376.jpg"
img_base64 = obtener_base64_de_imagen(nombre_imagen)

# Estilos CSS personalizados con inyección segura de fondo
if img_base64:
    css_background = f"""
    .stApp {{
        background-image: linear-gradient(rgba(10, 20, 50, 0.85), rgba(10, 20, 50, 0.85)),
                          url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """
else:
    # Si por alguna razón no la encuentra, mantiene el diseño con un degradado elegante
    css_background = f"""
    .stApp {{
        background: linear-gradient(135deg, #060c20 0%, #0b2254 100%);
        background-attachment: fixed;
    }}
    """

st.markdown(f"""
<style>
    {css_background}

    /* Encabezado principal */
    .encabezado-principal {{
        background: linear-gradient(135deg, rgba(26, 115, 232, 0.85), rgba(11, 53, 120, 0.9));
        border-radius: 16px;
        padding: 28px 20px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }}

    .encabezado-principal h1 {{
        color: #ffffff;
        font-size: 2.1em;
        font-weight: 700;
        margin: 0 0 6px 0;
        letter-spacing: 1px;
    }}

    .encabezado-principal h4 {{
        color: #aad4ff;
        font-size: 1em;
        margin: 0;
        font-weight: 400;
    }}

    /* Tarjetas de contenido */
    .tarjeta {{
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(11,53,120,0.97) 0%, rgba(10,20,50,0.97) 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }}

    section[data-testid="stSidebar"] * {{
        color: #e8f0fe !important;
    }}

    /* Textos generales */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
        color: #e8f0fe !important;
    }}

    /* Botones */
    .stButton > button {{
        background: linear-gradient(135deg, #1a73e8, #0b3578);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 0.95em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26,115,232,0.4);
        width: 100%;
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, #4285f4, #1a73e8);
        box-shadow: 0 6px 20px rgba(26,115,232,0.6);
        transform: translateY(-2px);
    }}

    /* Métricas */
    [data-testid="stMetric"] {{
        background: rgba(26, 115, 232, 0.15);
        border: 1px solid rgba(26, 115, 232, 0.3);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }}

    [data-testid="stMetricValue"] {{
        color: #7dc3ff !important;
        font-size: 1.6em !important;
        font-weight: 700 !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: #aad4ff !important;
        font-size: 0.85em !important;
    }}

    /* Tablas */
    .stDataFrame {{
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }}

    /* Inputs */
    .stSelectbox > div, .stNumberInput > div {{
        background: rgba(255,255,255,0.08) !important;
        border-radius: 8px;
    }}

    /* Separador */
    hr {{
        border-color: rgba(255,255,255,0.15) !important;
    }}

    /* Alertas */
    .stSuccess {{
        background: rgba(0, 200, 100, 0.15) !important;
        border: 1px solid rgba(0, 200, 100, 0.3) !important;
        border-radius: 10px !important;
        color: #a0ffcc !important;
    }}

    .stWarning {{
        background: rgba(255, 180, 0, 0.12) !important;
        border: 1px solid rgba(255,180,0,0.3) !important;
        border-radius: 10px !important;
    }}

    /* Footer */
    .footer-unach {{
        text-align: center;
        color: rgba(200,220,255,0.6) !important;
        font-size: 0.78em;
        padding: 10px;
        margin-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. ENCABEZADO PRINCIPAL
# ------------------------------------------------------------------------------

st.markdown("""
<div class="encabezado-principal">
    <h1>Sistema de Control de Gastos Personales</h1>
    <h4>Facultad de Ingeniería &nbsp;|&nbsp; Ciencia de Datos e Inteligencia Artificial &nbsp;|&nbsp; UNACH 2026</h4>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 6. MENÚ LATERAL (SIDEBAR)
# ------------------------------------------------------------------------------

st.sidebar.markdown("## Menú Principal")
st.sidebar.markdown("---")
opcion = st.sidebar.radio(
    "Selecciona una opción:",
    [
        "1. Agregar Gasto / Ahorro",
        "2. Mostrar Historial Detallado",
        "3. Análisis Anual y Mensual (Matriz)",
        "4. Análisis por Categoría y Gastos Hormiga"
    ]
)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:0.78em; color:#aad4ff; text-align:center;'>
    Gonzales Diego<br>Picausi Shirley<br>Pérez Mateo<br>Poaquiza Analy<br>Valverde Ashley
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. CÁLCULOS PREVIOS Y MÉTRICAS KEY PERFORMANCE INDICATORS (KPIs)
# ------------------------------------------------------------------------------

gasto_anual_total = obtener_gasto_total_anual()
gasto_promedio = gasto_anual_total / 12 if gasto_anual_total > 0 else 0.0
total_movimientos = len(st.session_state.historial_gastos)

# Extraer el vector columna de Gastos Hormiga para sumarlo
idx_hormiga = CATEGORIAS.index("Gastos Hormiga")
columna_hormiga = [st.session_state.matriz_gastos[i][idx_hormiga] for i in range(12)]
total_hormiga = suma_recursiva_vector(columna_hormiga, len(columna_hormiga))

# Fila superior de Indicadores (Dashboard Unificado)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric(label="Total Gastado (Anual)", value=f"${gasto_anual_total:.2f}")
kpi2.metric(label="Total Ahorrado", value=f"${st.session_state.ahorro_total:.2f}")
kpi3.metric(label="Gasto Promedio (Mensual)", value=f"${gasto_promedio:.2f}")
kpi4.metric(label="Total Movimientos", value=str(total_movimientos))

# AGREGADO Y CORREGIDO: Alerta dinámica de Gastos Hormiga con estilo condicional
msg_delta = "-¡Atención!" if total_hormiga > 0 else "↑ Limpio"
kpi5.metric(label="🚨 Alerta: Total Gastos Hormiga", value=f"${total_hormiga:.2f}", delta=msg_delta)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MODULO 1: REGISTRO DE GASTOS Y AHORROS
# ------------------------------------------------------------------------------
if opcion == "1. Agregar Gasto / Ahorro":

    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    st.subheader("Registrar Nuevo Movimiento Financiero")
    st.markdown("Ingresa los datos correspondientes para mapearlos en las estructuras matriciales.")
    st.markdown("</div>", unsafe_allow_html=True)

    col_gasto, col_ahorro = st.columns(2)

    with col_gasto:
        st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
        st.write("### Registrar un Gasto")
        mes_g = st.selectbox("Selecciona el Mes del Gasto:", MESES, key="mes_gasto")
        cat_g = st.selectbox("Categoría del Gasto:", CATEGORIAS, key="cat_gasto")
        val_g = st.number_input("Valor ($):", min_value=0.01, step=0.01, format="%.2f", key="val_gasto")

        if st.button("Grabar Gasto"):
            registrar_gasto_matriz(mes_g, cat_g, val_g)
            st.session_state.historial_gastos.append({"Mes": mes_g, "Categoría": cat_g, "Valor": val_g})
            st.success(f"Gasto de ${val_g:.2f} registrado en {mes_g} - {cat_g}.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ahorro:
        st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
        st.write("### Registrar un Ahorro")
        val_a = st.number_input("Monto a destinar a ahorros ($):", min_value=0.01, step=0.01, format="%.2f", key="val_ahorro")

        if st.button("Guardar Ahorro"):
            st.session_state.ahorro_total += val_a
            st.success(f"Has sumado ${val_a:.2f} a tu fondo de ahorros.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MODULO 2: HISTORIAL DE TRANSACCIONES
# ------------------------------------------------------------------------------
elif opcion == "2. Mostrar Historial Detallado":

    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    st.subheader("Lista de Gastos Registrados en el Vector Histórico")

    if len(st.session_state.historial_gastos) == 0:
        st.warning("No hay gastos registrados aún. Ve al menú y agrega uno.")
    else:
        df_historial = pd.DataFrame(st.session_state.historial_gastos)
        df_historial.index = df_historial.index + 1
        st.dataframe(df_historial, use_container_width=True)
        st.metric(label="Total de registros en el vector", value=len(st.session_state.historial_gastos))
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MODULO 3: ANALISIS DE LA MATRIZ
# ------------------------------------------------------------------------------
elif opcion == "3. Análisis Anual y Mensual (Matriz)":

    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    st.subheader("Visualización de la Estructura Matricial (Meses x Categorías)")

    df_matriz = pd.DataFrame(st.session_state.matriz_gastos, index=MESES, columns=CATEGORIAS)
    st.write("### Matriz de Datos:")
    st.dataframe(df_matriz, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    st.write("### Análisis de Totales por Mes")

    totales_por_mes = []
    for fila in st.session_state.matriz_gastos:
        suma_mes = suma_recursiva_vector(fila, len(fila))
        totales_por_mes.append(suma_mes)

    df_totales_mes = pd.DataFrame({"Total Gastado ($)": totales_por_mes}, index=MESES)

    col_tab, col_gra = st.columns([1, 2])
    with col_tab:
        st.dataframe(df_totales_mes, use_container_width=True)
    with col_gra:
        fig, ax = plt.subplots(figsize=(7, 3.5), facecolor='none')
        ax.set_facecolor('none')
        ax.bar(MESES, totales_por_mes, color='#4285f4', edgecolor=(1, 1, 1, 0.3))
        ax.set_title("Evolución del Gasto Mensual", color='white', fontsize=13, pad=12)
        ax.set_ylabel("Total ($)", color='white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_edgecolor((1, 1, 1, 0.2))
        plt.xticks(rotation=45, ha='right', color='white')
        plt.tight_layout()
        st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MODULO 4: ANALISIS POR CATEGORIA Y GASTOS HORMIGA
# ------------------------------------------------------------------------------
elif opcion == "4. Análisis por Categoría y Gastos Hormiga":

    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    st.subheader("Análisis Avanzado de Consumo y Detección de Gastos Hormiga")
    st.markdown("</div>", unsafe_allow_html=True)

    # Calculamos totales por categoría
    totales_por_categoria = [0.0] * len(CATEGORIAS)
    for j in range(len(CATEGORIAS)):
        columna_vector = [st.session_state.matriz_gastos[i][j] for i in range(12)]
        totales_por_categoria[j] = suma_recursiva_vector(columna_vector, len(columna_vector))

    # Ordenamos con QuickSort recursivo
    pares_categoria_gasto = [[CATEGORIAS[k], totales_por_categoria[k]] for k in range(len(CATEGORIAS))]
    pares_ordenados = ordenar_gastos_recursivo(pares_categoria_gasto)

    categorias_ordenadas = [p[0] for p in pares_ordenados]
    valores_ordenados = [p[1] for p in pares_ordenados]

    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    col_pie, col_ranking = st.columns(2)

    with col_pie:
        st.write("#### Distribución Porcentual del Gasto Anual")
        if gasto_anual_total == 0:
            st.info("No hay datos suficientes para graficar.")
        else:
            pares_filtrados = [(cat, val) for cat, val in zip(categorias_ordenadas, valores_ordenados) if val > 0]

            if len(pares_filtrados) == 0:
                st.info("No hay datos con valor mayor a 0 para graficar.")
            else:
                cats_filtradas = [p[0] for p in pares_filtrados]
                vals_filtrados = [p[1] for p in pares_filtrados]

                fig2, ax2 = plt.subplots(figsize=(5, 5), facecolor='none')
                ax2.set_facecolor('none')
                colores = plt.cm.Set3.colors[:len(cats_filtradas)]
                wedges, texts, autotexts = ax2.pie(
                    vals_filtrados,
                    labels=None,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colores,
                    pctdistance=0.75,
                    wedgeprops=dict(edgecolor='white', linewidth=1.5)
                )
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(9)
                    autotext.set_fontweight('bold')

                ax2.legend(
                    wedges,
                    cats_filtradas,
                    title="Categorías",
                    loc="center left",
                    bbox_to_anchor=(1, 0, 0.5, 1),
                    fontsize=8,
                    title_fontsize=9,
                    labelcolor='white',
                    facecolor='#0a1432',
                    edgecolor=(1, 1, 1, 0.2)
                )
                ax2.axis('equal')
                plt.tight_layout()
                st.pyplot(fig2)

    with col_ranking:
        st.write("#### Ranking de Categorías con Mayor Gasto")
        if gasto_anual_total == 0:
            st.info("No hay datos suficientes para graficar.")
        else:
            pares_ranking = [(cat, val) for cat, val in zip(categorias_ordenadas, valores_ordenados) if val > 0]

            if len(pares_ranking) == 0:
                st.info("No hay datos con valor mayor a 0 para graficar.")
            else:
                # Invertimos el orden para que la barra más alta quede arriba en el barh
                cats_ranking = [p[0] for p in pares_ranking][::-1]
                vals_ranking = [p[1] for p in pares_ranking][::-1]

                # Resaltamos "Gastos Hormiga" en un color distinto para llamar la atención
                colores_barras = ['#ff6b6b' if cat == "Gastos Hormiga" else '#4285f4' for cat in cats_ranking]

                fig3, ax3 = plt.subplots(figsize=(5, 5), facecolor='none')
                ax3.set_facecolor('none')
                barras = ax3.barh(cats_ranking, vals_ranking, color=colores_barras, edgecolor=(1, 1, 1, 0.3))

                for barra, valor in zip(barras, vals_ranking):
                    ax3.text(
                        barra.get_width() + (max(vals_ranking) * 0.02),
                        barra.get_y() + barra.get_height() / 2,
                        f"${valor:.2f}",
                        va='center',
                        ha='left',
                        color='white',
                        fontsize=8
                    )

                ax3.set_title("Gasto Total por Categoría", color='white', fontsize=13, pad=12)
                ax3.set_xlabel("Total ($)", color='white')
                ax3.tick_params(colors='white')
                for spine in ax3.spines.values():
                    spine.set_edgecolor((1, 1, 1, 0.2))
                ax3.set_xlim(0, max(vals_ranking) * 1.25)
                plt.tight_layout()
                st.pyplot(fig3)
    st.markdown("</div>", unsafe_allow_html=True)
