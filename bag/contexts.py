

def bag_content(request):
    bag_items = []
    total = 0
    items_count = 0
    context = {
        'bag_items': bag_items,
        'total': total,
        'items_count': items_count,
    }
    return context
