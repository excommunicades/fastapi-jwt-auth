from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.pkg.db.models import (
    Products,
)


class ProductRepository:

    def __init__(self, db: Session):

        self.db = db

    def create_product(self, title: str, description: str) -> Products:

        """Create product logic"""

        try:

            db_product = Products(title=title, description=description)

            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)

            return db_product

        except SQLAlchemyError as e:

            self.db.rollback()

            raise Exception("Error creating product") from e

    def get_product(self, product_id: int) -> Products:

        """Product returning logic"""

        return self.db.query(Products).filter(Products.id == product_id).first()


    def get_product_list(self) -> list[Products]:

        """Product list returning logic"""

        return self.db.query(Products).all()

    def update_product(self, product_id: int, title: str = None, description: str = None) -> Products:

        """Update product logic"""

        db_product = self.db.query(Products).filter(Products.id == product_id).first()

        if db_product:

            if title is not None:

                db_product.title = title

            if description is not None:

                db_product.description = description

            self.db.commit()

            self.db.refresh(db_product)

            return db_product

        return None

    def delete_product(self, product_id: str) -> Products | None:

        db_product = self.db.query(Products).filter(Products.id == product_id).first()

        if db_product:

            self.db.delete(db_product)

            self.db.commit()

            return db_product

        return None