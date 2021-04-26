import random

from django.shortcuts import render

from . import util
from django.http import HttpResponseRedirect, HttpResponse
from markdown import Markdown
from django.urls import reverse

wiki_entries_directory = "entries/"

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "Encyclopedia"
    })

def title(request, title):
    entry_contents = util.get_entry(title)
    html_entry_contents = Markdown().convert(entry_contents) if entry_contents else None

    return render(request, "encyclopedia/entry_page.html", {
        "body_content": html_entry_contents,
        "entry_exists": entry_contents is not None,
        "title": title if entry_contents is not None else "Error"
    })
    

def search(request):
    query = request.GET['q']
    if util.get_entry(query):
        return HttpResponseRedirect(reverse( "title", args=(query,)))
    else:
        #query does not match
        return render(request, "encyclopedia/index.html", {
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
            "title": f'"{query}" search results',
            "heading": f'Related search for "{query}" :'
            })
    

def new_page(request): 
    return render(request, "encyclopedia/new_page.html",{
        'edit_mode': False,
        'edit_title_page':'',
        'edit_page_content': ''
    })


def edit(request,title):
    entry_contents= util.get_entry(title)
    if entry_contents is None:
        #somebody came up with the url for editing a page that doesnot exists
        return HttpResponseRedirect(reverse('index'))
    
    return render( request, "encyclopedia/new_page.html", {
        "edit_mode": True,
        "edit_title_page": title,
        'edit_page_contents': entry_contents
    })

def save_page(request, title=None):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"))
    else:
        assert (request.method == 'POST')
        entry_content = request.POST['entry_content']
        if not title:
            # We are saving a new page
            title = request.POST['title']
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                return render(request, "encyclopedia/error.html", {
                    "error_title": "saving page",
                    "error_message": "An entry with that title already exists! Please change the title and try again."
                })

        filename = wiki_entries_directory + title + ".md"
        with open(filename, "w") as f:
            f.write(entry_content)
        return HttpResponseRedirect(reverse("title", args=(title,)))


def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", args=(title,)))