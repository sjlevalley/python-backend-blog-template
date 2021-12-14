# Blacklists are used to deny access. In this case, we will deny users if their id is in this blacklist

# E.G. - Below, user with ID of 2 or 3 will be denied

BLOCKLIST = {2, 3}

# Notes from Flask-JWT-Extended docs regarding blocklist:

    # Blacklist Changes

    # All occurrences of blacklist have been renamed to blocklist

    # The JWT_BLACKLIST_ENABLED option has been removed. If you do not want to check a JWT against your blocklist, do not register a callback function with @jwt.token_in_blocklist_loader.

    # The JWT_BLACKLIST_TOKEN_CHECKS option has been removed. If you don’t want to check a given token type against the blocklist, specifically ignore it in your callback function by checking the jwt_payload["type"] and short circuiting accordingly. jwt_payload["type"] will be either "access" or "refresh".