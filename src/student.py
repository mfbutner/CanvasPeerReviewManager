from typing import Any, Dict


class Student:
    def __init__(self, user: Dict[str, Any]):
        self.user = user

    @property
    def id(self) -> int:
        return self.user['id']

    @property
    def name(self) -> str:
        try:
            return self.user['display_name']
        except KeyError:
            return self.user['name']

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Student) and self.id == other.id

    def __ne__(self, other: Any):
        return not (self == other)

    def __hash__(self):
        return hash(self.id)

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return str(self)
