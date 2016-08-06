"""
To run:

muffin hello_world run

"""
import muffin


app = muffin.Application('example', DEBUG=True)


@app.register('/', '/hello/{name}')
def hello(request):
    name = request.match_info.get('name', 'anonymous')
    return 'Hello %s!' % name
