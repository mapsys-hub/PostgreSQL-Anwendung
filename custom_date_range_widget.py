from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QDateEdit, QCheckBox, QHBoxLayout, QWidget, \
    QVBoxLayout


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the table widget
        self.table = QTableWidget(1, 1)  # 1 row, 1 column
        self.table.setHorizontalHeaderLabels(['Date and Action'])

        # Create a QDateEdit widget and disable it initially
        self.date_edit = QDateEdit()
        self.date_edit.setEnabled(False)

        # Create a QCheckBox widget
        self.checkbox = QCheckBox()

        # Create a QWidget to hold both QDateEdit and QCheckBox in the same cell
        self.cell_widget = QWidget()
        self.cell_layout = QHBoxLayout(self.cell_widget)
        self.cell_layout.addWidget(self.date_edit)
        self.cell_layout.addWidget(self.checkbox)
        self.cell_layout.setContentsMargins(0, 0, 0, 0)
        self.cell_widget.setLayout(self.cell_layout)

        # Add the QWidget containing QDateEdit and QCheckBox to the table
        self.table.setCellWidget(0, 0, self.cell_widget)

        # Connect the checkbox's stateChanged signal to enable/disable the QDateEdit
        self.checkbox.stateChanged.connect(self.toggle_date_edit)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def toggle_date_edit(self, state):
        """Enable or disable the QDateEdit widget based on the checkbox state."""
        self.date_edit.setEnabled(self.checkbox.isChecked())


# Basic setup for the application
app = QApplication([])

# Create the main window and show it
window = TableWidget()
window.show()

app.exec()

