from ninja import NinjaAPI

from functional_chatbots.utils import render


app = NinjaAPI()


@app.get('/')
def index(request):
    # Renders templates/pages/index.jinja
    return render(request, 'index')
