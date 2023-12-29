import sys
import pyperclip

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar
from PyQt5.QtWidgets import QInputDialog, QColorDialog
from PyQt5.QtGui import QFont


# Класс главного окна
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main_menu.ui', self)
        self.setWindowTitle('Продвинутый шифровальщик')

        self.StatusBar = QStatusBar()
        self.setStatusBar(self.StatusBar)

        self.InformationBtn.clicked.connect(self.show_inf)
        self.EncryptBtn.clicked.connect(self.crypt)
        self.DecryptBtn.clicked.connect(self.crypt)
        self.SettingsBtn.clicked.connect(self.set_settings)
        self.CopypastBtn.clicked.connect(self.copy_to_clipboard)

        self.OutputTextEdit.setReadOnly(True)

    def resizeEvent(self, event):
        x, y = self.width(), self.height()

        self.EncryptBtn.move(x - 330, 20)
        self.DecryptBtn.move(x - 220, 20)
        self.SettingsBtn.move(x - 110, 20)
        self.CopypastBtn.move(x - 170, y - 55)

        new_size_y = (y - 160) // 2
        self.InputTextEdit.resize(x - 40, new_size_y)
        self.OutputTextEdit.move(20, y - 65 - new_size_y)
        self.OutputTextEdit.resize(x - 40, new_size_y)

    # функция для кнопки "Информация о шифровании"
    def show_inf(self):
        windows = {'Шифр Виженера': VigenerEnqInf(self),
                   'Шифр Цезаря': CaesarEnqInf(self),
                   'Шифр Гамбетта': GambettEnqInf(self),
                   'Матричное шифрование': MatrixEnqInf(self),
                   'Азбука Морзе': MorseEnqInf(self)}
        self.inf = windows[self.comboBox.currentText()]
        self.inf.show()

    # функция для кнопки настроек
    def set_settings(self):
        self.settings_window = Settings(self)
        self.settings_window.show()

    # функция для изменения шрифта
    def change_font(self, font_size):
        font = QFont("MS Shell Dlg 2", font_size)
        self.InputTextEdit.setFont(font)
        self.OutputTextEdit.setFont(font)

    # функция для изменения цвета фона
    def set_background_color(self, color):
        color = f"rgb{color.getRgb()[:3]}"
        self.setStyleSheet("#MainWindow {" + f"background-color: {color}" + "}")

    # функция для кнопки "Скопировать в буфер"
    def copy_to_clipboard(self):
        pyperclip.copy(self.OutputTextEdit.toPlainText())

    # основная функция для шифровки и расшифровки
    def crypt(self):
        encryption_type = self.comboBox.currentText()

        if encryption_type == 'Матричное шифрование':
            text = self.InputTextEdit.toPlainText()
            max_n = len(text)
            n, ok_pressed = QInputDialog.getInt(self, "Для матричного шифрования", "Введите число:", 2, 2, max_n - 1, 1)

            if ok_pressed:
                if self.sender().text() == 'Зашифровать':
                    self.OutputTextEdit.setPlainText(self.matrix_encrypt(text, n))
                    self.StatusBar.showMessage(f'Текст успешно зашифрован по ключу: "{n}"')
                elif self.sender().text() == 'Расшифровать':
                    self.OutputTextEdit.setPlainText(self.matrix_decrypt(text, n))
                    self.StatusBar.showMessage(f'Текст успешно расшифрован по ключу: "{n}"')

        elif encryption_type == 'Шифр Гамбетта':
            a, ok_pressed = QInputDialog.getItem(self, "Для шифра Гамбетта",
                                                 "Выберите язык", ("Русский", "Английский"), 0, False)
            if ok_pressed:
                key, ok_pressed = QInputDialog.getText(self, "Для шифра Гамбетта", "Введите кодовое слово:")
            else:
                key = ''

            if ok_pressed:
                word = self.InputTextEdit.toPlainText()

                alphabet = ''
                if a == 'Русский':
                    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
                elif a == 'Английский':
                    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

                try:
                    if self.sender().text() == 'Зашифровать':
                        self.OutputTextEdit.setPlainText(self.gambett_encrypt(alphabet, word, key))
                        self.StatusBar.showMessage(f'Текст успешно зашифрован по алфавиту: "{a}"; по ключу: "{key}"')
                    elif self.sender().text() == 'Расшифровать':
                        self.OutputTextEdit.setPlainText(self.gambett_decrypt(alphabet, word, key))
                        self.StatusBar.showMessage(f'Текст успешно расшифрован по алфавиту: "{a}"; по ключу: "{key}"')
                except KeyError:
                    self.StatusBar.showMessage('Ошибка: введено недопустимое кодовое слово')

        elif encryption_type == 'Шифр Цезаря':
            a, ok_pressed = QInputDialog.getItem(self, "Для шифра Цезаря", "Выберите язык:",
                                                 ("Русский", "Английский"), 0,
                                                 False)

            if ok_pressed:
                alphabet = ''
                if a == 'Русский':
                    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
                elif a == 'Английский':
                    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

                max_n = len(alphabet)
                n, ok_pressed = QInputDialog.getInt(self, "Для шифра Цезаря", "Введите число:", 0, 0, max_n - 1, 1)

                if ok_pressed:
                    text = self.InputTextEdit.toPlainText()

                    if self.sender().text() == 'Зашифровать':
                        self.OutputTextEdit.setPlainText(self.caesar_encrypt(alphabet, text, n))
                        self.StatusBar.showMessage(f'Текст успешно зашифрован по алфавиту: "{a}"; по ключу: "{n}"')
                    elif self.sender().text() == 'Расшифровать':
                        self.OutputTextEdit.setPlainText(self.caesar_decrypt(alphabet, text, n))
                        self.StatusBar.showMessage(f'Текст успешно расшифрован по алфавиту: "{a}"; по ключу: "{n}"')

        elif encryption_type == 'Шифр Виженера':
            a, ok_pressed = QInputDialog.getItem(self, "Для шифра Виженера", "Выберите язык:",
                                                 ("Русский", "Английский"), 0,
                                                 False)

            if ok_pressed:
                alphabet = ''
                if a == 'Русский':
                    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
                elif a == 'Английский':
                    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

                key, ok_pressed = QInputDialog.getText(self, "Для шифра Виженера", "Введите кодовое слово:")

                if ok_pressed:
                    text = self.InputTextEdit.toPlainText()

                    try:
                        if self.sender().text() == 'Зашифровать':
                            self.OutputTextEdit.setPlainText(self.vigener_encrypt(alphabet, text, key))
                            self.StatusBar.showMessage(f'Текст успешно зашифрован по алфавиту: "{a}";'
                                                       f' по ключу: "{key}"')
                        elif self.sender().text() == 'Расшифровать':
                            self.OutputTextEdit.setPlainText(self.vigener_decrypt(alphabet, text, key))
                            self.StatusBar.showMessage(f'Текст успешно расшифрован по алфавиту: "{a}";'
                                                       f' по ключу: "{key}"')
                    except KeyError:
                        self.StatusBar.showMessage('Ошибка: введено недопустимое кодовое слово')

        elif encryption_type == 'Азбука Морзе':
            a, ok_pressed = QInputDialog.getItem(self, "Для азбуки Морзе", "Выберите язык:",
                                                 ('Русский', "Английский",), 0,
                                                 False)

            if a == 'Английский':
                alphabet = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
                            'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
                            'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
                            'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----',
                            '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
                            '8': '---..', '9': '----.', '.': '......', ',': '-.-.-.', ':': '---...', '?': '..--..',
                            '!': '--..--', ';': '-.-.-.', ' ': ' '}
            else:
                alphabet = {'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ж': '...-',
                            'З': '--..', 'И': '..', 'Й': '.-----', 'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.',
                            'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-', 'У': '..-', 'Ф': '..-.',
                            'Х': '....', 'Ц': '-.-.', 'Ч': '---.', 'Ш': '----', 'Щ': '--.-', 'Ъ': '.--.-.', 'Ы': '-.--',
                            'Ь': '-..-', 'Э': '..-..', 'Ю': '..--', 'Я': '.-.-', '0': '-----', '1': '.----',
                            '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
                            '8': '---..', '9': '----.', '.': '......', ',': '-.-.-.', ':': '---...', '?': '..--..',
                            '!': '--..--', ';': '-.-.-.', ' ': ' '}

            if ok_pressed:
                text = self.InputTextEdit.toPlainText()
                if self.sender().text() == 'Зашифровать':
                    self.OutputTextEdit.setPlainText(self.to_morse(text, alphabet))
                    self.StatusBar.showMessage(f'Текст успешно зашифрован по алфавиту: "{a}"')
                elif self.sender().text() == 'Расшифровать':
                    self.OutputTextEdit.setPlainText(self.from_morse(text,
                                                                     {value: key for key, value in alphabet.items()}))
                    self.StatusBar.showMessage(f'Текст успешно расшифрован по алфавиту: "{a}"')

    # фнкция для матричной шифровки
    @staticmethod
    def matrix_encrypt(text, n=0):
        t1 = text + ' ' * (n - (len(text)) % n - n * (len(text) % n == 0))
        m = ''.join([''.join([t1[i] for i in range(j, len(t1), n)]) for j in range(n)])
        n = ''.join([m[i] for i in range(len(m)) if m[i:] != ' ' * (len(m) - i)])
        return n

    # фнкция для матричной расшифровки
    def matrix_decrypt(self, text, n):
        t1 = text + ' ' * (n - (len(text)) % n - n * (len(text) % n == 0))
        return self.matrix_encrypt(t1, len(t1) // n).rstrip()

    # функция для шифровки по Гамбетту
    @staticmethod
    def gambett_encrypt(a, text, key):
        key = list(filter(lambda x: x.upper() in a, key))
        if len(key) == 0:
            raise KeyError

        k = [a.index(x.upper()) for x in key]
        s = list()
        ind = 0

        for sym in text:
            if sym.upper() not in a:
                s.append(sym)
            else:
                if sym.isupper():
                    s.append(a[(a.index(sym.upper()) + k[ind]) % len(a)])
                else:
                    s.append(a[(a.index(sym.upper()) + k[ind]) % len(a)].lower())

                ind += 1
                ind %= len(k)

        return ''.join(s)

    # функция для расшифровки по Гамбетту
    @staticmethod
    def gambett_decrypt(a, text, key):
        key = list(filter(lambda x: x.upper() in a, key))
        if len(key) == 0:
            raise KeyError

        k = [a.index(x.upper()) for x in key]
        s = list()
        ind = 0

        for sym in text:
            if sym.upper() not in a:
                s.append(sym)
            else:
                if sym.isupper():
                    s.append(a[(a.index(sym.upper()) - k[ind]) % len(a)])
                else:
                    s.append(a[(a.index(sym.upper()) - k[ind]) % len(a)].lower())

                ind += 1
                ind %= len(k)

        return ''.join(s)

    # функция для шифровки по Цезарю
    @staticmethod
    def caesar_encrypt(a, text, key):
        result = list()
        for sym in text:
            if sym.upper() not in a:
                result.append(sym)
            else:
                if sym.isupper():
                    result.append(a[(a.find(sym.upper()) + key) % len(a)])
                else:
                    result.append(a[(a.find(sym.upper()) + key) % len(a)].lower())
        return ''.join(result)

    # функция для расшифровки по Цезарю
    def caesar_decrypt(self, a, text, key):
        return self.caesar_encrypt(a, text, -key)

    # функция для шифровки по Виженеру
    @staticmethod
    def vigener_encrypt(a, text, key):
        key = list(filter(lambda x: x.upper() in a, key))
        if len(key) == 0:
            raise KeyError

        k = [a.index(x.upper()) for x in key]
        res = list()
        ind = 0

        for sym in text:
            if sym.upper() not in a:
                res.append(sym)
            else:
                if sym.isupper():
                    res.append(a[(a.index(sym.upper()) + k[ind] + 1) % len(a)])
                else:
                    res.append(a[(a.index(sym.upper()) + k[ind] + 1) % len(a)].lower())

                ind += 1
                ind %= len(k)

        return ''.join(res)

    # функция для расшифровки по Виженеру
    @staticmethod
    def vigener_decrypt(a, text, key):
        key = list(filter(lambda x: x.upper() in a, key))
        if len(key) == 0:
            raise KeyError

        k = [a.index(x.upper()) for x in key]
        res = list()
        ind = 0

        for sym in text:
            if sym.upper() not in a:
                res.append(sym)
            else:
                if sym.isupper():
                    res.append(a[(a.index(sym.upper()) - k[ind] - 1) % len(a)])
                else:
                    res.append(a[(a.index(sym.upper()) - k[ind] - 1) % len(a)].lower())

                ind += 1
                ind %= len(k)

        return ''.join(res)

    # функция для шифрования Морзе
    @staticmethod
    def to_morse(text, a):
        return ' '.join(a.get(i.upper(), i) for i in text)

    # функция для расшифровки Морзе
    @staticmethod
    def from_morse(text, a):
        return ' '.join(map(lambda x: ''.join(map(lambda y: a.get(y, y),  x.split())), text.split('   '))).lower()


# Класс окна с информацией о шифре Виженера
class VigenerEnqInf(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('vigener_info.ui', self)

        VigenerEnqInf.setFixedWidth(self, 720)
        VigenerEnqInf.setFixedHeight(self, 350)


# Класс окна с информацией о шифре Цезаря
class CaesarEnqInf(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('caesar_info.ui', self)

        CaesarEnqInf.setFixedWidth(self, 720)
        CaesarEnqInf.setFixedHeight(self, 350)


# Класс окна с информацией о шифре Гамбетта
class GambettEnqInf(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('gambett_info.ui', self)

        GambettEnqInf.setFixedWidth(self, 720)
        GambettEnqInf.setFixedHeight(self, 350)


# Класс окна с информацией о матричном шифровании
class MatrixEnqInf(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('matrix_info.ui', self)

        MatrixEnqInf.setFixedWidth(self, 720)
        MatrixEnqInf.setFixedHeight(self, 350)


# Класс окна с информацией о Морзе
class MorseEnqInf(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('morse_info.ui', self)

        MorseEnqInf.setFixedWidth(self, 720)
        MorseEnqInf.setFixedHeight(self, 350)


# Класс окна для настроек
class Settings(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('settings_design.ui', self)
        self.setWindowTitle('Настройки')

        self.StatusBar = QStatusBar()
        self.setStatusBar(self.StatusBar)

        self.setFontBtn.clicked.connect(self.set_font)
        self.setColorBtn.clicked.connect(self.set_color)

        self.main_window = args[0]

    def set_font(self):
        n, ok_pressed = QInputDialog.getInt(self, "Задайте шрифт", "Введите размер:", 10, 8, 30, 1)

        if ok_pressed:
            self.main_window.change_font(n)
            self.StatusBar.showMessage(f"Задан новый размер шрифта: {n}")

    def set_color(self):
        color = QColorDialog.getColor()
        self.main_window.set_background_color(color)
        self.StatusBar.showMessage(f"Задан новый цвет фона: {color.getRgb()[:3]}")


def except_hook(cls, exception, traceback):
    return sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
