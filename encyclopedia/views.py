from django.http import HttpResponse
from django.shortcuts import render

from . import util
from markdown2 import Markdown


def index(request):
    entries = util.list_entries()
    return render(
        request,
        "encyclopedia/index.html",
        {
            "entries": entries,
        },
    )


def title(request, title):
    if not util.get_entry(title):
        return HttpResponse("Error. Page not found.")

    markdown = Markdown()
    markdown_file = markdown.convert(util.get_entry(title))
    return render(
        request,
        f"encyclopedia/article.html",
        {
            "title": title,
            "markdown_file": markdown_file,
        },
    )

def search(request):
    pass
