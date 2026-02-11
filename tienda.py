import streamlit as st
import pandas as pd
from datetime import datetime
import json

st.set_page_config(
    page_title="ElectroHogar - Tienda de Electrodomésticos",
    page_icon="🛒",
    layout="wide"
)

ELECTRODOMESTICOS = [
    {
        "id": 1,
        "nombre": "Refrigeradora Samsung",
        "categoria": "Refrigeración",
        "precio": 12000.00,
        "descripcion": "Refrigeradora Side-by-Side 650L, Inox"
    },
    {
        "id": 2,
        "nombre": "Lavadora LG",
        "categoria": "Lavado",
        "precio": 8500.00,
        "descripcion": "Lavadora de carga frontal 18kg, inteligente"
    },
    {
        "id": 3,
        "nombre": "Microondas Panasonic",
        "categoria": "Cocina",
        "precio": 2500.00,
        "descripcion": "Microondas 30L, grill y convección"
    },
    {
        "id": 4,
        "nombre": "Licuadora Oster",
        "categoria": "Cocina",
        "precio": 1200.00,
        "descripcion": "Licuadora profesional 1000W, vaso de vidrio"
    },
    {
        "id": 5,
        "nombre": "Aire Acondicionado Midea",
        "categoria": "Climatización",
        "precio": 18000.00,
        "descripcion": "Aire acondicionado Split 24,000 BTU, inverter"
    },
    {
        "id": 6,
        "nombre": "Plancha a Vapor Philips",
        "categoria": "Cuidado Personal",
        "precio": 800.00,
        "descripcion": "Plancha a vapor 2400W, sistema anti-cal"
    },
    {
        "id": 7,
        "nombre": "Televisor Sony 65\"",
        "categoria": "Entretenimiento",
        "precio": 22000.00,
        "descripcion": "TV OLED 65\", 4K, Smart TV"
    },
    {
        "id": 8,
        "nombre": "Cafetera Nespresso",
        "categoria": "Cocina",
        "precio": 1800.00,
        "descripcion": "Cafetera automática con espumador de leche"
    },
    {
        "id": 9,
        "nombre": "Horno Eléctrico Whirlpool",
        "categoria": "Cocina",
        "precio": 9500.00,
        "descripcion": "Horno eléctrico empotrable 60cm, multifunción"
    },
    {
        "id": 10,
        "nombre": "Aspiradora Dyson",
        "categoria": "Limpieza",
        "precio": 6500.00,
        "descripcion": "Aspiradora inalámbrica, potencia digital"
    }
]

def init_session_state():
    if 'carrito' not in st.session_state:
        st.session_state.carrito = []
    if 'total' not in st.session_state:
        st.session_state.total = 0.00
    if 'subtotal' not in st.session_state:
        st.session_state.subtotal = 0.00

