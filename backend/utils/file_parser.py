import os
from typing import Tuple

ALLOWED_EXT = {'.py'}
MAX_SIZE = 200 * 1024


def validate_upload(filename: str, content: bytes) -> Tuple[bool, str]:
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_EXT:
        return False, 'Unsupported file type'
    if len(content) > MAX_SIZE:
        return False, 'File too large'
    return True, ''
