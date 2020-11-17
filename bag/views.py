from django.shortcuts import render, redirect, reverse


def bag(request):

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):

    quantity = int(request.POST.get('quantity'))
    redirect_URL = request.POST.get('redirect_url')
    size = request.POST['item_size']
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        if size in bag[item_id]['item_size-quantity'].keys():
            bag[item_id]['item_size-quantity'][size] += quantity
        else:
            bag[item_id]['item_size-quantity'][size] = quantity
    else:
        bag[item_id]= {'item_size-quantity': {size: quantity}}

    request.session['bag'] = bag
    return redirect(redirect_URL)


def modify_quantity(request, item_id):
    quantity = int(request.POST.get('quantity'))
    size = request.POST['size']
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id]['item_size-quantity'][size] = quantity
    else:
        del bag[item_id]['item_size-quantity'][size]
        if not bag[item_id]['item_size-quantity']:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('bag'))


def remove_item(request, item_id):
    size = request.POST['size']
    bag = request.session.get('bag', {})
    del bag[item_id]['item_size-quantity'][size]
    if not bag[item_id]['item_size-quantity']:
        bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('bag'))