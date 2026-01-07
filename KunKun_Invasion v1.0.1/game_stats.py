class GameStats:
    '''跟踪游戏的统计信息。'''

    def __init__(self, ai_game):
        '''初始化统计信息。'''
        self.settings = ai_game.settings
        self.reset_stats()

        # 游戏刚启动时处于非活动状态。
        self.game_active = False

        # 任何情况下都不应重置最高得分。
        self.high_score = 0

        # 添加：是否胜利的标志
        self.game_won = False

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.game_paused = False
        # 注意：这里不重置 game_won，因为我们需要在游戏开始前知道是否是胜利状态
        # game_won 只在 check_play_button 开始时重置

    def reset_for_new_game(self):
        '''开始新游戏时的重置（区别于完全的统计重置）'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.game_won = False  # 新游戏时重置胜利标志

    def check_victory(self):
        '''检查是否达到胜利条件（35000分）'''
        if self.score >= 35000:
            self.game_won = True
            self.game_active = False
            return True
        return False