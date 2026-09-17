"""Good example code for CodeSense demo."""


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


class UserManager:
    """Manage user records."""
    def __init__(self):
        self.users = []

    def add_user(self, user: dict) -> None:
        """Add a user dictionary to the list."""
        self.users.append(user)


def calculate_total(items):
    """Calculate total price for items."""
    total = 0.0
    for item in items:
        total += item.get('price', 0.0)
    return total
