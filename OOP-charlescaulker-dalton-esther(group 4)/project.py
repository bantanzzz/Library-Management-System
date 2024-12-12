import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import sqlite3
import random
from datetime import datetime
from typing import Dict, List

class DatabaseManager:
    def __init__(self, db_name: str = 'library.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT PRIMARY KEY,
                genre TEXT,
                pub_year TEXT
            )
        ''')
        self.conn.commit()

    def add_book(self, book_data: tuple) -> bool:
        try:
            self.cursor.execute(
                'INSERT INTO books VALUES (?, ?, ?, ?, ?)',
                book_data
            )
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def get_all_books(self) -> List[tuple]:
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()

    def delete_book(self, isbn: str) -> bool:
        try:
            self.cursor.execute('DELETE FROM books WHERE isbn = ?', (isbn,))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def add_sample_books(self) -> None:
        sample_data = self._generate_sample_data()
        self.cursor.executemany('INSERT INTO books VALUES (?, ?, ?, ?, ?)', sample_data)
        self.conn.commit()

    def _generate_sample_data(self) -> List[tuple]:
        titles = [
            "The Art of Programming", "Digital Fortress", "The Silent Patient",
            "The Midnight Library", "Atomic Habits", "Deep Learning Basics",
            "Python Mastery", "Data Science 101", "Web Development Guide",
            "Artificial Intelligence"
        ]
        
        authors = [
            "John Smith", "Emma Wilson", "Michael Brown", "Sarah Davis",
            "James Johnson", "Robert Martin", "David Miller", "Lisa Anderson"
        ]
        
        genres = [
            "Programming", "Technology", "Computer Science", "Software Development",
            "Data Science", "Web Development", "Artificial Intelligence"
        ]

        books = []
        current_year = datetime.now().year
        
        for _ in range(50):
            title = f"{random.choice(titles)} {random.randint(1, 5)}"
            author = random.choice(authors)
            isbn = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            genre = random.choice(genres)
            pub_year = str(random.randint(current_year - 20, current_year))
            
            books.append((title, author, isbn, genre, pub_year))
        
        return books

class LibraryManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self._setup_styles()
        self.init_ui()

    def _setup_styles(self) -> None:
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 12px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 5px;
                min-height: 20px;
            }
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0a3d91;
            }
            QTableWidget {
                background-color: #2d2d2d;
                color: white;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #0d47a1;
                color: white;
                padding: 5px;
                border: 1px solid #3d3d3d;
            }
            QScrollBar {
                background-color: #2d2d2d;
            }
            QScrollBar::handle {
                background-color: #3d3d3d;
            }
        """)

    def init_ui(self) -> None:
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        self._setup_banner(layout)
        self._setup_input_fields(layout)
        self._setup_buttons(layout)
        self._setup_search(layout)
        self._setup_table(layout)
        self._setup_delete_button(layout)
        
        self.load_books()

    def _setup_banner(self, layout: QVBoxLayout) -> None:
        banner = QLabel("FICT BOOK MANAGEMENT")
        banner.setStyleSheet("""
            QLabel {
                background-color: #0d47a1;
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
                margin: 10px;
            }
        """)
        banner.setAlignment(Qt.AlignCenter)
        layout.addWidget(banner)

    def _setup_input_fields(self, layout: QVBoxLayout) -> None:
        self.inputs = {}
        fields = ['Title:', 'Author:', 'ISBN:', 'Genre:', 'Pub. Year:']
        
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        
        for field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(field)
            label.setMinimumWidth(80)
            line_edit = QLineEdit()
            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
            input_layout.addLayout(h_layout)
            self.inputs[field] = line_edit
        
        layout.addWidget(input_widget)

    def _setup_buttons(self, layout: QVBoxLayout) -> None:
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Book")
        add_btn.clicked.connect(self.add_book)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_fields)
        
        sample_btn = QPushButton("Add Sample Books")
        sample_btn.clicked.connect(self.add_sample_books)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(sample_btn)
        layout.addLayout(btn_layout)

    def _setup_search(self, layout: QVBoxLayout) -> None:
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setMinimumWidth(80)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search books...")
        self.search_input.textChanged.connect(self.search_books)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

    def _setup_table(self, layout: QVBoxLayout) -> None:
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Title", "Author", "ISBN", "Genre", "Publication Year"]
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setShowGrid(True)
        layout.addWidget(self.table)

    def _setup_delete_button(self, layout: QVBoxLayout) -> None:
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_book)
        layout.addWidget(delete_btn)

    def add_book(self) -> None:
        book_data = (
            self.inputs['Title:'].text(),
            self.inputs['Author:'].text(),
            self.inputs['ISBN:'].text(),
            self.inputs['Genre:'].text(),
            self.inputs['Pub. Year:'].text()
        )
        
        if self.db.add_book(book_data):
            self.load_books()
            self.clear_fields()

    def clear_fields(self) -> None:
        for input_field in self.inputs.values():
            input_field.clear()

    def load_books(self) -> None:
        books = self.db.get_all_books()
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def search_books(self) -> None:
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def delete_book(self) -> None:
        current_row = self.table.currentRow()
        if current_row >= 0:
            isbn = self.table.item(current_row, 2).text()
            if self.db.delete_book(isbn):
                self.load_books()

    def add_sample_books(self) -> None:
        self.db.add_sample_books()
        self.load_books()

def main():
    app = QApplication(sys.argv)
    window = LibraryManagementSystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

