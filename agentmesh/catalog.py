import json
from pathlib import Path
from data.type import CatalogItem

def load_catalog(path)-> list[CatalogItem] | None:
    catalogPath = Path(path)
    if catalogPath.exists():
        with catalogPath.open('r') as file:
            catalog = json.load(file)
            return [CatalogItem(**item) for item in catalog]
    return None

def find_product(catalog: list[CatalogItem], sku_id: str) -> CatalogItem | None:
    for item in catalog:
        if item.sku_id == sku_id:
            return item
    return None

def search_products(catalog: list[CatalogItem], query: str, limit: int = 5) -> list[CatalogItem]:
    import re
    query_words = re.findall(r"[a-z0-9]+", query.lower()) 
    # you can use str.split() to split the query into words, 
    # but it may not handle punctuation and special characters as effectively as regex. 
    # For example, query.lower().split() would split on whitespace, but it wouldn't remove punctuation. 
    # Using regex allows for more precise control over what constitutes a "word" in the search context.
    scored_products = []
    for item in catalog:
        score = sum(1 for word in query_words if word in item.name.lower() or word in item.brand.lower() or word in item.category.lower() or word in item.description.lower())
        if score > 0:
            scored_products.append((score, item))
    scored_products.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored_products[:limit]]

# Can we do search_products in any other way or is this the best way to do it?
# Ans: The current implementation of `search_products` is a straightforward and effective way to search through the catalog based on the query. It uses regex to extract words from the query and scores each product based on how many of those words appear in the product's attributes (name, brand, category, description).
# However, there are alternative approaches that could be considered depending on the requirements and scale of the application:
# 1. **Inverted Index**: For larger catalogs, building an inverted index could significantly speed up search queries. 
#    An inverted index maps each word to the list of products that contain that word, allowing for faster lookups.
# 2. **Full-Text Search Libraries**: Using libraries like Whoosh, Elasticsearch, 
#    or Solr can provide more advanced search capabilities, including ranking, stemming, and handling synonyms.