def main():
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Información del Estudiante")
        st.info("**Jose Ramon Lainez Amador**\n\n"
                "**Número de Cuenta:** 202310110034")
        st.markdown("---")
    
    # Título principal
    st.title("🛒 ElectroHogar - Tienda de Electrodomésticos")
    st.markdown("**Examen I Parcial - Computacion en la Nube**")
    st.markdown("---")
    
    init_session_state()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Catálogo de Productos")
        
        df_productos = pd.DataFrame(ELECTRODOMESTICOS)
        
        st.subheader("Productos Disponibles")
        st.dataframe(df_productos[['nombre', 'categoria', 'precio', 'descripcion']], 
                    hide_index=True,
                    column_config={
                        "nombre": "Producto",
                        "categoria": "Categoría",
                        "precio": st.column_config.NumberColumn("Precio (L.)", format="L. %.2f"),
                        "descripcion": "Descripción"
                    })
        
        st.subheader("🔍 Filtro por Precio")
        precio_min = float(df_productos['precio'].min())
        precio_max = float(df_productos['precio'].max())
        
        rango_precio = st.slider(
            "Selecciona el rango de precios:",
            min_value=precio_min,
            max_value=precio_max,
            value=(precio_min, precio_max),
            step=100.0,
            format="L. %.2f"
        )
        
        productos_filtrados = df_productos[
            (df_productos['precio'] >= rango_precio[0]) & 
            (df_productos['precio'] <= rango_precio[1])
        ]
        
        if not productos_filtrados.empty:
            st.write(f"**{len(productos_filtrados)} productos encontrados en el rango de precio:**")
            st.dataframe(productos_filtrados[['nombre', 'categoria', 'precio']], 
                        hide_index=True,
                        column_config={
                            "nombre": "Producto",
                            "categoria": "Categoría",
                            "precio": st.column_config.NumberColumn("Precio (L.)", format="L. %.2f")
                        })
        else:
            st.warning("No hay productos en este rango de precio.")
        
        st.subheader("🛍️ Selección de Producto")
        
        nombres_productos = [f"{p['nombre']} - L. {p['precio']:.2f}" for p in ELECTRODOMESTICOS]
        
        producto_seleccionado = st.selectbox(
            "Selecciona un producto:",
            options=nombres_productos,
            index=0,
            key="select_producto"
        )
        
        idx_seleccionado = nombres_productos.index(producto_seleccionado)
        producto = ELECTRODOMESTICOS[idx_seleccionado]
        
        st.info(f"""
        **Producto Seleccionado:** {producto['nombre']}
        
        **Categoría:** {producto['categoria']}
        
        **Precio Unitario:** L. {producto['precio']:.2f}
        
        **Descripción:** {producto['descripcion']}
        """)
        
        cantidad = st.number_input(
            "Cantidad:",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
            key=f"cantidad_{producto['id']}"
        )
        
        subtotal_producto = producto['precio'] * cantidad
        
        st.success(f"**Subtotal de {producto['nombre']}:** L. {subtotal_producto:.2f}")
        
        if st.button("➕ Agregar al Carrito", type="primary", key=f"add_{producto['id']}"):

            item_carrito = {
                "producto": producto['nombre'],
                "categoria": producto['categoria'],
                "precio_unitario": producto['precio'],
                "cantidad": cantidad,
                "subtotal": subtotal_producto
            }
            st.session_state.carrito.append(item_carrito)
            st.success(f"✅ {producto['nombre']} agregado al carrito!")
            st.rerun()
    
    with col2:
        st.header("🛒 Carrito de Compras")
        
        if st.session_state.carrito:
            df_carrito = pd.DataFrame(st.session_state.carrito)
            
            st.dataframe(df_carrito,
                        hide_index=True,
                        column_config={
                            "producto": "Producto",
                            "categoria": "Categoría",
                            "precio_unitario": st.column_config.NumberColumn("Precio Unitario", format="L. %.2f"),
                            "cantidad": "Cantidad",
                            "subtotal": st.column_config.NumberColumn("Subtotal", format="L. %.2f")
                        })
            
            subtotal = df_carrito['subtotal'].sum()
            impuesto = subtotal * 0.15  # 15% de ISV
            total = subtotal + impuesto
            
            st.session_state.subtotal = subtotal
            st.session_state.total = total
            
            st.subheader("📊 Resumen del Carrito")
            st.metric("Subtotal", f"L. {subtotal:.2f}")
            st.metric("ISV (15%)", f"L. {impuesto:.2f}")
            st.metric("**Total a Pagar**", f"**L. {total:.2f}**")
            
            if st.button("🗑️ Vaciar Carrito", type="secondary"):
                st.session_state.carrito = []
                st.rerun()
        else:
            st.info("El carrito está vacío. Agrega productos para continuar.")
        
        st.header("👤 Datos del Cliente")
        
        with st.form("datos_cliente"):
            nombre_cliente = st.text_input("Nombre Completo:", placeholder="Ingrese su nombre completo")
            rtn_identidad = st.text_input("RTN / Identidad:", placeholder="Ingrese su RTN o número de identidad")
            fecha_compra = st.date_input("Fecha de Compra:", value=datetime.now().date())
            
            submit_datos = st.form_submit_button("💾 Guardar Datos del Cliente")
            
            if submit_datos and nombre_cliente and rtn_identidad:
                st.session_state.nombre_cliente = nombre_cliente
                st.session_state.rtn_identidad = rtn_identidad
                st.session_state.fecha_compra = fecha_compra
                st.success("✅ Datos del cliente guardados correctamente!")
    
    st.markdown("---")
    st.header("🧾 Resumen de Facturación")
    
    col_fact1, col_fact2 = st.columns([2, 1])
    
    with col_fact1:
        if 'nombre_cliente' in st.session_state and st.session_state.carrito:
            st.subheader("Información del Cliente")
            st.write(f"**Nombre:** {st.session_state.nombre_cliente}")
            st.write(f"**RTN/Identidad:** {st.session_state.rtn_identidad}")
            st.write(f"**Fecha de Compra:** {st.session_state.fecha_compra}")
            
            st.subheader("Detalle de la Compra")
            
            df_detalle = pd.DataFrame(st.session_state.carrito)
            st.table(df_detalle.assign(
                **{
                    'Precio Unitario': df_detalle['precio_unitario'].map(lambda x: f"L. {x:.2f}"),
                    'Subtotal': df_detalle['subtotal'].map(lambda x: f"L. {x:.2f}")
                }
            )[['producto', 'cantidad', 'Precio Unitario', 'Subtotal']])
    
    with col_fact2:
        if 'nombre_cliente' in st.session_state and st.session_state.carrito:
            st.subheader("Cálculos Finales")
            
            subtotal = st.session_state.subtotal
            impuesto = subtotal * 0.15
            total = st.session_state.total
            
            st.write(f"**Subtotal General:** L. {subtotal:.2f}")
            st.write(f"**ISV (15%):** L. {impuesto:.2f}")
            st.write("---")
            st.write(f"### **Total a Pagar:** L. {total:.2f}")
            
            with st.expander("📝 Ver explicación del cálculo"):
                st.markdown("""
                **Fórmula de cálculo:**
                
                1. **Subtotal General:** Suma de todos los subtotales de productos
                
                2. **ISV (15%):** Subtotal × 0.15
                
                3. **Total a Pagar:** Subtotal + ISV
                
                **Ejemplo:**
                - Si el subtotal es L. 10,000.00
                - ISV (15%) = 10,000.00 × 0.15 = L. 1,500.00
                - Total = 10,000.00 + 1,500.00 = L. 11,500.00
                """)
            
            if st.button("🖨️ Generar Factura", type="primary"):
                factura = {
                    "cliente": st.session_state.nombre_cliente,
                    "rtn": st.session_state.rtn_identidad,
                    "fecha": str(st.session_state.fecha_compra),
                    "detalle": st.session_state.carrito,
                    "subtotal": subtotal,
                    "impuesto": impuesto,
                    "total": total
                }
                
                st.balloons()
                st.success("✅ Factura generada exitosamente!")
                
                st.download_button(
                    label="📥 Descargar Factura (JSON)",
                    data=json.dumps(factura, indent=2),
                    file_name=f"factura_{st.session_state.nombre_cliente}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    st.markdown("---")
    st.markdown("### 📋 Instrucciones de Uso")
    
    instrucciones = """
    1. **Explora el catálogo** de productos en la sección izquierda
    2. **Filtra productos** por rango de precio usando el slider
    3. **Selecciona un producto** del menú desplegable
    4. **Especifica la cantidad** deseada
    5. **Haz clic en 'Agregar al Carrito'** para añadir productos
    6. **Ingresa tus datos** en la sección "Datos del Cliente"
    7. **Revisa el resumen** en la sección de Facturación
    8. **Genera tu factura** cuando hayas terminado
    """
    
    st.info(instrucciones)

if __name__ == "__main__":
    main()