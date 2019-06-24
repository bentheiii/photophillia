from typing import Dict, Set, Optional

from os.path import abspath, splitext

from photophillia.__util__ import open_zipped
from photophillia.photo import Photo, Size, PhotoPositioning, FilePhoto
from photophillia.__data__ import __version__


class PhotophilliaProject:
    def __init__(self):
        self.photos: Dict[Photo, Dict[Size, PhotoPositioning]] = {}
        self.sizes: Set[Size] = set()
        self.default_directory: Optional[str] = None

    def add_photo(self, photo: Photo):
        if photo in self:
            raise Exception('duplicate photo')
        self.photos[photo] = {}

    def del_photo(self, photo: Photo):
        if photo not in self:
            raise Exception('photo not in manager')
        del self.photos[photo]

    def add_positioning(self, positioning: PhotoPositioning):
        if positioning.source not in self:
            raise Exception('source not added to manager')
        self.photos[positioning.source][positioning.dest_size] = positioning

    def add_size(self, size: Size):
        self.sizes.add(size)

    def del_size(self, size: Size):
        if size not in self.sizes:
            raise Exception('size not in manager')
        self.sizes.remove(size)
        for _, pos in self.photos.items():
            pos.pop(size, None)

    def __contains__(self, item):
        return item in self.photos

    def to_dict(self):
        files = []
        ret = {
            'photophillia_lib_version': __version__,
            'sizes': list(self.sizes),
            'photos_files': files
        }
        for photo, pos in self.photos.items():
            if not isinstance(photo, FilePhoto):
                raise TypeError(f'photos of type {type(photo)} are not supported')
            files.append(
                (abspath(photo.path), [p.to_dict() for p in pos.values()])
            )
        if self.default_directory:
            ret['default_directory'] = self.default_directory
        return ret

    @classmethod
    def from_dict(cls, d):
        ret = cls()
        d.pop('photophillia_lib_version')
        for size in d.pop('sizes'):
            ret.add_size(Size._make(size))
        for path, pos in d.pop('photos_files'):
            photo = FilePhoto(path)
            ret.add_photo(photo)
            for p in pos:
                positioning = PhotoPositioning(source=photo, **p)
                ret.add_positioning(positioning)
        ret.default_directory = d.pop('default_directory', None)

        assert not d
        return ret

    @staticmethod
    def open(path, mode='r'):
        _, ext = splitext(path)
        if ext in ('.zip', '.zpj'):
            return open_zipped(path, 'main.ppj', mode)
        return open(path, mode)
