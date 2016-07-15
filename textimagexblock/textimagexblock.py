"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class TextImageXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    background_url = String(help="URL of the background image", default=None, scope=Scope.content)
    text_color = String(help="Color of displayed text", default='white', scope=Scope.content)
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
                                                background_url=self.background_url,
                                                text_color=self.text_color,
                                                header_text=self.header_text,
                                                content_text=self.content_text
                                                ))

        frag.add_css(self.resource_string("static/css/textimagexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio_view.js"))
        frag.initialize_js('StudioEditSubmit')


        return frag


    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.display_name = data.get('display_name')
        self.background_url = data.get('background_url')
        self.text_color = data.get('text_color')
        self.header_text = data.get('header_text')
        self.content_text = data.get('content_text')

        return {'result': 'success'}

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
