from flask import Flask
from document import Document

class MyFlask(Flask):
    def __init__(self, *args, **kwargs):
        super(MyFlask, self).__init__(*args, **kwargs)
        self.first_doc = Document(self)
        self.second_doc = Document(self)