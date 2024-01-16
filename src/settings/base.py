from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import Integer

class Base(DeclarativeBase):
    __abstract__ = True 

    __name__: str 

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically.
        """
        return f"{cls.__name__.lower()}s"
    
    # __table_args__ = {'extend_existing': False}  

    # id: Mapped[int] = mapped_column(primary_key=True)
