import shutil
import unittest
from unittest import TestCase
from os.path import isdir
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

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_new_name(self):
        new_name = self.organizer.get_new_name(self.file_path)

        self.assertEqual(f'{self.test_dir}/play (2).py', new_name)

    def test_get_extensions(self):
        extensions = self.organizer.get_extensions(self.files)

        self.assertEqual({'Jpg', 'No extension', 'Mp3', 'Mp4', 'Py'}, extensions)

    def test_get_type_audio(self):
        extension = 'MP3'
        file_type = self.organizer.get_type(extension)

        self.assertEqual({'type': 'Audio', 'extension': extension}, file_type)

    def test_get_type_other(self):
        extension = 'NONE'
        file_type = self.organizer.get_type(extension)

        self.assertEqual({'type': 'Other', 'extension': extension}, file_type)

    def test_get_type_no_extension(self):
        extension = ''
        file_type = self.organizer.get_type(extension)

        self.assertEqual({'type': 'No extension', 'extension': 'No extension'}, file_type)

    def test_get_files_list(self):
        files_list = self.organizer.get_files_list(self.test_dir)

        self.assertEqual(['img.jpg', 'play.py', 'music.mp3', 'IMG_2328.mp4', 'noext.'], files_list)

    def test_create_folder_audio(self):
        self.organizer.create_folders(self.extensions, self.test_dir)
        self.assertTrue(isdir(f'{self.test_dir}/audio'))

    def test_create_folder_other(self):
        self.organizer.create_folders(self.extensions, self.test_dir)
        self.assertTrue(isdir(f'{self.test_dir}/Other/otherext'))

    def test_create_folder_no_ext(self):
        self.organizer.create_folders(self.extensions, self.test_dir)
        self.assertTrue(isdir(f'{self.test_dir}/No extension'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
