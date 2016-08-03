from aiohttp import web


def main():
    app = web.Application()
    app.router.add_route('GET', '/', index)
    app.router.add_route('POST', '/upload/', upload)
    web.run_app(app)


async def index(request):
    with open('index.html') as fp:
        return web.Response(text=fp.read(), content_type='text/html')


async def upload(request):
    data = await request.post()

    upload = data['upload']
    print(upload.filename)

    return web.Response(text='file uploaded', content_type='text/html')


if __name__ == '__main__':
    main()
