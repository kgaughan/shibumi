from os import path

import bottle

from .bootstrap import app, STATIC
from .model import Entry


@app.get('/', name='latest')
@bottle.view('latest')
def root():
    return {'entries': Entry.select().order_by(Entry.time_c.desc()).limit(50)}


@app.get('/<year:re:[0-9]{4}>-<month:re:[01][0-9]>', name='archive')
def archive(year, month):
    return 'view archive: ({} {})'.format(year, month)


@app.get('/;feed', name='feed')
def feed():
    return 'feed'


@app.get('/;add')
def show_add_entry():
    return 'add entry'


@app.post('/')
def add_entry():
    return 'adding an entry...'


@app.get('/<entry_id:int>', name='entry')
def entry(entry_id):
    return 'view entry: {}'.format(entry_id)


@app.get('/<entry_id:int>;edit')
def edit_entry(entry_id):
    return 'edit entry: {}'.format(entry_id)


@app.post('/<entry_id:int>')
def update_entry(entry_id):
    return 'updating entry: {}'.format(entry_id)


@app.get('/static/<path:path>', name='static')
def static_files(path):
    return bottle.static_file(path, root=STATIC)

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, debug=True)
