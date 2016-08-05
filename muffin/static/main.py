import subprocess
import mimetypes

import asyncio
from aiohttp import hdrs
from aiohttp.web_exceptions import HTTPNotFound, HTTPNotModified
import muffin
from muffin.urls import StaticRoute, StaticResource


app = muffin.Application('example')


@app.register('/hello/')
def hello(request):
    return 'Hello World!'


class CustomStaticRoute(StaticRoute):
    @asyncio.coroutine
    def handle(self, request):
        filename = request.match_info['filename']
        try:
            filepath = self._directory.joinpath(filename).resolve()
            filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError) as error:
            # relatively safe
            raise HTTPNotFound() from error
        except Exception as error:
            # perm error or other kind!
            request.logger.exception(error)
            raise HTTPNotFound() from error

        if filepath.is_dir():
            filepath = filepath / 'index.plim'
            if not filepath.exists():
                raise HTTPNotFound()
            else:
                resp = yield from render(request, self._response_factory, filepath)
                return resp

        st = filepath.stat()

        modsince = request.if_modified_since
        if modsince is not None and st.st_mtime <= modsince.timestamp():
            raise HTTPNotModified()

        ct, encoding = mimetypes.guess_type(str(filepath))
        if not ct:
            ct = 'application/octet-stream'

        resp = self._response_factory()
        resp.content_type = ct
        if encoding:
            resp.headers[hdrs.CONTENT_ENCODING] = encoding
        resp.last_modified = st.st_mtime

        file_size = st.st_size

        resp.content_length = file_size
        resp.set_tcp_cork(True)
        try:
            yield from resp.prepare(request)

            with filepath.open('rb') as f:
                yield from self._sendfile(request, resp, f, file_size)

        finally:
            resp.set_tcp_nodelay(True)

        return resp


@asyncio.coroutine
def render(request, resp_cls, tmplfile):
    from mako.template import Template
    from plim import preprocessor

    resp = resp_cls()
    resp.content_type = 'text/html'
    yield from resp.prepare(request)

    tmpl = Template(filename=str(tmplfile), preprocessor=preprocessor)
    output = tmpl.render().encode('utf-8')
    resp.content_length = len(output)
    resp.write(output)
    return resp


route = CustomStaticRoute(None, '/', '.')
resource = StaticResource(route)
app.router._reg_resource(resource)


if __name__ == '__main__':
    import sys
    sys.argv = ['', 'run', '--bind=127.0.0.1:8000', '--reload']
    app.manage()
