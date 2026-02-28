from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger()


def authenticate_google_calendar(
    credentials_path: str,
    token_path: str,
    scopes: list[str],
) -> Any:
    request_mod = importlib.import_module("google.auth.transport.requests")
    oauth2_mod = importlib.import_module("google.oauth2.credentials")
    oauthlib_flow_mod = importlib.import_module("google_auth_oauthlib.flow")

    request = request_mod.Request
    credentials_cls = oauth2_mod.Credentials
    installed_app_flow = oauthlib_flow_mod.InstalledAppFlow

    credentials: Any = None
    token_file = Path(token_path)

    if token_file.exists():
        credentials = credentials_cls.from_authorized_user_file(token_path, scopes)

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(request())

    if credentials is None or not credentials.valid:
        flow = installed_app_flow.from_client_secrets_file(credentials_path, scopes)
        credentials = flow.run_local_server(port=0)

    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text(credentials.to_json())
    logger.info("google_calendar.token_saved", token_path=token_path)
    return credentials
