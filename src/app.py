# Author: Maxat Akbanov
# Last Change Date: 17 April 2024
# Description: Cross-platform GUI app to fetch daily currency rates from the National Bank of Kazakhstan

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot
from datetime import datetime

import requests
from bs4 import BeautifulSoup

def get_currency_rate(currency):
    url = 'https://nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'table table--striped text-center text-primary text-size-xs'})
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                for i, cell in enumerate(cells):
                    if currency in cell.text:
                        if i + 1 < len(cells):
                            return cells[i + 1].text.strip()
    except Exception as e:
        return str(e)
    return "не найден"

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Курс Валют НБ РК'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 160
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create layout
        layout = QVBoxLayout()

        # Elements
        self.date_label = QLabel('Текущая дата (год-месяц-число): ' + datetime.now().strftime('%Y-%m-%d'), self) 
        self.currency_input = QLineEdit(self)
        self.currency_input.setPlaceholderText("Введите валюту на латинице (например., USD)")
        self.button = QPushButton('Получить курс по отношению к тенге', self)
        self.button.clicked.connect(self.on_click)
        self.result_label = QLabel('Результат запроса будет показан здесь', self)

        # Add widgets to the layout
        layout.addWidget(self.date_label)
        layout.addWidget(self.currency_input)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)

        # Set the layout on the application window
        self.setLayout(layout)
        self.show()

    @pyqtSlot()
    def on_click(self):
        currency = self.currency_input.text()
        rate = get_currency_rate(currency)
        self.result_label.setText(f"Курс для валюты {currency} - {rate}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
