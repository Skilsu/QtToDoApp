import os
import pickle
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt


class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 400, 400)

        # Create widgets
        self.task_input = QLineEdit()

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)

        self.task_list = QListWidget()

        self.complete_button = QPushButton("Mark Completed")
        self.complete_button.clicked.connect(self.mark_completed)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.clicked.connect(self.delete_task)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Add Task:"))
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_button)
        layout.addWidget(QLabel("To-Do List:"))
        layout.addWidget(self.task_list)
        layout.addWidget(self.complete_button)
        layout.addWidget(self.delete_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_task(self):
        text = self.task_input.text()
        if text:
            item = QListWidgetItem(text)  # Create a QListWidgetItem with the task text
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # Allow item to be checkable
            item.setCheckState(Qt.Unchecked)  # Set the initial check state to unchecked
            self.task_list.addItem(item)  # Add the item to the list widget
            self.task_input.clear()

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))

    def mark_completed(self):
        selected_items = self.task_list.selectedItems()  # Get the selected items from the list widget
        for item in selected_items:
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)  # Mark item as unchecked (incompleted)
            else:
                item.setCheckState(Qt.Checked)  # Mark item as checked (completed)

    def save_list_to_file(self):
        tasks = [(self.task_list.item(index).text(), self.task_list.item(index).checkState() == Qt.Checked)
                 for index in range(self.task_list.count())]
        with open("data/tasks.pkl", 'wb') as f:
            pickle.dump(tasks, f)

    def load_list_from_file(self):
        with open("data/tasks.pkl", 'rb') as f:
            tasks = pickle.load(f)
            for task_text, checked in tasks:
                item = QListWidgetItem(task_text)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked if checked else Qt.Unchecked)
                self.task_list.addItem(item)


def main():
    app = QApplication(sys.argv)
    todo_app = ToDoApp()
    if os.path.exists("data/tasks.pkl"):
        todo_app.load_list_from_file()
    app.aboutToQuit.connect(todo_app.save_list_to_file)
    todo_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
