from backend.core.model.auth import GoogleAuthRequest, GoogleUserInfo


class GoogleAuthProvider:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    async def verify_token(self, token: str) -> GoogleUserInfo:
        pass


    async def get_user_info(self, token: str) -> GoogleUserInfo:
        pass