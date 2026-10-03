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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="stdio")