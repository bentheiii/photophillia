import json

from PySide2.QtCore import Signal, QSize, Qt, Qt
from PySide2.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy, \
    QLabel, QFileDialog

from photophillia import PhotophilliaProject, ProjectManager
from photophillia_manager.analysis import ProjectAnalysisWindow


class ManagerWidget(QWidget):
    manager: ProjectManager
    save_path: str

    back = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        sp = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        esp = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        main_layout = QGridLayout()

        stats_btn = QPushButton('stats', sizePolicy=sp)
        main_layout.addWidget(stats_btn, 0, 0, 2, 1)

        @stats_btn.clicked.connect
        def _(*args):
            dialog = ProjectAnalysisWindow(self.manager, self, Qt.WindowFlags(Qt.Dialog))
            dialog.show()

        start_pos_btn = QPushButton('Begin Positioning',
                                    sizePolicy=QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))
        main_layout.addWidget(start_pos_btn, 0, 1, 1, 3)

        save_btn = QPushButton('Save As', sizePolicy=sp)
        main_layout.addWidget(save_btn, 2, 0)

        @save_btn.clicked.connect
        def _(*args):
            path, _ = QFileDialog.getSaveFileName(self, 'Save As...',
                                                  filter='photphillia project (*.zip *.zpj *.json *.ppj)'
                                                         ';;all files (*.*)')
            if not path:
                return
            with PhotophilliaProject.open(path, 'w') as write:
                json.dump(self.manager.project.to_dict(), write)

        back_btn = QPushButton('<- back', sizePolicy=sp)
        main_layout.addWidget(back_btn, 3, 0)

        @back_btn.clicked.connect
        def _(*args):
            self.back.emit()

        dnd_area = QLabel('Drag & Drop\nHere', alignment=Qt.AlignCenter, sizePolicy=esp)
        #dnd_area.setMinimumSize(QSize(100, 100))
        main_layout.addWidget(dnd_area, 1, 1, 3, 3)

        self.setLayout(main_layout)

    def set_project(self, project: PhotophilliaProject, path: str):
        self.manager = ProjectManager(project)
        self.save_path = path


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    mw = ManagerWidget()


    @mw.back.connect
    def _(*args):
        print(args)


    mw.show()
    app.exec_()
