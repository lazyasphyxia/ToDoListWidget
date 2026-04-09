import sys
from PyQt6.QtWidgets import QApplication, QListWidgetItem
from ui.view import TodoWidget
from ui.components import TaskComponent
from core.task_model import Task
from core.storage import StorageManager


class TodoController:
    def __init__(self):
        self.view = TodoWidget()
        self.storage = StorageManager()

        # Загружаем старые задачи
        self.tasks = self.storage.load_tasks()
        for task in self.tasks:
            self.add_task_to_ui(task)

        # Подключаем кнопку "Добавить"
        self.view.add_button.clicked.connect(self.handle_add_task)
        # Позволяем нажимать Enter в поле ввода
        self.view.input_field.returnPressed.connect(self.handle_add_task)

    def handle_add_task(self):
        text = self.view.input_field.text().strip()
        if not text:
            return

        # Создаем модель задачи
        new_task = Task(text=text)
        self.tasks.append(new_task)

        # Добавляем в интерфейс
        self.add_task_to_ui(new_task)

        # Сохраняем и очищаем поле
        self.storage.save_tasks(self.tasks)
        self.view.input_field.clear()

    def add_task_to_ui(self, task):
        # Создаем "контейнер" для списка
        item = QListWidgetItem(self.view.task_list)
        # Создаем наш красивый виджет
        component = TaskComponent(task)

        # Связываем размеры
        item.setSizeHint(component.sizeHint())

        # Устанавливаем виджет в список
        self.view.task_list.addItem(item)
        self.view.task_list.setItemWidget(item, component)

        # Обработка удаления
        component.deleted.connect(lambda: self.remove_task(item, task))
        # Обработка клика (сохранение состояния)
        component.changed.connect(lambda: self.storage.save_tasks(self.tasks))

    def remove_task(self, item, task):
        self.tasks.remove(task)
        self.view.task_list.takeItem(self.view.task_list.row(item))
        self.storage.save_tasks(self.tasks)


def main():
    app = QApplication(sys.argv)
    controller = TodoController()
    controller.view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()