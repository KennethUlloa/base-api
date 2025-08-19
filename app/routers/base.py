from fastapi import HTTPException


def or_error(obj, error):
    if obj is None:
        raise error
    return obj


def or_404(obj):
    return or_error(obj, HTTPException(status_code=404, detail="Not found"))


def value_or_error(obj, value, error):
    if obj is None:
        raise error
    return value


def value_or_404(obj, default):
    return value_or_error(
        obj, default, HTTPException(status_code=404, detail="Not found")
    )
