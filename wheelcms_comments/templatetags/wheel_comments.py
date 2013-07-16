from django import template
from django.template.loader import render_to_string
from django.template import RequestContext

from wheelcms_axle.access import has_access
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
        instance = context['instance']

        if 'comment_post' in request.session:
            data = request.session['comment_post']
            del request.session['comment_post']
            form = CommentForm(data)
        else:
            form = CommentForm()
        
        ha = has_access(request.user, instance)

        # if ha, show all, else show published + owner (from session)
        comments = [x.content()
                    for x in instance.children().filter(
                          contentbase__meta_type=Comment.classname)]
        mine = request.session.get('posted_comments', [])


        if not ha:
            comments = [c for c in comments
                        if c.state == "published" or c.node.path in mine]


        return render_to_string("wheelcms_comments/commentform.html",
            {'form':form, 'comments':comments, 'ha':ha},
            context_instance=RequestContext(request))
