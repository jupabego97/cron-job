# 🤖 Analista de Negocio con IA

Aplicación Streamlit interactiva que permite hacer preguntas en lenguaje natural sobre el negocio y recibe reportes completos con análisis, tablas y visualizaciones automáticas, usando Gemini (Google AI) para interpretar las consultas.

## 🚀 Características

- **Chat Interactivo**: Haz preguntas en lenguaje natural sobre tu negocio
- **Análisis Inteligente**: Gemini interpreta tus preguntas y genera consultas SQL optimizadas
- **Visualizaciones Automáticas**: Genera gráficos automáticamente según el tipo de datos
- **Reportes Profesionales**: Respuestas con formato de analista de negocio
- **Exportación**: Descarga resultados en CSV o Excel
- **Seguridad**: Solo consultas SELECT permitidas, validación de queries

## 📋 Requisitos Previos

1. **Python 3.8+**
2. **Base de datos PostgreSQL** con las tablas:
   - `facturas` (ventas a clientes)
   - `facturas_proveedor` (compras a proveedores)
   - `items` (inventario)
3. **API Key de Google Gemini** (obtener en: https://makersuite.google.com/app/apikey)

## 🔧 Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**

Crea un archivo `.env` en la raíz del proyecto con:
```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd
GOOGLE_API_KEY=tu-api-key-de-gemini-aqui
```

O configura las variables de entorno en tu sistema:
```bash
# Windows PowerShell
$env:DATABASE_URL="postgresql://..."
$env:GOOGLE_API_KEY="tu-api-key"

# Linux/Mac
export DATABASE_URL="postgresql://..."
export GOOGLE_API_KEY="tu-api-key"
```

## 🎯 Uso

1. **Ejecutar la aplicación:**
```bash
streamlit run app_analista_negocio.py
```

2. **En el navegador:**
   - La aplicación se abrirá automáticamente en `http://localhost:8501`
   - Si no tienes la API key configurada, ingrésala en el sidebar
   - Haz preguntas en el chat sobre tu negocio

## 💡 Ejemplos de Preguntas

- "¿Cuáles son las ventas totales del último mes?"
- "¿Cuáles son los 10 productos más vendidos?"
- "¿Cuánto hemos vendido por cliente este año?"
- "¿Cuál es el margen de ganancia promedio por producto?"
- "¿Qué proveedores son los más importantes?"
- "¿Cuáles son las ventas por método de pago?"
- "¿Qué vendedor tiene mejor desempeño?"
- "¿Cuál es la tendencia de ventas mensuales?"

## 📊 Tipos de Visualizaciones

La aplicación detecta automáticamente el tipo de visualización apropiada:

- **Gráficos de Línea**: Para series temporales y tendencias
- **Gráficos de Barras**: Para comparaciones y rankings
- **Gráficos de Torta**: Para proporciones y distribuciones
- **Scatter Plots**: Para relaciones entre variables
- **Histogramas**: Para distribuciones de datos

## 🔒 Seguridad

- Solo se permiten consultas `SELECT` (sin UPDATE, DELETE, INSERT, etc.)
- Validación de queries SQL antes de ejecutar
- Sanitización de inputs del usuario
- Se recomienda usar una conexión de solo lectura a la base de datos

## 🛠️ Estructura del Código

- `app_analista_negocio.py`: Aplicación principal
- `requirements.txt`: Dependencias del proyecto
- `.env`: Variables de entorno (no incluido en el repo)

## 📝 Notas

- La primera ejecución puede tardar un poco mientras se carga el modelo de Gemini
- Las consultas complejas pueden tomar varios segundos
- El historial de conversación se mantiene durante la sesión
- Los resultados se pueden exportar en cualquier momento

## 🐛 Solución de Problemas

**Error: "LangChain no está instalado"**
```bash
pip install langchain langchain-community langchain-google-genai
```

**Error: "API Key no configurada"**
- Verifica que `GOOGLE_API_KEY` esté en el archivo `.env` o en las variables de entorno
- O ingresa la API key en el sidebar de la aplicación

**Error: "Error conectando a PostgreSQL"**
- Verifica que `DATABASE_URL` esté correctamente configurada
- Asegúrate de que la base de datos esté accesible
- Verifica credenciales y permisos

**Error: "Columna o tabla no encontrada"**
- Verifica que las tablas `facturas`, `facturas_proveedor`, `items` existan
- Revisa la ortografía de los nombres de columnas en tu pregunta
- Usa los nombres exactos de las columnas de tu base de datos

## 📚 Dependencias Principales

- `streamlit`: Framework para la interfaz web
- `langchain`: Framework para aplicaciones con LLMs
- `langchain-google-genai`: Integración con Google Gemini
- `pandas`: Manipulación de datos
- `plotly`: Visualizaciones interactivas
- `sqlalchemy`: ORM para PostgreSQL

## 📄 Licencia

Este proyecto es de uso interno.





