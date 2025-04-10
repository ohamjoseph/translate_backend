from src.core.logger import get_logger

logger = get_logger()

audit_logger = logger.bind(context="AUDIT")

def log_audit_event(message: str, email: str = ""):
    audit_logger.info(f"{message} | utilisateur: {email}")

def log_success(message: str):
    logger.success(f"{message}")

def log_warning(message: str):
    logger.warning(f"{message}")

def log_error(message: str, exception: Exception | None = None):
    if exception:
        logger.error(f"{message} | Exception: {str(exception)}")
    else:
        logger.error(f"{message}")
