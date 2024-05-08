# document.py
import os
import glob
from werkzeug.utils import secure_filename
import docx2txt as docx
from odf import text, teletype
from odf.opendocument import load

class Document:
    def __init__(self, app):
        self.app = app
        self.filename = ''
        self.extension = ''

    def set_file(self, file):
        self.filename = secure_filename(file.filename)
        self.extension = os.path.splitext(self.filename)[1]

    def save_file(self, file):
        file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], self.filename)) # Сохраняем файл в директории UPLOAD_FOLDER

    def read_content(self) -> str:
        try:
            if self.extension == ".docx":
                return docx.process(os.path.join(self.app.config['UPLOAD_FOLDER'], self.filename))
            else:
                textdoc = load(os.path.join(self.app.config['UPLOAD_FOLDER'], self.filename))
                allparas = textdoc.getElementsByType(text.P)
                all_text = ""
                for par in allparas:
                    all_text += teletype.extractText(par)
                return all_text
        except Exception as e:
            self.app.flash('Error processing file: {}'.format(e), 'error')
            return ""

    @staticmethod
    def delete_previous_documents(app):
        previous_docs = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
        for doc in previous_docs:
            os.remove(doc)