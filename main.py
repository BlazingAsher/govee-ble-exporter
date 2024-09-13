from asyncio import run
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_client import disable_created_metrics, make_asgi_app

from app.utils import constants
from app.jobs import bluetooth_scan

app = FastAPI()

# Prometheus metrics
disable_created_metrics()
metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)

# Scheduler
scheduler = BackgroundScheduler()

# Start background jobs using APScheduler
scheduler.add_job(lambda: run(bluetooth_scan.run()), 'interval', seconds=constants.SCAN_FREQUENCY)  # Scan every 15 minutes
# Run once at startup so we don't need to wait as long for data
# Just that a couple log lines might be missed if you are running the Python file directly, since the logger isn't configured until later
scheduler.add_job(lambda: run(bluetooth_scan.run()))

scheduler.start()

# Ensure scheduler stops on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()

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
