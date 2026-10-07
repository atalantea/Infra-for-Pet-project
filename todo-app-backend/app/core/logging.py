import logging


def configure_logging():
    root_logger = logging.getLogger()
    if not root_logger.handlers:  # Чтобы не навесить обработчики повторно
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            force=True,
        )

    logging.getLogger("app").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
