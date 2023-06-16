from src.services.crypto.service import ServiceCrypto
from src.services.router.service import Router

router = Router.get_router()
crypto_service_instance = ServiceCrypto()


# colocar rota
@router.get("/confirm_jwt", tags=["Crypto"])
async def confirm_jwt(jwt: str, rota):
    return crypto_service_instance.confirm_jwt(jwt, rota)


@router.get("/decode_jwt_user", tags=["Crypto"])
async def decode_jwt(jwt: str):
    return crypto_service_instance.descrypting_jwt(jwt)


@router.get("/create_jwt", tags=["Crypto"])
async def create_jwt(pass_cripto, password, email):
    return crypto_service_instance.create_jwt(pass_cripto, password, email)


@router.get("/descrypting", tags=["Crypto"])
async def descrypting(password):
    return crypto_service_instance.descrypting(password)


@router.get("/encrypted", tags=["Crypto"])
async def encrypted(password):
    return crypto_service_instance.encrypting(password)

