# Graphviz Rendering Demos

## Python Implementation

Takes a raw string in a dot file format and converts to an image file. Not the best for displaying to the website unless we plan on saving images in the database.

[Documentation](https://graphviz.readthedocs.io/en/stable/)

#### Dependencies:

* `pip3 install graphviz`

## JavaScript Implementation

Takes a raw string in a dot file format and renders the graphviz visualization on a web page as an svg. This is very flexible, and after playing around with for a bit, I like this option the best.

[Documentation](https://github.com/magjac/d3-graphviz#d3-graphviz)

#### Dependencies:

These dependencies are manually specified in the html display file.
* `npm install d3`, must be d3 v5 or greater
* `npm install graphviz`, dependency for `d3-graphviz`
* `npm install d3-graphviz`
