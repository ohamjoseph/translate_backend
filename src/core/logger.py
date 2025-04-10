from loguru import logger
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Nettoyage et configuration
logger.remove()

# Console
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}")

# Fichier principal (tout)
logger.add(LOG_DIR / "app.log", level="DEBUG", rotation="1 MB", retention="7 days")

# Audit
logger.add(LOG_DIR / "audit.log", level="INFO", rotation="1 MB", retention="30 days", filter=lambda record: "context" in record["extra"] and record["extra"]["context"] == "AUDIT")

# Erreurs
logger.add(LOG_DIR / "errors.log", level="ERROR", rotation="500 KB", retention="15 days")

def get_logger():
    return logger
