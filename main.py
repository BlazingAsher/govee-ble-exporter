import asyncio

from threading import Thread
from fastapi import FastAPI
from prometheus_client import disable_created_metrics, make_asgi_app

from app.utils import constants
from app.jobs import bluetooth_scan

app = FastAPI()

# Prometheus metrics
disable_created_metrics()
metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)

thread = Thread(target=lambda: asyncio.run(bluetooth_scan.run()),  daemon=True)
thread.start()

if __name__ == "__main__":
    import uvicorn
    import uvicorn.config

    uvicorn.config.LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.config.LOGGING_CONFIG["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    uvicorn.config.LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.config.LOGGING_CONFIG["loggers"]["app"] = {
        'handlers': ['default'],
        'level': 'INFO',
        'propagate': False
    }

    uvicorn.run(app, host=constants.LISTEN_ADDRESS, port=constants.LISTEN_PORT)
