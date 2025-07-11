from django import template

from posts.models import Post

register = template.Library()

class RecentPostsNode(template.Node):
    def __init__(self, count, var_name):
        self.count = int(count)
        self.var_name = var_name

    def render(self, context):
        recent_posts = Post.objects.order_by('-created_at')[:self.count]
        context[self.var_name] = recent_posts
        return ''


@register.tag
def get_recent_posts(parser, token):
    try:
        tag_name, count, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "Tag 'get_recent_posts' requires exactly three arguments"
        )
    return RecentPostsNode(count, varname)