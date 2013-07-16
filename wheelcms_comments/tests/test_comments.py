from wheelcms_axle.node import Node
from wheelcms_axle.tests.models import Type1
from wheelcms_axle.tests.test_handler import superuser_request

from wheelcms_comments.models import Comment
from wheelcms_comments.templatetags.wheel_comments import CommentFormNode

class TestComments(object):
    def test_show_comments_authenticated(self, client):
        n = Node.root()
        t = Type1(node=n)
        c1 = Comment(title="1", body="1", node=n.add("c1")).save()
        c2 = Comment(title="2", body="2", node=n.add("c2")).save()
        cfn = CommentFormNode()
        req = superuser_request("/")
        res = cfn.show_comments(n, req)

        assert len(res) == 2
        assert set(res) == set((c1, c2))

        ## komt testfailure door south gemiep?
