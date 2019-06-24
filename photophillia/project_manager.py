from random import sample
from typing import Set, Tuple, Optional

from photophillia import PhotophilliaProject, Photo, Size, PhotoPositioning
from photophillia.__util__ import remove_where

Job = Tuple[Photo, Size]


class ProjectManager:
    def __init__(self, project: PhotophilliaProject):
        self.project = project

        self._jobs_to_to: Set[Job] = set()

        for photo, done in self.project.photos.items():
            for size in self.project.sizes:
                if size not in done:
                    self._jobs_to_to.add((photo, size))

    def __len__(self):
        return len(self._jobs_to_to)

    def __iter__(self):
        while True:
            yield from sample(self._jobs_to_to, 1)

    def complete_job(self, job: Job, positioning: Optional[PhotoPositioning]):
        photo, size = job
        self.project.photos[photo][size] = positioning
        self._jobs_to_to.discard(job)

    def add_photo(self, photo: Photo):
        if photo in self.project.photos:
            raise Exception(f'duplicate photo {photo}')

        self.project.add_photo(photo)
        for s in self.project.sizes:
            self._jobs_to_to.add((photo, s))

    def add_size(self, size: Size):
        if size in self.project.sizes:
            raise Exception(f'duplicate size {size}')

        self.project.add_size(size)
        for p in self.project.photos:
            self._jobs_to_to.add((p, size))

    def del_photo(self, photo: Photo):
        self.project.del_photo(photo)
        remove_where(self._jobs_to_to, lambda x: x[0] == photo)

    def del_size(self, size: Size):
        self.project.del_size(size)
        remove_where(self._jobs_to_to, lambda x: x[1] == size)


