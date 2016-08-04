import muffin


app = muffin.Application('example')


@app.register('/', '/hello/{name}')
def hello(request):
    name = request.match_info.get('name', 'anonymous')
    return 'Hello %s!' % name


if __name__ == '__main__':
    import sys
    sys.argv = ['', 'run', '--bind=127.0.0.1:8000', '--reload']
    app.manage()
