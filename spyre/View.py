import __main__
import os
import codecs
import io
ENCODING = 'utf-8'


class View:
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.JS_PATH = os.path.join(self.ROOT_DIR, 'public', 'js')
        self.CSS_PATH = os.path.join(self.ROOT_DIR, 'public', 'css')
        self.APP_PATH = os.path.dirname(os.path.realpath(__main__.__file__))

    def getHTML(self):
        file_path = os.path.join(self.ROOT_DIR, 'view.html')
        with codecs.open(file_path, 'r', ENCODING) as f:
            return f.read()

    def getJS(self):
        self.JS = ""
        for file in os.listdir(self.JS_PATH):
            if file.find('.js') > 0:
                file_path = os.path.join(self.JS_PATH, file)
                with codecs.open(file_path, 'rb') as f:
                    self.JS += f.read().decode('utf-8')
                self.JS += "\n"
        return self.JS

    def getCSS(self):
        self.CSS = ""
        for file in os.listdir(self.CSS_PATH):
            if file.find('.css') > 0:
                file_path = os.path.join(self.CSS_PATH, file)
                with open(file_path, 'rb') as f:
                    self.CSS += f.read().decode('utf-8')
                self.CSS += "\n"
        return self.CSS

    def getSpinningWheel(self, spinnerFile=None):
        buffer = io.BytesIO()
        if spinnerFile is None:
            path = os.path.join(self.ROOT_DIR, 'public', 'images', "loading_wheel.gif")
        else:
            path = os.path.join(self.APP_PATH, spinnerFile)
        with open(path, 'rb') as f:
            buffer.write(f.read())
        return buffer
