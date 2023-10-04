from django.shortcuts import render
from markdown2 import Markdown 
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_md_to_html(title):    
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    

def entry(request, entry):

    entry_content = convert_md_to_html(entry)

    if(entry_content):
        return render(request, 'encyclopedia/entry.html', {
            'entry': entry,
            'entry_content': entry_content
        })
    else:
        return render(request, 'encyclopedia/error.html', {
            'error_message': "This entry does not exist."
        })

   
def search(request):
    if request.method == 'POST':
        query = request.POST['q']
        entry_html = convert_md_to_html(query) 

        if entry_html is not None:
            return render(request, 'encyclopedia/entry.html', {
                'entry': query,
                'entry_content': entry_html
            })
        else:
            allEntries = util.list_entries()
            recommendations = []

            for entry in allEntries:
                if query.lower() in entry.lower():
                    recommendations.append(entry)

            return render(request, 'encyclopedia/recommendations.html', {
                'query': query,
                'recommendations': recommendations
            })
        

def new_page(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html')
    else:
        title = request.POST['title']
        content = request.POST['content']

        entryExists = util.get_entry(title)
        
        if entryExists:
            return render(request, 'encyclopedia/new_page.html', {
                'message': f"There's already an entry with this title ({title})."
            })
        else:
            util.save_entry(title, content)

            content_html = convert_md_to_html(title)

            return render(request, 'encyclopedia/entry.html', {
                'entry_content': content_html,
                'entry': title
            })
        

def edit_entry(request, entry):
    if request.method == 'GET':
        entry_content = util.get_entry(entry)

        return render(request, 'encyclopedia/edit_entry.html', {
            'entry': entry,
            'entry_content': entry_content
        })
    else:
        title = request.POST['title']
        content = request.POST['content'] 
        
        util.save_entry(title, content)

        entry_content = convert_md_to_html(title)

        return render(request, 'encyclopedia/entry.html', {
            'entry': title,
            'entry_content': entry_content
        })


def delete_entry(request, entry):
    if request.method == 'POST':
        util.delete_entry(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def random_entry(request):
    allEntries = util.list_entries()
    random_entry = random.choice(allEntries)
    entry_content = convert_md_to_html(random_entry)

    return render(request, 'encyclopedia/entry.html', {
        'entry': random_entry,
        'entry_content': entry_content
    })

