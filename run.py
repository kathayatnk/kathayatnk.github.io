#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn

if __name__ == '__main__':
    try:
        config = uvicorn.Config(app='src.main:app', reload=True, port=8080)
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
