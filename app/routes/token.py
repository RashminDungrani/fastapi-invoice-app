from fastapi import APIRouter, Depends

# from app.routes.user.user_views import login

# * This aspects two parameters access_token and token_type,
# * we can also add additional data like in /login endpoint i passed user object
token_router = APIRouter()


# @token_router.post("/token")
# async def login_for_access_token(
#     result=Depends(login),
# ):
#     return result
