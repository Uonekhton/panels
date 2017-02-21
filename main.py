import asyncio, jinja2, aiohttp_jinja2, await, subprocess
from aiohttp import web


commands = {
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
    context = {}
    for daemon in service:
        status = subprocess.call('service %s status' %daemon,
                        shell=True,
                        stdout=open('/dev/null', 'w'),
                        stderr=subprocess.STDOUT
                        )
        tt = {daemon: commands[status]}
        context.update({daemon: tt})

    return aiohttp_jinja2.render_template('index.html', request, context)


@asyncio.coroutine
def command(self):
    data = await.processes(self.request.post())
    pass

app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('templates/'))
app.router.add_static('/static/', path='static/', name='static')
app.router.add_get('/', handle)

web.run_app(app)