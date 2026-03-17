from django.shortcuts import render, redirect
import re
import markdown2
from django.template.defaultfilters import length

from .import util
import random


def index(request):
    entries = util.list_entries()
    print(entries)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    q = request.POST.get("q")
    entry_list = util.list_entries()
    if q in entry_list:
        entry = util.get_entry(q)
        return render(request, "encyclopedia/page.html", {
            "title": q,
            "body": entry
        })
    matches = []
    for entry in entry_list:
        if q.lower() in entry.lower():
            matches.append(entry)
    if matches:
        return render(request, "encyclopedia/search_results.html", {
            "matches": matches
        })
    else:
        return render(request, "encyclopedia/page_not_found.html", {
            "title": q
        })

def wiki_page(request, title):
    entry = util.get_entry(title)
    html = markdown2.markdown(entry)
    if entry:
        return render(request, "encyclopedia/page.html", {
        "title": title,
        "body": html})
    else: return render(request, "encyclopedia/page_not_found.html", {"title":title} )

def create_page_form(request):
    return render(request, "encyclopedia/create_new_page.html")

def create_page(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    with open(f"D:\Python_projects\wiki\entries\{title}.md", "w", encoding="utf-8") as f:
        f.write(content)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "body": content})

def edit_page(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html" , {"title":title, "body":entry})

def save_edit(request, title):
    content = request.POST.get("content")
    util.save_entry(title, content)
    return redirect("wiki_page", title=title)

def random_page(request):
    entries = util.list_entries()
    page = random.choice(entries)
    entry = util.get_entry(page)
    return render(request, "encyclopedia/page.html", {
        "title": page,
        "body": entry})