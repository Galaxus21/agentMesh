from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = PROJECT_ROOT/"data"/"catalog.json"
MAX_QUANTITY_PER_ORDER = 5