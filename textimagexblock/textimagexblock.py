"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from functools import partial

from django.conf import settings
import uuid

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

from webob.response import Response
from xmodule.contentstore.content import StaticContent
from xmodule.contentstore.django import contentstore

from xblock_django.mixins import FileUploadMixin


class TextImageXBlock(XBlock, FileUploadMixin):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    display_name = String(display_name="Display Name",
                          default="Image",
                          scope=Scope.settings,
                          help="This name appears in the horizontal navigation at the top of the page.")
    background_url = String(help="URL of the background image", default=None, scope=Scope.content)
    mit_type = String(help="Type: text or image", default='text', scope=Scope.settings)
    text_color = String(help="Color of displayed text", default='#ffffff', scope=Scope.content)
    header_text = String(help="Header text content", default='', scope=Scope.content)
    content_text = String(help="Paragraph text content", default='', scope=Scope.content)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the TextImageXBlock, shown to students
        when viewing courses.
        """

        html_str = pkg_resources.resource_string(__name__, "static/html/textimagexblock.html")
        frag = Fragment(unicode(html_str).format(
            display_name=self.display_name,
            mit_type=self.mit_type,
            background_url=self.background_url,
            text_color=self.text_color,
            header_text=self.header_text,
            content_text=self.content_text
        ))

        frag.add_css(self.resource_string("static/css/textimagexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/textimagexblock.js"))
        frag.initialize_js('TextImageXBlock')
        return frag

    # TO-DO: change this view to display your data your own way.
    def studio_view(self, context=None):
        """
        The primary view of the TextImageXBlock, shown to students
        when viewing courses.
        """
        html_str = pkg_resources.resource_string(__name__, "static/html/studio_view.html")
        # display variables
        frag = Fragment(unicode(html_str).format(
            display_name=self.display_name,
            display_description=self.display_description,
            mit_type=self.mit_type,
            background_url=self.background_url,
            text_color=self.text_color,
            header_text=self.header_text,
            content_text=self.content_text
        ))

        frag.add_css(self.resource_string("static/css/textimagexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio_view.js"))
        frag.initialize_js('StudioEditSubmit')

        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        data = request.POST

        self.display_name = data['display_name']
        self.display_description = data['display_description']
        self.mit_type = data['mit_type']
        self.text_color = data['text_color']
        self.header_text = data['header_text']
        self.content_text = data['content_text']

        block_id = data['usage_id']
        if not isinstance(data['thumbnail'], basestring):
            upload = data['thumbnail']
            self.thumbnail_url = self.upload_to_s3('THUMBNAIL', upload.file, block_id, self.thumbnail_url)

        if not isinstance(data['background'], basestring):
            upload = data['background']
            self.background_url = self.upload_to_s3('BACKGROUND', upload.file, block_id, self.background_url)

        return Response(json_body={'result': 'success'})

    def _file_storage_name(self, filename):
        # pylint: disable=no-member
        """
        Get file path of storage.
        """
        path = (
            '{loc.block_type}/{loc.block_id}'
            '/{filename}'.format(
                loc=self.location,
                filename=filename
            )
        )
        return path

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TextImageXBlock",
             """<textimagexblock/>
             """),
            ("Multiple TextImageXBlock",
             """<vertical_demo>
                <textimagexblock/>
                <textimagexblock/>
                <textimagexblock/>
                </vertical_demo>
             """),
        ]
