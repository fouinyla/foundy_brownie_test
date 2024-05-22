from os import path, curdir
import subprocess
import logging

from fastapi import Depends, FastAPI

# from dependencies import verify_api_key


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Brownie Integration!"}


@app.post(
    path="/update_meta",
    # dependencies=[Depends(verify_api_key)],
)
def update_meta():
    current_dir = path.abspath(curdir)
    brownie_app_dir: str = f'{current_dir}/brownie_app'
    logger.info(f'Brownie app dir - {brownie_app_dir}')

    result = subprocess.run(
        ['brownie', 'run', 'scripts/dindex_updater.py', '--network', 'polygon-main'],
        # ['brownie', 'run', 'scripts/dindex_updater.py', '--network', 'bsc-main'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=f'/{brownie_app_dir}/',
    )
    if result.stdout:
        logger.info(f"Subprocess stdout: {result.stdout}")
    if result.stderr:
        logger.error(f"Subprocess stderr: {result.stderr}")

    return {"stdout": result.stdout, "stderr": result.stderr}
