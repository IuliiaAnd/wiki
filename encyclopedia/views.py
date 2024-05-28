from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
from django import forms
import random
from django.urls import reverse


def convert_markdown_to_html(content):
    markdowner = Markdown()
    return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    # Check if no title exists
    if not util.get_entry(title):      
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
            })                       
    else:
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "content": convert_markdown_to_html(util.get_entry(title))
        })   


def search (request): 
    if request.method == "GET":   
        query = request.GET.get("q", "").lower()
        entry_list = util.list_entries()
        for entry in entry_list:
            if query.lower() == entry.lower():   #if exact match
                return render(request, "encyclopedia/entry_page.html", {
                "title": entry,
                "content": convert_markdown_to_html(util.get_entry(entry))
                })        
        # Substring match
        results = []          
        for entry in entry_list:
            if query.lower() in entry.lower():
                results.append(entry)        
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results
        })    
    # If the request method is not GET
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create_new_entry(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')        
        # if the title already exists return error
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This title already exists."
            })
        else:
            #add to list of entries
            util.save_entry(title, content)   
            return render(request,"encyclopedia/entry_page.html", {
                "title": title,
                "content": convert_markdown_to_html(content)
                })
    # If the request method is not GET
    return render(request, "encyclopedia/create_entry.html")
    
class EditForm(forms.Form):
    content = forms.CharField(label="Markdown Content:", widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}))    

def edit_content(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        if content is not None:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "edit_form": EditForm(initial={'content': content})
            })
        return render(request, "encyclopedia/error.html", {
            "message": "Something went wrong."
        })
    else:
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry_page.html", {
                "title": title,
                "content": convert_markdown_to_html(content)
            })
        
'''Random Page Option1

def random_page(request):
    all_entries = util.list_entries()
    title = random.choice(all_entries)
    return redirect(reverse('entry', args=[title]))
'''
''' Option2 '''
                  
def random_page(request):
    # Get a list of all entries
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    # Get the content
    content = util.get_entry(random_entry)
    random_content = convert_markdown_to_html(content)
    return render(request, "encyclopedia/entry_page.html", {
                "title": random_entry,
                "content":  random_content
            })         
   
