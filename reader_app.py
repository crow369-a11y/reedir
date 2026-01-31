import sys
import fitz
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog
)
from PyQt6.QtCore import Qt
from deep_translator import GoogleTranslator
from PyQt6.QtWidgets import QMessageBox


class ReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reedir")
        self.setGeometry(100, 100, 900, 600)
        # Разрешаем drag & drop
        self.setAcceptDrops(True)
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        # Кнопка открытия PDF
        self.open_button = QPushButton("Open PDF")
        self.open_button.clicked.connect(self.open_pdf_dialog)
        layout.addWidget(self.open_button)
        # Поле для текста
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
    # ====== Открытие через кнопку ======

    def open_pdf_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF file",
            "",
            "PDF Files (*.pdf)"
        )
        if file_path:
            self.load_pdf(file_path)
    # Перевод

    def translate_selected_text(self):
        selected_text = self.text_area.textCursor().selectedText()
        if not selected_text.strip():
            QMessageBox.warning(
                self,
                "No text selected",
                "Please select some text to translate."
            )
            return

            translator = GoogleTranslator(source="en", target="ru")
            translation = translator.translate(selected_text)

            self.translation_area.setText(translation)  # 222222222
    # ====== Общая функция загрузки PDF ======

    def load_pdf(self, file_path):
        document = fitz.open(file_path)
        full_text = ""

        for page_number, page in enumerate(document, start=1):
            full_text += f"\n\n===== Page {page_number} =====\n\n"

            text = page.get_text("text")
            full_text += text
            images = page.get_images()
            if images:
                full_text += "\n[IMAGE ON THIS PAGE]\n"

        self.text_area.setText(full_text)  # 888
        self.translate_button = QPushButton("Translate selected text")
        self.translate_button.clicked.connect(self.translate_selected_text)
        layout.addWidget(self.translate_button)

        self.translation_area = QTextEdit()
        self.translation_area.setReadOnly(True)
        self.translation_area.setPlaceholderText(
            "Translation will appear here...")
        layout.addWidget(self.translation_area)  # 888
    # ====== Drag & Drop ======

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        file_path = urls[0].toLocalFile()
        if file_path.lower().endswith(".pdf"):
            self.load_pdf(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReaderApp()
    window.show()
    sys.exit(app.exec())
