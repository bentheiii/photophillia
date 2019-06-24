import shiboken2
from PySide2.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QTreeWidget, QPushButton, QDialog

from photophillia import ProjectManager
from photophillia_manager.__util__ import ComparingTreeWidgetItem
from photophillia_manager.size_input import SizeInput


class SizeView(QWidget):
    def __init__(self, manager: ProjectManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager

        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        table = QTreeWidget()
        table.setHeaderLabels(['name', 'width', 'height', 'ratio'])
        table.setSortingEnabled(True)
        items = []
        for size in self.manager.project.sizes:
            i = ComparingTreeWidgetItem(None, [
                f'{size.width}x{size.height}', str(size.width), str(size.height), str(size.ratio())
            ])
            i.__data__ = size
            items.append(i)
        table.addTopLevelItems(items)

        @table.currentItemChanged.connect
        def _(item, prev):
            del_btn.setEnabled(item is not None)

        layout.addWidget(table, 0, 0, 1, 2)

        add_btn = QPushButton('add new')
        @add_btn.clicked.connect
        def _(*args):
            diag = SizeInput(self.manager.project.sizes, self)
            if diag.exec_() != QDialog.Accepted:
                return
            size = diag.value
            self.manager.add_size(size)
            item = ComparingTreeWidgetItem(None, [
                f'{size.width}x{size.height}', str(size.width), str(size.height), str(size.ratio())
            ])
            table.addTopLevelItem(item)

        layout.addWidget(add_btn, 1, 0)

        del_btn = QPushButton('delete')
        del_btn.setEnabled(False)

        @del_btn.clicked.connect
        def _(*args):
            item = table.currentItem()
            size = item.__data__
            self.manager.del_size(size)
            shiboken2.delete(item)

        layout.addWidget(del_btn, 1, 1)

        self.setLayout(layout)

class PhotoView(QWidget):
    def __init__(self, manager: ProjectManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager

        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        table = QTreeWidget()
        table.setHeaderLabels(['name', 'type', 'width', 'height'])
        table.setSortingEnabled(True)
        items = []
        for photo in self.manager.project.photos:
            if not photo.is_available():
                w = h = 'N/A!'
            else:
                w, h = photo.raw_size()
            i = ComparingTreeWidgetItem(None, [
                str(photo), type(photo).__name__, str(w), str(h)
            ])
            i.__data__ = photo
            items.append(i)
        table.addTopLevelItems(items)

        @table.currentItemChanged.connect
        def _(item, prev):
            del_btn.setEnabled(item is not None)

        layout.addWidget(table, 0, 0)

        del_btn = QPushButton('delete')
        del_btn.setEnabled(False)

        @del_btn.clicked.connect
        def _(*args):
            item = table.currentItem()
            size = item.__data__
            self.manager.del_photo(size)
            shiboken2.delete(item)

        layout.addWidget(del_btn, 1, 0)

        self.setLayout(layout)


class ProjectAnalysisWindow(QWidget):
    def __init__(self, manager: ProjectManager, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.changed = False
        self.manager = manager

        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        layout.addWidget(PhotoView(self.manager))

        layout.addWidget(SizeView(self.manager))

        self.setLayout(layout)
