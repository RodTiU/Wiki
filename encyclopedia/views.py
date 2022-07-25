from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from . import util
from markdown2 import Markdown


class NewSearchForm(forms.Form):
    substring = forms.CharField(max_length=64, label="search")


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
        "encyclopedia/article.html",
        {
            "title": title,
            "markdown_file": markdown_file,
        },
    )


def form(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data["substring"]
            articles = util.list_entries()
            success_articles = []

            for article in articles:
                if article.lower().__contains__(search_string.lower()):
                    success_articles.append(article)
            
            return render(
                request,
                "encyclopedia/search.html",
                {
                    "articles": success_articles,
                },
            )
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse("Error. Request POST method not found")
