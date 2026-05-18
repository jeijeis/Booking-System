from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QGridLayout, QVBoxLayout,
    QSpacerItem, QSizePolicy, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap
import sys


# ================= FIXED BANNER =================
class BannerLabel(QLabel):
    def __init__(self, image_path):
        super().__init__()
        self.pix = QPixmap(image_path)

        self.setFixedHeight(150)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #2c3e50;")

    def resizeEvent(self, event):
        if not self.pix.isNull():
            scaled = self.pix.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            rect = scaled.rect()
            x = (rect.width() - self.width()) // 2
            y = (rect.height() - self.height()) // 2

            cropped = scaled.copy(x, y, self.width(), self.height())
            self.setPixmap(cropped)

        super().resizeEvent(event)


class HotelReservation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reservation System")
        self.setGeometry(100, 100, 1100, 600)

        self.setStyleSheet("background-color: white; color: black;")

        INPUT_HEIGHT = 44
        DROPDOWN_HEIGHT = 46

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch(1)

        container = QWidget()
        container.setFixedWidth(900)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 15, 20, 15)
        container_layout.setSpacing(10)

        # ================= HEADER (FIXED) =================
        header = BannerLabel("ban.png")

        # ================= GRID =================
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(0)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        def input_field(label_text, placeholder):
            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setSpacing(6)
            layout.setContentsMargins(0, 0, 0, 0)

            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 14px; font-weight: 500;")

            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setFixedHeight(INPUT_HEIGHT)
            inp.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                    color: black;
                    background-color: white;
                }
            """)

            layout.addWidget(lbl)
            layout.addWidget(inp)
            return wrapper

        def dropdown_field(label_text):
            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setSpacing(6)
            layout.setContentsMargins(0, 0, 0, 0)

            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 14px; font-weight: 500;")

            combo = QComboBox()
            combo.setFixedHeight(DROPDOWN_HEIGHT)
            combo.setStyleSheet("""
                QComboBox {
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                    color: black;
                    background-color: white;
                }
            """)

            layout.addWidget(lbl)
            layout.addWidget(combo)
            return wrapper, combo

        def calendar_field(label_text):
            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setSpacing(6)
            layout.setContentsMargins(0, 0, 0, 0)

            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 14px; font-weight: 500;")

            date = QDateEdit()
            date.setCalendarPopup(True)
            date.setDate(QDate.currentDate())
            date.setDisplayFormat("MM/dd/yyyy")
            date.setFixedHeight(DROPDOWN_HEIGHT)
            date.setStyleSheet("""
                QDateEdit {
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                    color: black;
                    background-color: white;
                }
            """)

            layout.addWidget(lbl)
            layout.addWidget(date)
            return wrapper

        # ================= FIELDS =================
        service_wrapper, self.service = dropdown_field("Service")
        self.service.addItems(["Hotel Reservation", "Restaurant Reservation"])

        type_wrapper, self.type_box = dropdown_field("Room Type")

        guests = input_field("No. of Guests", "Enter number")
        time = input_field("Time", "HH:MM")
        arrival = calendar_field("Arrival Date")

        # ================= LOGIC =================
        def update_types():
            self.type_box.clear()
            if self.service.currentText() == "Hotel Reservation":
                self.type_box.addItems(["Standard", "Deluxe", "Suite"])
            else:
                self.type_box.addItems([
                    "Standard Table",
                    "Booth",
                    "Window Table",
                    "Private Room"
                ])

        self.service.currentIndexChanged.connect(update_types)
        update_types()

        # ================= ROW 1 =================
        grid.addWidget(service_wrapper, 0, 0)
        grid.addWidget(type_wrapper, 0, 1)
        grid.addWidget(guests, 0, 2)

        grid.addItem(QSpacerItem(
            0, 18, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 0)

        # ================= ROW 2 =================
        grid.addWidget(time, 2, 0)
        grid.addWidget(arrival, 2, 1)
        grid.addWidget(QWidget(), 2, 2)

        # ================= BUTTON =================
        submit = QPushButton("SUBMIT")
        submit.setFixedWidth(200)
        submit.setFixedHeight(45)
        submit.setStyleSheet("""
            QPushButton {
                background-color: #41A67E;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
        """)

        # ================= LAYOUT =================
        container_layout.addWidget(header)
        container_layout.addSpacing(60)
        container_layout.addLayout(grid)
        container_layout.addStretch(1)
        container_layout.addWidget(submit, alignment=Qt.AlignLeft)

        outer.addWidget(container, alignment=Qt.AlignCenter)
        outer.addStretch(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HotelReservation()
    window.show()
    sys.exit(app.exec())
