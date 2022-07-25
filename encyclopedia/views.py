from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
from . import util
from markdown2 import Markdown
import random
import urllib.parse



class NewSearchForm(forms.Form):
    substring = forms.CharField(max_length=64, label="search")


class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=64, label="title")
    content = forms.CharField(widget=forms.Textarea)


class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


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


def form_search(request):
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


def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")


def new_entry_form(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["content"]

            article = f"#{title}\n{markdown}"

            open(f"./entries/{title}.md", "x")

            with open(f"entries/{title}.md", "w") as file:
                file.write(article)

            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse("Error. Request POST method not found")


def edit_redirector(request, title):
    file = open(f"./entries/{title}.md", "r")
    data = str()
    for line in file:
        data += line
    file.close()
    return render(
        request,
        "encyclopedia/edit_entry.html",
        {
            "article": data,
            "title": title,
        },
    )


def send_edit_form(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            referrer_url = urllib.parse.unquote(request.META.get("HTTP_REFERER"))
            title = referrer_url.split("/")[-1][:-1]
            with open(f"./entries/{title}.md", "w+") as file:
                file.write(content)
            return HttpResponseRedirect(f"wiki/{title}")


def random_entry(request):
    article_sample_size = len(util.list_entries())
    random_article = util.list_entries()[random.randint(0, article_sample_size - 1)]
    markdown = Markdown()
    markdown_file = markdown.convert(util.get_entry(random_article))
    return render(
        request,
        f"encyclopedia/article.html",
        {
            "title": random_article,
            "markdown_file": markdown_file,
        },
    )
