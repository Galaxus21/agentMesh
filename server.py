import logging
from mcp.server import MCPServer

from agentmesh.config import CATALOG_PATH
from agentmesh.catalog import load_catalog, search_products as search_catalog_products
from data.type import CatalogItem

logger = logging.getLogger("agentmesh")
mcp = MCPServer("agentmesh")
catalog = load_catalog(CATALOG_PATH)

@mcp.tool(name="searchProducts")
def search_products(query: str, limit: int = 5) -> list[CatalogItem]:
    """Search products by keywords in their name, brand, category, and description.
    Returns up to `limit` matching products, ranked by relevance.
    """
    if not catalog:
        logger.warning("Catalog is empty or not loaded.")
        return []
    logger.info("search_products query=%r limit=%d", query, limit)
    return search_catalog_products(catalog, query, limit)

# get_quote(sku_id, quantity) tool that returns the breakdown with both paise and ₹ strings. For
# expected problems (unknown SKU, bad quantity), return {"status": "refused", "reason": "..."} so
# Claude can explain the problem to the user. Let unexpected bugs raise
@mcp.tool(name="getProductQuote")
def get_quote(sku_id: str, quantity: int) -> dict:
    """Get a quote for a product by SKU ID and quantity.
    Returns a breakdown of the quote including subtotal, GST, and total in both paise and ₹ strings.
    If the SKU is unknown or the quantity is invalid, returns a refusal reason.
    """
    from agentmesh.pricing import build_quote, format_rupees
    from agentmesh.catalog import find_product

    if not catalog:
        logger.warning("Catalog is empty or not loaded.")
        return {"status": "refused", "reason": "Catalog is empty or not loaded."}

    product = find_product(catalog, sku_id)
    if not product:
        logger.warning("Unknown SKU ID: %s", sku_id)
        return {"status": "refused", "reason": f"Unknown SKU ID: {sku_id}"}
    
    quote = build_quote(product, quantity)
    # Add formatted rupee strings to the quote
    quote["unit_price"] = format_rupees(quote["unit_price_paise"])
    quote["subtotal"] = format_rupees(quote["subtotal_paise"])
    quote["gst"] = format_rupees(quote["gst_paise"])
    quote["total"] = format_rupees(quote["total_paise"])
    return quote

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="stdio")