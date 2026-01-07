import pygame
from pygame.sprite import Sprite

import sys
import os

def get_resource_path(relative_path):
    """获取资源的正确路径，兼容开发环境和打包环境"""
    try:
        # PyInstaller创建临时文件夹，将路径存在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 正常开发环境
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class Alien(Sprite):
    '''表示坤坤的类'''

    def __init__(self, ai_game):
        '''初始化坤坤并设置其起始位置'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 直接加载坤坤图片
        original_image = pygame.image.load(get_resource_path('images/kunkun.png'))

        # 将图片转换为与显示兼容的格式
        self.image = original_image.convert_alpha()

        # 缩放图片到合适大小
        self.image = pygame.transform.smoothscale(self.image, (130, 130))

        # 获取图像的rect属性
        self.rect = self.image.get_rect()

        # 每个坤坤最初都在屏幕左上角附近
        self.rect.x = 0
        self.rect.y = 0

        # 储存坤坤精确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        '''如果坤坤位于屏幕边缘，就返回True'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self):
        '''向左或向右移动坤坤'''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x