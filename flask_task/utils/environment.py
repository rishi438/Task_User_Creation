import os

DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///:memory:")
TEMPLATES_AUTO_RELOAD = os.environ.get("TEMPLATES_AUTO_RELOAD", True)
