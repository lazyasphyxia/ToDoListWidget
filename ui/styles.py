STYLESHEET = """
QWidget#MainWindow {
    background-color: rgba(30, 30, 30, 220);
    border-radius: 20px;
}

/* СТИЛЬ ДЛЯ ЗАМКА */
QPushButton#LockButton {
    background-color: transparent; 
    border: none;
    padding: 0px; /* Убираем гигантские отступы */
    font-size: 20px;
    color: white;
}

QPushButton#LockButton:hover {
    background-color: rgba(255, 255, 255, 30);
    border-radius: 5px;
}

/* Остальные стили... */
QLabel {
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

QLineEdit {
    background-color: rgba(255, 255, 255, 20);
    border: 1px solid rgba(255, 255, 255, 40);
    border-radius: 10px;
    padding: 8px;
    color: white;
}

QPushButton {
    background-color: #007AFF;
    color: white;
    border-radius: 10px;
    padding: 8px 15px;
}
"""