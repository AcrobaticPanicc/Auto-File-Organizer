import logging
from tkinter import Tk, Button, END, EXTENDED, messagebox, Frame, Listbox, filedialog
from organizer_app import FileOrganizer

logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s:%(message)s')


class FileOrganizerGui:

    def __init__(self, master):

        self.master = master
        self.master.resizable(False, False)
        self.master.title("File Organizer")

        self.organizer = FileOrganizer()

        logging.info('-' * 20)
        logging.info('APP STARTED')

        self.paths = []

        """CANVAS"""
        self.top_frame = Frame(root)
        self.top_frame.grid()

        self.listbox = Listbox(bg="#ffe6a1", width=50, height=10,
                               highlightcolor='black', borderwidth=0,
                               highlightthickness=0, selectmode=EXTENDED)
        self.listbox.grid()

        self.bottom_frame = Frame(root)
        self.bottom_frame.grid()

        """BUTTONS"""
        self.select_path_button = Button(self.top_frame, text='Select Folder', command=self.get_path)
        self.select_path_button.grid(padx=5, pady=5)

        self.remove_all = Button(self.top_frame, text='Remove All', command=self.clear_list)
        self.remove_all['state'] = 'disabled'
        self.remove_all.grid(padx=5, pady=5)

        self.organize_button = Button(root, text='Organize', command=self.start)
        self.organize_button['state'] = 'disabled'
        self.organize_button.grid(padx=5, pady=5)

        self.quit = Button(root, text='Quit', command=root.quit)
        self.quit.grid(padx=5, pady=5)

    def get_path(self):

        path = filedialog.askdirectory()

        if path:
            logging.info(f'Selected directory: {path}')
            self.organize_button['state'] = 'active'
            if path not in self.paths:
                self.paths.append(path)
            self.remove_all['state'] = 'active'
            self.listbox.insert(END, path)
        else:
            logging.info('No folder selected')

    def clear_list(self):
        self.listbox.delete(0, END)
        self.paths = []
        logging.info('Selected paths deleted')

    def start(self):
        logging.info(f'Clicked Organize')
        logging.info(f'Paths: {self.paths}')

        for path in self.paths:
            self.organizer.run_app(path)

        self.organize_button['state'] = 'disabled'
        self.paths = []
        self.clear_list()
        self.remove_all['state'] = 'disabled'

        messagebox.showinfo(title='Process completed', message='Done')


root = Tk()
gui = FileOrganizerGui(root)
root.mainloop()

logging.info('APP CLOSED')
logging.info('-' * 20)
