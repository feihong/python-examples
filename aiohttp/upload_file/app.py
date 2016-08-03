from aiohttp import web


def main():
    app = web.Application()
    app.router.add_route('GET', '/', index)
    app.router.add_route('POST', '/upload-using-form/', upload_using_form)
    app.router.add_route('POST', '/upload-using-ajax/', upload_using_ajax)
    web.run_app(app)


async def index(request):
    with open('index.html') as fp:
        return web.Response(text=fp.read(), content_type='text/html')


async def upload_using_form(request):
    data = await request.post()
    print(data['upload'].filename)
    print(data['upload'].content_type)
    return web.Response(text='file uploaded', content_type='text/html')


async def upload_using_ajax(request):
    data = await request.read()
    print('Size: %d' % len(data))
    return web.Response(text='file uploaded', content_type='text/html')


if __name__ == '__main__':
    main()
