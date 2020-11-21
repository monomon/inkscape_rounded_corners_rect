#!/usr/bin/env python

"""
Generates a rectangle with rounded corners as a path.
The user can specify each corner's radius in css corner order.

Also allows selecting multiple rectangles, and each gets processed in order.

Quadratic Bezier curves are not yet supported, otherwise they would make the task easier.
And SVG rects do not support different radii for different corners (cite proposal).
"""

__author__ = "Mois Moshev"
__email__ = "mois@monomon.me"
__copyright__ = "Copyright (C) 2017 Mois Moshev"
__license__ = "GPL"

import gettext
import inkex
import inkex.localization
from lxml import etree

inkex.localization.localize()


class RoundCorners(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--top-left", dest="tl",
                                     action="store", type=float,
                                     default=0.0, help="top-left")

        self.arg_parser.add_argument("--top-right", dest="tr",
                                     action="store", type=float,
                                     default=0.0, help="top-right")

        self.arg_parser.add_argument("--bottom-right", dest="br",
                                     action="store", type=float,
                                     default=0.0, help="bottom-right")

        self.arg_parser.add_argument("--bottom-left", dest="bl",
                                     action="store", type=float,
                                     default=0.0, help="bottom-left")
        self.arg_parser.add_argument("--remove-original", dest="remove",
                                     action="store", type=inkex.Boolean,
                                     default=False, help="Remove original rect")

        self.arg_parser.add_argument("--inherit-style", dest="inheritstyle",
                                     action="store", type=inkex.Boolean,
                                     default=True, help="Inherit style from rect")

    @staticmethod
    def createRoundedRect(parent, bbox, corner_radii):
        x, y, w, h = bbox
        tl, tr, br, bl = corner_radii

        pathEl = etree.SubElement(parent, inkex.addNS("path", "svg"))
        d = []

        if tl > 0:
            d.append(["M", [x + tl, y]])
        else:
            d.append(["M", [x, y]])

        if tr > 0:
            d.append(["L", [x + w - tr, y]])
            d.append(["Q", [x + w, y, x + w, y + tr]])
        else:
            d.append(["L", [x + w, y]])

        if br > 0:
            d.append(["L", [x + w, y + h - br]])
            d.append(["Q", [x + w, y + h, x + w - br, y + h]])
        else:
            d.append(["L", [x + w, y + h]])

        if bl > 0:
            d.append(["L", [x + bl, y + h]])
            d.append(["Q", [x, y + h, x, y + h - bl]])
        else:
            d.append(["L", [x, y + h]])

        if tl > 0:
            d.append(["L", [x, y + tl]])
            d.append(["Q", [x, y, x + tl, y]])
        else:
            d.append(["L", [x, y]])
            d.append(["z", []])

        pathEl.set("d", str(inkex.Path(d)))

        return pathEl

    def effect(self):
        tl = float(self.options.tl)
        tr = float(self.options.tr)
        br = float(self.options.br)
        bl = float(self.options.bl)

        paths = []

        print(self.svg.selected)
        for nodeName in self.svg.selected:
            node = self.svg.selected[nodeName]
            # print(dir(self.svg.selected[node]))
            if node.tag == inkex.addNS("rect", "svg"):
                x = float(node.get("x", 0))
                y = float(node.get("y", 0))
                w = float(node.get("width"))
                h = float(node.get("height"))

                pathEl = RoundCorners.createRoundedRect(
                    node.getparent(),
                    (x, y, w, h),
                    (tl, tr, br, bl)
                )
                if self.options.inheritstyle:
                    # copy the styles
                    pathEl.set("style", node.get("style"))

                    # set the same css class if there is one
                    if node.get("class"):
                        pathEl.set("class", node.get("class"))

                paths.append(pathEl)

                if self.options.remove:
                    node.getparent().remove(node)

        if len(paths) == 0:
            inkex.errormsg(_("Please select at least one rectangle."))

if __name__ == "__main__":
    e = RoundCorners()
    e.run()
