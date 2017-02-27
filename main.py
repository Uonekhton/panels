import asyncio, jinja2, aiohttp_jinja2, await, subprocess
from aiohttp import web


signal2 = {
    0: 'запущен',
    3: 'остановлен',
    127: 'недостаточно прав',
}


service = (
    'nginx',
    'mysql',
)
        

@asyncio.coroutine
def handle(request):
    daemons = {}
    signal = signal2
    for item in service:
        status = Command._status(item)
        daemon = item
        daemons[daemon] = status

    return aiohttp_jinja2.render_template('index.html', request, {'daemons': daemons,
                                                                  'signal': signal,
                                                                  })


@asyncio.coroutine
class Command:
    def _status(item):
        status = subprocess.call('service %s status' % item,
                                 shell=True,
                                 stdout=open('/dev/null', 'w'),
                                 stderr=subprocess.STDOUT
                                 )
        return status
    
    def panel(request):
        panel = subprocess.call('service %s %s' % (request.url.query.get('daemon'), request.url.path.replace('/', '')),
                                shell=True,
                                stdout=open('/dev/null', 'w'),
                                stderr=subprocess.STDOUT
                                )
        return web.HTTPFound('/')

app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('templates/'))
app.router.add_static('/static/', path='static/', name='static')
app.router.add_get('/', handle)
app.router.add_get('/{command}', Command.panel)

web.run_app(app)