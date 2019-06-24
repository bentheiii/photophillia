from PySide2.QtWidgets import QWidget, QStackedLayout

from photophillia_manager.get_proj import GetProject
from photophillia_manager.manager_widget import ManagerWidget


class MainWidget(QWidget):
    def __init__(self, *args, proj_path = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui(proj_path)

    def setup_ui(self, proj_path = None):
        switch = QStackedLayout()

        get_proj = GetProject()
        manager_wig = ManagerWidget()

        switch.addWidget(get_proj)
        switch.addWidget(manager_wig)

        @get_proj.submit.connect
        def submit(proj, path):
            manager_wig.set_project(proj, path)
            switch.setCurrentWidget(manager_wig)

        @manager_wig.back.connect
        def back():
            switch.setCurrentWidget(get_proj)

        self.setLayout(switch)

        if proj_path:
            get_proj.try_open(proj_path)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    mw = MainWidget()

    mw.show()
    app.exec_()
