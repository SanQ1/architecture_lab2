from abc import ABC, abstractmethod
from src.domain.interfaces import AbstractProductRepository, AbstractOrderRepository, AbstractUserRepository

class AbstractUnitOfWork(ABC):
    products: AbstractProductRepository
    orders: AbstractOrderRepository
    users: AbstractUserRepository

    @abstractmethod
    def __enter__(self): return self
    
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb): self.rollback()

    @abstractmethod
    def commit(self): raise NotImplementedError
    
    @abstractmethod
    def rollback(self): raise NotImplementedError
