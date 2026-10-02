from data.type import CatalogItem

catalog: list[CatalogItem] = [
    CatalogItem(
        sku_id="SKU-CHAIR-01",
        name="Ergonomic Office Chair",
        brand="ErgoMax",
        category="furniture",
        price_paise=420000,
        gst_rate_percent=18,
        stock=50,
        description="A comfortable ergonomic office chair with adjustable height and lumbar support.",
    ),
    CatalogItem(
        sku_id="SKU-DESK-01",
        name="Standing Desk",
        brand="DeskPro",
        category="furniture",
        price_paise=750000,
        gst_rate_percent=18,
        stock=30,
        description="A height-adjustable standing desk with a spacious work surface.",
    ),
    CatalogItem(
        sku_id="SKU-LAPTOP-01",
        name="Laptop Pro 15",
        brand="TechBrand",
        category="electronics",
        price_paise=1200000,
        gst_rate_percent=18,
        stock=20,
        description="A high-performance laptop with a 15-inch display and powerful processor.",
    ),
    CatalogItem(
        sku_id="SKU-MOUSE-01",
        name="Wireless Mouse",
        brand="ClickTech",
        category="electronics",
        price_paise=25000,
        gst_rate_percent=18,
        stock=100,
        description="A sleek wireless mouse with ergonomic design and long battery life.",
    ),
    CatalogItem(
        sku_id="SKU-HEADPHONES-01",
        name="Noise-Cancelling Headphones",
        brand="SoundMaster",
        category="electronics",
        price_paise=150000,
        gst_rate_percent=18,
        stock=40,
        description="Over-ear headphones with active noise cancellation and superior sound quality.",
    ),
]

from agentmesh.catalog import find_product, search_products

def test_find_product():
    # Test finding an existing product
    result = find_product(catalog, "SKU-CHAIR-01")
    assert result is not None
    assert result.sku_id == "SKU-CHAIR-01"
    assert result.name == "Ergonomic Office Chair"

    # Test finding a non-existing product
    result = find_product(catalog, "SKU-NONEXISTENT")
    assert result is None


def test_search_products():
    # Test searching for products with a common term
    results = search_products(catalog, "office")
    assert len(results) == 1
    assert results[0].sku_id == "SKU-CHAIR-01"

    # Limit the number of results returned
    results = search_products(catalog, "electronics", limit=2)
    assert len(results) <= 2

    # Test searching for products with a term that matches multiple products
    results = search_products(catalog, "electronics")
    assert len(results) == 3
    assert any(item.sku_id == "SKU-LAPTOP-01" for item in results)
    assert any(item.sku_id == "SKU-MOUSE-01" for item in results)
    assert any(item.sku_id == "SKU-HEADPHONES-01" for item in results)

    # Test searching with a term that has no matches
    results = search_products(catalog, "nonexistent")
    assert len(results) == 0

    result = search_products(catalog, "High Performance laptOP")
    assert result is not None
    assert result[0].sku_id == "SKU-LAPTOP-01"

    # A product matching two query words ranks above one matching only one
    results = search_products(catalog, "ergonomic chair")
    assert len(results) == 2
    assert results[0].sku_id == "SKU-CHAIR-01"
    assert results[1].sku_id == "SKU-MOUSE-01"

    results = search_products(catalog, "CHAIR")
    assert len(results) == 1
    assert results[0].sku_id == "SKU-CHAIR-01"

    results = search_products(catalog, "ergonomic", limit=1)
    assert len(results) == 1
    assert results[0].sku_id == "SKU-CHAIR-01"
