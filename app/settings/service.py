import json
import os

from loguru import logger

SERVICE = {
    "file": {
        "url": os.getenv("SERVICE_FILE_URL"),
        "datetime-format": "%d/%m/%Y %H:%M:%S",
        "server-auth": os.getenv("SERVICE_FILE_SERVICE_AUTH"),
        "authorization": "bearer 1"
    },
    "file-upload": {
        "file_limit": int(os.getenv("FILE_LIMIT", 10)),
        "file_size_max": int(os.getenv("FILE_SIZE_MAX", 2000000))
    },
    "template": {
        "url": os.getenv("SERVICE_TEMPLATE_URL"),
        "server-auth": os.getenv("SERVICE_TEMPLATE_SERVICE_AUTH")
    }
}

logger.info("=== config service ===")
print(json.dumps(SERVICE, indent=4, sort_keys=True))
