from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.users.dependencies import get_current_user
from app.exceptions import raise_http_exception
from app.users.models import Users
from app.variations.dao import VariationDAO
from app.variations.exceptions import (
    VariationNotFoundException,
    VariationsNotFoundException,
)
from app.variations.schemas import (
    SVariation,
    SVariationCreate,
    SVariationCreateOptional,
    SVariations,
    SVariationWithCategoryAndOptions,
)

router = APIRouter(prefix="/variations", tags=["Variations"])


@router.post(
    "",
    response_model=SVariation,
    name="Add variation to the category.",
    description="Creates a new variation in the specified category.",
)
async def create_variation(
    variation_data: SVariationCreate,
    user: Users = Depends(get_current_user),
):
    variation = await VariationDAO.add(user, variation_data)
    if not variation:
        raise_http_exception(VariationNotFoundException)
    return variation


@router.get(
    "",
    name="Get all variations.",
    response_model=SVariations,
    description="Retrieves all variations in the system.",
)
async def get_all_variations():
    variations = await VariationDAO.find_all()
    if not variations:
        raise_http_exception(VariationsNotFoundException)
    return {"variations": variations}


@router.get(
    "/{variation_id}",
    name="Get certain variation.",
    response_model=SVariationWithCategoryAndOptions,
    description="Fetches a specific variation by its ID.",
)
async def get_variation_by_id(variation_id: UUID):
    variation = await VariationDAO.find_by_id(variation_id)
    if not variation:
        raise_http_exception(VariationNotFoundException)
    return variation


@router.patch(
    "/{variation_id}",
    response_model=SVariation,
    response_model_exclude_none=True,
    name="Change certain variation.",
    description="Updates an existing variation with the provided data.",
)
async def change_variation_by_id(
    variation_id: UUID,
    data: SVariationCreateOptional,
    user: Users = Depends(get_current_user),
):
    variation = await VariationDAO.change(variation_id, user, data)
    if not variation:
        raise_http_exception(VariationNotFoundException)
    return variation


@router.delete(
    "/{variation_id}",
    name="Delete certain variation.",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deletes a variation by its ID.",
)
async def delete_variation_by_id(
    variation_id: UUID,
    user: Users = Depends(get_current_user),
):
    variation = await VariationDAO.delete(user, variation_id)
    if not variation:
        raise_http_exception(VariationNotFoundException)
