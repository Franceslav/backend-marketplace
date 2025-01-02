from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from app.products.configurations.models import ProductConfiguration  # noqa
from app.variations.models import Variation  # noqa


class VariationOption(Base):
    __tablename__ = "variation_options"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    value: Mapped[str]
    variation_id: Mapped[UUID] = mapped_column(
        ForeignKey("variations.id", ondelete="CASCADE"), nullable=False
    )

    variation = relationship("Variation", back_populates="options")

    product_items: Mapped[list["ProductItem"]] = relationship(  # noqa
        back_populates="variations",
        secondary="configuration_product",
    )
