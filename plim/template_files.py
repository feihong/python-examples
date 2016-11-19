from pathlib import Path
from mako.template import Template
from mako.lookup import TemplateLookup
from plim import preprocessor


def main():
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render('index.plim', message='画虎画皮难画骨，知人知面不知心')

    app.run(debug=True, port=8000)


lookup = TemplateLookup(
    directories=['static'],
    preprocessor=preprocessor)


def render(tmpl_file, **kwargs):
    tmpl = lookup.get_template(tmpl_file)
    return tmpl.render(**kwargs)


if __name__ == '__main__':
    main()
