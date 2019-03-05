from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Sanic
from sanic.response import json

app = Sanic()
env = Environment(
    loader=PackageLoader('ilswlol', 'templates'),
    autoescape=select_autoescape(['html'])
)

@app.route('/')
async def index(request):
    schon_wach = True

    template = env.get_template('index.html')

    if schon_wach:
        if is_curl_like(request.user_agent.string) or request.args.get('raw'):
            return "JA"
        else:
            return template.render('index.html', schon_wach=True)
    else:
        if is_curl_like(request.user_agent.string) or request.args.get('raw'):
            return "NEIN"
        else:
            return template.render('index.html', schon_wach=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
