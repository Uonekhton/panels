import asyncio
import subprocess
from aiohttp import web


@asyncio.coroutine
def handle(request):
    status = subprocess.call('service nginx status',
                    shell=True,
                    stdout=open('/dev/null', 'w'),
                    stderr=subprocess.STDOUT
                    )
    if status == 3:
        text = 'Сервис Nginx остановлен'
    elif status == 0:
        text = 'Сервис Nginx работает'
    return web.Response(text=text)

app = web.Application()
app.router.add_get('/', handle)

web.run_app(app)