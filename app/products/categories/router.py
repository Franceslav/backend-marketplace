from fastapi import APIRouter, Depends, status

from app.users.dependencies import get_current_user
from app.examples import example_product_category
from app.exceptions import raise_http_exception
from app.products.categories.dao import ProductCategoryDAO
from app.products.categories.exceptions import (
    ProductCategoriesNotFoundException,
    ProductCategoryNotFoundException,
    ProductCategoryNotImplementedException,
)

from app.products.categories.schemas import (
    SProductCategories,
    SProductCategory,
    SProductCategoryCreate,
    SProductCategoryOptional,
    SProductCategoryWithChildren,
)
from app.products.exceptions import ProductsNotFoundException
from app.users.models import Users
from app.variations.exceptions import VariationsNotFoundException
from app.variations.schemas import (
    SProductCategoryWithProducts,
    SProductCategoryWithVariations,
)


router = APIRouter(prefix="/categories")


@router.post(
    "",
    response_model=SProductCategory,
    name="Add product category.",

)
async def create_product_category(
    product_category_data: SProductCategoryCreate = example_product_category,
    user: Users = Depends(get_current_user),
):
    product_category = await ProductCategoryDAO.add(
        user, product_category_data
    )

    if not product_category:
        raise ProductCategoryNotImplementedException

    return product_category


@router.get(
    "",
    name="Get all categories.",
    response_model=SProductCategories,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Man",
                        },
                        {"id": 4, "name": "Tops", "parent_category_id": 1},
                    ]
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": {
                        "Categories not found.": {
                            "summary": "Categories not found.",
                            "value": {"detail": "Categories not found."},
                        },
                    }
                }
            }
        },
    },
)
async def get_all_categories():
    categories = await ProductCategoryDAO.find_all()

    if not categories:
        raise ProductCategoriesNotFoundException

    return {"product_categories": categories}


@router.get(
    "/{product_category_id}",
    name="Get certain product category.",
    response_model=SProductCategoryWithChildren,

)
async def get_category_by_id(product_category_id: int):
    category = await ProductCategoryDAO.find_by_id_and_children(
        product_category_id
    )

    if not category:
        raise_http_exception(ProductCategoryNotFoundException)

    return category


@router.patch(
    "/{product_category_id}",
    response_model=SProductCategory,
    response_model_exclude_none=True,
    name="Change certain product category.",

)
async def change_category_by_id(
    product_category_id: int,
    data: SProductCategoryOptional,
    user: Users = Depends(get_current_user),
):
    product_category = await ProductCategoryDAO.change(
        product_category_id, user, data
    )

    if not product_category:
        raise ProductCategoryNotFoundException

    return product_category


@router.delete(
    "/{product_category_id}",
    name="Delete certain product category.",
    status_code=status.HTTP_204_NO_CONTENT,

)
async def delete_category_by_id(
    product_category_id: int,
    user: Users = Depends(get_current_user),
):
    product_category = await ProductCategoryDAO.delete(
        user, product_category_id
    )

    if not product_category:
        return {"detail": "The product category was deleted."}


@router.get(
    "/{product_category_id}/variations",
    name="Get all variations of product category.",
    response_model=SProductCategoryWithVariations,

)
async def get_category_variations(product_category_id: int):
    category = await ProductCategoryDAO.get_product_category_variations(
        product_category_id
    )

    if not category:
        raise_http_exception(ProductCategoryNotFoundException)

    if not category.__dict__["variations"]:
        raise_http_exception(VariationsNotFoundException)

    return category


@router.get(
    "/{product_category_id}/products",
    name="Get all products of product category.",
    response_model=SProductCategoryWithProducts,

)
async def get_category_products(product_category_id: int):
    category = await ProductCategoryDAO.get_product_category_products(
        product_category_id
    )

    if not category:
        raise_http_exception(ProductCategoryNotFoundException)

    if not category.__dict__["products"]:
        raise_http_exception(ProductsNotFoundException)

    return category
