STYLESHEET = """
QMainWindow {
    background: transparent;
}

QWidget#MainWindow {
    background-color: rgba(18, 18, 22, 95);
    border: none;
    border-radius: 24px;
}

/* СТИЛЬ ДЛЯ ЗАМКА */
QPushButton#LockButton {
    background-color: transparent; 
    border: none;
    padding: 0px; /* Убираем гигантские отступы */
    font-family: "Segoe MDL2 Assets", "Segoe UI Symbol", "Segoe UI";
    font-size: 18px;
    font-weight: 500;
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

QPushButton#AddButton {
    background-color: rgba(255, 255, 255, 240);
    color: #111111;
    border: none;
    border-radius: 12px;
    padding: 8px 15px;
    font-weight: 600;
}

QPushButton#AddButton:hover {
    background-color: rgba(255, 255, 255, 255);
}

QPushButton#AddButton:pressed {
    background-color: rgba(230, 230, 230, 255);
}
"""