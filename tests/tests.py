# -*- coding: utf-8 -*-
import cherrypy
import unittest

from cptestcase import BaseCherryPyTestCase
from test_app import TestApp
from spyre import server
import json


def setUpModule():
    app = TestApp()
    cherrypy.tree.mount(app.getRoot(), '/')
    cherrypy.engine.start()


setup_module = setUpModule


def tearDownModule():
    cherrypy.engine.exit()


teardown_module = tearDownModule


class TestCherryPyApp(BaseCherryPyTestCase):
    def test_index(self):
        response = self.request('/')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        # response body is wrapped into a list internally by CherryPy
        # self.assertEqual(response.body, ['hello world'])

    def test_html(self):
        response = self.request('/html', output_id='html1')
        print("hello")
        print(response.body[0].decode('utf8'))
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        self.assertEqual(response.body[0].decode('utf8'), "hello world")

    def test_table(self):
        response = self.request('/table', ex_first='__float__0', output_id='table_id')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        self.assertTrue(response.body[0].decode('utf8').replace(" ", "").find("<td>4</td>") >= 0)

    def test_data(self):
        response = self.request('/data', ex_first='__float__0', output_id='table_id')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        resp_dict = json.loads(response.body[0].decode('utf8'))
        print(resp_dict['data'])
        self.assertTrue(len(resp_dict['data']['count']) == 3)

    def test_plot(self):
        response = self.request(
            '/plot', title='t', func_type='sin',
            axis_label='__list__,1', color='g', freq='__float__2',
            output_id='plot1'
        )
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')

    def test_download(self):
        response = self.request('/download', ex_first='__float__0')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')

    def test_no_output(self):
        response = self.request('/no_output')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')

    def test_spinner(self):
        response = self.request('/spinning_wheel')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')

    def test_dropdown_value(self):
        response = self.request('/')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        body = response.body[0].decode('utf8').replace(" ", "")
        self.failUnless('<optionvalue="b"selected="selected">Blue</option>' in body)
        self.failIf('<optionvalue="b">Blue</option>' in body)
        self.failUnless('<optionvalue="g">Green</option>' in body)
        self.failIf('<optionvalue="g"selected="selected">Green</option>' in body)
        self.failUnless('<optionvalue="s">Spotify</option>' in body)
        self.failIf('<optionvalue="s"selected="selected">Spotify</option>' in body)
        self.failUnless('<optionvalue="a">AppleMusic</option>' in body)
        self.failIf('<optionvalue="a"selected="selected">AppleMusic</option>' in body)

        response = self.request('/', color='g')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        body = response.body[0].decode('utf8').replace(" ", "")
        self.failIf('<optionvalue="b"selected="selected">Blue</option>' in body)
        self.failUnless('<optionvalue="b">Blue</option>' in body)
        self.failIf('<optionvalue="g">Green</option>' in body)
        self.failUnless('<optionvalue="g"selected="selected">Green</option>' in body)
        self.failUnless('<optionvalue="s">Spotify</option>' in body)
        self.failIf('<optionvalue="s"selected="selected">Spotify</option>' in body)
        self.failUnless('<optionvalue="a">AppleMusic</option>' in body)
        self.failIf('<optionvalue="a"selected="selected">AppleMusic</option>' in body)

        response = self.request('/', color='asdf', on_demand_streaming_service='a')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        body = response.body[0].decode('utf8').replace(" ", "")
        self.failIf('<optionvalue="b"selected="selected">Blue</option>' in body)
        self.failUnless('<optionvalue="b">Blue</option>' in body)
        self.failUnless('<optionvalue="g">Green</option>' in body)
        self.failIf('<optionvalue="g"selected="selected">Green</option>' in body)
        self.failUnless('<optionvalue="s">Spotify</option>' in body)
        self.failIf('<optionvalue="s"selected="selected">Spotify</option>' in body)
        self.failIf('<optionvalue="a">AppleMusic</option>' in body)
        self.failUnless('<optionvalue="a"selected="selected">AppleMusic</option>' in body)


class TestCallOutputMethod(unittest.TestCase):
    """Unit tests for the _call_output_method security validation."""

    def setUp(self):
        self.app = TestApp()

    def test_valid_method_is_called(self):
        result = self.app._call_output_method({'output_id': 'html1'})
        self.assertEqual(result, "hello world")

    def test_non_identifier_output_id_rejected(self):
        # Attempts to inject code via output_id should raise ValueError
        with self.assertRaises(ValueError):
            self.app._call_output_method({'output_id': '__import__("os").system("id")'})

    def test_dunder_attribute_callable(self):
        # Dunder names are valid identifiers — but should not be callable in a
        # harmful way; this just confirms isidentifier() passes for them.
        # The real guard is that getattr raises AttributeError for missing names.
        with self.assertRaises((AttributeError, TypeError)):
            self.app._call_output_method({'output_id': '__nonexistent__'})

    def test_nonexistent_method_raises(self):
        with self.assertRaises(AttributeError):
            self.app._call_output_method({'output_id': 'no_such_method'})

    def test_non_callable_attribute_rejected(self):
        # A plain data attribute (e.g. 'title') should be rejected as not callable
        with self.assertRaises(ValueError):
            self.app._call_output_method({'output_id': 'title'})


class TestTableXSSEscaping(BaseCherryPyTestCase):
    """Table output must escape HTML in DataFrame cell values."""

    def test_html_in_cell_is_escaped(self):
        # TestApp.getJsonData returns a cell containing a raw <a> tag.
        # With escape=True the tag must not appear verbatim in the response.
        response = self.request('/table', ex_first='__float__0', output_id='table_id')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        body = response.body[0].decode('utf8')
        self.assertNotIn('<a href=', body)
        self.assertIn('&lt;a', body)


if __name__ == '__main__':
    unittest.main()
