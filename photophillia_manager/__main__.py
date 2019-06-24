import argparse

from photophillia_manager.main_widget import MainWidget

parser = argparse.ArgumentParser()
parser.add_argument('project_path', nargs='?')


def main(args=None):
    from PySide2.QtWidgets import QApplication

    app = QApplication()

    args = parser.parse_args(args)
    mw = MainWidget(proj_path=args.project_path)

    mw.show()
    app.exec_()

if __name__ == '__main__':
    main()
