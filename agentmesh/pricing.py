from agentmesh.config import MAX_QUANTITY_PER_ORDER
from data.type import CatalogItem

def format_rupees(amount_paise: int) -> str:
    """Format an integer amount in paise as Indian Rupees."""
    return f"₹{amount_paise / 100:,.2f}"

def build_quote(product: CatalogItem, quantity: int) -> dict:
    """Build a quote for a given catalog item and quantity."""
    if 1 > quantity:
        raise ValueError(f"Requested quantity {quantity} is out of bounds.")
    elif quantity > MAX_QUANTITY_PER_ORDER:
        raise ValueError(f"Requested quantity {quantity} exceeds maximum allowed {MAX_QUANTITY_PER_ORDER}.")
    elif quantity > product.stock:
        raise ValueError(f"Requested quantity {quantity} exceeds available stock {product.stock}.")

    total_price_paise = product.price_paise * quantity
    gst_rate_percent = product.gst_rate_percent
    gst_numerator = total_price_paise * gst_rate_percent
    whole_paise, remainder = divmod(gst_numerator, 100)

    if remainder >= 50:
        whole_paise += 1
    gst_paise = whole_paise
    
    total_paise = total_price_paise + gst_paise

    return {
        "sku_id": product.sku_id,
        "quantity": quantity,
        "unit_price_paise": product.price_paise,
        "subtotal_paise": total_price_paise,
        "gst_rate_percent": product.gst_rate_percent,
        "gst_paise": gst_paise,
        "total_paise": total_paise,
    }
