import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Gestor de Inventario y Negocio", page_icon="📦", layout="wide"
)

st.title("📦 Gestor Inteligente de Inventario y Ventas")
st.markdown(
    "Aplicación web diseñada para optimizar el control de stock, precios y"
    " márgenes de ganancia en pequeños comercios."
)

# Inicializar base de datos simulada en la sesión
if "inventario" not in st.session_state:
  st.session_state.inventario = pd.DataFrame({
      "Producto": [
          "Arroz Extra (1kg)",
          "Azúcar Rubia (1kg)",
          "Aceite Vegetal (1L)",
          "Leche Evaporada",
      ],
      "Categoría": ["Abarrotes", "Abarrotes", "Abarrotes", "Lácteos"],
      "Precio Compra (S/.)": [4.20, 3.80, 8.50, 4.00],
      "Precio Venta (S/.)": [5.50, 4.80, 10.50, 4.80],
      "Stock": [45, 12, 8, 30],
      "Stock Mínimo": [15, 20, 10, 10],
  })

df = st.session_state.inventario

# Cálculos automáticos de negocio
df["Margen Unitario (S/.)"] = df["Precio Venta (S/.)"] - df["Precio Compra (S/.)"]
df["Rentabilidad (%)"] = (
    df["Margen Unitario (S/.)"] / df["Precio Compra (S/.)"]
) * 100

# --- Menú Lateral ---
st.sidebar.header("🛠️ Menú de Navegación")
menu = st.sidebar.selectbox(
    "Selecciona una sección",
    ["📊 Dashboard General", "➕ Registrar Producto", "⚠️ Alertas de Stock"],
)

if menu == "📊 Dashboard General":
  st.subheader("Indicadores Clave del Negocio")

  col1, col2, col3 = st.columns(3)
  total_productos = len(df)
  valor_inventario = (df["Precio Compra (S/.)"] * df["Stock"]).sum()
  stock_critico = len(df[df["Stock"] <= df["Stock Mínimo"]])

  col1.metric("Total de Productos", total_productos)
  col2.metric("Inversión en Inventario", f"S/. {valor_inventario:.2f}")
  col3.metric(
      "Alertas de Stock",
      stock_critico,
      delta=-stock_critico if stock_critico > 0 else "Óptimo",
      delta_color="inverse",
  )

  st.divider()
  st.subheader("Inventario Actualizado y Márgenes")
  st.dataframe(
      df.style.format({
          "Precio Compra (S/.)": "S/. {:.2f}",
          "Precio Venta (S/.)": "S/. {:.2f}",
          "Margen Unitario (S/.)": "S/. {:.2f}",
          "Rentabilidad (%)": "{:.1f}%",
      }),
      use_container_width=True,
  )

  st.subheader("📊 Rentabilidad Porcentual por Producto")
  st.bar_chart(df.set_index("Producto")["Rentabilidad (%)"])

elif menu == "➕ Registrar Producto":
  st.subheader("Agregar Nuevo Producto")

  with st.form("form_producto"):
    col1, col2 = st.columns(2)
    with col1:
      nombre = st.text_input("Nombre del Producto")
      categoria = st.selectbox(
          "Categoría",
          ["Abarrotes", "Lácteos", "Bebidas", "Limpieza", "Otros"],
      )
      precio_compra = st.number_input(
          "Precio de Compra (S/.)", min_value=0.0, format="%.2f"
      )
    with col2:
      precio_venta = st.number_input(
          "Precio de Venta (S/.)", min_value=0.0, format="%.2f"
      )
      stock = st.number_input("Stock Actual", min_value=0, step=1)
      stock_min = st.number_input(
          "Stock Mínimo de Alerta", min_value=0, step=1, value=10
      )

    submit = st.form_submit_button("Guardar en el Sistema")

    if submit:
      if nombre and precio_compra > 0 and precio_venta > 0:
        nuevo_prod = pd.DataFrame({
            "Producto": [nombre],
            "Categoría": [categoria],
            "Precio Compra (S/.)": [precio_compra],
            "Precio Venta (S/.)": [precio_venta],
            "Stock": [stock],
            "Stock Mínimo": [stock_min],
        })
        st.session_state.inventario = pd.concat(
            [st.session_state.inventario, nuevo_prod], ignore_index=True
        )
        st.success(f"¡Producto '{nombre}' registrado con éxito!")
      else:
        st.error(
            "Por favor, complete todos los campos con valores mayores a 0."
        )

elif menu == "⚠️ Alertas de Stock":
  st.subheader("⚠️ Productos que Requieren Reposición")
  alertas = df[df["Stock"] <= df["Stock Mínimo"]]

  if not alertas.empty:
    st.warning(
        "Atención: Los siguientes productos están por debajo del stock mínimo"
        " recomendado:"
    )
    st.dataframe(alertas, use_container_width=True)
  else:
    st.success("¡Excelente! Todo el inventario se encuentra en niveles óptimos.")