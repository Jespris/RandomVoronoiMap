# RandomVoronoiMap
Make randomized Voronoi diagrams with coloring to slightly resemble a map

This project is made as part of a bigger project I'm working on, where I need randomly generated maps of regions colored differenly.
I used the Voronoi package which generates voronoi diagrams, and good ol' pygame to construct a colored image.

Run the script with parameters <image width (int)> <image height (int)> <tiles (int)> <show center points (True/False)>

Some bugs may remain, mainly the "minimum distance between region centers" - property, which is calculated via a formula that hasn't been finetuned, so the value may be too large resulting in the specified amount of tiles might not fit in the image and the process runs indefinately
