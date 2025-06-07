import os
from urllib.parse import urljoin
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse

from src.core.path_config import path_config


router = APIRouter()

@router.get("/",include_in_schema=False, response_class=HTMLResponse)
async def root(request: Request):
        base_url = str(request.base_url).rstrip("/")
        docs_url = urljoin(base_url, "docs")
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Swipewise API</title>
        <style>
            body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            text-align: center;
            }}

            h1 {{
            font-size: 3em;
            margin-bottom: 0.2em;
            }}

            p {{
            font-size: 1.2em;
            max-width: 600px;
            margin: 0.5em 0 2em 0;
            }}

            a {{
            background-color: #fff;
            color: #00bcd4;
            text-decoration: none;
            padding: 0.75em 1.5em;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s, color 0.3s;
            }}

            a:hover {{
            background-color: #00bcd4;
            color: #fff;
            }}

            footer {{
            position: absolute;
            bottom: 20px;
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.8);
            }}
        </style>
        </head>
        <body>
        <h1>Swipewise API</h1>
        <p>Maximize your credit card rewards.</p>
        <a href="{docs_url}">View API Documentation</a>
        <footer>&copy; 2025 Cashback API Service</footer>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)


@router.get("/log")
async def get_log_file(request: Request):
    # Define the path to your log file
    log_file_path = path_config.log_dir / 'swipe_error.log'
    
    # Check if the file exists
    if not os.path.exists(log_file_path):
        raise HTTPException(status_code=404, detail="Log file not found")
    
    # Return the file for download
    return FileResponse(
        path=log_file_path,
        filename="swipe_error.log",
        media_type="application/octet-stream"  # Generic binary file type
    )