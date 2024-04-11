import glob
import os

from flask import Flask, render_template, url_for, request, redirect, flash
import docx2txt as docx
from odf import text, teletype
from odf.opendocument import load
import difflib as dl

from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, CONTEXT_N

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.secret_key = '1234567899'

first_doc_filename, second_doc_filename, first_doc_extension, second_doc_extension = '', '', '', ''


def read_document_content(filename: str, extension: str) -> str:
    try:
        if extension == ".docx":
            return docx.process(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            textdoc = load(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            allparas = textdoc.getElementsByType(text.P)
            all_text = ""
            for par in allparas:
                all_text += teletype.extractText(par)
            return all_text
    except Exception as e:
        flash('Error processing file: {}'.format(e), 'error')
        return None


@app.route('/comparison_result')
def how_document_comparison():
    text1 = read_document_content(first_doc_filename, first_doc_extension).split()
    text2 = read_document_content(second_doc_filename, second_doc_extension).split()
    diffiter = dl.context_diff(text1, text2, first_doc_filename, second_doc_filename, n=CONTEXT_N)

    diff = [d.replace(" ", "").replace("\n", "") for d in diffiter]
    return render_template('differences_display.html', differences=diff)


def delete_previous_documents():
    previous_docs = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    for doc in previous_docs:
        os.remove(doc)

def create_directory_if_missing(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


@app.route('/', methods=['GET', 'POST'])
def handle_document_upload():
    if request.method == 'GET':
        return render_template('document_upload.html')

    first_doc = request.files.get('doc1_file')
    second_doc = request.files.get('doc2_file')

    if not first_doc or not second_doc:
        flash('No files chosen', 'error')
        return redirect(url_for('handle_document_upload'))

    global first_doc_filename, second_doc_filename, first_doc_extension, second_doc_extension
    first_doc_filename, second_doc_filename = secure_filename(first_doc.filename), secure_filename(second_doc.filename)
    first_doc_extension, second_doc_extension = os.path.splitext(first_doc_filename)[1], os.path.splitext(second_doc_filename)[1]

    if first_doc_extension not in app.config['ALLOWED_EXTENSIONS'] or second_doc_extension not in app.config['ALLOWED_EXTENSIONS']:
        flash('Choose .docx or .odt files', 'error')
        return redirect(url_for('handle_document_upload'))

    # create_directory_if_missing(app.config['UPLOAD_FOLDER'])
    # first_doc_filename = secure_filename(first_doc.filename)
    # second_doc_filename = secure_filename(second_doc.filename)

    delete_previous_documents()

    first_doc.save(os.path.join(app.config['UPLOAD_FOLDER'], first_doc_filename))
    second_doc.save(os.path.join(app.config['UPLOAD_FOLDER'], second_doc_filename))
    return redirect(url_for('how_document_comparison'))


if __name__ == '__main__':
    app.run()
