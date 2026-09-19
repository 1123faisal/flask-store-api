from datetime import datetime, timezone

BLOCKLIST_KEY_PREFIX = "jwt_blocklist:"


def add_token_to_blocklist(conn, jti, exp_timestamp):
    ttl = exp_timestamp - int(datetime.now(timezone.utc).timestamp())
    if ttl > 0:
        conn.setex(f"{BLOCKLIST_KEY_PREFIX}{jti}", ttl, "true")


def is_token_blocklisted(conn, jti):
    return conn.exists(f"{BLOCKLIST_KEY_PREFIX}{jti}") > 0
