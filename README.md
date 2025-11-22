# Cron Job - ETL Automatizado para Alegra

Sistema automatizado de ETL que extrae datos de Alegra y los procesa diariamente a las 2:00 AM.

## 📋 Descripción

Este proyecto contiene un sistema de cron job que ejecuta automáticamente un proceso ETL (Extract, Transform, Load) para:

1. Extraer facturas de ventas de Alegra
2. Extraer facturas de proveedor de Alegra
3. Extraer ítems/inventario de Alegra
4. Generar reportes de ventas de 30 días
5. Generar tabla para pedidos

## 🚀 Características

- ✅ Ejecución automática diaria a las 2:00 AM
- ✅ Configurado para Railway
- ✅ Logging detallado
- ✅ Manejo de errores robusto
- ✅ Reinicio automático en caso de fallos

## 📁 Estructura del Proyecto

```
cron-job/
├── main.py                          # Script principal que orquesta el ETL
├── cron_runner.py                   # Runner del cron job (ejecuta main.py diariamente)
├── generar_reporte_ventas_30dias.py # Generador de reportes de ventas
├── generar_tabla_para_pedidos.py   # Generador de tabla para pedidos
├── requirements.txt                 # Dependencias Python
├── railway-cron.json               # Configuración de Railway para el cron job
├── Procfile.cron                   # Procfile para Railway
├── runtime.txt                     # Versión de Python
├── README.md                       # Este archivo
├── README_CRON.md                  # Documentación detallada del cron job
└── README_RAILWAY.md               # Guía de despliegue en Railway
```

## ⚙️ Configuración

### Variables de Entorno Requeridas

- `DATABASE_URL` - URL de conexión a PostgreSQL
- `ALEGRA_API_KEY` - Clave API de Alegra (si es necesaria)

### Horario de Ejecución

El cron job está configurado para ejecutarse **todos los días a las 2:00 AM** (hora del servidor).

Para cambiar el horario, modifica las variables en `cron_runner.py`:
```python
CRON_HOUR = 2  # Hora (0-23)
CRON_MINUTE = 0  # Minuto (0-59)
```

## 🚢 Despliegue en Railway

### Pasos Rápidos

1. **Crear un nuevo servicio en Railway:**
   - Haz clic en "New" → "GitHub Repo"
   - Selecciona el repositorio `jupabego97/cron-job`

2. **Configurar el servicio:**
   - El archivo `railway-cron.json` ya está configurado
   - Start Command: `python cron_runner.py`
   - Restart Policy: `ON_FAILURE`

3. **Configurar variables de entorno:**
   - Agrega `DATABASE_URL` y otras variables necesarias
   - Puedes compartir variables entre servicios en Railway

4. **Verificar:**
   - Revisa los logs en Railway para confirmar que el servicio está corriendo
   - El cron ejecutará `main.py` todos los días a las 2:00 AM

Para más detalles, consulta [README_CRON.md](README_CRON.md) y [README_RAILWAY.md](README_RAILWAY.md).

## 📦 Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/jupabego97/cron-job.git
cd cron-job

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar manualmente
python main.py

# O ejecutar el cron runner (para pruebas)
python cron_runner.py
```

## 📝 Scripts Principales

### main.py
Script principal que ejecuta todos los extractores en secuencia:
1. `extractor_facturas_alegra_sagrado.py` - Facturas de ventas
2. `extractor_facturas_proveedor_optimizado.py` - Facturas de proveedor
3. `items-extract.py` - Ítems/inventario
4. `generar_reporte_ventas_30dias.py` - Reporte de ventas
5. `generar_tabla_para_pedidos.py` - Tabla para pedidos

### cron_runner.py
Runner del cron job que:
- Ejecuta `main.py` todos los días a las 2:00 AM
- Maneja errores y reinicios
- Proporciona logging detallado

## 🔍 Monitoreo

Los logs están disponibles en:
- **Railway:** Pestaña "Deployments" → Logs del servicio
- **Local:** Salida estándar con formato estructurado

## 🛠️ Solución de Problemas

### El cron no se ejecuta
1. Verifica que el servicio esté activo en Railway
2. Revisa los logs del servicio
3. Confirma que las variables de entorno estén configuradas
4. Verifica que `main.py` se ejecute correctamente manualmente

### Errores en la ejecución
1. Revisa los logs detallados en Railway
2. Verifica que todas las dependencias estén instaladas
3. Confirma que la base de datos esté accesible
4. Verifica que las credenciales de Alegra sean válidas

## 📚 Documentación Adicional

- [README_CRON.md](README_CRON.md) - Documentación detallada del cron job
- [README_RAILWAY.md](README_RAILWAY.md) - Guía de despliegue en Railway
- [README_ANALISTA.md](README_ANALISTA.md) - Documentación para analistas

## 📄 Licencia

Este proyecto es privado.

## 👤 Autor

jupabego97

