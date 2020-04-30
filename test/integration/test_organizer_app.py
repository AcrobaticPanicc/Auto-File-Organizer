from unittest import TestCase
from os.path import isfile
from organizer_app import FileOrganizer
from os import path, makedirs


class TestOrganizer(TestCase):

    def setUp(self):
        self.organizer = FileOrganizer()

        desktop = path.join(path.join(path.expanduser('~')), 'Desktop')
        self.test_dir = f'{desktop}/FileOrganizerTest'

        makedirs(self.test_dir, exist_ok=True)

        self.files = ['play.py', 'music.mp3', 'noext.', 'img.jpg', 'IMG_2328.mp4']

        for file in self.files:
            with open(f'{self.test_dir}/{file}', 'w+') as f:
                pass

        self.file_path = f'{self.test_dir}/play.py'
        self.extensions = ['MP3', '', 'NOEXT.', 'otherext']

        self.src_file = f'{self.test_dir}/IMG_2328.mp4'
        self.dst = f'{self.test_dir}/Video'

    def test_move_files_audio(self):
        extensions = self.organizer.get_extensions(self.files)
        self.organizer.create_folders(extensions, self.test_dir)
        self.organizer.move_files(self.files, self.test_dir)
        self.assertTrue(isfile(f'{self.test_dir}/Audio/music.mp3'))

    def test_move_files_video(self):
        extensions = self.organizer.get_extensions(self.files)
        self.organizer.create_folders(extensions, self.test_dir)
        self.organizer.move_files(self.files, self.test_dir)

        self.assertTrue(isfile(f'{self.test_dir}/Video/IMG_2328.mp4'))

    def test_move_files_no_extension(self):
        extensions = self.organizer.get_extensions(self.files)
        self.organizer.create_folders(extensions, self.test_dir)
        self.organizer.move_files(self.files, self.test_dir)
        self.assertTrue(isfile(f'{self.test_dir}/Other/No extension/noext.'))
