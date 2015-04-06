# -*- coding: utf-8 -*-
import cherrypy

from cptestcase import BaseCherryPyTestCase
from test_app import TestApp
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
        self.assertTrue(response.body[0].decode('utf8').replace(" ","").find("<td>4</td>")>=0)

    def test_data(self):
        response = self.request('/data', ex_first='__float__0', output_id='table_id')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')
        resp_dict = json.loads(response.body[0].decode('utf8'))
        print(resp_dict['data'])
        self.assertTrue(len(resp_dict['data']['count'])==3)

    def test_plot(self):
        response = self.request('/plot', title='t', func_type='sin', axis_label='__list__,1', color='g', freq='__float__2',  output_id='plot1')
        self.assertEqual(response.output_status.decode('utf8'), '200 OK')

    def test_image(self):
        response = self.request('/image', ex_first='__float__0', output_id='image')
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

if __name__ == '__main__':
    import unittest
    unittest.main()