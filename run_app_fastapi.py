import sys

import uvicorn

from app_fastapi.configurations.configuration import get_settings
from commons.enums import AppEnviromentType

if __name__ == "__main__":
    argv = sys.argv[1:]

    settings = get_settings()

    if len(argv) == 0:

        if settings.APP_ENVIROMENT_TYPE == AppEnviromentType.DEV:
            print("Envrioment Type : dev")

            uvicorn.run(
                "app_fastapi.main:app",
                reload=True,
                log_level="debug",
                host="0.0.0.0",
                port=settings.FASTAPI_PORT,
            )
        elif settings.APP_ENVIROMENT_TYPE == AppEnviromentType.STAGING:
            print("Envrioment Type : staging")

            uvicorn.run(
                "app_fastapi.main:app",
                workers=4,
                log_level="debug",
                host="0.0.0.0",
                port=settings.FASTAPI_PORT,
            )
        elif settings.APP_ENVIROMENT_TYPE == AppEnviromentType.PROD:
            print("Envrioment Type : prod")

            uvicorn.run(
                "app_fastapi.main:app",
                workers=4,
                log_level="debug",
                host="0.0.0.0",
                port=settings.FASTAPI_PORT,
            )
        else:
            print("Error: Invalid App enviroment type")

    else:
        print("Error: Arguments detected. No arguments are required.")
