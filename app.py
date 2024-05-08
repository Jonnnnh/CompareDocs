# app.py
from flask import render_template, url_for, request, redirect, flash
import difflib as dl
from config import configure_app
from document import Document
from my_flask import MyFlask

app = MyFlask(__name__)
configure_app(app)
configure_app(app)
app.secret_key = '1234567899'

@app.route('/comparison_result')
def how_document_comparison():
    context_n = app.config['CONTEXT_N']
    text1 = app.first_doc.read_content().split()
    text2 = app.second_doc.read_content().split()
    diffiter = dl.context_diff(text1, text2, app.first_doc.filename, app.second_doc.filename, n=context_n)

    diff = [d.replace(" ", "").replace("\n", "") for d in diffiter]
    return render_template('differences_display.html', differences=diff)


@app.route('/', methods=['GET', 'POST'])
def handle_document_upload():
    if request.method == 'GET':
        return render_template('document_upload.html')

    first_file = request.files.get('doc1_file')
    second_file = request.files.get('doc2_file')

    if not first_file or not second_file:
        flash(app.config['ERROR_NO_FILES_CHOSEN'], 'error')
        return redirect(url_for('handle_document_upload'))

    app.first_doc.set_file(first_file)
    app.second_doc.set_file(second_file)

    if app.first_doc.extension not in app.config['ALLOWED_EXTENSIONS'] or app.second_doc.extension not in app.config[
        'ALLOWED_EXTENSIONS']:
        flash(app.config['ERROR_INVALID_FILE_TYPE'], 'error')
        return redirect(url_for('handle_document_upload'))

    Document.delete_previous_documents(app)

    app.first_doc.save_file(first_file)
    app.second_doc.save_file(second_file)
    return redirect(url_for('how_document_comparison'))


if __name__ == '__main__':
    app.run()
