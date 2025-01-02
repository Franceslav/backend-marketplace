from functools import wraps

from app.database import async_session_maker


def manage_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            if "session" not in kwargs:
                kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper
