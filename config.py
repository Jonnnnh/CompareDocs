# config.py
def configure_app(app):
    app.config['UPLOAD_FOLDER'] = "docs"
    app.config['ALLOWED_EXTENSIONS'] = {'.docx', '.odt'}
    app.config['CONTEXT_N'] = 7
    app.config['ERROR_NO_FILES_CHOSEN'] = 'No files chosen'
    app.config['ERROR_INVALID_FILE_TYPE'] = 'Choose .docx or .odt files'