import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

from design.MainWindow import Ui_MainWindow as MainWindowDesign
from design.RatingDialog import Ui_Dialog as RatingDialogDesign
from design.GetNameDialog import Ui_Dialog as GetNameDesign
from design.SettingsDialog import Ui_Dialog as SettingsDialogDesign
from design.Ending import Ui_MainWindow as EndingDesign

from main import *
import json

user_name = ""


class NameDialog(QDialog, GetNameDesign):
    def __init__(self):
        super(NameDialog, self).__init__()
        self.setupUi(self)

        self.ok_btn.clicked.connect(self.press_ok)
        self.setWindowTitle("Имя?")
        self.ok_pressed = False

    def get_name(self):
        self.exec_()
        return self.name_input.text(), self.ok_pressed

    def press_ok(self):
        self.ok_pressed = True
        self.close()


class SettingsDialog(QDialog, SettingsDialogDesign):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.ok_btn.clicked.connect(self.ok_action)
        self.setWindowTitle('Settings')

        self.skins_list.addItems(skins.keys())
        self.skins_list.currentTextChanged.connect(self.on_skin_changed)

        with open("config.json", encoding="utf-8") as config_file:
            self.config = json.load(config_file)

    def on_skin_changed(self, text):
        spine, head = skins[text]
        self.preview_spine.setPixmap(QPixmap(f"pictures/{spine}"))
        self.preview_head.setPixmap(QPixmap(f"pictures/{head}"))

    def ok_action(self):
        global SPEED
        if temp := self.skins_list.currentItem():
            self.config["skin"] = temp.text()

        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(self.config, config_file)

        change_image()
        self.close()


class RatingDialog(QDialog, RatingDialogDesign):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Rating')

        with open('raiting.json', encoding='utf-8') as rating_file:
            rating_file = json.load(rating_file)
            rating_file = sorted(rating_file.items(), key=lambda x: -x[1])
        rating = list(enumerate(rating_file, 1))
        rating = "\n".join(f"{i}.\t{val[0]}\t{val[1]}" for i, val in rating)
        self.rating_info.setText(rating)


class MainWindow(QMainWindow, MainWindowDesign):
    def __init__(self):
        global user_name

        super().__init__()
        self.setupUi(self)

        self.play_btn.clicked.connect(self.play)
        self.settings_btn.clicked.connect(self.open_settings)
        self.rating_btn.clicked.connect(self.open_rating)
        self.exit_btn.clicked.connect(lambda: exit(0))
        self.setWindowTitle("MENU")
        while True:
            user_name, ok = NameDialog().get_name()
            if not ok:
                exit(0)
            if user_name:
                break
            print("Введи имя, падаль!")
        self.play_clicked = False

    def open_settings(self):
        dialog = SettingsDialog()
        dialog.exec_()

    def play(self):
        self.play_clicked = True
        self.close()

    def open_rating(self):
        rating_dialog = RatingDialog()
        rating_dialog.exec_()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super(MainWindow, self).close()
        if not self.play_clicked:
            exit(0)


class Ending(QMainWindow, EndingDesign):
    def __init__(self, score):
        super(Ending, self).__init__()
        self.setupUi(self)
        self.score_txt.setText(f'СЧЕТ: {str(score)}')
        self.setWindowTitle('Score')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    while True:
        ex = MainWindow()
        ex.show()
        sys.excepthook = except_hook
        app.exec_()
        pygame.init()
        game = Game()
        game.run()
        pygame.quit()

        with open("raiting.json", encoding="utf8") as f:
            f = json.load(f)
            if user_name not in f.keys() or f[user_name] < game.score:
                f[user_name] = game.score
        with open("raiting.json", "w", encoding='utf8') as file:
            json.dump(f, file)

        ending = Ending(game.score)
        ending.show()
        app.exec_()
