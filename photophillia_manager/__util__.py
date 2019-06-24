import numpy as np
from PySide2.QtGui import QImage
from PySide2.QtWidgets import QTreeWidgetItem


def cv_to_qt(bmp: np.ndarray) -> QImage:
    height, width, channel = bmp.shape
    bytes_per_line = 3 * width
    return QImage(bmp.data, width, height, bytes_per_line, QImage.Format_BGR30)


class ComparingTreeWidgetItem(QTreeWidgetItem):
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        try:
            return float(self.text(column)) > float(other.text(column))
        except ValueError:
            return self.text(column) > other.text(column)
