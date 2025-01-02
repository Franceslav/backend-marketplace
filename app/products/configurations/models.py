from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProductConfiguration(Base):
    __tablename__ = "configuration_product"

    product_item_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("product_items.id", ondelete="CASCADE"),
        primary_key=True,
    )

    variation_option_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("variation_options.id", ondelete="CASCADE"),
        primary_key=True,
    )
