from django import template
from django.template.loader import render_to_string
from django.template import RequestContext

from wheelcms_comments.models import CommentForm, Comment

register = template.Library()

@register.tag(name="commentform")
def commentform(parser, token):
    return CommentFormNode()

class CommentFormNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        request = context['request']
        if 'comment_post' in request.session:
            data = request.session['comment_post']
            del request.session['comment_post']
            form = CommentForm(data)
        else:
            form = CommentForm()
        
        comments = [x.content() for x in context['instance'].children().filter(contentbase__meta_type=Comment.classname)]
        return render_to_string("wheelcms_comments/commentform.html", 
            {'form':form, 'comments':comments},
            context_instance=RequestContext(request))
