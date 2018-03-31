import functools
from os import path

import bottle
import markdown

from . import model


app = bottle.Bottle()
app.install(model.db)

# Shortcuts.
bottle.BaseTemplate.defaults['get_url'] = app.get_url
bottle.BaseTemplate.defaults['markdown'] = functools.partial(
        markdown.markdown,
        extensions=[
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.smarty',
            'markdown.extensions.tables'])

BASE = path.dirname(path.abspath(__file__))
STATIC = path.join(BASE, 'static')
bottle.TEMPLATE_PATH = [path.join(BASE, 'templates')]
