from commerce.models import Category


def categories(request):
    return {
        'categories': Category.tree()
    }
