import sys

ext_dir = '/usr/share/inkscape/extensions/'
sys.path.append(ext_dir)
sys.path.append('../')

import unittest
import inkex
import simplepath

from rounded_corners import RoundCorners

testdoc='./set_css_class.test.svg'

class RoundCornersTest(unittest.TestCase):
    def test_adds_path(self):
        args = ['--top-right=1.0', '--id=rect', testdoc]
        e = RoundCorners()
        e.affect(args, False)
        rect = e.document.xpath('//svg:rect', namespaces=inkex.NSS)
        self.assertTrue(len(rect)>0, "Test that rectangle el was found")
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)
        self.assertTrue(len(path)>0, "Test that path el was found")

    def test_adds_six_nodes(self):
        args = ['--top-left=1.0',
                '--top-right=1.0',
                '--bottom-right=1.0',
                '--bottom-left=1.0',
                '--id=rect', testdoc]
        e=RoundCorners()
        e.affect(args, False)
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0]
        parsed_path = simplepath.parsePath(path.attrib['d'])
        self.assertEquals(len(parsed_path), 10) # close segment is part of the path

    def test_adds_three_nodes(self):
        args = ['--top-left=1.0',
                '--id=rect', testdoc]
        e=RoundCorners()
        e.affect(args, False)
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0]
        parsed_path = simplepath.parsePath(path.attrib['d'])
        self.assertEquals(len(parsed_path), 7) # close segment is part of the path
        
if __name__ == '__main__':
    unittest.main()
