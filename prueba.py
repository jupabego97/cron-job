#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis Estratégico Completo de Ventas - Retail de Tecnología Colombia
========================================================================

Análisis exhaustivo de la tabla facturas para identificar insights clave
y oportunidades de negocio para un retail de tecnología en Colombia.

Áreas de análisis:
1. Patrones temporales (hora, día, mes, estacionalidad)
2. Análisis de productos (top productos, rotación, categorías)
3. Análisis de clientes (frecuencia, ticket promedio, segmentación)
4. Análisis de vendedores (performance, eficiencia, productividad)
5. Análisis de métodos de pago (preferencias, tendencias)
6. Análisis de rentabilidad y márgenes
7. Tendencias y predicciones
8. Recomendaciones estratégicas
"""
import sys
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Conexión a la base de datos
DB_URL = "postgresql://postgres:UBxmwADTQguutZmWTcakCPsxpqpODfKO@yamabiko.proxy.rlwy.net:33503/railway"

print("=" * 100)
print(" " * 20 + "ANÁLISIS ESTRATÉGICO COMPLETO DE VENTAS")
print(" " * 15 + "RETAIL DE TECNOLOGÍA - COLOMBIA")
print(" " * 30 + "AÑO 2025")
print("=" * 100)

try:
    engine = create_engine(DB_URL)
    
    # ========================================================================
    # CARGA DE DATOS
    # ========================================================================
    print("\n📊 CARGANDO DATOS DE FACTURAS...")
    print("-" * 100)
    
    query = """
    SELECT 
        id,
        fecha,
        hora,
        total,
        cantidad,
        precio,
        metodo,
        vendedor,
        nombre,
        cliente,
        totalfact,
        item_id
    FROM facturas
    WHERE EXTRACT(YEAR FROM fecha) = 2025
    ORDER BY fecha, hora
    """
    
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("❌ No hay datos en la tabla facturas")
        exit(1)
    
    print(f"✅ {len(df):,} registros cargados")
    print(f"📅 Rango de fechas: {df['fecha'].min()} a {df['fecha'].max()}")
    print(f"📦 Productos únicos: {df['nombre'].nunique():,}")
    print(f"👥 Clientes únicos: {df['cliente'].nunique():,}")
    print(f"👤 Vendedores únicos: {df['vendedor'].nunique():,}")
    
    # Convertir tipos de datos
    if df['hora'].dtype == 'object':
        df['hora'] = pd.to_datetime(df['hora'])
    
    # Extraer componentes temporales
    df['fecha_dt'] = pd.to_datetime(df['fecha'])
    df['hora_dt'] = pd.to_datetime(df['hora'])
    df['hora_solo'] = df['hora_dt'].dt.hour
    df['minuto'] = df['hora_dt'].dt.minute
    df['dia_semana'] = df['fecha_dt'].dt.day_name()
    df['dia_semana_num'] = df['fecha_dt'].dt.dayofweek
    df['mes'] = df['fecha_dt'].dt.month
    df['año'] = df['fecha_dt'].dt.year
    df['trimestre'] = df['fecha_dt'].dt.quarter
    df['semana_año'] = df['fecha_dt'].dt.isocalendar().week
    
    # Calcular métricas adicionales
    df['ticket_promedio'] = df['totalfact'] / df.groupby(['fecha', 'id'])['totalfact'].transform('count')
    df['items_por_factura'] = df.groupby(['fecha', 'id'])['nombre'].transform('count')
    
    # ========================================================================
    # 1. ANÁLISIS TEMPORAL DETALLADO
    # ========================================================================
    print("\n" + "=" * 100)
    print("1️⃣ ANÁLISIS TEMPORAL - PATRONES DE VENTAS")
    print("=" * 100)
    
    # 1.1 Análisis por hora del día
    print("\n📊 1.1 DISTRIBUCIÓN DE VENTAS POR HORA DEL DÍA")
    print("-" * 100)
    
    ventas_por_hora = df.groupby('hora_solo').agg({
        'total': ['sum', 'count', 'mean'],
        'cantidad': 'sum',
        'totalfact': 'sum'
    }).round(2)
    ventas_por_hora.columns = ['Total_Items', 'Num_Transacciones', 'Ticket_Promedio_Item', 'Total_Unidades', 'Total_Facturado']
    ventas_por_hora['Ticket_Promedio_Factura'] = (ventas_por_hora['Total_Facturado'] / ventas_por_hora['Num_Transacciones']).round(2)
    ventas_por_hora['%_del_Total'] = (ventas_por_hora['Total_Facturado'] / ventas_por_hora['Total_Facturado'].sum() * 100).round(2)
    ventas_por_hora = ventas_por_hora.sort_values('Total_Facturado', ascending=False)
    
    print("\n🏆 TOP 10 HORAS CON MAYOR VOLUMEN DE VENTAS:")
    print(ventas_por_hora.head(10).to_string())
    
    # Horario de atención óptimo
    horas_80pct = ventas_por_hora.nlargest(int(len(ventas_por_hora) * 0.8), 'Total_Facturado')
    hora_inicio_80 = horas_80pct.index.min()
    hora_fin_80 = horas_80pct.index.max()
    
    horas_90pct = ventas_por_hora.nlargest(int(len(ventas_por_hora) * 0.9), 'Total_Facturado')
    hora_inicio_90 = horas_90pct.index.min()
    hora_fin_90 = horas_90pct.index.max()
    
    print(f"\n⏰ HORARIO DE ATENCIÓN RECOMENDADO:")
    print(f"   📌 Horario óptimo (80% ventas): {hora_inicio_80:02d}:00 - {hora_fin_80:02d}:00 ({hora_fin_80 - hora_inicio_80} horas)")
    print(f"   📌 Horario extendido (90% ventas): {hora_inicio_90:02d}:00 - {hora_fin_90:02d}:00 ({hora_fin_90 - hora_inicio_90} horas)")
    
    # Períodos del día
    def clasificar_periodo(hora):
        if 6 <= hora < 9:
            return 'Madrugada (6-9)'
        elif 9 <= hora < 12:
            return 'Mañana Temprano (9-12)'
        elif 12 <= hora < 15:
            return 'Mediodía (12-15)'
        elif 15 <= hora < 18:
            return 'Tarde (15-18)'
        elif 18 <= hora < 21:
            return 'Noche (18-21)'
        else:
            return 'Noche Tarde (21-6)'
    
    df['periodo'] = df['hora_solo'].apply(clasificar_periodo)
    
    ventas_por_periodo = df.groupby('periodo').agg({
        'totalfact': ['sum', 'count', 'mean'],
        'total': 'sum',
        'cantidad': 'sum'
    }).round(2)
    ventas_por_periodo.columns = ['Total_Facturado', 'Num_Facturas', 'Ticket_Promedio', 'Total_Items', 'Total_Unidades']
    ventas_por_periodo['%_del_Total'] = (ventas_por_periodo['Total_Facturado'] / ventas_por_periodo['Total_Facturado'].sum() * 100).round(2)
    ventas_por_periodo = ventas_por_periodo.sort_values('Total_Facturado', ascending=False)
    
    print("\n📊 DISTRIBUCIÓN DE VENTAS POR PERÍODO DEL DÍA:")
    print(ventas_por_periodo.to_string())
    
    # 1.2 Análisis por día de la semana
    print("\n📅 1.2 ANÁLISIS POR DÍA DE LA SEMANA")
    print("-" * 100)
    
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    orden_dias_esp = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    ventas_por_dia = df.groupby('dia_semana').agg({
        'totalfact': ['sum', 'count', 'mean', 'std'],
        'total': 'sum',
        'cantidad': 'sum',
        'items_por_factura': 'mean'
    }).round(2)
    ventas_por_dia.columns = ['Total_Facturado', 'Num_Facturas', 'Ticket_Promedio', 'Desv_Ticket', 'Total_Items', 'Total_Unidades', 'Items_Por_Factura']
    ventas_por_dia = ventas_por_dia.reindex(orden_dias)
    ventas_por_dia['%_del_Total'] = (ventas_por_dia['Total_Facturado'] / ventas_por_dia['Total_Facturado'].sum() * 100).round(2)
    ventas_por_dia['Coef_Variacion'] = (ventas_por_dia['Desv_Ticket'] / ventas_por_dia['Ticket_Promedio'] * 100).round(2)
    
    print("\n📊 VENTAS POR DÍA DE LA SEMANA:")
    print(ventas_por_dia.to_string())
    
    mejor_dia = ventas_por_dia['Total_Facturado'].idxmax()
    peor_dia = ventas_por_dia['Total_Facturado'].idxmin()
    
    print(f"\n🏆 MEJOR DÍA: {mejor_dia} (${ventas_por_dia.loc[mejor_dia, 'Total_Facturado']:,.2f} - {ventas_por_dia.loc[mejor_dia, '%_del_Total']:.1f}%)")
    print(f"📉 PEOR DÍA: {peor_dia} (${ventas_por_dia.loc[peor_dia, 'Total_Facturado']:,.2f} - {ventas_por_dia.loc[peor_dia, '%_del_Total']:.1f}%)")
    
    # 1.3 Análisis mensual y estacional
    print("\n📆 1.3 ANÁLISIS MENSUAL Y ESTACIONAL")
    print("-" * 100)
    
    ventas_por_mes = df.groupby(['año', 'mes']).agg({
        'totalfact': ['sum', 'count', 'mean'],
        'total': 'sum',
        'cantidad': 'sum'
    }).round(2)
    ventas_por_mes.columns = ['Total_Facturado', 'Num_Facturas', 'Ticket_Promedio', 'Total_Items', 'Total_Unidades']
    ventas_por_mes['Dias_Activos'] = df.groupby(['año', 'mes'])['fecha'].nunique()
    ventas_por_mes['Promedio_Diario'] = (ventas_por_mes['Total_Facturado'] / ventas_por_mes['Dias_Activos']).round(2)
    
    print("\n📊 VENTAS POR MES:")
    print(ventas_por_mes.to_string())
    
    # Análisis por trimestre
    ventas_por_trimestre = df.groupby(['año', 'trimestre']).agg({
        'totalfact': ['sum', 'count', 'mean'],
        'total': 'sum'
    }).round(2)
    ventas_por_trimestre.columns = ['Total_Facturado', 'Num_Facturas', 'Ticket_Promedio', 'Total_Items']
    
    print("\n📊 VENTAS POR TRIMESTRE:")
    print(ventas_por_trimestre.to_string())
    
    # ========================================================================
    # 2. ANÁLISIS DE PRODUCTOS
    # ========================================================================
    print("\n" + "=" * 100)
    print("2️⃣ ANÁLISIS DE PRODUCTOS - ROTACIÓN Y RENTABILIDAD")
    print("=" * 100)
    
    # 2.1 Top productos por ventas
    print("\n🏆 2.1 TOP PRODUCTOS POR VOLUMEN DE VENTAS")
    print("-" * 100)
    
    productos_ventas = df.groupby('nombre').agg({
        'total': ['sum', 'count', 'mean'],
        'cantidad': 'sum',
        'precio': 'mean',
        'fecha': ['min', 'max', 'nunique']
    }).round(2)
    productos_ventas.columns = ['Total_Ventas', 'Num_Ventas', 'Ticket_Promedio', 'Total_Unidades', 'Precio_Promedio', 'Primera_Venta', 'Ultima_Venta', 'Dias_Con_Ventas']
    productos_ventas = productos_ventas.sort_values('Total_Ventas', ascending=False)
    productos_ventas['%_del_Total'] = (productos_ventas['Total_Ventas'] / productos_ventas['Total_Ventas'].sum() * 100).round(2)
    productos_ventas['Rotacion'] = (productos_ventas['Total_Unidades'] / productos_ventas['Dias_Con_Ventas']).round(2)
    
    print("\n🏆 TOP 20 PRODUCTOS CLAVE POR VOLUMEN DE VENTAS (2025):")
    print("-" * 100)
    top_20_productos = productos_ventas.head(20)
    # Mostrar en formato más legible
    for idx, (nombre, row) in enumerate(top_20_productos.iterrows(), 1):
        print(f"\n{idx:2d}. {nombre}")
        print(f"    💰 Total Ventas: ${row['Total_Ventas']:,.2f} ({row['%_del_Total']:.2f}% del total)")
        print(f"    📦 Unidades Vendidas: {row['Total_Unidades']:,.0f}")
        print(f"    🧾 Número de Ventas: {row['Num_Ventas']:,.0f}")
        print(f"    💵 Precio Promedio: ${row['Precio_Promedio']:,.2f}")
        print(f"    🔄 Rotación: {row['Rotacion']:.2f} unidades/día")
        print(f"    📅 Días con Ventas: {row['Dias_Con_Ventas']:.0f}")
    
    print("\n" + "=" * 100)
    print("📊 TABLA COMPLETA TOP 20 PRODUCTOS:")
    print("=" * 100)
    print(top_20_productos.to_string())
    
    # Análisis de concentración (Pareto)
    productos_ventas_cumsum = productos_ventas['Total_Ventas'].cumsum()
    productos_ventas_cumsum_pct = (productos_ventas_cumsum / productos_ventas['Total_Ventas'].sum() * 100).round(2)
    
    top_20_pct = productos_ventas_cumsum_pct.iloc[19] if len(productos_ventas_cumsum_pct) > 19 else productos_ventas_cumsum_pct.iloc[-1]
    top_50_pct = productos_ventas_cumsum_pct.iloc[49] if len(productos_ventas_cumsum_pct) > 49 else productos_ventas_cumsum_pct.iloc[-1]
    
    print(f"\n📊 ANÁLISIS DE CONCENTRACIÓN (PARETO):")
    print(f"   Top 20 productos representan: {top_20_pct:.1f}% de las ventas")
    print(f"   Top 50 productos representan: {top_50_pct:.1f}% de las ventas")
    
    # 2.2 Productos por frecuencia de venta
    print("\n🔄 2.2 ANÁLISIS DE ROTACIÓN DE PRODUCTOS")
    print("-" * 100)
    
    productos_rotacion = productos_ventas.sort_values('Rotacion', ascending=False)
    
    print("\n🔄 TOP 20 PRODUCTOS CON MAYOR ROTACIÓN (unidades/día):")
    print(productos_rotacion.head(20)[['Total_Unidades', 'Dias_Con_Ventas', 'Rotacion', 'Total_Ventas']].to_string())
    
    # Productos estancados (baja rotación)
    umbral_rotacion = productos_rotacion['Rotacion'].quantile(0.25)
    productos_baja_rotacion = productos_rotacion[productos_rotacion['Rotacion'] < umbral_rotacion].sort_values('Total_Ventas', ascending=False)
    
    print(f"\n⚠️ PRODUCTOS CON BAJA ROTACIÓN (Rotación < {umbral_rotacion:.2f} unidades/día):")
    print(f"   Total de productos: {len(productos_baja_rotacion)}")
    if len(productos_baja_rotacion) > 0:
        print(f"   Valor total estancado: ${productos_baja_rotacion['Total_Ventas'].sum():,.2f}")
        print("\n   Top 10 productos con baja rotación pero alto valor:")
        print(productos_baja_rotacion.head(10)[['Total_Ventas', 'Rotacion', 'Total_Unidades']].to_string())
    
    # 2.3 Análisis de precio por producto
    print("\n💰 2.3 ANÁLISIS DE PRECIOS")
    print("-" * 100)
    
    productos_precio = df.groupby('nombre').agg({
        'precio': ['min', 'max', 'mean', 'std', 'count']
    }).round(2)
    productos_precio.columns = ['Precio_Min', 'Precio_Max', 'Precio_Promedio', 'Desv_Precio', 'Num_Ventas']
    productos_precio['Rango_Precio'] = productos_precio['Precio_Max'] - productos_precio['Precio_Min']
    productos_precio['Coef_Variacion_Precio'] = (productos_precio['Desv_Precio'] / productos_precio['Precio_Promedio'] * 100).round(2)
    productos_precio = productos_precio.sort_values('Precio_Promedio', ascending=False)
    
    print("\n💰 TOP 20 PRODUCTOS MÁS CAROS (por precio promedio):")
    print(productos_precio.head(20).to_string())
    
    # Productos con variación de precio (posibles promociones)
    productos_variacion_precio = productos_precio[productos_precio['Rango_Precio'] > 0].sort_values('Rango_Precio', ascending=False)
    
    print(f"\n📊 PRODUCTOS CON VARIACIÓN DE PRECIO (posibles promociones):")
    print(f"   Total productos con variación: {len(productos_variacion_precio)}")
    if len(productos_variacion_precio) > 0:
        print("\n   Top 10 productos con mayor variación de precio:")
        print(productos_variacion_precio.head(10)[['Precio_Min', 'Precio_Max', 'Precio_Promedio', 'Rango_Precio']].to_string())
    
    # ========================================================================
    # 3. ANÁLISIS DE CLIENTES
    # ========================================================================
    print("\n" + "=" * 100)
    print("3️⃣ ANÁLISIS DE CLIENTES - SEGMENTACIÓN Y VALOR")
    print("=" * 100)
    
    # 3.1 Análisis de clientes por frecuencia y valor
    print("\n👥 3.1 ANÁLISIS DE CLIENTES")
    print("-" * 100)
    
    clientes_analisis = df.groupby('cliente').agg({
        'totalfact': ['sum', 'count', 'mean'],
        'total': 'sum',
        'cantidad': 'sum',
        'fecha': ['min', 'max', 'nunique']
    }).round(2)
    clientes_analisis.columns = ['Total_Compras', 'Num_Compras', 'Ticket_Promedio', 'Total_Items', 'Total_Unidades', 'Primera_Compra', 'Ultima_Compra', 'Dias_Activos']
    clientes_analisis = clientes_analisis.sort_values('Total_Compras', ascending=False)
    clientes_analisis['%_del_Total'] = (clientes_analisis['Total_Compras'] / clientes_analisis['Total_Compras'].sum() * 100).round(2)
    
    # Calcular días desde última compra
    ultima_fecha = df['fecha_dt'].max()
    clientes_analisis['Dias_Desde_Ultima_Compra'] = (ultima_fecha - pd.to_datetime(clientes_analisis['Ultima_Compra'])).dt.days
    
    # Segmentación de clientes (RFM simplificado)
    def segmentar_cliente(row):
        if row['Total_Compras'] >= clientes_analisis['Total_Compras'].quantile(0.8):
            if row['Dias_Desde_Ultima_Compra'] <= 30:
                return 'VIP - Activo'
            elif row['Dias_Desde_Ultima_Compra'] <= 90:
                return 'VIP - En Riesgo'
            else:
                return 'VIP - Dormido'
        elif row['Total_Compras'] >= clientes_analisis['Total_Compras'].quantile(0.5):
            if row['Dias_Desde_Ultima_Compra'] <= 30:
                return 'Regular - Activo'
            elif row['Dias_Desde_Ultima_Compra'] <= 90:
                return 'Regular - En Riesgo'
            else:
                return 'Regular - Dormido'
        else:
            if row['Dias_Desde_Ultima_Compra'] <= 30:
                return 'Ocasional - Activo'
            elif row['Dias_Desde_Ultima_Compra'] <= 90:
                return 'Ocasional - En Riesgo'
            else:
                return 'Ocasional - Dormido'
    
    clientes_analisis['Segmento'] = clientes_analisis.apply(segmentar_cliente, axis=1)
    
    print("\n👥 TOP 20 CLIENTES POR VOLUMEN DE COMPRAS:")
    print(clientes_analisis.head(20)[['Total_Compras', 'Num_Compras', 'Ticket_Promedio', 'Dias_Activos', 'Dias_Desde_Ultima_Compra', 'Segmento']].to_string())
    
    # Análisis de concentración de clientes
    clientes_cumsum = clientes_analisis['Total_Compras'].cumsum()
    clientes_cumsum_pct = (clientes_cumsum / clientes_analisis['Total_Compras'].sum() * 100).round(2)
    
    top_10_clientes_pct = clientes_cumsum_pct.iloc[9] if len(clientes_cumsum_pct) > 9 else clientes_cumsum_pct.iloc[-1]
    top_20_clientes_pct = clientes_cumsum_pct.iloc[19] if len(clientes_cumsum_pct) > 19 else clientes_cumsum_pct.iloc[-1]
    
    print(f"\n📊 CONCENTRACIÓN DE CLIENTES:")
    print(f"   Top 10 clientes representan: {top_10_clientes_pct:.1f}% de las ventas")
    print(f"   Top 20 clientes representan: {top_20_clientes_pct:.1f}% de las ventas")
    
    # Segmentación de clientes
    print("\n📊 SEGMENTACIÓN DE CLIENTES:")
    segmentacion = clientes_analisis.groupby('Segmento').agg({
        'Total_Compras': ['sum', 'count', 'mean'],
        'Num_Compras': 'mean',
        'Ticket_Promedio': 'mean'
    }).round(2)
    segmentacion.columns = ['Total_Ventas', 'Num_Clientes', 'Promedio_Cliente', 'Compras_Promedio', 'Ticket_Promedio']
    segmentacion['%_del_Total'] = (segmentacion['Total_Ventas'] / segmentacion['Total_Ventas'].sum() * 100).round(2)
    segmentacion['%_Clientes'] = (segmentacion['Num_Clientes'] / segmentacion['Num_Clientes'].sum() * 100).round(2)
    print(segmentacion.to_string())
    
    # Clientes en riesgo (no compran hace más de 90 días)
    clientes_riesgo = clientes_analisis[clientes_analisis['Dias_Desde_Ultima_Compra'] > 90].sort_values('Total_Compras', ascending=False)
    
    print(f"\n⚠️ CLIENTES EN RIESGO (no compran hace más de 90 días):")
    print(f"   Total: {len(clientes_riesgo)} clientes")
    print(f"   Valor potencial perdido: ${clientes_riesgo['Total_Compras'].sum():,.2f}")
    if len(clientes_riesgo) > 0:
        print("\n   Top 10 clientes en riesgo (mayor valor histórico):")
        print(clientes_riesgo.head(10)[['Total_Compras', 'Num_Compras', 'Dias_Desde_Ultima_Compra']].to_string())
    
    # ========================================================================
    # 4. ANÁLISIS DE VENDEDORES
    # ========================================================================
    print("\n" + "=" * 100)
    print("4️⃣ ANÁLISIS DE VENDEDORES - PERFORMANCE Y PRODUCTIVIDAD")
    print("=" * 100)
    
    # 4.1 Performance de vendedores
    print("\n👤 4.1 PERFORMANCE DE VENDEDORES")
    print("-" * 100)
    
    vendedores_analisis = df.groupby('vendedor').agg({
        'totalfact': ['sum', 'count', 'mean'],
        'total': 'sum',
        'cantidad': 'sum',
        'fecha': 'nunique',
        'cliente': 'nunique'
    }).round(2)
    vendedores_analisis.columns = ['Total_Ventas', 'Num_Transacciones', 'Ticket_Promedio', 'Total_Items', 'Total_Unidades', 'Dias_Activos', 'Clientes_Atendidos']
    vendedores_analisis = vendedores_analisis.sort_values('Total_Ventas', ascending=False)
    vendedores_analisis['%_del_Total'] = (vendedores_analisis['Total_Ventas'] / vendedores_analisis['Total_Ventas'].sum() * 100).round(2)
    vendedores_analisis['Ventas_Por_Dia'] = (vendedores_analisis['Total_Ventas'] / vendedores_analisis['Dias_Activos']).round(2)
    vendedores_analisis['Transacciones_Por_Dia'] = (vendedores_analisis['Num_Transacciones'] / vendedores_analisis['Dias_Activos']).round(2)
    vendedores_analisis['Clientes_Por_Dia'] = (vendedores_analisis['Clientes_Atendidos'] / vendedores_analisis['Dias_Activos']).round(2)
    
    print("\n👤 PERFORMANCE DE VENDEDORES:")
    print(vendedores_analisis.to_string())
    
    # Eficiencia de vendedores
    promedio_ventas_dia = vendedores_analisis['Ventas_Por_Dia'].mean()
    vendedores_analisis['Eficiencia'] = ((vendedores_analisis['Ventas_Por_Dia'] / promedio_ventas_dia) * 100).round(2)
    
    print("\n🏆 TOP 5 VENDEDORES MÁS EFICIENTES (por ventas/día):")
    top_vendedores = vendedores_analisis.nlargest(5, 'Ventas_Por_Dia')
    print(top_vendedores[['Total_Ventas', 'Ventas_Por_Dia', 'Transacciones_Por_Dia', 'Ticket_Promedio', 'Eficiencia']].to_string())
    
    # ========================================================================
    # 5. ANÁLISIS DE MÉTODOS DE PAGO
    # ========================================================================
    print("\n" + "=" * 100)
    print("5️⃣ ANÁLISIS DE MÉTODOS DE PAGO")
    print("=" * 100)
    
    metodos_pago = df.groupby('metodo').agg({
        'totalfact': ['sum', 'count', 'mean'],
        'total': 'sum'
    }).round(2)
    metodos_pago.columns = ['Total_Facturado', 'Num_Transacciones', 'Ticket_Promedio', 'Total_Items']
    metodos_pago = metodos_pago.sort_values('Total_Facturado', ascending=False)
    metodos_pago['%_del_Total'] = (metodos_pago['Total_Facturado'] / metodos_pago['Total_Facturado'].sum() * 100).round(2)
    metodos_pago['%_Transacciones'] = (metodos_pago['Num_Transacciones'] / metodos_pago['Num_Transacciones'].sum() * 100).round(2)
    
    print("\n💳 DISTRIBUCIÓN POR MÉTODO DE PAGO:")
    print(metodos_pago.to_string())
    
    # Tendencias de métodos de pago por mes
    metodos_tendencia = df.groupby(['año', 'mes', 'metodo']).agg({
        'totalfact': 'sum'
    }).reset_index()
    metodos_tendencia_pivot = metodos_tendencia.pivot_table(
        index=['año', 'mes'],
        columns='metodo',
        values='totalfact',
        fill_value=0
    ).round(2)
    
    print("\n📈 TENDENCIA DE MÉTODOS DE PAGO POR MES:")
    print(metodos_tendencia_pivot.tail(12).to_string())
    
    # ========================================================================
    # 6. ANÁLISIS DE CORRELACIONES Y PREDICCIONES
    # ========================================================================
    print("\n" + "=" * 100)
    print("6️⃣ ANÁLISIS DE CORRELACIONES Y PREDICCIONES")
    print("=" * 100)
    
    # 6.1 Correlación: Ventas de mañana vs resto del día
    print("\n🔮 6.1 CORRELACIÓN: VENTAS DE MAÑANA vs RESTO DEL DÍA")
    print("-" * 100)
    
    ventas_manana = df[df['hora_solo'].between(6, 11)].groupby('fecha').agg({
        'totalfact': 'sum',
        'cantidad': 'sum'
    })
    ventas_manana.columns = ['Total_Manana', 'Cantidad_Manana']
    
    ventas_resto = df[~df['hora_solo'].between(6, 11)].groupby('fecha').agg({
        'totalfact': 'sum',
        'cantidad': 'sum'
    })
    ventas_resto.columns = ['Total_Resto', 'Cantidad_Resto']
    
    analisis_diario = ventas_manana.join(ventas_resto, how='outer').fillna(0)
    correlacion = analisis_diario[['Total_Manana', 'Total_Resto']].corr().iloc[0, 1]
    
    print(f"\n📊 CORRELACIÓN entre ventas de mañana (6-11h) y resto del día: {correlacion:.3f}")
    
    if correlacion > 0.6:
        print("   ✅ ALTA CORRELACIÓN: Las ventas de la mañana son excelente predictor del resto del día")
        print("   💡 RECOMENDACIÓN: Usar ventas de mañana para predecir el día completo")
    elif correlacion > 0.4:
        print("   ⚠️ CORRELACIÓN MODERADA: Hay relación entre mañana y resto del día")
        print("   💡 RECOMENDACIÓN: Considerar ventas de mañana como indicador parcial")
    else:
        print("   ❌ BAJA CORRELACIÓN: Las ventas de la mañana no predicen bien el resto del día")
        print("   💡 RECOMENDACIÓN: Usar otros factores (día de semana, temporada) para predicción")
    
    # Análisis detallado
    umbral_alto = analisis_diario['Total_Manana'].quantile(0.75)
    umbral_bajo = analisis_diario['Total_Manana'].quantile(0.25)
    
    dias_alta_manana = analisis_diario[analisis_diario['Total_Manana'] >= umbral_alto]
    dias_baja_manana = analisis_diario[analisis_diario['Total_Manana'] <= umbral_bajo]
    
    if len(dias_alta_manana) > 0 and len(dias_baja_manana) > 0:
        promedio_resto_alta = dias_alta_manana['Total_Resto'].mean()
        promedio_resto_baja = dias_baja_manana['Total_Resto'].mean()
        promedio_resto_general = analisis_diario['Total_Resto'].mean()
        
        print(f"\n📈 COMPORTAMIENTO:")
        print(f"   Días con ventas ALTAS en mañana (>{umbral_alto:.2f}):")
        print(f"   - Promedio resto del día: ${promedio_resto_alta:,.2f}")
        print(f"   - Diferencia vs promedio: ${promedio_resto_alta - promedio_resto_general:,.2f} ({((promedio_resto_alta/promedio_resto_general - 1) * 100):.1f}%)")
        print(f"\n   Días con ventas BAJAS en mañana (<{umbral_bajo:.2f}):")
        print(f"   - Promedio resto del día: ${promedio_resto_baja:,.2f}")
        print(f"   - Diferencia vs promedio: ${promedio_resto_baja - promedio_resto_general:,.2f} ({((promedio_resto_baja/promedio_resto_general - 1) * 100):.1f}%)")
    
    # 6.2 Predictibilidad por día de la semana
    print("\n🎯 6.2 PREDICTIBILIDAD POR DÍA DE LA SEMANA")
    print("-" * 100)
    
    ventas_diarias = df.groupby(['fecha', 'dia_semana']).agg({
        'totalfact': 'sum'
    }).reset_index()
    
    predictibilidad = ventas_diarias.groupby('dia_semana').agg({
        'totalfact': ['mean', 'std', 'min', 'max']
    }).round(2)
    predictibilidad.columns = ['Promedio', 'Desviacion', 'Min', 'Max']
    predictibilidad = predictibilidad.reindex(orden_dias)
    predictibilidad['Coef_Variacion'] = (predictibilidad['Desviacion'] / predictibilidad['Promedio'] * 100).round(2)
    predictibilidad['Rango'] = predictibilidad['Max'] - predictibilidad['Min']
    
    print("\n📊 PREDICTIBILIDAD POR DÍA:")
    print(predictibilidad.to_string())
    
    print("\n🎯 NIVEL DE PREDICTIBILIDAD:")
    for dia in orden_dias:
        cv = predictibilidad.loc[dia, 'Coef_Variacion']
        if cv < 25:
            nivel = "✅ MUY PREDECIBLE"
        elif cv < 40:
            nivel = "⚠️ MODERADAMENTE PREDECIBLE"
        else:
            nivel = "❌ VARIABLE"
        print(f"   {dia}: CV={cv:.1f}% - {nivel}")
    
    # ========================================================================
    # 7. ANÁLISIS DE TICKET PROMEDIO
    # ========================================================================
    print("\n" + "=" * 100)
    print("7️⃣ ANÁLISIS DE TICKET PROMEDIO")
    print("=" * 100)
    
    # Ticket promedio por diferentes dimensiones
    facturas_unicas = df.groupby(['fecha', 'id']).agg({
        'totalfact': 'first',
        'hora_solo': 'first',
        'dia_semana': 'first',
        'metodo': 'first',
        'vendedor': 'first',
        'cliente': 'first',
        'cantidad': 'sum'
    }).reset_index()
    
    ticket_por_hora = facturas_unicas.groupby('hora_solo')['totalfact'].agg(['mean', 'median', 'std', 'count']).round(2)
    ticket_por_hora.columns = ['Ticket_Promedio', 'Ticket_Mediana', 'Desviacion', 'Num_Facturas']
    ticket_por_hora = ticket_por_hora.sort_values('Ticket_Promedio', ascending=False)
    
    print("\n💰 TICKET PROMEDIO POR HORA:")
    print(ticket_por_hora.head(15).to_string())
    
    ticket_por_dia = facturas_unicas.groupby('dia_semana')['totalfact'].agg(['mean', 'median', 'std']).round(2)
    ticket_por_dia.columns = ['Ticket_Promedio', 'Ticket_Mediana', 'Desviacion']
    ticket_por_dia = ticket_por_dia.reindex(orden_dias)
    
    print("\n💰 TICKET PROMEDIO POR DÍA DE LA SEMANA:")
    print(ticket_por_dia.to_string())
    
    ticket_por_metodo = facturas_unicas.groupby('metodo')['totalfact'].agg(['mean', 'median', 'count']).round(2)
    ticket_por_metodo.columns = ['Ticket_Promedio', 'Ticket_Mediana', 'Num_Facturas']
    ticket_por_metodo = ticket_por_metodo.sort_values('Ticket_Promedio', ascending=False)
    
    print("\n💰 TICKET PROMEDIO POR MÉTODO DE PAGO:")
    print(ticket_por_metodo.to_string())
    
    # ========================================================================
    # 8. ANÁLISIS DE ESTACIONALIDAD Y TENDENCIAS
    # ========================================================================
    print("\n" + "=" * 100)
    print("8️⃣ ANÁLISIS DE ESTACIONALIDAD Y TENDENCIAS")
    print("=" * 100)
    
    # Tendencia mensual
    ventas_mensuales = df.groupby(['año', 'mes'])['totalfact'].sum().reset_index()
    ventas_mensuales['Fecha'] = pd.to_datetime({
        'year': ventas_mensuales['año'],
        'month': ventas_mensuales['mes'],
        'day': 1
    })
    ventas_mensuales = ventas_mensuales.sort_values('Fecha')
    
    if len(ventas_mensuales) > 1:
        ventas_mensuales['Variacion_Mensual'] = ventas_mensuales['totalfact'].pct_change() * 100
        ventas_mensuales['Variacion_Mensual'] = ventas_mensuales['Variacion_Mensual'].round(2)
        
        print("\n📈 TENDENCIA MENSUAL:")
        print(ventas_mensuales[['Fecha', 'totalfact', 'Variacion_Mensual']].to_string())
        
        # Crecimiento promedio
        crecimiento_promedio = ventas_mensuales['Variacion_Mensual'].mean()
        print(f"\n📊 CRECIMIENTO MENSUAL PROMEDIO: {crecimiento_promedio:.2f}%")
        
        if crecimiento_promedio > 5:
            print("   ✅ TENDENCIA CRECIENTE FUERTE")
        elif crecimiento_promedio > 0:
            print("   ⚠️ TENDENCIA CRECIENTE MODERADA")
        elif crecimiento_promedio > -5:
            print("   ⚠️ TENDENCIA ESTABLE/DECRECIENTE LEVE")
        else:
            print("   ❌ TENDENCIA DECRECIENTE")
    
    # Análisis por día del mes (para identificar patrones de quincena)
    df['dia_mes'] = df['fecha_dt'].dt.day
    ventas_por_dia_mes = df.groupby('dia_mes')['totalfact'].agg(['sum', 'mean', 'count']).round(2)
    ventas_por_dia_mes.columns = ['Total', 'Promedio', 'Num_Dias']
    
    print("\n📅 VENTAS POR DÍA DEL MES (identificar patrones de quincena):")
    print(ventas_por_dia_mes.to_string())
    
    # Comparar primera vs segunda quincena
    primera_quincena = df[df['dia_mes'] <= 15]['totalfact'].sum()
    segunda_quincena = df[df['dia_mes'] > 15]['totalfact'].sum()
    total_mes = primera_quincena + segunda_quincena
    
    print(f"\n📊 COMPARACIÓN QUINCENAS:")
    print(f"   Primera quincena (1-15): ${primera_quincena:,.2f} ({(primera_quincena/total_mes*100):.1f}%)")
    print(f"   Segunda quincena (16-31): ${segunda_quincena:,.2f} ({(segunda_quincena/total_mes*100):.1f}%)")
    
    # ========================================================================
    # 9. INSIGHTS Y RECOMENDACIONES ESTRATÉGICAS
    # ========================================================================
    print("\n" + "=" * 100)
    print("9️⃣ INSIGHTS Y RECOMENDACIONES ESTRATÉGICAS")
    print("=" * 100)
    
    print("\n💡 INSIGHTS CLAVE PARA RETAIL DE TECNOLOGÍA:")
    print("-" * 100)
    
    # Insight 1: Horario de atención
    print("\n1️⃣ HORARIO DE ATENCIÓN ÓPTIMO:")
    print(f"   ⏰ Horario recomendado: {hora_inicio_80:02d}:00 - {hora_fin_80:02d}:00")
    print(f"   📊 Este horario cubre el 80% de las ventas")
    print(f"   💰 Valor potencial: ${ventas_por_hora.loc[ventas_por_hora.index.isin(range(hora_inicio_80, hora_fin_80+1)), 'Total_Facturado'].sum():,.2f}")
    
    # Insight 2: Días críticos
    print("\n2️⃣ DÍAS CRÍTICOS PARA OPERACIÓN:")
    print(f"   🏆 Mejor día: {mejor_dia} - ${ventas_por_dia.loc[mejor_dia, 'Total_Facturado']:,.2f}")
    print(f"   📉 Día más débil: {peor_dia} - ${ventas_por_dia.loc[peor_dia, 'Total_Facturado']:,.2f}")
    print(f"   💡 Diferencia: ${ventas_por_dia.loc[mejor_dia, 'Total_Facturado'] - ventas_por_dia.loc[peor_dia, 'Total_Facturado']:,.2f}")
    print(f"   📊 Oportunidad: Mejorar {peor_dia} podría incrementar ventas significativamente")
    
    # Insight 3: Concentración de productos
    print("\n3️⃣ ESTRATEGIA DE INVENTARIO:")
    print(f"   📦 Top 20 productos representan {top_20_pct:.1f}% de las ventas")
    print(f"   💡 RECOMENDACIÓN: Enfocar gestión de inventario en estos productos")
    print(f"   ⚠️ {len(productos_baja_rotacion)} productos con baja rotación")
    print(f"   💰 Valor estancado: ${productos_baja_rotacion['Total_Ventas'].sum():,.2f}")
    print(f"   💡 RECOMENDACIÓN: Revisar estrategia de precios/promociones para productos estancados")
    
    # Insight 4: Clientes
    print("\n4️⃣ ESTRATEGIA DE CLIENTES:")
    print(f"   👥 Top 20 clientes representan {top_20_clientes_pct:.1f}% de las ventas")
    print(f"   💡 RECOMENDACIÓN: Programa de fidelización para clientes VIP")
    print(f"   ⚠️ {len(clientes_riesgo)} clientes en riesgo (no compran >90 días)")
    print(f"   💰 Valor potencial: ${clientes_riesgo['Total_Compras'].sum():,.2f}")
    print(f"   💡 RECOMENDACIÓN: Campaña de reactivación para clientes en riesgo")
    
    # Insight 5: Vendedores
    print("\n5️⃣ GESTIÓN DE VENDEDORES:")
    mejor_vendedor = vendedores_analisis.index[0]
    peor_vendedor = vendedores_analisis.index[-1]
    print(f"   🏆 Mejor vendedor: {mejor_vendedor} - ${vendedores_analisis.loc[mejor_vendedor, 'Total_Ventas']:,.2f}")
    print(f"   📉 Vendedor con menor performance: {peor_vendedor} - ${vendedores_analisis.loc[peor_vendedor, 'Total_Ventas']:,.2f}")
    print(f"   💡 RECOMENDACIÓN: Capacitación y mentoría del mejor vendedor a otros")
    
    # Insight 6: Métodos de pago
    metodo_principal = metodos_pago.index[0]
    print(f"\n6️⃣ MÉTODOS DE PAGO:")
    print(f"   💳 Método principal: {metodo_principal} ({metodos_pago.loc[metodo_principal, '%_del_Total']:.1f}% del total)")
    print(f"   💡 RECOMENDACIÓN: Optimizar proceso para método más usado")
    
    # Insight 7: Predictibilidad
    print("\n7️⃣ PREDICCIÓN Y PLANIFICACIÓN:")
    if correlacion > 0.5:
        print(f"   ✅ Alta correlación mañana-resto del día ({correlacion:.2f})")
        print(f"   💡 RECOMENDACIÓN: Usar ventas de mañana para ajustar personal y stock durante el día")
    
    dia_mas_predecible = predictibilidad['Coef_Variacion'].idxmin()
    cv_dia_predecible = predictibilidad.loc[dia_mas_predecible, 'Coef_Variacion']
    promedio_dia_predecible = predictibilidad.loc[dia_mas_predecible, 'Promedio']
    
    print(f"   📊 Día más predecible: {dia_mas_predecible} (CV={cv_dia_predecible:.1f}%)")
    print(f"   💡 RECOMENDACIÓN: Usar este día como referencia para planificación")
    
    # Explicación detallada sobre qué significa usar Monday como día de referencia
    print("\n" + "=" * 100)
    print("📚 EXPLICACIÓN: ¿QUÉ SIGNIFICA USAR 'MONDAY' COMO DÍA DE REFERENCIA?")
    print("=" * 100)
    print(f"\nEl análisis identificó que {dia_mas_predecible} es el día más predecible (menor variabilidad)")
    print(f"con un Coeficiente de Variación (CV) de {cv_dia_predecible:.1f}%.")
    print(f"\n📊 INTERPRETACIÓN DEL COEFICIENTE DE VARIACIÓN:")
    print(f"   - CV < 30%: MUY PREDECIBLE (ventas muy consistentes)")
    print(f"   - CV 30-50%: MODERADAMENTE PREDECIBLE (ventas relativamente consistentes)")
    print(f"   - CV > 50%: VARIABLE (ventas impredecibles)")
    print(f"\n💡 ¿QUÉ SIGNIFICA USAR {dia_mas_predecible} COMO DÍA DE REFERENCIA?")
    print(f"\n1. PLANIFICACIÓN DE INVENTARIO:")
    print(f"   → Basar las proyecciones de stock en el patrón de ventas de {dia_mas_predecible}")
    print(f"   → Si {dia_mas_predecible} tiene ventas promedio de ${promedio_dia_predecible:,.2f}")
    print(f"   → Puedes usar este valor como línea base para planificar compras y reposición")
    print(f"\n2. ASIGNACIÓN DE PERSONAL:")
    print(f"   → Programar el personal necesario basado en la demanda típica de {dia_mas_predecible}")
    print(f"   → Como es más predecible, puedes calcular mejor cuántos vendedores necesitas")
    print(f"\n3. PROYECCIONES Y PRESUPUESTOS:")
    print(f"   → Usar el promedio de {dia_mas_predecible} (${promedio_dia_predecible:,.2f}) como referencia")
    print(f"   → Multiplicar por la frecuencia del día para estimar ventas mensuales/anuales")
    print(f"   → Ejemplo: Si {dia_mas_predecible} ocurre ~4 veces al mes:")
    print(f"     Proyección mensual = ${promedio_dia_predecible:,.2f} × 4 = ${promedio_dia_predecible * 4:,.2f}")
    print(f"\n4. DETECCIÓN DE ANOMALÍAS:")
    print(f"   → Comparar ventas reales de {dia_mas_predecible} con el promedio histórico")
    print(f"   → Si las ventas se desvían significativamente, investigar causas:")
    print(f"     * Promociones especiales")
    print(f"     * Eventos externos")
    print(f"     * Cambios en el mercado")
    print(f"     * Problemas operativos")
    print(f"\n5. BENCHMARK PARA OTROS DÍAS:")
    print(f"   → Usar {dia_mas_predecible} como punto de comparación para otros días")
    print(f"   → Si otro día tiene ventas muy diferentes, analizar por qué")
    print(f"   → Identificar oportunidades de mejora en días menos predecibles")
    print(f"\n⚠️ IMPORTANTE:")
    print(f"   - El CV de {cv_dia_predecible:.1f}% indica que {dia_mas_predecible} es {'MUY PREDECIBLE' if cv_dia_predecible < 30 else 'MODERADAMENTE PREDECIBLE' if cv_dia_predecible < 50 else 'VARIABLE'}")
    print(f"   - Aún así, siempre considera factores estacionales, promociones y eventos especiales")
    print(f"   - Combina esta referencia con análisis de tendencias y factores externos")
    
    # ========================================================================
    # 10. MÉTRICAS CLAVE DE NEGOCIO (KPIs)
    # ========================================================================
    print("\n" + "=" * 100)
    print("🔟 MÉTRICAS CLAVE DE NEGOCIO (KPIs)")
    print("=" * 100)
    
    total_ventas = df['totalfact'].sum()
    total_transacciones = df.groupby(['fecha', 'id']).ngroups
    total_items = len(df)
    total_unidades = df['cantidad'].sum()
    ticket_promedio = df.groupby(['fecha', 'id'])['totalfact'].first().mean()
    items_por_factura = df.groupby(['fecha', 'id']).size().mean()
    
    dias_totales = (df['fecha_dt'].max() - df['fecha_dt'].min()).days + 1
    dias_activos = df['fecha'].nunique()
    
    print(f"\n📊 MÉTRICAS GENERALES:")
    print(f"   💰 Total facturado: ${total_ventas:,.2f}")
    print(f"   🧾 Total de facturas: {total_transacciones:,}")
    print(f"   📦 Total de items vendidos: {total_items:,}")
    print(f"   📊 Total de unidades: {total_unidades:,}")
    print(f"   💵 Ticket promedio: ${ticket_promedio:,.2f}")
    print(f"   📦 Items por factura promedio: {items_por_factura:.2f}")
    print(f"   📅 Días activos: {dias_activos} de {dias_totales} días ({dias_activos/dias_totales*100:.1f}%)")
    print(f"   💰 Ventas promedio diaria: ${total_ventas/dias_activos:,.2f}")
    print(f"   🧾 Facturas promedio diaria: {total_transacciones/dias_activos:.1f}")
    
    # Tasa de conversión (si hay datos de visitas, usar estimación)
    print(f"\n📈 MÉTRICAS DE EFICIENCIA:")
    print(f"   💵 Valor promedio por item: ${df['precio'].mean():,.2f}")
    print(f"   📦 Unidades promedio por transacción: {total_unidades/total_transacciones:.2f}")
    
    # ========================================================================
    # RESUMEN EJECUTIVO
    # ========================================================================
    print("\n" + "=" * 100)
    print("📋 RESUMEN EJECUTIVO - ACCIONES PRIORITARIAS")
    print("=" * 100)
    
    print("\n🎯 ACCIONES PRIORITARIAS PARA MAXIMIZAR VALOR:")
    print("-" * 100)
    
    print("\n1. ⏰ OPTIMIZACIÓN DE HORARIOS:")
    print(f"   → Implementar horario {hora_inicio_80:02d}:00 - {hora_fin_80:02d}:00 como horario principal")
    print(f"   → Considerar horario extendido {hora_inicio_90:02d}:00 - {hora_fin_90:02d}:00 para cubrir 90% de ventas")
    
    print("\n2. 📦 GESTIÓN DE INVENTARIO:")
    print(f"   → Priorizar stock de top 20 productos ({top_20_pct:.1f}% de ventas)")
    print(f"   → Revisar estrategia para {len(productos_baja_rotacion)} productos con baja rotación")
    print(f"   → Oportunidad: ${productos_baja_rotacion['Total_Ventas'].sum():,.2f} en productos estancados")
    
    print("\n3. 👥 PROGRAMA DE CLIENTES:")
    print(f"   → Crear programa VIP para top 20 clientes ({top_20_clientes_pct:.1f}% de ventas)")
    print(f"   → Campaña de reactivación para {len(clientes_riesgo)} clientes en riesgo")
    print(f"   → Potencial de recuperación: ${clientes_riesgo['Total_Compras'].sum():,.2f}")
    
    print("\n4. 👤 DESARROLLO DE EQUIPO:")
    print(f"   → Capacitación basada en mejores prácticas de {mejor_vendedor}")
    print(f"   → Mentoría para mejorar performance de vendedores con menor rendimiento")
    
    print("\n5. 📊 PREDICCIÓN Y PLANIFICACIÓN:")
    if correlacion > 0.5:
        print(f"   → Implementar sistema de predicción basado en ventas de mañana")
        print(f"   → Ajustar personal y stock durante el día según ventas matutinas")
    print(f"   → Usar {dia_mas_predecible} como día de referencia para planificación")
    
    print("\n6. 💳 OPTIMIZACIÓN DE PAGOS:")
    print(f"   → Optimizar proceso de {metodo_principal} (método más usado)")
    print(f"   → Considerar incentivos para métodos de pago con mayor ticket promedio")
    
    print("\n" + "=" * 100)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 100)
    print(f"\n📊 Reporte generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
