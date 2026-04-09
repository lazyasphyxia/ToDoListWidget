import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    text: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        """Превращает объект в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "text": self.text,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект Task из словаря."""
        return cls(**data)