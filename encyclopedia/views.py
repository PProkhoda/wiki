from html import entities
from django.shortcuts import render

from . import util

# import Markdown for transform Markdown to HTML
from markdown2 import Markdown
# import random for "random page"
from random import choice

from django import forms

from django.urls import reverse
from django.http import HttpResponseRedirect


# create class for "new page"
class NewEntryForm(forms.Form):
    title = forms.CharField(label='title', widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    

# function for "index page"
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# function for "entry page"
def entry(request, title):
    markdowner = Markdown()
    entrypage = util.get_entry(title)
    if entrypage is None:
        return render(request, "encyclopedia/nonentry.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "text": markdowner.convert(entrypage),
            "title": title
        })
        

# function for "serch page"        
def search(request):
    value = request.GET.get('q', '')
    # value = request.GET.get('q')
    entries = util.list_entries()
    search_entry = util.get_entry(value)
    if search_entry is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'title': value}))
    else:
        search_entries = []
        for entry in entries:
            if value.upper() in entry.upper():
                search_entries.append(entry)
                
        return render(request, "encyclopedia/search.html", {
            "entries": search_entries,
            "value": value
        })


# function for "new page"
def new(request):
    if request.method == "POST":
        # fill in the form from POST request
        form = NewEntryForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            title = form.cleaned_data["title"]
            if(util.get_entry(title)) is None:
                util.save_entry(title, text)
                # return HttpResponseRedirect(reverse("index"))
                return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "exist": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
                "exist": False
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm(),
            "exist": False
        })
        
        
def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "text": text
        })
        
        
def save(request):
    if request.method == "POST":
        title = request.POST['edittitle']
        text = request.POST['edittext']
        util.save_entry(title, text)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
            
    
def random(request):
    titles = util.list_entries()
    title = choice(titles)
    return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    
