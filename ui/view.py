import win32gui
import win32con
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from .styles import STYLESHEET


class TodoWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_locked = False
        self.setWindowTitle("Todo Widget")
        self.setFixedSize(300, 450)

        # Флаги: Без рамок + Tool (чтобы не было в таскбаре) + StaysOnBottom
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnBottomHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # --- ТВОЙ UI ---
        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainWindow")
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(15, 10, 15, 20)

        self.header_layout = QHBoxLayout()
        self.lock_btn = QPushButton("🔓")
        self.lock_btn.setFixedSize(30, 30)
        self.lock_btn.setObjectName("LockButton")
        self.lock_btn.clicked.connect(self.toggle_lock)
        self.header_layout.addWidget(self.lock_btn)

        self.title_label = QLabel("Tasks")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addSpacing(40)
        self.layout.addLayout(self.header_layout)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background: transparent; border: none; color: white;")
        self.layout.addWidget(self.task_list)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Что нужно сделать?")
        self.layout.addWidget(self.input_field)

        self.add_button = QPushButton("Добавить")
        self.layout.addWidget(self.add_button)

        self.setStyleSheet(STYLESHEET)

    def showEvent(self, event):
        """Когда окно появляется, делаем его спутником рабочего стола."""
        super().showEvent(event)
        # Небольшая задержка, чтобы окно 100% создалось в системе
        QTimer.singleShot(100, self.make_desktop_companion)

    def make_desktop_companion(self):
        """Устанавливает рабочий стол владельцем виджета."""
        try:
            hwnd = int(self.winId())

            # Ищем системное окно рабочего стола по имени класса "Progman"
            desktop_hwnd = win32gui.FindWindow("Progman", None)

            # Если вдруг Progman не найден, берем самое базовое окно рабочего стола
            if not desktop_hwnd:
                desktop_hwnd = win32gui.GetDesktopWindow()

            # Устанавливаем рабочий стол как Владельца (Owner).
            # Окно-владелец никогда не перекроет наше окно, и Win+D его проигнорирует.
            win32gui.SetWindowLong(hwnd, win32con.GWL_HWNDPARENT, desktop_hwnd)

            # Жестко фиксируем виджет на самом нижнем слое
            win32gui.SetWindowPos(
                hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0,
                win32con.SWP_NOSIZE | win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE
            )
            print(f"Виджет успешно привязан к окну {desktop_hwnd}!")

        except Exception as e:
            print(f"Ошибка привязки: {e}")

    def toggle_lock(self):
        self.is_locked = not self.is_locked
        self.lock_btn.setText("🔒" if self.is_locked else "🔓")

        if self.is_locked:
            # 1. Скрываем элементы ввода
            self.input_field.setVisible(False)
            self.add_button.setVisible(False)

            # 2. Вычисляем новую высоту
            # Берем высоту заголовка + высоту списка задач
            # 100 - это примерный запас под заголовок и отступы
            items_height = self.task_list.count() * 35  # примерно 35px на строку
            new_height = max(150, min(items_height + 100, 450))

            self.setFixedSize(300, new_height)
        else:
            # 1. Показываем элементы обратно
            self.input_field.setVisible(True)
            self.add_button.setVisible(True)

            # 2. Возвращаем стандартную высоту
            self.setFixedSize(300, 450)

        # 3. Важно: после изменения размера нужно обновить привязку к рабочему столу,
        # иначе Windows может "вытолкнуть" окно на передний план.
        self.make_desktop_companion()

    # Логика перемещения
    def mousePressEvent(self, event):
        if not self.is_locked and event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.is_locked and hasattr(self, 'drag_pos') and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()