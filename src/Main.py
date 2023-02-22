import math
import random

import matplotlib
from foronoi import Voronoi, Polygon

import sys

import pygame as p


class Settings:
    def __init__(self, args):
        self.width: int = int(args[0])
        self.height: int = int(args[1])
        self.tiles: int = int(args[2])
        self.min_size: float = math.sqrt(min(self.width, self.height) / self.tiles)
        self.show_centers: bool = False if args[3] == "False" else True


class Tile:
    def __init__(self, color, center):
        self.color: (int, int, int) = color
        self.center: (int, int) = center


def too_close(center: (int, int), tiles: [Tile], settings: Settings) -> bool:
    for tile in tiles:
        if get_euclidean(center, tile.center) < settings.min_size:
            return True
    return False


def get_random_color():
    i = random.randint(0, 10)
    # color names in pygame can be found at:
    # https://mike632t.wordpress.com/2018/02/10/displaying-a-list-of-the-named-colours-available-in-pygame/
    if i <= 6:
        return p.Color("yellowgreen")
    elif i <= 8:
        return p.Color("darkgreen")
    else:
        return p.Color("royalblue")


def calculate_voronoi_diagram(tiles, settings: Settings):
    # use Fortune's algorithm to generate a Voronoi diagram
    # https://en.wikipedia.org/wiki/Fortune%27s_algorithm
    # using existing code and examples from
    # https://voronoi.readthedocs.io/en/latest/pages/quickstart.html

    points = []
    for tile in tiles:
        points.append(tile.center)
    boundary_box = Polygon([(0, 0), (0, settings.height), (settings.width, settings.height), (settings.width, 0)])

    v = Voronoi(boundary_box)
    v.create_diagram(points=points)
    print(matplotlib.get_backend())
    matplotlib.use('TkAgg')  # because pycharm is wierd
    # Visualizer(v).plot_sites(show_labels=False).plot_edges(show_labels=False).plot_vertices().show()
    return v


def get_euclidean(a, b) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def create_image(v: Voronoi, tiles: [Tile], settings: Settings):
    # maybe use pygame for this?

    screen = p.display.set_mode((settings.width, settings.height))
    screen.fill(p.Color("white"))

    for tile in tiles:
        for site in v.sites:
            if tile.center == site.xy:
                p.draw.polygon(screen, tile.color, [vertex.xy for vertex in site.vertices()])
                p.draw.polygon(screen, p.Color("black"), [vertex.xy for vertex in site.vertices()], 1)
                if settings.show_centers:
                    p.draw.circle(screen, p.Color("black"), tile.center, 2)

    filename = "C:/Users/jespe/PycharmProjects/RandomTilesProject/src/output/Voronoi_map.png"
    p.image.save(screen, filename)
    print(f"Voronoi map has been saved in: {filename}")


def create_tiles(settings: Settings):
    tiles = []
    i = settings.tiles
    while i > 0:
        x = random.randint(0, settings.width - 1)
        y = random.randint(0, settings.height - 1)
        if not too_close((x, y), tiles, settings):
            color = get_random_color()
            tiles.append(Tile(color, (x, y)))
            i -= 1
    return tiles


def main(argv):
    print("This is the main function, hello!")

    settings = Settings(argv)  # settings class is made to better keep track of script arguments

    print("Creating tiles...")
    tiles = create_tiles(settings)
    print("Creating Voronoi diagram...")
    v = calculate_voronoi_diagram(tiles, settings)
    print("Creating image...")
    create_image(v, tiles, settings)


if __name__ == "__main__":
    main(sys.argv[1:])  # skip first arg (script name)
