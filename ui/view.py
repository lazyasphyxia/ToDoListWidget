from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from .styles import STYLESHEET


class TodoWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_locked = False

        self.setWindowTitle("Todo Widget")
        self.setFixedSize(300, 450)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnBottomHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainWindow")
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(15, 10, 15, 20)

        # --- ШАПКА ---
        self.header_layout = QHBoxLayout()

        # Кнопка-замок
        self.lock_btn = QPushButton("🔓")  # Возвращаем красоту
        self.lock_btn.setFixedSize(30, 30)
        self.lock_btn.setObjectName("LockButton")
        self.lock_btn.setCursor(Qt.CursorShape.PointingHandCursor)  # Чтобы было понятно, что кликабельно
        self.lock_btn.clicked.connect(self.toggle_lock)
        self.header_layout.addWidget(self.lock_btn)

        # Заголовок
        self.title_label = QLabel("Tasks")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        self.header_layout.addWidget(self.title_label)

        # Отступ справа для баланса
        self.header_layout.addSpacing(40    )

        self.layout.addLayout(self.header_layout)
        # -------------

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background: transparent; border: none; color: white;")
        self.layout.addWidget(self.task_list)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Что нужно сделать?")
        self.layout.addWidget(self.input_field)

        self.add_button = QPushButton("Добавить")
        self.layout.addWidget(self.add_button)

        self.setStyleSheet(STYLESHEET)

    def toggle_lock(self):
        self.is_locked = not self.is_locked
        self.lock_btn.setText("🔒" if self.is_locked else "🔓")
        print(f"Widget locked: {self.is_locked}")  # Проверка в консоли

    def mousePressEvent(self, event):
        if not self.is_locked and event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.is_locked and hasattr(self, 'drag_pos') and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()