from django import template

register = template.Library()


@register.simple_tag()
def url_query_append_tag(request, field, value):  # field = page or recipe_name
    dict_ = request.GET.copy()  # request.GET => {"recipe_name": "lasagnia"}
    dict_[field] = value  # {"precipe_name": "lasagnia", "page": 2}

    return dict_.urlencode()  # {"recipe_name": "lasagnia", "page": 2} => ?recipe_name=lasagnia&page=2
