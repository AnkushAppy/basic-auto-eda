import os
import sys
import random
from code.settings import REPORT_PATH

class CreateReport:

    def __init__(self, file_name=None):
        self.file_name = file_name
        if file_name is not None:
            if file_name[-3:] == ".md":
                pass
            else:
                file_name = file_name + ".md"
        else:
            raise ("File name not given")

        self.folder_name = REPORT_PATH + file_name[:-3]

        self.file_path = "/".join([self.folder_name, self.file_name])
        self.create_report_folder()
        self.fp = open(self.file_path, 'w+')

    def create_report_folder(self):
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        else:
            self.folder_name = self.folder_name + "_" + str(random.randint(1000,9999))
            os.makedirs(self.folder_name)

    def get_report_folder(self):
        return self.folder_name

    def get_image_path(self, graph_type, col):
        col = "".join(col.lower().split(' '))
        image_name = "{0}_{1}.png".format(graph_type, col)
        image_path = self.folder_name + '/' + image_name
        return image_path, image_name

    def get_report_file(self):
        return self.fp

    def add_header(self, header="Header", size=4):
        header = "#" * size + " " + header
        self.fp.write(header)
        self.add_space()
        self.add_space()

    def add_paragraph(self, paragraph="paragraph"):
        self.fp.write(paragraph)
        self.add_space()
        self.add_space()

    def add_bullets(self, text=None, values_text=None):
        self.fp.write(text)
        self.add_space()
        for i in values_text:
            bullet = "* " + i
            self.fp.write(bullet)
            self.add_space()
        self.add_space()
        self.add_space()

    def add_space(self):
        self.fp.write('\n')

    def add_plot(self, file_name="", text=""):
        image_text = "![{0}]({1})".format(text, file_name)
        self.fp.write(image_text)
        self.add_space()
        self.add_space()

    def add_code():
        pass

    def close(self):
        self.fp.close()
