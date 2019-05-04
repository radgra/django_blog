from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_post_liked(context):
    post = context['post']
    request = context['request']
    if request.user.is_authenticated and not request.user.is_writer:
        liked = request.user.userprofil.like_set.filter(post=post)
        print(liked)
        if len(liked) > 0:
            return True
    
    return None