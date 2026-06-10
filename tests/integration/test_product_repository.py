from src.infrastructure.repositories import PostgresProductRepository
from src.domain.models import Product
from src.infrastructure.models import ProductEntity 

def test_repository_save_product(db_session):
    repo = PostgresProductRepository(db_session)
    product = Product(name="Gaming Mouse", price=50.0)

    repo.add(product)
    db_session.commit()

    assert db_session.query(ProductEntity).count() == 1

    saved_entity = db_session.query(ProductEntity).first()
    assert saved_entity.name == "Gaming Mouse"
