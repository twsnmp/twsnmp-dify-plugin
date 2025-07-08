from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from twsnmpapi.twsnmpapi import TwsnmpAPI

class TwsnmpProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        url = credentials.get("twsnmp_url")
        user = credentials.get("twsnmp_user")
        password = credentials.get("twsnmp_password")
        if not url:
            raise ToolProviderCredentialValidationError("URLは必須です。")
        if not user:
            raise ToolProviderCredentialValidationError("ユーザーIDは必須です。")
        if not password:
            raise ToolProviderCredentialValidationError("パスワードは必須です。")
        api = TwsnmpAPI(url)
        r = api.login(user,password)
        if r:
            raise ToolProviderCredentialValidationError(f"TWSNMP FCへの接続またはログイン中にエラーが発生しました。({r})")
