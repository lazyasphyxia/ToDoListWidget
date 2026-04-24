from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel
from PyQt6.QtCore import pyqtSignal, QTimer


class TaskComponent(QWidget):
    deleted = pyqtSignal()
    changed = pyqtSignal()

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.original_text = task.text  # Запоминаем исходный текст задачи

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Чекбокс
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(task.completed)
        self.checkbox.stateChanged.connect(self.on_toggle)
        layout.addWidget(self.checkbox)

        # Текст задачи
        self.label = QLabel(task.text)
        self.label.setStyleSheet("font-size: 14px; color: white;")
        if task.completed:
            self.label.setStyleSheet("font-size: 14px; color: gray; text-decoration: line-through;")
        layout.addWidget(self.label, stretch=1)

    def on_toggle(self, state):
        self.task.completed = bool(state)
        if self.task.completed:
            self.label.setStyleSheet("font-size: 14px; color: gray; text-decoration: line-through;")
            self.start_deletion_timer(3)
        else:
            self.label.setStyleSheet("font-size: 14px; color: white;")
            # Если галочку сняли — возвращаем оригинальный текст.
            self.label.setText(self.original_text)

        self.changed.emit()

    def start_deletion_timer(self, seconds):
        """Запускает обратный отсчет перед автоудалением отмеченной задачи."""
        if not self.checkbox.isChecked():
            return

        if seconds > 0:
            self.label.setText(f"{self.original_text} (удаление через {seconds}...)")
            QTimer.singleShot(1000, lambda: self.start_deletion_timer(seconds - 1))
            return

        if self.checkbox.isChecked():
            self.deleted.emit()