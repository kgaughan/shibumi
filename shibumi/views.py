import hashlib
import httplib
from os import path
import urlparse

from adjunct import xmlutils
import bottle

from .bootstrap import app, fmt, STATIC
from .model import Entry


TAG = 'tag:talideon.com,2001:weblog'

def base_url():
    parts = bottle.request.urlparts
    return '{}://{}{}'.format(parts.scheme,
                              parts.netloc,
                              bottle.request.script_name)


def get_full_url(*args, **kwargs):
    return urlparse.urljoin(base_url(), app.get_url(*args, **kwargs))


def make_etag(src):
    return '"' + hashlib.md5(src).hexdigest() + '"'


@app.get('/', name='latest')
@bottle.view('latest')
def root():
    return {'entries': Entry.get_latest()}


@app.get('/<year:re:[0-9]{4}>-<month:re:[01][0-9]>', name='archive')
@bottle.view('archive')
def archive(year, month):
    entries = Entry.get_month(int(year), int(month))
    if len(entries) == 0:
        bottle.response.status = httplib.NOT_FOUND
        return ''
    return {'entries': entries}


@app.get('/;feed', name='feed')
def feed():
    modified = Entry.get_most_recent_modification().strftime('%Y-%m-%dT%H:%M:%SZ')
    etag = make_etag(modified)
    if bottle.request.headers.get('If-None-Match', '').lstrip('W/') == etag:
        bottle.response.status = httplib.NOT_MODIFIED
        return ''

    bottle.response.headers['ETag'] = etag
    bottle.response.content_type = 'application/atom+xml; charset=UTF-8'

    xml = xmlutils.XMLBuilder()
    with xml.within('feed', xmlns='http://www.w3.org/2005/Atom'):
        xml.tag('title', 'Inklings')
        xml.tag('subtitle', 'A stream of random things')
        xml.tag('updated', modified)
        with xml.within('author'):
            xml.tag('name', 'Keith Gaughan')
        xml.tag('id', 'tag:talideon.com,2001:weblog')
        xml.tag('rights', 'Copyright (c) Keith Gaughan, 2001-2018')
        xml.tag('link',
                rel='alternate',
                type='text/html',
                hreflang='en',
                href=get_full_url('latest'))
        xml.tag('link',
                rel='self',
                type='application/atom+xml',
                href=bottle.request.url)

        for entry in Entry.get_feed():
            with xml.within('entry'):
                xml.tag('title', entry.title or 'Untitled')
                xml.tag('published', entry.time_c.strftime('%Y-%m-%dT%H:%M:%SZ'))
                xml.tag('updated', entry.time_m.strftime('%Y-%m-%dT%H:%M:%SZ'))
                xml.tag('tag', '{}:{}'.format(TAG, entry.id))

                entry_link = get_full_url('entry', entry_id=entry.id)
                xml.tag('link',
                        rel='alternate',
                        type='text/html',
                        href=entry_link)
                if entry.link:
                    xml.tag('link',
                            rel='related',
                            type='text/html',
                            href=entry_link)
                if entry.via:
                    xml.tag('link',
                            rel='via',
                            type='text/html',
                            href=entry.via)
                attrs = {
                    'type': 'html',
                    'xml:lang': 'en',
                    'xml:base': entry_link,
                }
                xml.tag('content', fmt(entry.note), **attrs)

    return xml.as_string()


@app.get('/;add')
def show_add_entry():
    return 'add entry'


@app.post('/')
def add_entry():
    return 'adding an entry...'


@app.get('/<entry_id:int>', name='entry')
@bottle.view('entry')
def entry(entry_id):
    try:
        entry = Entry.get(Entry.id == entry_id)
    except Entry.DoesNotExist:
        bottle.response.status = httplib.NOT_FOUND
        return ''
    return {'entry': entry}


@app.get('/<entry_id:int>;edit', name='edit')
@bottle.view('edit_entry')
def edit_entry(entry_id):
    try:
        entry = Entry.get(Entry.id == entry_id)
    except Entry.DoesNotExist:
        bottle.response.status = httplib.NOT_FOUND
        return ''
    return {'entry': entry}


@app.post('/<entry_id:int>')
def update_entry(entry_id):
    return 'updating entry: {}'.format(entry_id)


@app.get('/static/<path:path>', name='static')
def static_files(path):
    return bottle.static_file(path, root=STATIC)

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, debug=True)
