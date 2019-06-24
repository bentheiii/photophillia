import json
import logging
from glob import iglob
from os.path import exists, isdir
import argparse

import sys

from photophillia.photo import FilePhoto, Size
from photophillia.project import PhotophilliaProject
from photophillia.__data__ import __version__

parser = argparse.ArgumentParser(__name__)

parser.add_argument('--version', action='version', version=__version__)
parser.add_argument('project_path', help='the path to a photophillia manager file')
parser.add_argument('--verbose', dest='verbose', default='INFO', required=False)


def photophillia(args=None):
    args = parser.parse_args(args)
    if args.verbose:
        logging.basicConfig(level=args.verbose)

    proj_path = args.project_path
    if not exists(proj_path):
        project = PhotophilliaProject()
        logging.info('file not found, new manager created')
    else:
        with PhotophilliaProject.open(proj_path, 'r') as read:
            project = PhotophilliaProject.from_dict(json.load(read))
    logging.info(f'loaded manager has {len(project.sizes)} sizes, {len(project.photos)} photos')

    def glob_photos(path: str):
        added = skipped = 0
        for p in iglob(path, recursive=True):
            if isdir(p):
                continue
            fp = FilePhoto(p)
            if fp not in project:
                project.add_photo(fp)
                logging.debug(f'added photo: {p}')
                added += 1
            else:
                logging.debug(f'photo skipped: {p}')
                skipped += 1
        logging.info(f'{added} photos added, {skipped} photos skipped')

    def save(path=...):
        if path is ...:
            path = proj_path
        if path != proj_path and exists(path):
            if input('overwrite file? (y/N)').lower() != 'y':
                logging.warning('writing aborted')
                return
        with PhotophilliaProject.open(path, 'w') as write:
            json.dump(project.to_dict(), write)
        logging.info(f'saved manager {path}')

    def add_size(width, height):
        project.add_size(Size(width, height))
        logging.info(f'added size {width}x{height}')

    def ls_photos(filter: str = None):
        if filter is None:
            logging.info(f'{len(project.photos)} photos in manager')
        else:
            matches = 0
            for photo in project.photos:
                if filter in str(photo):
                    logging.info(str(photo))
                    matches += 1
            logging.info(f'{matches} matches')

    def ls_sizes():
        logging.info(f'{len(project.sizes)} sizes:')
        for size in project.sizes:
            logging.info(str(size))

    def exit():
        logging.info('exited')
        sys.exit()

    eval_ns = {
        '__builtins__': {}
    }
    for f in (
        glob_photos,
        save,
        add_size,
        ls_photos,
        ls_sizes,
        exit
    ):
        eval_ns[f.__name__] = f

    while True:
        command = input('enter command:\n')
        if not command.endswith(')'):
            command += '()'
        try:
            r = eval(command, eval_ns)
            if r is not None:
                logging.info(str(r))
        except (SyntaxError, NameError) as e:
            logging.warning(str(e))


if __name__ == '__main__':
    photophillia()
