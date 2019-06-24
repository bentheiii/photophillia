import json
from traceback import format_exc

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QMessageBox, QPushButton

from photophillia import PhotophilliaProject, ProjectManager


class GetProject(QWidget):
    submit = Signal(PhotophilliaProject, str)

    def try_open(self, path):
        try:
            with PhotophilliaProject.open(path) as read:
                proj = PhotophilliaProject.from_dict(json.load(read))
        except Exception as e:
            QMessageBox.warning(self, 'error opening file', format_exc())
        else:
            self.submit.emit(proj, path)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        new_btn = QPushButton('Create New Project')

        @new_btn.clicked.connect
        def _(*args):
            path, _ = QFileDialog.getSaveFileName(self, 'create a new manager',
                                                  filter='photphillia project (*.zip *.zpj *.json *.ppj)'
                                                         ';;all files (*.*)')
            if not path:
                return
            self.submit.emit(PhotophilliaProject(), path)

        main_layout.addWidget(new_btn)

        load_btn = QPushButton('Open Project')

        @load_btn.clicked.connect
        def _(*args):
            path, _ = QFileDialog.getOpenFileName(self, 'Open a Project',
                                                  filter='photphillia project (*.json *.ppj *.zip *.zpj)'
                                                         ';;all files (*.*)')
            if not path:
                return

            self.try_open(path)

        main_layout.addWidget(load_btn)
        self.setLayout(main_layout)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    gp = GetProject()
    m = None


    @gp.submit.connect
    def _(*args):
        global m
        print(args)
        p, _ = args
        m = ProjectManager(p)
        print(m)
        print(len(m._jobs_to_to))


    gp.show()
    app.exec_()
    print(m)
