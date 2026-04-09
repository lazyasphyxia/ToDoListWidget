from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class TaskComponent(QWidget):
    # Сигналы, чтобы окно узнало, когда задачу удалили или изменили
    deleted = pyqtSignal()
    changed = pyqtSignal()

    def __init__(self, task):
        super().__init__()
        self.task = task

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

        # Кнопка удаления (крестик)
        self.del_btn = QPushButton("×")
        self.del_btn.setFixedSize(24, 24)
        self.del_btn.setStyleSheet("background: transparent; color: #FF453A; font-size: 18px; border: none;")
        self.del_btn.clicked.connect(self.deleted.emit)
        layout.addWidget(self.del_btn)

    def on_toggle(self, state):
        self.task.completed = bool(state)
        if self.task.completed:
            self.label.setStyleSheet("font-size: 14px; color: gray; text-decoration: line-through;")
        else:
            self.label.setStyleSheet("font-size: 14px; color: white;")
        self.changed.emit()