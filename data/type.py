from dataclasses import dataclass

@dataclass
class CatalogItem:
    """Represents an item in the catalog."""

    sku_id: str
    name: str
    brand: str
    category: str
    price_paise: int
    gst_rate_percent: int
    stock: int
    description: str