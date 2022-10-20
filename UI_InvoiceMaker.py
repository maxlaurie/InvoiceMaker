# UI_InvoiceMaker.py
# Version 1.0
# Max Laurie 18/10/2022

# Generates an invoice from the GUI form/config.ini

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QRadioButton
from configparser import ConfigParser
from PIL import Image, ImageDraw, ImageFont
import time
import re
import sys
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 1070)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.527, y1:0, x2:0.53202, y2:0.261364, stop:0 rgba(194, 255, 244, 255), stop:1 rgba(91, 217, 184, 255));")

        parsed_config = self.config_parse()

        # Style Sheets

        label_style_sheet = ("background-color: rgba(255, 255, 255, 0);")
        box_style_sheet = ("background-color: rgb(255, 255, 255);selection-background-color: rgb(78, 193, 207);color: rgb(77, 77, 77);")

        small_boxes_font = QtGui.QFont()
        small_boxes_font.setPointSize(13)
        small_boxes_font.setFamily(".AppleSystemUIFont")
        small_boxes_left_alignment = (QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        small_boxes_right_alignment = (QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        # Company Logo

        self.company_logo = QtWidgets.QLabel(MainWindow)
        self.company_logo.setGeometry(QtCore.QRect(20, 20, 760, 140))
        self.company_logo.setStyleSheet(label_style_sheet)
        self.company_logo.setPixmap(QtGui.QPixmap("bits/GuiBanner.png"))
        self.company_logo.setScaledContents(True)

        # Company Name

        self.company_name_label = QtWidgets.QLabel(MainWindow)
        self.company_name_label.setGeometry(QtCore.QRect(20, 180, 101, 16))
        self.company_name_label.setStyleSheet(label_style_sheet)
        self.company_name_box = QtWidgets.QLineEdit(MainWindow)
        self.company_name_box.setGeometry(QtCore.QRect(20, 200, 261, 32))
        self.company_name_box.setFont(small_boxes_font)
        self.company_name_box.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.company_name_box.setStyleSheet(box_style_sheet)
        self.company_name_box.setText(parsed_config["company_name"])
        self.company_name_box.setMaxLength(38)
        self.company_name_box.setCursorPosition(0)
        self.company_name_box.setAlignment(small_boxes_left_alignment)

        # Company Address

        self.company_address_label = QtWidgets.QLabel(MainWindow)
        self.company_address_label.setGeometry(QtCore.QRect(20, 244, 111, 16))
        self.company_address_label.setStyleSheet(label_style_sheet)
        self.company_address_box = QtWidgets.QTextEdit(MainWindow)
        self.company_address_box.setGeometry(QtCore.QRect(20, 270, 361, 91))
        self.company_address_box.setFont(small_boxes_font)
        self.company_address_box.setStyleSheet(box_style_sheet)
        self.company_address_box.acceptRichText()
        self.company_address_box.setText(parsed_config["company_address"])

        # Company Email

        self.company_email_label = QtWidgets.QLabel(MainWindow)
        self.company_email_label.setGeometry(QtCore.QRect(20, 380, 151, 16))
        self.company_email_label.setStyleSheet(label_style_sheet)
        self.company_email_box = QtWidgets.QLineEdit(MainWindow)
        self.company_email_box.setGeometry(QtCore.QRect(20, 400, 261, 32))
        self.company_email_box.setFont(small_boxes_font)
        self.company_email_box.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.company_email_box.setStyleSheet(box_style_sheet)
        self.company_email_box.setText(parsed_config["company_email"])
        self.company_email_box.setMaxLength(38)
        self.company_email_box.setCursorPosition(0)
        self.company_email_box.setAlignment(small_boxes_left_alignment)

        # Company Bank Name

        self.company_bank_name_label = QtWidgets.QLabel(MainWindow)
        self.company_bank_name_label.setGeometry(QtCore.QRect(530, 180, 131, 16))
        self.company_bank_name_label.setStyleSheet(label_style_sheet)
        self.company_bank_name_label.setAlignment(small_boxes_right_alignment)
        self.company_bank_name_box = QtWidgets.QLineEdit(MainWindow)
        self.company_bank_name_box.setGeometry(QtCore.QRect(670, 170, 111, 32))
        self.company_bank_name_box.setFont(small_boxes_font)
        self.company_bank_name_box.setStyleSheet(box_style_sheet)
        self.company_bank_name_box.setText(parsed_config["bank_name"])
        self.company_bank_name_box.setMaxLength(20)
        self.company_bank_name_box.setAlignment(small_boxes_right_alignment)

        # Company Bank No

        self.company_bank_account_no_label = QtWidgets.QLabel(MainWindow)
        self.company_bank_account_no_label.setGeometry(QtCore.QRect(580, 220, 111, 16))
        self.company_bank_account_no_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.company_bank_account_no_label.setStyleSheet(label_style_sheet)
        self.company_bank_account_no_label.setAlignment(small_boxes_right_alignment)
        self.company_bank_account_no_box = QtWidgets.QLineEdit(MainWindow)
        self.company_bank_account_no_box.setGeometry(QtCore.QRect(700, 210, 81, 32))
        self.company_bank_account_no_box.setFont(small_boxes_font)
        self.company_bank_account_no_box.setStyleSheet(box_style_sheet)
        self.company_bank_account_no_box.setText(parsed_config["account_no"])
        self.company_bank_account_no_box.setMaxLength(8)
        self.company_bank_account_no_box.setAlignment(small_boxes_right_alignment)

        # Company Bank Sort Code

        self.company_bank_sort_code_label = QtWidgets.QLabel(MainWindow)
        self.company_bank_sort_code_label.setGeometry(QtCore.QRect(580, 260, 111, 16))
        self.company_bank_sort_code_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.company_bank_sort_code_label.setStyleSheet(label_style_sheet)
        self.company_bank_sort_code_label.setAlignment(small_boxes_right_alignment)
        self.company_bank_sort_code_box = QtWidgets.QLineEdit(MainWindow)
        self.company_bank_sort_code_box.setGeometry(QtCore.QRect(700, 250, 81, 32))
        self.company_bank_sort_code_box.setFont(small_boxes_font)
        self.company_bank_sort_code_box.setStyleSheet(box_style_sheet)
        self.company_bank_sort_code_box.setText(parsed_config["sort_code"])
        self.company_bank_sort_code_box.setMaxLength(8)
        self.company_bank_sort_code_box.setAlignment(small_boxes_right_alignment)

        # Transaction Currency

        self.transaction_currency_label = QtWidgets.QLabel(MainWindow)
        self.transaction_currency_label.setGeometry(QtCore.QRect(610, 300, 131, 16))
        self.transaction_currency_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.transaction_currency_label.setStyleSheet(label_style_sheet)
        self.transaction_currency_label.setAlignment(small_boxes_right_alignment)
        self.transaction_currency_box = QtWidgets.QLineEdit(MainWindow)
        self.transaction_currency_box.setGeometry(QtCore.QRect(750, 290, 32, 32))
        self.transaction_currency_box.setFont(small_boxes_font)
        self.transaction_currency_box.setStyleSheet(box_style_sheet)
        self.transaction_currency_box.setText(parsed_config["currency"])
        self.transaction_currency_box.setMaxLength(2)
        self.transaction_currency_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Company Phone No

        self.company_phone_no_label = QtWidgets.QLabel(MainWindow)
        self.company_phone_no_label.setGeometry(QtCore.QRect(520, 340, 131, 16))
        self.company_phone_no_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.company_phone_no_label.setStyleSheet(label_style_sheet)
        self.company_phone_no_label.setAlignment(small_boxes_right_alignment)
        self.company_phone_no_box = QtWidgets.QLineEdit(MainWindow)
        self.company_phone_no_box.setGeometry(QtCore.QRect(660, 330, 121, 32))
        self.company_phone_no_box.setFont(small_boxes_font)
        self.company_phone_no_box.setStyleSheet(box_style_sheet)
        self.company_phone_no_box.setText(parsed_config["company_phone"])
        self.company_phone_no_box.setMaxLength(15)
        self.company_phone_no_box.setAlignment(small_boxes_right_alignment)

        # Company Website URL

        self.company_website_label = QtWidgets.QLabel(MainWindow)
        self.company_website_label.setGeometry(QtCore.QRect(640, 380, 141, 16))
        self.company_website_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.company_website_label.setStyleSheet(label_style_sheet)
        self.company_website_label.setAlignment(small_boxes_right_alignment)
        self.company_website_box = QtWidgets.QLineEdit(MainWindow)
        self.company_website_box.setGeometry(QtCore.QRect(520, 400, 261, 32))
        self.company_website_box.setFont(small_boxes_font)
        self.company_website_box.setStyleSheet(box_style_sheet)
        self.company_website_box.setText(parsed_config["company_website"])
        self.company_website_box.setMaxLength(41)
        self.company_website_box.setAlignment(small_boxes_right_alignment)

        # Payment Terms

        self.payment_terms_label = QtWidgets.QLabel(MainWindow)
        self.payment_terms_label.setGeometry(QtCore.QRect(640, 440, 141, 16))
        self.payment_terms_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.payment_terms_label.setStyleSheet(label_style_sheet)
        self.payment_terms_label.setAlignment(small_boxes_right_alignment)
        self.payment_terms_box = QtWidgets.QLineEdit(MainWindow)
        self.payment_terms_box.setGeometry(QtCore.QRect(520, 460, 261, 32))
        self.payment_terms_box.setFont(small_boxes_font)
        self.payment_terms_box.setStyleSheet(box_style_sheet)
        self.payment_terms_box.setText(parsed_config["payment_terms"])
        self.payment_terms_box.setMaxLength(41)
        self.payment_terms_box.setAlignment(small_boxes_right_alignment)

        # Footer Message

        self.footer_message_label = QtWidgets.QLabel(MainWindow)
        self.footer_message_label.setGeometry(QtCore.QRect(20, 440, 101, 16))
        self.footer_message_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.footer_message_label.setStyleSheet(label_style_sheet)
        self.footer_message_label.setAlignment(small_boxes_left_alignment)
        self.footer_message_box = QtWidgets.QLineEdit(MainWindow)
        self.footer_message_box.setGeometry(QtCore.QRect(20, 460, 361, 32))
        self.footer_message_box.setFont(small_boxes_font)
        self.footer_message_box.setStyleSheet(box_style_sheet)
        self.footer_message_box.setText(parsed_config["footer_message"])
        self.footer_message_box.setMaxLength(41)
        self.footer_message_box.setAlignment(small_boxes_left_alignment)

        # Client Details

        self.client_details_label = QtWidgets.QLabel(MainWindow)
        self.client_details_label.setGeometry(QtCore.QRect(20, 510, 91, 16))
        self.client_details_label.setStyleSheet(label_style_sheet)
        self.client_details_box = QtWidgets.QPlainTextEdit(MainWindow)
        self.client_details_box.setGeometry(QtCore.QRect(20, 540, 361, 91))
        self.client_details_box.setFont(small_boxes_font)
        self.client_details_box.setStyleSheet(box_style_sheet)
        self.client_details_box.setPlainText("")

        # Invoice No

        self.invoice_no_label = QtWidgets.QLabel(MainWindow)
        self.invoice_no_label.setGeometry(QtCore.QRect(590, 560, 81, 31))
        self.invoice_no_label.setStyleSheet(label_style_sheet)
        self.invoice_no_label.setAlignment(small_boxes_right_alignment)
        self.invoice_no_box = QtWidgets.QLineEdit(MainWindow)
        self.invoice_no_box.setGeometry(QtCore.QRect(690, 560, 91, 31))
        self.invoice_no_box.setFont(small_boxes_font)
        self.invoice_no_box.setStyleSheet(box_style_sheet)
        self.invoice_no_box.setText(self.pad_and_advance_invoice_no(True))
        self.invoice_no_box.setMaxLength(12)
        self.invoice_no_box.setAlignment(small_boxes_right_alignment)

        # Date

        self.date_label = QtWidgets.QLabel(MainWindow)
        self.date_label.setGeometry(QtCore.QRect(590, 600, 81, 31))
        self.date_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.date_label.setStyleSheet(label_style_sheet)
        self.date_label.setAlignment(small_boxes_right_alignment)
        self.date_box = QtWidgets.QLineEdit(MainWindow)
        self.date_box.setGeometry(QtCore.QRect(690, 600, 91, 31))
        self.date_box.setFont(small_boxes_font)
        self.date_box.setStyleSheet(box_style_sheet)
        self.date_box.setText(time.strftime("%d/%m/%Y"))
        self.date_box.setMaxLength(12)
        self.date_box.setAlignment(small_boxes_right_alignment)


        # Item Description Boxes

        description_box_font = QtGui.QFont()
        description_box_font.setPointSize(16)
        description_box_max_length = 75

        self.description_label = QtWidgets.QLabel(MainWindow)
        self.description_label.setGeometry(QtCore.QRect(20, 660, 91, 16))
        self.description_label.setStyleSheet(label_style_sheet)

        self.invoice_item_desc_box_1 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_desc_box_1.setGeometry(QtCore.QRect(20, 690, 581, 41))
        self.invoice_item_desc_box_1.setFont(description_box_font)
        self.invoice_item_desc_box_1.setStyleSheet(box_style_sheet)
        self.invoice_item_desc_box_1.setMaxLength(description_box_max_length)

        self.invoice_item_desc_box_2 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_desc_box_2.setGeometry(QtCore.QRect(20, 740, 581, 41))
        self.invoice_item_desc_box_2.setFont(description_box_font)
        self.invoice_item_desc_box_2.setStyleSheet(box_style_sheet)
        self.invoice_item_desc_box_2.setMaxLength(description_box_max_length)

        self.invoice_item_desc_box_3 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_desc_box_3.setGeometry(QtCore.QRect(20, 790, 581, 41))
        self.invoice_item_desc_box_3.setFont(description_box_font)
        self.invoice_item_desc_box_3.setStyleSheet(box_style_sheet)
        self.invoice_item_desc_box_3.setMaxLength(description_box_max_length)

        self.invoice_item_desc_box_4 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_desc_box_4.setGeometry(QtCore.QRect(20, 840, 581, 41))
        self.invoice_item_desc_box_4.setFont(description_box_font)
        self.invoice_item_desc_box_4.setStyleSheet(box_style_sheet)
        self.invoice_item_desc_box_4.setMaxLength(description_box_max_length)

        self.invoice_item_desc_box_5 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_desc_box_5.setGeometry(QtCore.QRect(20, 890, 581, 41))
        self.invoice_item_desc_box_5.setFont(description_box_font)
        self.invoice_item_desc_box_5.setStyleSheet(box_style_sheet)
        self.invoice_item_desc_box_5.setMaxLength(description_box_max_length)

        self.invoice_item_desc_box_6 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_desc_box_6.setGeometry(QtCore.QRect(20, 940, 581, 41))
        self.invoice_item_desc_box_6.setFont(description_box_font)
        self.invoice_item_desc_box_6.setStyleSheet(box_style_sheet)
        self.invoice_item_desc_box_6.setMaxLength(description_box_max_length)

        # Item Total Boxes

        total_box_font = QtGui.QFont()
        total_box_font.setPointSize(16)
        total_box_max_length = 12

        big_total_box_font = QtGui.QFont()
        big_total_box_font.setPointSize(19)
        big_total_box_max_length = 10

        total_boxes_alignment = (QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.total_label = QtWidgets.QLabel(MainWindow)
        self.total_label.setGeometry(QtCore.QRect(720, 660, 61, 20))
        self.total_label.setStyleSheet(label_style_sheet)
        self.total_label.setAlignment(total_boxes_alignment)

        self.invoice_item_total_box_1 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_total_box_1.setGeometry(QtCore.QRect(660, 690, 121, 41))
        self.invoice_item_total_box_1.setFont(total_box_font)
        self.invoice_item_total_box_1.setStyleSheet(box_style_sheet)
        self.invoice_item_total_box_1.setMaxLength(total_box_max_length)
        self.invoice_item_total_box_1.setAlignment(total_boxes_alignment)

        self.invoice_item_total_box_2 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_total_box_2.setGeometry(QtCore.QRect(660, 740, 121, 41))
        self.invoice_item_total_box_2.setFont(total_box_font)
        self.invoice_item_total_box_2.setStyleSheet(box_style_sheet)
        self.invoice_item_total_box_2.setMaxLength(total_box_max_length)
        self.invoice_item_total_box_2.setAlignment(total_boxes_alignment)

        self.invoice_item_total_box_3 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_total_box_3.setGeometry(QtCore.QRect(660, 790, 121, 41))
        self.invoice_item_total_box_3.setFont(total_box_font)
        self.invoice_item_total_box_3.setStyleSheet(box_style_sheet)
        self.invoice_item_total_box_3.setMaxLength(total_box_max_length)
        self.invoice_item_total_box_3.setAlignment(total_boxes_alignment)

        self.invoice_item_total_box_4 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_total_box_4.setGeometry(QtCore.QRect(660, 840, 121, 41))
        self.invoice_item_total_box_4.setFont(total_box_font)
        self.invoice_item_total_box_4.setStyleSheet(box_style_sheet)
        self.invoice_item_total_box_4.setMaxLength(total_box_max_length)
        self.invoice_item_total_box_4.setAlignment(total_boxes_alignment)

        self.invoice_item_total_box_5 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_total_box_5.setGeometry(QtCore.QRect(660, 890, 121, 41))
        self.invoice_item_total_box_5.setFont(total_box_font)
        self.invoice_item_total_box_5.setStyleSheet(box_style_sheet)
        self.invoice_item_total_box_5.setMaxLength(total_box_max_length)
        self.invoice_item_total_box_5.setAlignment(total_boxes_alignment)

        self.invoice_item_total_box_6 = QtWidgets.QLineEdit(MainWindow)
        self.invoice_item_total_box_6.setGeometry(QtCore.QRect(660, 940, 121, 41))
        self.invoice_item_total_box_6.setFont(total_box_font)
        self.invoice_item_total_box_6.setStyleSheet(box_style_sheet)
        self.invoice_item_total_box_6.setMaxLength(total_box_max_length)
        self.invoice_item_total_box_6.setAlignment(total_boxes_alignment)

        self.invoice_total_total_box = QtWidgets.QLineEdit(MainWindow)
        self.invoice_total_total_box.setGeometry(QtCore.QRect(660, 1000, 121, 51))
        self.invoice_total_total_box.setFont(big_total_box_font)
        self.invoice_total_total_box.setStyleSheet(box_style_sheet)
        self.invoice_total_total_box.setText(self.transaction_currency_box.text() + "0.00")
        self.invoice_total_total_box.setMaxLength(big_total_box_max_length)
        self.invoice_total_total_box.setAlignment(total_boxes_alignment)

        # Buttons

        radio_button_style_sheet = ("background-color: rgba(194, 255, 244, 0);color: rgb(77, 77, 77);")

        self.format_selector_png = QRadioButton(MainWindow)
        self.format_selector_png.setGeometry(QtCore.QRect(260, 1000, 61, 20))
        self.format_selector_png.setStyleSheet(radio_button_style_sheet)
        self.format_selector_png.setChecked(False)
        
        self.format_selector_pdf = QRadioButton(MainWindow)
        self.format_selector_pdf.setGeometry(QtCore.QRect(340, 1000, 61, 20))
        self.format_selector_pdf.setStyleSheet(radio_button_style_sheet)
        self.format_selector_pdf.setChecked(True)
        
        self.format_selector_both = QRadioButton(MainWindow)
        self.format_selector_both.setGeometry(QtCore.QRect(420, 1000, 61, 20))
        self.format_selector_both.setStyleSheet(radio_button_style_sheet)
        self.format_selector_both.setChecked(False)

        button_style_sheet = ("background-color: rgba(194, 255, 244, 125);color: rgb(77, 77, 77);")

        self.clear_button = QtWidgets.QPushButton(MainWindow, clicked= lambda: self.clear_form())
        self.clear_button.setGeometry(QtCore.QRect(20, 1010, 100, 32))
        self.clear_button.setStyleSheet(button_style_sheet)

        self.next_invoice_button = QtWidgets.QPushButton(MainWindow, clicked= lambda: self.next_invoice())
        self.next_invoice_button.setGeometry(QtCore.QRect(140, 1010, 100, 32))
        self.next_invoice_button.setStyleSheet(button_style_sheet)

        self.calculate_total_button = QtWidgets.QPushButton(MainWindow, clicked= lambda: self.calculate_total(True))
        self.calculate_total_button.setGeometry(QtCore.QRect(500, 1010, 100, 32))
        self.calculate_total_button.setStyleSheet(button_style_sheet)

        self.generate_invoice_button = QtWidgets.QPushButton(MainWindow, clicked= lambda: self.generate_invoice())
        self.generate_invoice_button.setGeometry(QtCore.QRect(260, 1030, 221, 21))
        self.generate_invoice_button.setStyleSheet(button_style_sheet)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Invoice Maker"))

        self.invoice_no_label.setText(_translate("MainWindow", "Invoice No."))
        self.date_label.setText(_translate("MainWindow", "Date"))
        self.client_details_label.setText(_translate("MainWindow", "Client Details"))
        self.description_label.setText(_translate("MainWindow", "Description"))
        self.total_label.setText(_translate("MainWindow", "Total"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.company_name_label.setText(_translate("MainWindow", "Company Name"))
        self.company_address_label.setText(_translate("MainWindow", "Company Address"))
        self.company_bank_account_no_label.setText(_translate("MainWindow", "Bank Account No."))
        self.company_bank_name_label.setText(_translate("MainWindow", "Company Bank Name"))
        self.company_bank_sort_code_label.setText(_translate("MainWindow", "Bank Sort Code"))
        self.transaction_currency_label.setText(_translate("MainWindow", "Transaction Currency"))
        self.footer_message_label.setText(_translate("MainWindow", "Footer Message"))
        self.company_phone_no_label.setText(_translate("MainWindow", "Company Phone No."))
        self.company_website_label.setText(_translate("MainWindow", "Company Website URL"))
        self.payment_terms_label.setText(_translate("MainWindow", "Payment Terms"))
        self.company_email_label.setText(_translate("MainWindow", "Company Email Address"))
        self.next_invoice_button.setText(_translate("MainWindow", "Next Invoice"))
        self.calculate_total_button.setText(_translate("MainWindow", "Calculate Total"))
        self.generate_invoice_button.setText(_translate("MainWindow", "Generate!"))
        self.format_selector_png.setText(_translate("MainWindow", "PNG"))
        self.format_selector_pdf.setText(_translate("MainWindow", "PDF"))
        self.format_selector_both.setText(_translate("MainWindow", "BOTH"))



    ############################################################
    # Class functions
    ############################################################

    def config_parse(self):
        '''Returns a dictionary containing the parsed contents of config.ini'''
        config = ConfigParser()
        config.read("config.ini")
        config.sections()
        return {
                "invoice_number": config["invoice"]["last_number"],
                "company_name": config["user_info"]["company_name"],
                "company_address": config["user_info"]["company_address"],
                "company_phone": config["user_info"]["company_phone"],
                "company_email": config["user_info"]["company_email"],
                "company_website": config["user_info"]["company_website"],
                "footer_message": config["user_info"]["footer_message"],
                "bank_name": config["payment_info"]["bank_name"],
                "account_no": config["payment_info"]["account_no"],
                "sort_code": config["payment_info"]["sort_code"],
                "currency": config["payment_info"]["currency"],
                "payment_terms": config["payment_info"]["payment_terms"]
                }


    def update_config(self, section, subsection, value):
        '''Writes a new value into the config (config.ini)'''
        config = ConfigParser()
        config.read("config.ini")
        config.set(section, subsection, value)
        with open("config.ini", "w") as config_file:
            config.write(config_file)


    def pad_and_advance_invoice_no(self, from_config):
        '''Takes the invoice number from the config or the form and adds 1. ie 00123 -> 00124
            Then updates the config and returns the new number. If the number parsed (form or config)
            is blank, will return 00001.'''
        if from_config is True: 
            parsed_config = self.config_parse()
            invoice_no = parsed_config["invoice_number"]
        else:
            invoice_no = self.invoice_no_box.text()
        
        if invoice_no != "":
            next_invoice_int = int(invoice_no) + 1
            next_invoice_str = str(next_invoice_int).zfill(5)
            self.update_config("invoice", "last_number", next_invoice_str)
            return next_invoice_str
        else:
            next_invoice_str = "00001"
            self.update_config("invoice", "last_number", next_invoice_str)
            return next_invoice_str


    def clear_form(self):
        '''Clears and resets the below boxes in the gui'''
        boxes = [self.invoice_item_desc_box_1,
                self.invoice_item_desc_box_2,
                self.invoice_item_desc_box_3,
                self.invoice_item_desc_box_4,
                self.invoice_item_desc_box_5,
                self.invoice_item_desc_box_6,
                self.invoice_item_total_box_1,
                self.invoice_item_total_box_2,
                self.invoice_item_total_box_3,
                self.invoice_item_total_box_4,
                self.invoice_item_total_box_5,
                self.invoice_item_total_box_6]
        for box in boxes:
            box.setText("")

        self.client_details_box.setPlainText("")
        self.invoice_total_total_box.setText(self.transaction_currency_box.text() + "0.00")


    def next_invoice(self):
        '''Clears and resets the gui and advances the invoice number'''
        self.clear_form()
        self.invoice_no_box.setText(self.pad_and_advance_invoice_no(False))
        pass


    def calculate_total(self, change_box_text):
        '''Adds up the totals in the invoice items boxes. Will change the value
            in the invoice total total box if the change_box_text input is set to True'''
        totals = [self.invoice_item_total_box_1.text(),
                self.invoice_item_total_box_2.text(),
                self.invoice_item_total_box_3.text(),
                self.invoice_item_total_box_4.text(),
                self.invoice_item_total_box_5.text(),
                self.invoice_item_total_box_6.text()]
        calculated_total = 0.00
        for number in totals:
            if number != "":
                int_only = re.compile(r'[^\d.]+')
                int_only = int_only.sub("", number)
                try:
                    calculated_total = calculated_total + float(int_only)
                except ValueError:
                    calculated_total = 0.00
        formatted_total = "{}{:.2f}".format(self.transaction_currency_box.text(), calculated_total)
        
        if change_box_text is True:
            self.invoice_total_total_box.setText(formatted_total)
        else:
            return formatted_total


    def form_and_total_mismatch_check(self):
        '''Checks to see if the calculated total of the invoice item boxes match the value
            in the total total box. Will warn the user if there is a mismatch and give the
            choice to proceed or not'''
        calculated_total = self.calculate_total(False)
        if self.invoice_total_total_box.text() != calculated_total:
            box = QMessageBox()
            box.setWindowTitle("Invoice Maker")
            box.setText("Form and calculated total don't match, proceed with form total?")
            box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            box.setIcon(QMessageBox.Icon.Question)
            
            user_clicked = box.exec()
            
            if user_clicked == 16384: # Yes
                self.invoice_total = self.invoice_total_total_box.text()
                return True
            elif user_clicked == 65536: # No
                return False
        else:
            self.invoice_total = self.invoice_total_total_box.text()
            return True


    def save_file_dialog(self, format_choice):
        '''Generates a filename template and asks the user where they'd like to save the output file
            If the choice of output format is both png and pdf, the file selection only asks for a pdf filename
            Whatever the choice, the returned filename has no extension, so it can be added at time of file creation'''
        if format_choice == "BOTH":
            format_choice = "PDF"
        
        filename_template = (f"Invoice{self.invoice_no_box.text()}_"
                            f"{time.strftime('%d%m%Y', time.localtime(time.time()))}.{format_choice.casefold()}")
        output_filename = QFileDialog.getSaveFileName(None, "Save Invoice", filename_template,
                            f"{format_choice} Files (*.{format_choice.casefold()});;All Files (*)")
        if output_filename:
            return os.path.splitext(output_filename[0])[0]
        else:
            return


    def return_format_choice(self):
        '''Return the name of the selected format radio button'''
        for radio_button in (self.format_selector_png, self.format_selector_pdf, self.format_selector_both):
            if radio_button.isChecked():
                return radio_button.text()
        # if somehow none are selected
        return "BOTH"


    def generate_invoice(self):
        '''Final checks and the output file is generated'''
        if self.form_and_total_mismatch_check() is True:
            pass
        else:
            return

        format_choice = self.return_format_choice()
        output_filename = self.save_file_dialog(format_choice)
        if os.path.isdir(os.path.dirname(output_filename)):
            pass
        else:
            return

        match format_choice:
            case "PNG":
                png_filename = f"{output_filename}.png"
                self.generate_png(png_filename)

                self.success_dialog(png_filename)

            case "PDF":
                png_filename = f"{output_filename}.png"
                self.generate_png(png_filename)

                pdf_filename = f"{output_filename}.pdf"
                self.generate_pdf(png_filename, pdf_filename)
                
                os.remove(png_filename)
                self.success_dialog(pdf_filename)

            case "BOTH":
                png_filename = f"{output_filename}.png"
                self.generate_png(png_filename)

                pdf_filename = f"{output_filename}.pdf"
                self.generate_pdf(png_filename, pdf_filename)

                self.success_dialog(png_filename, pdf_filename)

        self.save_all_to_config()


    def generate_png(self, output_filename):
        '''Writes the information on to the template image and generates a PNG'''
        template_file = Image.open("bits/Invoice Template.png")
        
        text_to_add = self.gather_text()
        add_text = ImageDraw.Draw(template_file)
        
        for element in text_to_add:
            add_text.text(element.coordinates, element.text, font=element.font, fill=element.font_colour,
                          anchor=element.anchor, align=element.align)

        template_file.save(output_filename)


    def generate_pdf(self, output_png, output_pdf_filename):
        '''Creates a PDF from the PNG'''
        file_to_convert = Image.open(output_png)
        output_pdf = file_to_convert.convert('RGB')
        output_pdf.save(output_pdf_filename)


    def success_dialog(self, *files):
        '''Alerts the user to whether the output file(s) were created or not'''
        box = QMessageBox()
        box.setWindowTitle("Invoice Maker")
        box.setStandardButtons(QMessageBox.StandardButton.Ok)

        if len(files) > 1:
            plural_or_not = "Invoices"
        else:
            plural_or_not = "Invoice"

        for file in files:
            if os.path.isfile(file):
                box.setText(f"{plural_or_not} generated!")
                box.setIcon(QMessageBox.Icon.Information)
            else:
                box.setText(f"Unable to generate {plural_or_not.casefold()} :(")
                box.setIcon(QMessageBox.Icon.Critical)
                break

        box.exec()


    def save_all_to_config(self):
        '''Takes all the below values from the gui and updates the config'''
        self.update_config("invoice", "last_number", self.invoice_no_box.text())

        self.update_config("user_info", "company_name", self.company_name_box.text())
        self.update_config("user_info", "company_address", self.company_address_box.toPlainText())
        self.update_config("user_info", "company_phone", self.company_phone_no_box.text())
        self.update_config("user_info", "company_email", self.company_email_box.text())
        self.update_config("user_info", "company_website", self.company_website_box.text())
        self.update_config("user_info", "footer_message", self.footer_message_box.text())
        
        self.update_config("payment_info", "bank_name", self.company_bank_name_box.text())
        self.update_config("payment_info", "account_no", self.company_bank_account_no_box.text())
        self.update_config("payment_info", "sort_code", self.company_bank_sort_code_box.text())
        self.update_config("payment_info", "currency", self.transaction_currency_box.text())
        self.update_config("payment_info", "payment_terms", self.payment_terms_box.text())


    def gather_text(self):
        '''Collates all the text that will go on to the output file in to a list'''
        parsed_config = self.config_parse()

        title = TextLayer("INVOICE", (408, 577), "mm", "center", "bold", 65, "white")
        
        invoice_title = TextLayer("INVOICE", (2350, 856), "rs", "right", "bold", 43, "black")
        invoice_no = TextLayer(self.invoice_no_box.text(), (2350, 910), "rs", "right", "medium", 43, "black")

        date_title = TextLayer("DATE", (2350, 1077), "rs", "right", "bold", 43, "black")
        invoice_date = TextLayer(self.date_box.text(), (2350, 1130), "rs", "right", "medium", 43, "black")

        description_title = TextLayer("DESCRIPTION", (130, 1320), "lm", "left", "bold", 43, "black")
        total_title = TextLayer("TOTAL", (2350, 1320), "rm", "right", "bold", 43, "black")
        
        payment_title = TextLayer("Payment via Bank Transfer", (100, 2828), "ls", "left", "medium", 50, "black")
        payment_details_formatted = (f"{self.company_bank_name_box.text()}\n"
                                    f"{self.company_bank_sort_code_box.text()}\n"
                                    f"{self.company_bank_account_no_box.text()}\n\n"
                                    f"{self.payment_terms_box.text()}")
        payment_details = TextLayer(payment_details_formatted, (100, 2880), "ls", "left", "medium", 40, "black")
        
        total_total_title = TextLayer("TOTAL", (2350, 2885), "rs", "right", "medium", 43, "white")
        total_total = TextLayer(self.invoice_total, (2350, 3000), "rs", "right", "medium", 65, "white")

        company_name = TextLayer(self.company_name_box.text(), (2350, 200), "rs", "right", "medium", 50, "white")
        company_details = (f"{self.company_address_box.toPlainText()}\n\n"
                            f"{self.company_email_box.text()}\n"
                            f"{self.company_phone_no_box.text()}")
        company_address = TextLayer(company_details, (2350, 280), "rs", "right", "medium", 40, "white")

        client_address = TextLayer(self.client_details_box.toPlainText(), (130, 910), "ls", "left", "medium", 43, "black")

        item_1_desc = TextLayer(self.invoice_item_desc_box_1.text(), (130, 1530), "ls", "left", "medium", 43, "black")
        item_2_desc = TextLayer(self.invoice_item_desc_box_2.text(), (130, 1730), "ls", "left", "medium", 43, "black")
        item_3_desc = TextLayer(self.invoice_item_desc_box_3.text(), (130, 1930), "ls", "left", "medium", 43, "black")
        item_4_desc = TextLayer(self.invoice_item_desc_box_4.text(), (130, 2130), "ls", "left", "medium", 43, "black")
        item_5_desc = TextLayer(self.invoice_item_desc_box_5.text(), (130, 2330), "ls", "left", "medium", 43, "black")
        item_6_desc = TextLayer(self.invoice_item_desc_box_6.text(), (130, 2530), "ls", "left", "medium", 43, "black")

        item_1_total = TextLayer(self.invoice_item_total_box_1.text(), (2350, 1530), "rs", "right", "medium", 43, "black")
        item_2_total = TextLayer(self.invoice_item_total_box_2.text(), (2350, 1730), "rs", "right", "medium", 43, "black")
        item_3_total = TextLayer(self.invoice_item_total_box_3.text(), (2350, 1930), "rs", "right", "medium", 43, "black")
        item_4_total = TextLayer(self.invoice_item_total_box_4.text(), (2350, 2130), "rs", "right", "medium", 43, "black")
        item_5_total = TextLayer(self.invoice_item_total_box_5.text(), (2350, 2330), "rs", "right", "medium", 43, "black")
        item_6_total = TextLayer(self.invoice_item_total_box_6.text(), (2350, 2530), "rs", "right", "medium", 43, "black")

        formatted_footer = (f"{self.footer_message_box.text()}\n"
                            f"{self.company_website_box.text()}")
        footer = TextLayer(formatted_footer, (1240, 3345), "mm", "center", "medium", 40, "black")


        return [title, invoice_title, invoice_no, date_title, invoice_date, description_title, total_title,
                payment_title, payment_details, total_total_title, total_total, company_name, company_address,
                client_address, item_1_desc, item_2_desc, item_3_desc, item_4_desc, item_5_desc, item_6_desc, 
                item_1_total, item_2_total, item_3_total, item_4_total, item_5_total, item_6_total, footer]


class TextLayer:
    def __init__(self, text, coordinates, anchor, align, font, font_size, font_colour):
        self.text = text
        self.coordinates = coordinates
        self.anchor = anchor
        self.align = align

        if font == "medium":
            self.font = ImageFont.truetype("bits/Font-Medium.ttf", font_size)
        elif font == "bold":
            self.font = ImageFont.truetype("bits/Font-Bold.ttf", font_size)

        if font_colour == "black":
            self.font_colour = (0, 0, 0)
        elif font_colour == "white":
            self.font_colour = (255, 255, 255)
