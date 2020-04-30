import json
import logging
from shutil import move, Error
from os import makedirs, rename, listdir
from os.path import isfile, splitext, join


class FileOrganizer:

    def __init__(self):

        logging.basicConfig(filename='logs.log',
                            level=logging.INFO,
                            format='%(asctime)s:%(message)s')

        with open('extensions.json') as f:
            self.data = json.load(f)

        self.files_list = []
        self.extensions_list = []

    """INNER FUNCTIONS"""

    @staticmethod
    def get_new_name(file_path):
        """return a new file name. used in case the file already exists in DST folder"""
        file_name, ext = splitext(file_path)

        if not ext:
            new_file_name = file_name + ' ' + '(2)'
            return new_file_name

        else:
            new_file_name = file_name + ' ' + '(2)' + ext
            return new_file_name

    def get_type(self, extension):
        """return dict with the file type and extension"""
        extension = extension.upper()

        for k, v in self.data.items():
            if extension and extension in v:
                return dict(type=k.capitalize(), extension=extension)

        if extension != '':
            return dict(type='Other', extension=extension)

        else:
            return dict(type='No extension', extension='No extension')

    def move_rename(self, src, dst):
        while True:
            src_file = src.split('/')[-1]
            dst_files = listdir(dst)

            if src_file not in dst_files:
                move(src, dst)
                break

            else:
                new_file_name = self.get_new_name(src)
                rename(src, new_file_name)
                src = new_file_name

                try:
                    move(new_file_name, dst)
                    break

                except Error:
                    continue

    """MAIN FUNCTIONS"""

    @staticmethod
    def get_files_list(path):
        """return a list of all the files in the directory"""
        files = []
        for file in listdir(path):
            if isfile(join(path, file)) and not file.startswith('.'):
                files.append(file)

        logging.info(f'Files found: {files}')
        return files

    @staticmethod
    def get_extensions(files):
        """return a list of all the extensions in the directory"""
        extensions = set()

        for file in files:
            extension = file.split('.')[1].lower().capitalize()

            if extension:
                extensions.add(extension)

            elif not extension and not file.startswith('.'):
                extensions.add('No extension')

        logging.info(f'extensions found: {extensions}')

        return extensions

    def create_folders(self, extensions, path):
        """create folders by the types of the files by extensions"""
        for extension in extensions:

            file_type = self.get_type(extension)["type"]

            if file_type != 'Other':
                makedirs(f'{path}/{file_type}', exist_ok=True)
                logging.info(f'folder created {f"{path}/{file_type}"}')

            else:
                makedirs(f'{path}/Other/{extension}', exist_ok=True)
                logging.info(f'folder created f"{path}/Other/{extension}"')

    def move_files(self, files, path):
        """moving the files to the matching directory"""
        for file in files:

            extension = splitext(file)[1].replace('.', '')
            file_type = self.get_type(extension)['type']

            original_file_dir = f'{path}/{file}'
            file_type_dir = f'{path}/{file_type}'
            other_type_dir = f'{path}/Other/{extension}'
            no_extension_dir = f'{path}/Other/No extension'

            if file_type == 'Other':
                self.move_rename(original_file_dir, other_type_dir)

            elif file_type == 'No extension':
                try:
                    self.move_rename(original_file_dir, no_extension_dir)

                except FileNotFoundError:
                    pass

            else:
                self.move_rename(original_file_dir, file_type_dir)

    def run_app(self, path):
        files = self.get_files_list(path)
        extensions = self.get_extensions(files)
        self.create_folders(extensions, path)
        self.move_files(files, path)
