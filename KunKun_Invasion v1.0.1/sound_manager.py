# sound_manager.py
import pygame
import os


class SoundManager:
    def __init__(self):
        """初始化音效管理器"""
        pygame.mixer.init()

        # 音效文件路径
        self.sound_dir = "sounds"

        # 确保音效目录存在
        if not os.path.exists(self.sound_dir):
            os.makedirs(self.sound_dir)

        # 加载音效
        self.bullet_fire_sound = self._load_sound("鸡.mp3", volume=0.6)
        self.alien_hit_sound = self._load_sound("你干嘛.mp3", volume=0.8)

        # 是否启用音效
        self.sound_enabled = True

    def _load_sound(self, filename, volume=1.0):
        """加载音效文件"""
        try:
            path = os.path.join(self.sound_dir, filename)
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except:
            # 如果加载失败，返回None但不影响游戏
            return None

    def play_bullet_fire(self):
        """播放子弹发射音效"""
        if self.sound_enabled and self.bullet_fire_sound:
            self.bullet_fire_sound.play()

    def play_alien_hit(self):
        """播放坤坤被击中音效"""
        if self.sound_enabled and self.alien_hit_sound:
            self.alien_hit_sound.play()


# 创建全局音效管理器实例
sound_manager = SoundManager()