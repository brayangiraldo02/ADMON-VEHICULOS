from fastapi import APIRouter
from controller.collection_account import get_collection_accounts, download_collection_accounts
from schemas.owners import OwnersList

collectionAccount_router = APIRouter()

@collectionAccount_router.post("/collection-accounts/", tags=["Collection Account"])
async def post_collection_accounts_route(owners_list: OwnersList):
    return await get_collection_accounts(owners_list.owners)

@collectionAccount_router.post("/collection-accounts/download", tags=["Collection Account"])
async def post_download_collection_accounts(owners_list: OwnersList):
    return await download_collection_accounts(owners_list.owners)