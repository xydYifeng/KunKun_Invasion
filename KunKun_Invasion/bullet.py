import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''管理飞船所发射子弹的类'''

    def __init__(self, ai_game):
        '''在飞船位置创建一个子弹对象。'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载子弹图片（新增代码）
        try:
            # 加载球图片
            original_image = pygame.image.load('images/ball.png')
            # 转换为与显示格式兼容的格式
            self.image = original_image.convert_alpha()
            # 缩放图片到合适大小（可以根据需要调整尺寸）
            bullet_size = 30  # 设置子弹大小
            self.image = pygame.transform.smoothscale(self.image, (bullet_size, bullet_size))
        except pygame.error as e:
            print(f"无法加载子弹图片: {e}")
            # 如果图片加载失败，创建一个圆形替代
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (10, 10), 10)  # 红色圆形

        # 获取图像的rect属性
        self.rect = self.image.get_rect()

        # 设置子弹的初始位置为飞船顶部中心
        self.rect.midtop = ai_game.ship.rect.midtop

        # 储存用小数表示的子弹位置
        self.y = float(self.rect.y)

        # 保留原始颜色设置（可选，用于调试）
        self.color = (255, 0, 0) if self.settings.bullet_color is None else self.settings.bullet_color

    def update(self):
        '''向上移动子弹'''
        # 更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        # 使用图片绘制子弹
        self.screen.blit(self.image, self.rect)
