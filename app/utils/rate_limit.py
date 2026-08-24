from time import time

login_attempts: dict[str, list[float]] = {}

def check_login_rate_limit(
    key: str,
    max_attempts: int,
    window_seconds: int
) -> bool:

    now = time()

    attempts = login_attempts.get(key, [])

    attempts = [
        timestamp
        for timestamp in attempts
        if now - timestamp < window_seconds
    ]

    if len(attempts) >= max_attempts:
        login_attempts[key] = attempts

        return False

    attempts.append(now)

    login_attempts[key] = attempts

    return True