import subprocess
import muffin
from muffin.urls import StaticRoute, StaticResource


app = muffin.Application('example')


@app.register('/hello/')
def hello(request):
    return 'Hello World!'


route = StaticRoute(None, '/', '.')
resource = StaticResource(route)
app.router._reg_resource(resource)


if __name__ == '__main__':
    import sys
    sys.argv = ['', 'run', '--bind=127.0.0.1:8000', '--reload']
    app.manage()
