import os
import subprocess
from subprocess import PIPE, run
import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

AUTHENTICATION_KEY: str = os.getenv('WEB_SERVER_AUTHENTICATION_KEY')

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(x_api_key: str = Depends(api_key_header)):
    if x_api_key != AUTHENTICATION_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Key"
        )
    return x_api_key

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Brownie Integration!"}

@app.post("/update_meta")
def update_meta(x_api_key: str = Depends(verify_api_key)):
    current_dir = os.path.abspath(os.curdir)
    brownie_app_dir: str =  f'{current_dir}/brownie_app'
    logger.info(f'Brownie app dir - {brownie_app_dir}')
    result = subprocess.run(
        ['brownie', 'run', 'scripts/dindex_updater.py', '--network', 'polygon-main'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=f'/{brownie_app_dir}/'
    )
    if result.stdout:
        logger.info(f"Subprocess stdout: {result.stdout}")
    if result.stderr:
        logger.error(f"Subprocess stderr: {result.stderr}")

    return {
        "stdout": result.stdout,
        "stderr": result.stderr
    }