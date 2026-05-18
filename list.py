import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QFrame, QLabel, QVBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt


class ReservationDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reservation Dashboard")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: #f5f7fb;")

        # ================= MAIN LAYOUT =================
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= CONTENT =================
        content = QFrame()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 15, 20, 15)
        content_layout.setSpacing(10)

        main_layout.addWidget(content)

        # ================= HEADER =================
        header = QLabel("4 Properties")
        header.setStyleSheet("font-size:18px; font-weight:bold; color:#222;")
        content_layout.addWidget(header)

        # ================= TABLE =================
        self.table = QTableWidget()
        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "Room",
            "Guest name",
            "No. guest",
            "Check-in",
            "Phone Number",
            "Revenue",
            "Booking code",
            "Status"
        ])

        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: none;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background: #f1f3f6;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #333;
            }
        """)

        # ================= COLUMN WIDTH ADJUSTMENT =================
        self.table.setColumnWidth(0, 160)  # Room (longer)
        self.table.setColumnWidth(1, 260)  # Guest name (longer)

        # ================= SAMPLE DATA =================
        data = [
            ["NT 401", "Joaquin Phoenix", "2", "Oct 19",
                "09123456789", "$139", "HMAB9F9JHZ", "Accepted"],
            ["NT 301", "Ahmed Avanoglu", "2", "Oct 15",
                "09876543210", "$169", "2853941056", "Pending"],
            ["NT 201", "Trung Le", "1", "Oct 16",
                "09112223344", "$239", "3153403385", "Accepted"],
        ]

        self.table.setRowCount(len(data))

        for r, row in enumerate(data):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(val))

        content_layout.addWidget(self.table)


# ================= RUN =================
app = QApplication(sys.argv)
window = ReservationDashboard()
window.show()
app.exec()
