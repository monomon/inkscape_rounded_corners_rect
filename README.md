![Rounded corners demo](https://media.inkscape.org/media/resources/render/rounded_corners_demo_W5NKSkM.png)

# Custom rounded corners rect

Ever wanted to make some of these fancy folder flap top-side only rounded corners?

Or rounded corners with different radii?

This extension allows the user to draw a rectangle with rounded corners as a path, specifying each corner's radius, in css order.

It also provides an option to remove the selected rectangle when it's done.

The extension works with multiple rectangles selected, too, processing each.

## Installation

Use the included `setup.py` script:

    python setup.py install

This will copy the necessary files to your extensions directory:
* Windows - `%APPDATA%\inkscape\extensions` (e.g. `C:\Users\User\AppData\Roaming\inkscape\extensions`)
* Linux - `$HOME/.config/inkscape/extensions`

## Usage

* Select rectangles in the document, in the menu select `Render->Custom rounded corners rect`.
* Input a radius for each corner in the popup dialog.

## Updates

* 21.10.2020: Updated to work with Inkscape 1.0

## License

GPL-2.0
