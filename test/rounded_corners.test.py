import sys
import os

ext_dir = '/usr/share/inkscape/extensions/'
sys.path.append(ext_dir)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

import unittest
import inkex

from rounded_corners import RoundCorners

testdoc=os.path.join(root_dir, 'test', 'rounded_corners.test.svg')


class RoundCornersTest(unittest.TestCase):
    def test_adds_path(self):
        args = ['--top-right=1.0', '--id=rect', testdoc]
        e = RoundCorners()
        e.run(args)
        rect = e.document.xpath('//svg:rect', namespaces=inkex.NSS)
        self.assertTrue(len(rect)>0, "Test that rectangle el was found")
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)
        self.assertTrue(len(path)>0, "Test that path el was found")

    def test_adds_ten_nodes(self):
        args = ['--top-left=1.0',
                '--top-right=1.0',
                '--bottom-right=1.0',
                '--bottom-left=1.0',
                '--id=rect', testdoc]
        e=RoundCorners()
        e.run(args)
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0]
        parsed_path = path.path.to_arrays()
        self.assertEqual(len(parsed_path), 9, "Test that four rounded corners result in ten nodes of the path.") # close segment is part of the path?

    def test_adds_seven_nodes(self):
        args = ['--top-left=1.0',
                '--id=rect', testdoc]
        e=RoundCorners()
        e.run(args)
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0]
        parsed_path = path.path.to_arrays()
        self.assertEqual(len(parsed_path), 6, "Test that one rounded corner results in seven nodes of the path.") # close segment is part of the path

    def test_inherit_style(self):
        args = ['--top-left=1.0',
                '--id=rect',
                '--inherit-style=true',
                testdoc]

        e=RoundCorners()
        e.run(args)
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0]
        self.assertEqual(path.attrib['class'], 'black-rect', 'Test that css class was copied')
        self.assertEqual(path.attrib['style'], 'fill:#000000', 'Test that style was copied')

    def test_not_inherit_style(self):
        args = ['--top-left=1.0',
                '--id=rect',
                '--inherit-style=false',
                testdoc]

        e=RoundCorners()
        e.run(args)
        path = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0]
        self.assertFalse('class' in path.attrib, 'Test that css class was not copied')
        self.assertFalse('style' in path.attrib, 'Test that style was copied')

if __name__ == '__main__':
    unittest.main()
