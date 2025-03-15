from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates

servers = [
    {
        "url": "/v1",
        "description": "API 버전 1.0",
        "version": "v1.0",
        "extended_description": "API v1.0 문서입니다.",
    },
    {
        "url": "/v2",
        "description": "API 버전 2.0",
        "version": "v2.0",
        "extended_description": "API v2.0 문서입니다.",
    },
]


def http_get(request: Request):
    from app_fastapi.main import app

    """
    API 버전 별 문서 페이지 링크 제공을 위한 엔드포인트
    """
    templates_path = Path(__file__).parent / "html_response_templates"
    templates = Jinja2Templates(directory=templates_path)

    return templates.TemplateResponse(
        "api_docs_selector.html",
        {
            "request": request,
            "app_title": app.title,
            "app_description": app.description,
            "servers": servers,
        },
    )
