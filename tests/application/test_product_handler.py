import pytest
from unittest.mock import Mock
from src.application.handlers import ProductHandler

def test_add_product_success(mock_uow):
    handler = ProductHandler(uow=mock_uow)
    
    product_id = handler.add_product(name="Laptop", price=25000.0)
    
    mock_uow.products.add.assert_called_once()
    mock_uow.commit.assert_called_once()
    
def test_list_all_products(mock_uow):
    handler = ProductHandler(uow=mock_uow)
    mock_uow.products.list.return_value = ["Product1", "Product2"]
    
    products = handler.list_all()
    
    assert len(products) == 2
    assert products[0] == "Product1"
