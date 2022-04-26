from category.models import Category

def categories(request):

    catogories_list = Category.objects.all()

    return dict(links=catogories_list)




