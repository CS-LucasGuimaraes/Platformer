import pygame
import json

from scripts.entities import enemy

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
GATES = {'key_door'}
PHYSICS_TILES = {'grass', 'snow', 'stone', 'boxes', 'crates', 'door', 'fence', 'leaves', 'mushroom', 'path', 'pipe', 'tree', 'key_door','mario_box_closed','mario_box_opened'}
PLATAFORM_TILES = {'cloud_plataform', 'scaffolding'}
ANIMATED_TILES = {'coin', 'diamond', 'water', 'water_surface', 'key', 'flag', 'blue_flag','heart'}
COLLECTIBLES = {'coin', 'diamond', 'key'}
DEATH_TILES = {'dye_point'}
SPIKES = {'spike'}
EDITOR_ONLY = {'dye_point', 'enemy', 'spawn_point'}
POLES = {'mushroom'}
CHECKPOINT = {'flag', 'flag_pole'}
NEXT_LEVEL = {'blue_flag', 'blue_flag_pole'}
MARIO_BOX = {'mario_box_closed'}
HEARTS = {'heart'}


class Tilemap:
    def __init__(self, game, tile_size=18):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        self.ANIMATED_TILES = ANIMATED_TILES
        self.EDITOR_ONLY = EDITOR_ONLY

    def render(self, surf, offset=[0,0], mode='game'):
        surf.fill((165,229,255))

        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for tile in ANIMATED_TILES: 
                self.game.assets[tile].update()

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    
                    if tile['type'] in ANIMATED_TILES:
                        surf.blit(self.game.assets[tile['type']].img(),
                                (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size -offset[1]))
                    
                    elif tile['type'] in EDITOR_ONLY:
                        if mode == 'editor':
                            self.game.assets[tile['type']][0].set_alpha(100)
                            surf.blit(self.game.assets[tile['type']][0],
                                (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size -offset[1]))
                        else:
                            if tile['type'] == 'enemy':
                                self.game.enemies.append((enemy(self.game, [tile['pos'][0]*self.tile_size, tile['pos'][1]*self.tile_size], [15,14], self.game.players)))
                            
                            if tile['type'] not in DEATH_TILES:
                                del self.tilemap[loc]
                    else:
                        surf.blit(self.game.assets[tile['type']][tile['variant']],
                                (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size -offset[1]))

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0]+ offset[0]) + ';' + str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    

    def check_fall_right(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in [(1,1)]:
            check_loc = str(tile_loc[0]+ offset[0]) + ';' + str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def check_fall_left(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in [(-1,1)]:
            check_loc = str(tile_loc[0]+ offset[0]) + ';' + str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    

    def hearts_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in HEARTS:
                rects.append((pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),tile['type'], (str(tile['pos'][0])) + ';' + str(tile['pos'][1])))
        return rects
    

    def mario_boxes_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in MARIO_BOX:
                rects.append((pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),tile['pos']))
        return rects
    

    def checkpoints_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in CHECKPOINT:
                rects.append((pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),tile['pos']))
        return rects
    

    def next_level_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in NEXT_LEVEL:
                rects.append((pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),tile['pos']))
        return rects
    

    def collectibles_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in COLLECTIBLES:
                rects.append((pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),tile['type'], (str(tile['pos'][0])) + ';' + str(tile['pos'][1])))
        return rects
    

    def gates_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in GATES:
                rects.append((pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size),tile['type'], (str(tile['pos'][0])) + ';' + str(tile['pos'][1])))
        return rects
    

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                if tile['type'] in POLES:
                    rects.append(pygame.Rect(((tile['pos'][0] * self.tile_size) + (self.tile_size//3)), tile['pos'][1] * self.tile_size, self.tile_size//3, self.tile_size))
                else:
                    rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    

    def plataform_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PLATAFORM_TILES:
                if tile['type'] in POLES:
                    rects.append(pygame.Rect(((tile['pos'][0] * self.tile_size) + (self.tile_size//3)), tile['pos'][1] * self.tile_size, self.tile_size//3, self.tile_size))
                else:
                    rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    

    def death_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in DEATH_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def spike_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in SPIKES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size/2))
        return rects
    

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles, 'spawn_point': self.game.spawn_point}, f)
        f.close()

        print("saved successfully".upper())
    
    def  load(self, path):
        f = open(path, 'r')
        data = json.load(f)
        f.close()

        self.tilemap = data['tilemap']
        self.tile_size = data['tile_size']
        self.offgrid_tiles = data['offgrid']
        self.spawn_point = data['spawn_point']