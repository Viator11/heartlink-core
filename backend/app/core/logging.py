import logging, structlog
from .config import get_settings

def setup_logging():
    lvl_name = get_settings().LOG_LEVEL.upper()
    lvl = getattr(logging, lvl_name, logging.INFO)
    logging.basicConfig(level=lvl)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(lvl),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )
    return structlog.get_logger()