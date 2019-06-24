from typing import Set

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QSpinBox, QLabel, QPushButton, QMessageBox

from photophillia import Size


class SizeInput(QDialog):
    def __init__(self, blacklist: Set[Size], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blacklist = blacklist
        self.value = None

        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        def v_changed(*a):
            size = self.value = Size(w_box.value(), h_box.value())
            valid = (size not in self.blacklist) and size.height > 0 and size.width > 0
            ok_btn.setEnabled(valid)
            if not valid:
                msg = 'size is invalid'
                if size in self.blacklist:
                    msg = 'size is present'
            else:
                msg = size.ratio()
            v_label.setText(f'{size.width}x{size.height}\n{msg}')

        w_box = QSpinBox()
        w_box.setMinimum(1)
        w_box.setMaximum(1_000_000)
        w_box.valueChanged.connect(v_changed)
        h_box = QSpinBox()
        h_box.setMinimum(1)
        h_box.setMaximum(1_000_000)
        h_box.valueChanged.connect(v_changed)
        x_label = QLabel('x')
        x_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(w_box, 0, 0)
        layout.addWidget(x_label, 0, 1)
        layout.addWidget(h_box, 0, 2)

        v_label = QLabel()
        v_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(v_label, 1, 0)

        preset_btn = QPushButton('Get From Screen')

        try:
            import screeninfo as si
        except ImportError:
            si = None
            preset_btn.setEnabled(False)
        else:
            @preset_btn.clicked.connect
            def _(*a):
                candidates = set()
                for m in si.get_monitors():
                    candidates.add((m.width, m.height))
                if len(candidates) != 1:
                    QMessageBox.warning(self, 'multiple monitors not yet supported')  # todo
                else:
                    w, h = next(iter(candidates))
                    w_box.setValue(w)
                    h_box.setValue(h)

        layout.addWidget(preset_btn, 1, 2)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn, 2, 0)

        ok_btn = QPushButton('Ok')
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, 2, 2)

        self.setLayout(layout)

        v_changed()
