from django.core.checks import messages
from django.forms import widgets
from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
from django import forms
import random

class EditorForm(forms.Form):
    title = forms.CharField(initial='Title',widget=forms.TextInput(attrs={
        'class': 'form-control title',
    }))
    
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'content',
        'name': 'content'
    }))

def apology(request, message, status_code):
    return render(request, "encyclopedia/apology.html", {
        "message": message,
        "status_code": status_code 
    })

def index(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    if query:
        return search(request, query)
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    query = request.GET.get("q")
    if query:
        return search(request, query)

    md_string = util.get_entry(title)

    if not md_string:
        return apology(request, "Entry Not Found", 404)
    else:
        md_html = markdown(md_string)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "md_html": md_html,
        })

def search(request, query):
    entries = util.list_entries()
    exact_match = [entry for entry in entries if query == entry]
    if exact_match:
        return redirect('wiki', title=query)
    else:
        matches = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "matches": matches,
            })

def new(request):
    if request.method == "POST":
        form = EditorForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if util.save_new_entry(title, content):
                return redirect('wiki', title=title)
            else:
                return render(request,"encyclopedia/new.html", {
                    "form": form,
                    "file_exists": True,
                })
        else:               
            return render(request,"encyclopedia/new.html", {
                "form": form
                })                
    return render(request, "encyclopedia/new.html", {
        "form": EditorForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = EditorForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            util.save_entry(title, content)
            return redirect('wiki', title=title)
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    
    form = EditorForm(initial={
        'title': title,
        'content': util.get_entry(title)
    })

    return render(request, "encyclopedia/edit.html", {
        "form": form,
    })

def random_wiki(request):
    
    entries = util.list_entries()
    previous_title = request.session.get('last-random-title')

    if len(entries) > 1:
        title = random.choice(entries)
        while title == previous_title:
            title = random.choice(entries)
    else:
        title = random.choice(entries) if entries else None

    request.session['last-random-title'] = title
    
    return redirect('wiki', title=title)