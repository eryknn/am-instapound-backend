import uuid


def is_valid_uuid(id_to_check: str) -> bool:
    try:
        uuid.UUID(id_to_check)
        return True
    except ValueError:
        return False
