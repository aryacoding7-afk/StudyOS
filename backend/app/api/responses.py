from typing import Any


def success(message: str, data: Any = None):
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error(message: str):
    return {
        "success": False,
        "message": message,
    }