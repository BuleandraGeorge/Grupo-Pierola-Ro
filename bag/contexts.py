from django.shortcuts import get_object_or_404
from products.models import product


def bag_content(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        Product = get_object_or_404(product, pk=item_id)
        for size, quantity in item_data['item_size-quantity'].items():
            total += quantity * Product.price
            product_count += quantity
            bag_items.append(
                {
                    'item_id': item_id,
                    'quantity': quantity,
                    'size': size,
                    'product': Product
                })
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count
    }
    return context
