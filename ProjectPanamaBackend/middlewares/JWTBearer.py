from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, Depends
from security.jwt_handler import decode_jwt
from config.dbconnection import session
from models.permisosusuario import PermisosUsuario

class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__()

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_user_in_db(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

    def verify_user_in_db(self, jwt_token: str):
        user_data = decode_jwt(jwt_token)
        db = session()
        if "error" in user_data:
            raise HTTPException(status_code=403, detail=user_data["error"])
        user = db.query(PermisosUsuario).filter(PermisosUsuario.NOMBRE == user_data["nombre"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return True