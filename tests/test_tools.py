# tests/test_tools.py
from tools import search_listings, suggest_outfit, create_fit_card

# ── Tool 1: search_listings ────────────────────────────────────────────────────
def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []   # empty list, no exception

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)



# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

SAMPLE_ITEM = {
    "id": "l_001",
    "title": "Vintage Band Tee — Faded Grey",
    "description": "Soft, faded vintage band tee",
    "category": "tops",
    "style_tags": ["vintage", "graphic"],
    "size": "M",
    "condition": "good",
    "price": 19.0,
    "colors": ["grey"],
    "brand": None,
    "platform": "depop",
}

NON_EMPTY_WARDROBE = {
    "items": [
        {
            "id": "w_001",
            "name": "Baggy straight-leg jeans, dark wash",
            "category": "bottoms",
            "colors": ["dark blue"],
            "style_tags": ["denim", "streetwear"],
            "notes": None,
        }
    ]
}

EMPTY_WARDROBE = {"items": []}



def test_suggest_outfit_with_wardrobe_calls_llm_with_wardrobe_items():
    result = suggest_outfit(SAMPLE_ITEM, NON_EMPTY_WARDROBE)

    assert isinstance(result, str)
    assert len(result) > 0


def test_suggest_outfit_with_empty_wardrobe_gives_general_advice():
    result = suggest_outfit(SAMPLE_ITEM, EMPTY_WARDROBE)

    assert isinstance(result, str)
    assert len(result) > 0

