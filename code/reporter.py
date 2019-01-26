import os
import sys


class CreateReport:

    def __init__(self, file_name=None):
        if file_name is not None:
            if file_name[-3:] == ".md":
                pass
            else:
                file_name = file_name + ".md"
        else:
            raise ("File name not given")
        self.fp = open(file_name, 'w+')

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
