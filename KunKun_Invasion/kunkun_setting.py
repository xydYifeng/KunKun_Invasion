import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''表示坤坤的类'''

    def __init__(self, ai_game):
        '''初始化坤坤并设置其起始位置'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 直接加载坤坤图片
        original_image = pygame.image.load('images/kunkun.png')

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