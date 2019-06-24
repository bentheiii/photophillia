from PySide2.QtWidgets import QLabel


class DropDestLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for uri in event.mimeData().urls():
            print(uri)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication()

    mw = DropDestLabel('hi there')

    mw.show()
    app.exec_()