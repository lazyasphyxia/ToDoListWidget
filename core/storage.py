import json
import os
from .task_model import Task


class StorageManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load_tasks(self) -> list[Task]:
        """Загружает задачи из файла."""
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self, tasks: list[Task]):
        """Сохраняет список задач в файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(
                [task.to_dict() for task in tasks],
                f,
                ensure_ascii=False,
                indent=4
            )
