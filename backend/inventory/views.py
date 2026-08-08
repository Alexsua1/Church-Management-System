from django.shortcuts import render, redirect
from django.contrib import messages

from .models import InventoryItem
from .forms import InventoryItemForm
from backend.accounts.decorators import staff_required


@staff_required
def item_list(request):
    items = InventoryItem.objects.all()
    return render(request, "inventory/item_list.html", {"items": items})


@staff_required
def item_create(request):
    form = InventoryItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Inventory item added.")
        return redirect('inventory:list')
    return render(request, "inventory/item_form.html", {"form": form})
