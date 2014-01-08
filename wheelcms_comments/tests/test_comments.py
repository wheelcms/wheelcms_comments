from two.ol.base import Redirect
from twotest.util import create_request

from wheelcms_axle.node import Node
from wheelcms_axle.main import MainHandler
from wheelcms_axle.tests.models import Type1
from wheelcms_axle.tests.test_handler import superuser_request
from wheelcms_axle.tests.test_spoke import BaseSpokeTest, BaseSpokeTemplateTest
from wheelcms_axle.tests.test_impexp import BaseSpokeImportExportTest
from wheelcms_axle.tests.utils import MockedQueryDict

from wheelcms_comments.models import CommentType
from wheelcms_comments.models import Comment, handle_comment_post
from wheelcms_comments.templatetags.wheel_comments import CommentFormNode


class TestComments(object):
    """
        Test specific comment behaviour
    """
    def test_comment_initial_state(self, client, root):
        """ The initial state of a comment is 'pending' """
        t = Type1(node=root).save()
        req = superuser_request("/", method="POST", name="1", body="1", captcha="1")
        handler = MainHandler(request=req, instance=root)
        try:
            handle_comment_post(handler, req, "+post_comment")
        except Redirect:
            pass  ## expected
        assert root.children()[0].content().state == "pending"

    def test_show_comments_authenticated(self, client, root):
        """ An authenticated user (with sufficient access) should see
            pending and published comments """
        t = Type1(node=root).save()
        c1 = Comment(title="1", body="1", state="pending",
                     node=root.add("c1")).save()
        c2 = Comment(title="2", body="2", state="published",
                     node=root.add("c2")).save()
        cfn = CommentFormNode()
        req = superuser_request("/")
        res = cfn.show_comments(root, req)

        assert len(res) == 2
        assert set(res) == set((c1, c2))

    def test_hide_rejected_authenticated(self, client, root):
        """ An authenticated user (with sufficient access) should still
            not see rejected comments """
        t = Type1(node=root).save()
        c1 = Comment(title="1", body="1", state="rejected",
             node=root.add("c1")).save()
        cfn = CommentFormNode()
        req = superuser_request("/")
        res = cfn.show_comments(root, req)

        assert len(res) == 0

    def test_show_comments_anonymous(self, client, root):
        """ An anonymous user should only see published and "own" comments """
        t = Type1(node=root).save()
        req = create_request("POST", "/",
                             data=dict(name="1", body="1", captcha="1"))
        handler = MainHandler(request=req, instance=root)
        try:
            handle_comment_post(handler, req, "+post_comment")
        except Redirect:
            pass  ## expected
        c2 = Comment(title="2", body="2", state="published",
                     node=root.add("c2")).save()
        rejected = Comment(title="3", body="3", state="rejected",
                           node=root.add("c3")).save()
        cfn = CommentFormNode()
        res = cfn.show_comments(root, req)

        assert len(res) == 2
        ## all children except rejected
        assert set(res) == set(c.content() for c in root.children()) - \
                           set((rejected,))


class TestCommentSpokeTemplate(BaseSpokeTemplateTest):
    """ Test the Comment type """
    type = CommentType

    def valid_data(self):
        """ return additional data for Comment validation """
        return MockedQueryDict(name="J. Doe", body="Hello World",
                               captcha="fail")


class TestCommentSpoke(BaseSpokeTest):
    """ Test the Comment type """
    type = CommentType

class TestCommentSpokeImpExp(BaseSpokeImportExportTest):
    type = Comment
    spoke = CommentType

#class TestCommentSpokeSearch(BaseTestSearch):
#    type = CommentType
# comments are not searchable, so these tests will fail. Current search testing
# setup isn't too good anyway
