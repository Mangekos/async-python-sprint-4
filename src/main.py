import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import ORJSONResponse

from api.links_router import router_links
from api.status_router import router_status
from core import config
from db.db import create_model

BLACK_LIST = [
    # "127.0.0.1"
]


async def check_allowed_ip(request: Request):
    def is_ip_banned(ip):
        is_banned = ip in BLACK_LIST
        return is_banned

    if request.client is not None and is_ip_banned(request.client.host):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


app = FastAPI(
    title=config.app_settings.app_title,
    default_response_class=ORJSONResponse,
    dependencies=[Depends(check_allowed_ip)],
)


app.include_router(router_links, prefix="/links")
app.include_router(router_status, prefix="/status")


@app.on_event("startup")
async def startup_event():
    await create_model()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.app_settings.project_host,
        port=config.app_settings.project_port,
        reload=True,
        log_config=config.LOGGING,
    )
