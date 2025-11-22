#!/usr/bin/env python3
"""
Cron Runner para ejecutar main.py periódicamente
-------------------------------------------------

Este script está diseñado para ejecutarse como un servicio de cron en Railway.
Ejecuta main.py todos los días a las 2:00 AM usando schedule.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Intentar importar schedule, si no está disponible, usar time.sleep
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    logging.warning("schedule no está disponible. Instala con: pip install schedule")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Configuración de horario
CRON_HOUR = 2  # 2 AM
CRON_MINUTE = 0  # Minuto 0
SCRIPT_NAME = "main.py"


def run_main_script():
    """Ejecuta el script main.py."""
    script_dir = Path(__file__).resolve().parent
    script_path = script_dir / SCRIPT_NAME
    
    if not script_path.exists():
        logger.error(f"❌ No se encontró el script {script_path}")
        return False
    
    logger.info(f"🚀 Ejecutando {SCRIPT_NAME}...")
    start_time = datetime.now()
    
    try:
        # Ejecutar el script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(script_dir),
            capture_output=False,
            text=True,
            check=True
        )
        
        duration = datetime.now() - start_time
        logger.info(f"✅ {SCRIPT_NAME} ejecutado exitosamente en {duration}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error ejecutando {SCRIPT_NAME}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        return False


def main():
    """Función principal del cron runner."""
    logger.info("=" * 60)
    logger.info(f"🔄 Iniciando Cron Runner para ejecutar main.py todos los días a las {CRON_HOUR:02d}:{CRON_MINUTE:02d}")
    logger.info("=" * 60)
    
    # Calcular próxima ejecución
    now = datetime.now()
    next_run = now.replace(hour=CRON_HOUR, minute=CRON_MINUTE, second=0, microsecond=0)
    
    # Si ya pasó la hora de hoy, programar para mañana
    if next_run <= now:
        next_run += timedelta(days=1)
    
    logger.info(f"⏰ Próxima ejecución programada para: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if SCHEDULE_AVAILABLE:
        # Usar schedule para programar ejecuciones diarias a las 2 AM
        schedule.every().day.at(f"{CRON_HOUR:02d}:{CRON_MINUTE:02d}").do(run_main_script)
        
        logger.info("⏰ Servicio de cron iniciado. Esperando próximas ejecuciones...")
        logger.info(f"📅 Ejecutará {SCRIPT_NAME} todos los días a las {CRON_HOUR:02d}:{CRON_MINUTE:02d}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto para mayor precisión
    else:
        # Fallback: usar time.sleep con cálculo de tiempo hasta las 2 AM
        logger.warning("⚠️ schedule no disponible. Usando modo simple...")
        while True:
            now = datetime.now()
            next_run = now.replace(hour=CRON_HOUR, minute=CRON_MINUTE, second=0, microsecond=0)
            
            # Si ya pasó la hora de hoy, programar para mañana
            if next_run <= now:
                next_run += timedelta(days=1)
            
            wait_seconds = (next_run - now).total_seconds()
            logger.info(f"⏰ Esperando hasta {next_run.strftime('%Y-%m-%d %H:%M:%S')} ({wait_seconds/3600:.1f} horas)...")
            time.sleep(wait_seconds)
            
            logger.info(f"⏰ Ejecutando tarea programada...")
            run_main_script()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Cron runner detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)

