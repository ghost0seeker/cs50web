from django.core.checks import messages
from django.forms import widgets
from django.http import JsonResponse
from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
from django import forms

class EditorForm(forms.Form):
    title = forms.CharField(initial='Title',widget=forms.TextInput(attrs={
        'class': 'form-control title',
        'autocomplete': 'off',
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
               return JsonResponse({
                'status': 'success',
                'message': 'File Created!'
               }, status=200) 
            else:
                return JsonResponse({
                    'status': 'file_exists',
                    'message': 'File Exists'
                }, status=409)
        else:               
            return JsonResponse({
                'status': 'form_invalid',
                'message': 'Form validation failed',
                'errors': form.errors
            }, status=400)

    return render(request, "encyclopedia/new.html", {
        "form": EditorForm()
    })