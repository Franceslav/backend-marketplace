from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from starlette import status

from app.users.dependencies import get_current_user
from app.exceptions import raise_http_exception
from app.products.categories.router import router as categories_router
from app.products.configurations.router import router as configurations_router
from app.products.dao import ProductDAO
from app.products.exceptions import (
    ProductNotFoundException,
    ProductsNotFoundException,
)
from app.products.items.exceptions import ProductItemsNotFoundException
from app.products.items.router import router as items_router
from app.products.items.schemas import SProductWithItems

from app.products.schemas import (
    SProduct,
    SProductCreate,
    SProductCreateOptional,
    SProducts,
    SProductWithCategory,
)
from app.users.models import Users


router = APIRouter(prefix="/products", tags=["Products"])

router.include_router(categories_router)
router.include_router(items_router)
router.include_router(configurations_router)


@router.patch(
    "/image",
    response_model=SProduct,
    name="Change product image.",

)
async def change_product_image_by_id(
    file: UploadFile = File(...),
    product_id: UUID = Form(...),
    user: Users = Depends(get_current_user),
):
    product = await ProductDAO.change_image(user, file, product_id)

    return product


@router.post(
    "",
    response_model=SProduct,
    name="Add product to the category.",

)
async def create_product(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    user: Users = Depends(get_current_user),
):
    product_data = SProductCreate(
        name=name, description=description, category_id=category_id
    )

    product = await ProductDAO.add(user, product_data, file)

    return product


@router.get(
    "",
    name="Get all products.",
    response_model=SProducts,

)
async def get_all_products():
    products = await ProductDAO.find_all()

    if not products:
        raise_http_exception(ProductsNotFoundException)

    return {"products": products}


@router.get(
    "/{product_id}",
    name="Get certain product.",
    response_model=SProductWithCategory,

)
async def get_product_by_id(product_id: UUID):
    product = await ProductDAO.find_by_id(product_id)

    if not product:
        raise_http_exception(ProductNotFoundException)

    return product


@router.get(
    "/{product_id}/product_items",
    name="Get all product items of product.",
    response_model=SProductWithItems,

)
async def get_product_product_items(product_id: UUID):
    product = await ProductDAO.get_product_product_items(product_id)

    if not product:
        raise_http_exception(ProductNotFoundException)

    if not product.__dict__["product_items"]:
        raise_http_exception(ProductItemsNotFoundException)

    return product


@router.patch(
    "/{product_id}",
    response_model=SProduct,
    response_model_exclude_none=True,
    name="Change certain product.",

)
async def change_product_by_id(
    product_id: UUID,
    data: SProductCreateOptional,
    user: Users= Depends(get_current_user),
):
    product = await ProductDAO.change(product_id, user, data)

    if not product:
        raise ProductNotFoundException

    return product


@router.delete(
    "/{product_id}",
    name="Delete certain product.",
    status_code=status.HTTP_204_NO_CONTENT,

)
async def delete_product_by_id(
    product_id: UUID,
    user: Users = Depends(get_current_user),
):
    product = await ProductDAO.delete(user, product_id)

    if not product:
        return {"detail": "The product was deleted."}
