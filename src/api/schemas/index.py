# Imports

from src.api.schemas.base import ApiMessageResponse

# Classes


class HelloResponse(ApiMessageResponse):
    """
    Resposta do endpoint `GET /`
    """


class HealthcheckResponse(ApiMessageResponse):
    """
    Resposta do endpoint `GET /healthcheck`
    """
