from django import template

register = template.Library()


@register.filter(name=u'modify_field_title')
def modify_field_title(form):
    """
    Modifies form request_to_join_group when an error occurs to
    prevent rendering group id without title in select2
    """
    new_data = form.data.copy()
    new_data[u'request_to_join_group'] = ''
    form.data = new_data
