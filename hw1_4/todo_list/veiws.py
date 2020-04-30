from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import TodoItem, TodoLists
from .forms import TodoForm


def index(request):
    lists_ = TodoLists.objects.order_by('id')
    lists = {}
    items = TodoItem.objects.order_by('id')
    for l in lists_.values_list():
        lists[l[1]] = items.filter(list_id_id=l[0])
    form = TodoForm()
    context = {
        'lists': lists,
        'form': form
    }

    return render(request, 'todo_list/index.html', context)


@require_POST
def add_todo(request, l_id):
    form = TodoForm(request.POST)
    if form.is_valid():
        list_ = TodoLists.objects.get(list_name=l_id)
        new_item = TodoItem(text=request.POST['text'], list_id=list_)
        new_item.save()
    return redirect('index')


def complete_todo(request, item_id):
    item = TodoItem.objects.get(pk=item_id)
    item.completed = not item.completed
    item.save()
    print("onclick")
    return redirect('index')


@require_POST
def create_list(request):
    form = TodoForm(request.POST)
    if form.is_valid():
        new_list = TodoLists(list_name=request.POST['text'])
        try:
            new_list.save()
        except Exception as e:
            print(e)
    return redirect('index')


def remove_list(request, l_name):
    TodoLists.objects.get(list_name=l_name).delete()

    return redirect('index')
