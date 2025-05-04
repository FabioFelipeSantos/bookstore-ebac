from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import git


@csrf_exempt
def update(request):
    if request.method == "POST":
        """
        Caminho até o diretório com o clone do REPO no site do PythonAnywhere
        """
        repo = git.Repo("/home/fabiosantos2506/bookstore-ebac")
        origin = repo.remotes.origin

        origin.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


def hello_world(request):
    template = loader.get_template("hello_world.html")
    return HttpResponse(template.render())
