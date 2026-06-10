from src.domain.models import Product

def test_product_initialization():
    p = Product(name="Laptop", price=1000.0)
    assert p.name == "Laptop"
    assert p.price == 1000.0
    assert p.id is None
