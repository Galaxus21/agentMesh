import pytest

from agentmesh.config import MAX_QUANTITY_PER_ORDER
from data.type import CatalogItem
from agentmesh.pricing import build_quote, format_rupees


item1 = CatalogItem(
        sku_id="SKU-CHAIR-01",
        name="Ergonomic Office Chair",
        brand="ErgoMax",
        category="furniture",
        price_paise=420000,
        gst_rate_percent=18,
        stock=50,
        description="A comfortable ergonomic office chair with adjustable height and lumbar support.",
    )
item2 = CatalogItem(
        sku_id="SKU-DESK-01",
        name="Standing Desk",
        brand="DeskPro",
        category="furniture",
        price_paise=750000,
        gst_rate_percent=18,
        stock=3,
        description="A height-adjustable standing desk with a spacious work surface.",
    )


@pytest.mark.parametrize(
    ("product", "quantity", "expected_exception"),
    [
        (item2, 4, ValueError),
        (item1, 0, ValueError),
        (item1, -1, ValueError),
        (item1, MAX_QUANTITY_PER_ORDER + 1, ValueError),
    ],
)
def test_build_quote_invalid_quantity(product, quantity, expected_exception):
    with pytest.raises(expected_exception):
        build_quote(product, quantity)

@pytest.mark.parametrize(
    ("subtotal_paise", "gst_rate_percent", "expected_gst_paise"),
    [
        (420_000, 18, 75_600),  # Exact result, no rounding
        (4_999, 18, 900),       # 899.82 rounds up
        (4_997, 18, 899),       # 899.46 rounds down
        (2_475, 18, 446),       # 445.50 rounds half up
        (50_000, 0, 0),         # Zero GST rate
    ],
)
def test_build_quote_gst_rounding(
    subtotal_paise: int,
    gst_rate_percent: int,
    expected_gst_paise: int,
):
    product = CatalogItem(
        sku_id="SKU-TEST-01",
        name="Test Product",
        brand="Test Brand",
        category="test",
        price_paise=subtotal_paise,
        gst_rate_percent=gst_rate_percent,
        stock=1,
        description="Test product for GST rounding",
    )

    quote = build_quote(product, 1)

    assert quote["subtotal_paise"] == subtotal_paise
    assert quote["gst_paise"] == expected_gst_paise
    assert quote["total_paise"] == subtotal_paise + expected_gst_paise


def test_build_quote_four_keyboards():
    keyboard = CatalogItem(
        sku_id="SKU-KEYBOARD-01",
        name="Mechanical Keyboard",
        brand="KeyPro",
        category="computer accessories",
        price_paise=349_900,
        gst_rate_percent=18,
        stock=100,
        description="Mechanical keyboard for desktop computers",
    )

    quote = build_quote(keyboard, 4)

    assert quote["sku_id"] == keyboard.sku_id
    assert quote["quantity"] == 4
    assert quote["unit_price_paise"] == 349_900
    assert quote["subtotal_paise"] == 1_399_600
    assert quote["gst_rate_percent"] == 18
    assert quote["gst_paise"] == 251_928
    assert quote["total_paise"] == 1_651_528


def test_format_rupees_from_paise():
    assert format_rupees(495_600) == "₹4,956.00"
    assert format_rupees(1_234_567) == "₹12,345.67"
    assert format_rupees(0) == "₹0.00"
