import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from kunkun_setting import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from score_board import Scoreboard
from sound_manager import sound_manager
import sys


class AlienInvation:
    '''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化并创建游戏资源。'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('KunKun Invasion')

        # 创建一个用于储存游戏统计信息的实例并创建记分牌。
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # 设置背景色
        self.bg_color = (230, 230, 230)

        # 子弹的编组
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建Play按钮
        self.play_button = Button(self, "开始")

        # 保存最终得分
        self.final_score = 0

        # 暂停相关属性
        self.paused = False
        self.pause_font = pygame.font.SysFont('SimHei', 72)
        self.hint_font = pygame.font.SysFont('SimHei', 36)

    def _create_fleet(self):
        '''创建坤坤群'''
        # 创建一个坤坤并计算一行能容纳几个坤坤。
        # 坤坤的间距为坤坤宽度。
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕能容纳多少行坤坤
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建第一行坤坤。
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        '''创建一个坤坤，并将其放在首行'''
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''当有坤坤到达边缘时采取相应的措施。'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break  # 一旦有坤坤到达边缘，就不再检查其他坤坤

    def _change_fleet_direction(self):
        '''改变坤坤群的方向，并下移整群。'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        "开始游戏的主循环"
        while True:
            # 监视键盘和鼠标事件
            self._check_events()

            if self.stats.game_active and not self.paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        '''响应按键'''
        if event.key == pygame.K_RIGHT:#右
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:#左
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:#上
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:#下
            self.ship.moving_down = True
        elif event.key == pygame.K_q:#退出
            sys.exit()
        elif event.key == pygame.K_SPACE:#射击
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:#暂停
            if self.stats.game_active:
                self.paused = not self.paused

    def _check_keyup_events(self, event):
        '''响应松开'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        '''创建一颗子弹，并将其加入编组bullets中'''
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

        # 播放子弹发射音效
        sound_manager.play_bullet_fire()

    def _update_bullets(self):
        '''更新子弹的位置并删除消失的子弹'''
        # 更新子弹的位置。
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹击中了坤坤。
        # 如果是，就删除相应的子弹和坤坤
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            # 播放坤坤被击中音效
            sound_manager.play_alien_hit()

            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

            # 检查是否达到胜利分数
            if self.stats.score >= 35000:
                print(f"胜利！得分: {self.stats.score}")
                self.stats.game_won = True
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
                return

        if not self.aliens:
            # 删除现有的子弹并新建一群坤坤。
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

        if not self.aliens:
            # 删除现有的子弹并新建一群坤坤。
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _check_victory_condition(self):
        '''检查游戏胜利条件'''
        if self.stats.score >= 35000 and self.stats.game_active:
            self.stats.game_won = True
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            return True
        return False

    def _update_aliens(self):
        '''检查是否有坤坤位于屏幕边缘
        更新坤坤群中所有坤坤的位置'''
        self._check_fleet_edges()
        self.aliens.update()

        # 检测坤坤和飞船间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有坤坤到达了屏幕底端。
        self._check_aliens_bottom()

    def _update_screen(self):
        '''更新屏幕上的图像，并切换新屏幕。'''
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分。
        self.sb.show_score()

        # 如果游戏暂停，显示暂停提示
        if self.paused and self.stats.game_active:
            # 绘制半透明遮罩
            overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 黑色半透明遮罩
            self.screen.blit(overlay, (0, 0))

            # 显示"游戏暂停"文字
            pause_text = self.pause_font.render("游戏暂停", True, (255, 255, 255))
            pause_rect = pause_text.get_rect()
            pause_rect.center = self.screen.get_rect().center
            self.screen.blit(pause_text, pause_rect)

            # 显示提示文字
            hint_text = self.hint_font.render("按 ESC 键恢复游戏", True, (255, 255, 255))
            hint_rect = hint_text.get_rect()
            hint_rect.centerx = pause_rect.centerx
            hint_rect.top = pause_rect.bottom + 20
            self.screen.blit(hint_text, hint_rect)

        # 原有的游戏非活动状态处理（保持不变）
        if not self.stats.game_active:
            # 先保存当前分数（因为可能会被重置）
            current_score = self.stats.score

            # 判断游戏状态：胜利、失败、还是未开始
            if current_score >= 35000:  # 胜利状态（分数达到35000）
                button_text = "再来一局"
                tip_text1 = "你成功打退了坤坤的进攻！我们赢了！"
                tip_text2 = f"最终得分：{current_score}  最高分：{self.stats.high_score}"

            elif self.stats.ships_left == self.settings.ship_limit and current_score == 0:  # 游戏未开始
                button_text = "开始"
                tip_text1 = "邪恶坤坤入侵了地球，你是人类最后一道防线，坤坤的速度会不断加快，尽可能消灭他们吧！"
                tip_text2 = "'↑↓←→'移动，'Space'射击，游戏中按'Esc'暂停，小写模式下按'q'退出。"
                # 确保胜利标志被重置
                self.stats.game_won = False

            else:  # 游戏已失败
                button_text = "再来一局"
                tip_text1 = "我们失败了，要再来一局吗？"
                tip_text2 = f"最终得分：{current_score}  最高分：{self.stats.high_score}"

            # 更新按钮文字
            self.play_button._prep_msg(button_text)
            self.play_button.draw_button()

            # 绘制提示文字
            tip_font = pygame.font.SysFont('SimHei', 36)

            # 第一行提示文字
            tip_surface1 = tip_font.render(tip_text1, True, (0, 0, 0))
            tip_rect1 = tip_surface1.get_rect()
            tip_rect1.centerx = self.play_button.rect.centerx
            tip_rect1.bottom = self.play_button.rect.top - 20
            self.screen.blit(tip_surface1, tip_rect1)

            # 第二行提示文字
            tip_surface2 = tip_font.render(tip_text2, True, (0, 0, 0))
            tip_rect2 = tip_surface2.get_rect()
            tip_rect2.centerx = self.play_button.rect.centerx
            tip_rect2.bottom = self.play_button.rect.bottom + 50
            self.screen.blit(tip_surface2, tip_rect2)

        pygame.display.flip()

    def _ship_hit(self):
        '''响应飞船被坤坤撞到'''
        if self.stats.ships_left > 0:
            # 将 ship_left 减1
            self.stats.ships_left -= 1
            self.sb.prep_ship()

            # 清空余下的坤坤和子弹。
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的坤坤，并将飞船放到屏幕底端的中央。
            self._create_fleet()
            self.ship.center_ship()

            # 暂停。
            sleep(0.5)
        else:
            # 游戏失败，标记为不是胜利
            self.stats.game_won = False

            self.stats.game_active = False
            pygame.mouse.set_visible(True)

            # 重新设置游戏统计信息，以便下一次玩游戏时重新开始。
            self.stats.reset_stats()

    def _check_aliens_bottom(self):
        '''检查是否有坤坤到达了屏幕底端'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理。
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        '''在玩家单击play按钮时开启新游戏'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置胜利标志（无论之前是胜利还是失败）
            self.stats.game_won = False

            # 重置游戏设置（速度重置）
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计信息（注意：这里重置分数但保留最高分）
            self.stats.ships_left = self.settings.ship_limit
            self.stats.score = 0
            self.stats.level = 1
            self.stats.game_active = True

            # 更新记分牌
            self.sb.prep_score()
            self.sb.prep_ship()

            # 清空余下的坤坤和子弹。
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的坤坤并让飞船居中。
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标。
            pygame.mouse.set_visible(False)

            # 立即更新屏幕，清除之前的胜利/失败消息
            self._update_screen()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvation()
    ai.run_game()