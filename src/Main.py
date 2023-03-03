import math
import random

import matplotlib
import matplotlib.pyplot as plt
from foronoi import Voronoi, Polygon
import perlin

import sys

import pygame as p


class Settings:
    def __init__(self):
        self.width: int = int(2480)
        self.height: int = int(3508)  # width and height in pixels, (2480, 3508) is common A4 size
        self.tiles: int = int(50)  # nr of tiles
        self.min_size: float = math.sqrt(min(self.width, self.height) / self.tiles)
        self.seed: int = None  # set custom seed (integer or None for random seed)
        if not self.seed:
            self.seed = random.randint(1, 99999)
        # print(f'Seed: {self.seed}')
        self.perlin_map: perlin.Perlin = perlin.Perlin(self.seed)
        self.show_centers: bool = False


class Tile:
    def __init__(self, color, center):
        self.color: (int, int, int) = color
        self.center: (int, int) = center


def too_close(center: (int, int), tiles: [Tile], settings: Settings) -> bool:
    for tile in tiles:
        if get_euclidean(center, tile.center) < settings.min_size:
            return True
    return False


def get_rbg(ratio: float, a: (int, int, int), b: (int, int, int)) -> (int, int, int):
    r = a[0] + (b[0]-a[0]) * ratio
    g = a[1] + (b[1] - a[1]) * ratio
    b = a[2] + (b[2] - a[2]) * ratio
    return (r, g, b)


def get_color_from_perlin(p_value: int) -> (int, int, int):
    # value range from -50 to 50 apparently
    min_value = -50
    max_value = 50
    more_land = -10
    if p_value <= more_land:
        # blue
        if p_value < min_value:
            p_value = min_value
        light_blue = (0, 164, 255)
        dark_blue = (0, 70, 255)
        ratio = (p_value+max_value)/(max_value+more_land)
        return get_rbg(ratio, dark_blue, light_blue)
    else:
        # green
        if p_value > max_value:
            p_value = max_value
        dark_green = (0, 120, 20)
        light_green = (50, 210, 70)
        ratio = (p_value-more_land)/(max_value-1-more_land)
        return get_rbg(ratio, light_green, dark_green)


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


def get_perlin_map_color(pos: (int, int), settings: Settings) -> (int, int, int):
    # use perlin noise to create a reasonable map of heights to determine tile color
    # the whole region is colored according to the tile center positions eval in the perlin map
    scale = 2/10
    p_value = settings.perlin_map.two(pos[0]*scale, pos[1]*scale)

    print(f'Pos {pos}: {p_value}')

    return get_color_from_perlin(p_value)


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


def create_image(v: Voronoi, tiles: [Tile], settings: Settings, i: int):
    # maybe use pygame for this?

    screen = p.display.set_mode((settings.width, settings.height))
    screen.fill(p.Color("white"))

    for tile in tiles:
        for site in v.sites:
            if tile.center == site.xy:
                color = get_perlin_map_color(tile.center, settings)
                p.draw.polygon(screen, p.Color(color), [vertex.xy for vertex in site.vertices()])
                p.draw.polygon(screen, p.Color("black"), [vertex.xy for vertex in site.vertices()], 1)
                if settings.show_centers:
                    p.draw.circle(screen, p.Color("black"), tile.center, 2)

    filename = "C:/Users/jespe/PycharmProjects/RandomTilesProject/src/output/Voronoi_map"+str(i)+".png"
    p.image.save(screen, filename)
    print(f"Voronoi map has been saved in: {filename}")


def create_tiles(settings: Settings):
    random.seed(settings.seed)
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


def main():
    print("This is the main function, hello!")
    for i in range(10):
        settings = Settings()  # settings class is made to better keep track of script arguments
        print("Creating tiles...")
        tiles = create_tiles(settings)
        print("Creating Voronoi diagram...")
        v = calculate_voronoi_diagram(tiles, settings)
        print("Creating image...")
        create_image(v, tiles, settings, i)


if __name__ == "__main__":
    main()
