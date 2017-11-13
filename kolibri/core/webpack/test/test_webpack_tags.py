from __future__ import absolute_import, print_function, unicode_literals

from django.template import Template, Context
from django.test.testcases import TestCase

from .base import TestHook
from kolibri.core.webpack.hooks import WebpackBundleHook
import os
import random

DEFAULT_PLUGINS = [
    # Note from Devon -
    # Temporarily adding these here to get things working for most devs.
    # It's not clear to me where the correct place to add them is.
    "kolibri.plugins.management",
    "kolibri.plugins.learn",
    "kolibri.plugins.document_pdf_render",
    "kolibri.plugins.html5_app_renderer",
    "kolibri.plugins.media_player",
    "kolibri.plugins.setup_wizard",
    "kolibri.plugins.coach",
    "kolibri.plugins.user",
    "kolibri.plugins.style_guide"  # TODO - remove before merging in to a release branch
]

class KolibriTagNavigationTestCase(TestCase):

    def r_flag_body(self, specified_plugins):
        file = open(".input_file.txt", "w+")
        file.write(specified_plugins)
        file.close()

        file = open(".input_file.txt", "r+")
        input_file = file.read().split('\n')
        input_file = filter(None, input_file)

        result = [hook.webpack_bundle_data for hook in WebpackBundleHook().registered_hooks if (hook.webpack_bundle_data and any(hook.__module__.startswith(input) for input in input_file))]
        return result

    def setUp(self):
        super(KolibriTagNavigationTestCase, self).setUp()
        self.test_hook = TestHook()

    def test_r_flag_3_plugins(self):

        result = self.r_flag_body("kolibri.plugins.html5_app_renderer\nkolibri.plugins.learn\nkolibri.plugins.document_pdf_render")

        os.remove('./.input_file.txt')
        self.assertEqual(len(result), 3)

    def test_r_flag_random(self):

        specified_plugins = ""
        num_elems = 0
        for plugin in DEFAULT_PLUGINS:
            if random.random() >= .5:
                specified_plugins += plugin + '\n'
                num_elems += 1
                # there's two management plugins
                if plugin == "kolibri.plugins.management":
                    num_elems += 1

        print (specified_plugins)
        result = self.r_flag_body(specified_plugins)

        os.remove('./.input_file.txt')
        self.assertEqual(len(result), num_elems)

    def test_frontend_tag(self):
        self.assertIn(
            "non_default_frontend",
            self.test_hook.render_to_page_load_sync_html()
        )

    def test_frontend_tag_in_template(self):
        t = Template(
            """{% load webpack_tags %}\n{% webpack_asset 'non_default_frontend' %}""")
        c = Context({})
        self.test_hook._stats_file
        self.assertIn(
            self.test_hook.TEST_STATS_FILE_DATA['chunks'][TestHook.unique_slug][0]['name'],
            t.render(c)
        )
