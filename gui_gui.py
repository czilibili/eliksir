from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime
import sys
from dodaj_baze import SkulKwery
import przelew_gui



class GuiPrzelew(QDialog, przelew_gui.Ui_CzasPrzelewu):

    def __init__(self):

        QDialog.__init__(self)

        self.setupUi(self)

        self.butt_close.clicked.connect(self.close)
        self.butt_ok.clicked.connect(self.show_results)
        self.timeEdit.timeChanged.connect(self.set_hour)
        self.bank_odbiorca.activated.connect(self.set_bank_in)
        self.bank_nadawca.activated.connect(self.set_bank_out)

        self.database_connection = SkulKwery()
        self.banks_list = self.database_connection.wyświetl_banki()

        self.bank_nadawca.addItems(self.banks_list)
        self.bank_odbiorca.addItems(self.banks_list)

        self.timeEdit.setTime(QTime(datetime.now().hour, datetime.now().minute))
        self.bank_odbiorca.setCurrentIndex(20)
        self.bank_nadawca.setCurrentIndex(24)

        self.bank_in = "Nest Bank"
        self.bank_out = "Raiffeisen Polbank"

        # these is a section of atributes which are later are to be created
        # to do some comparing operations inside functions D2,D1,D0
        # they are time objects
        self.cash_order_time_string = self.set_cash_order_time_str()
        self.cash_travel_times = None
        self.cash_transfer_order_time = None
        self.bank_cash_release_time = None
        self.kir_cash_release_time = None
        self.bank_cash_receipt_time = None

    def set_hour(self, time):
        """It handles signal sent by PyQtTimeEdit object and sets one of class attributes"""
        self.cash_order_time_string = time.toString("h:mm")

    def set_bank_in(self):
        """It handles connection to signal sent by PyQtComboList object and sets one of class attributes"""
        self.bank_in = self.bank_odbiorca.currentText()

    def set_bank_out(self):
        """It handles connection to signal sent by PyQtComboList object and sets one of class attributes"""
        self.bank_out = self.bank_nadawca.currentText()

    def format_cash_travel_times(self):
        """It takes strings which represent times set by sql_request function, and converts them into time objects
        to be used by functions D0, D1, D2
        """
        self.bank_cash_release_time, self.kir_cash_release_time, self.bank_cash_receipt_time = \
            tuple(map(self.str_to_time, self.cash_travel_times))

        self.cash_transfer_order_time = self.str_to_time(self.cash_order_time_string)

    def str_to_time(self, time_string):
        """Takes string representing time in format '%H:%M'
        Returns time object"""
        return datetime.strptime(time_string, "%H:%M").time()

    def set_cash_order_time_str(self):
        return datetime.now().strftime("%H:%M")

    def sql_request(self):
        """It connects to database and queries for cash travel times, returns three-element tuple, sets one of class
        attributes.
        """
        self.cash_travel_times = self.database_connection.zapytanie\
            (self.cash_order_time_string, self.bank_out, self.bank_in)

    def is_day_after_tomorrow_transfer(self):
        """Checks if money are received day after tomorrow, return True if yes
        """
        return True if all({self.cash_transfer_order_time > self.bank_cash_release_time,
                            self.bank_cash_receipt_time > self.kir_cash_release_time,
                            self.kir_cash_release_time > self.bank_cash_receipt_time}) else False

    def is_tomorrow_transfer(self):
        """Checks if money are received tomorrow, return True if yes
        """
        return True if all({self.cash_transfer_order_time > self.kir_cash_release_time,
                            self.bank_cash_receipt_time > self.kir_cash_release_time}) else False

    def is_today_transfer(self):
        """Checks if money are received today, return True if yes
        """
        return True if all({self.cash_transfer_order_time < self.bank_cash_release_time,
                            self.bank_cash_release_time < self.kir_cash_release_time,
                            self.kir_cash_release_time < self.bank_cash_receipt_time}) else False

    def transfer_message(self):
        """Returns correct time transfer message, there might be only one correct transfer message"""
        return {self.is_today_transfer(): "dzisiaj", self.is_tomorrow_transfer(): "w najbliższym dniu roboczym",
                self.is_day_after_tomorrow_transfer(): "za dwa dni robocze"}[True]

    def show_results(self):
        """Displays result in QtMessageBox with correct communicate
        """

        # Run database queries. Set class attributes.
        self.sql_request()

        # Format cash travel times into time objects. Set class attributes.
        self.format_cash_travel_times()

        # Pop up message box with results. Format message with hour and correct time adverb (check transfer_message()).
        QMessageBox.information(
                                self,
                                "TP",
                                "Przelew zostanie zaksiegowany {today_tomorrow} o godzinie {time_receipt}"
                                .format(time_receipt=self.cash_travel_times[2], today_tomorrow=self.transfer_message())
                                )

        # Set default settings in app window
        self.timeEdit.setTime(QTime(datetime.now().hour, datetime.now().minute))
        self.bank_odbiorca.setCurrentIndex(20)
        self.bank_nadawca.setCurrentIndex(24)
