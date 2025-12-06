import pygame
import os

BASE_PATH = "../assets"

class SpriteManager:
    def __init__(self, base_path="BASE_PATH", sprites_path="sprites", animation_path="sprites/animation"):
        self.base_path = base_path
        self.cache = {}          # отдельные спрайты
        self.animations = {}     # анимации по папкам

    def load_sprite(self, path):
        if path not in self.cache:
            full_path = os.path.join(self.base_path, path)
            self.cache[path] = pygame.image.load(full_path).convert_alpha()
        return self.cache[path]

    def load_animation(self, folder):
        if folder not in self.animations:
            folder_path = os.path.join(self.base_path, folder)
            frames = []
            for file_name in sorted(os.listdir(folder_path)):
                if file_name.endswith(".png"):
                    frame = self.load_sprite(os.path.join(folder, file_name))
                    frames.append(frame)
            self.animations[folder] = frames
        return self.animations[folder]

sprites = SpriteManager(BASE_PATH)