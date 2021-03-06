# ======================================

#describe:外星人类
#author: FarkasG
#CreateTime: #20/11/14#
#Edition: v1.0

#Update:
#UpdateTime:
#UpdateDescribe:

#=======================================

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    
    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/2.bmp')
        self.rect = self.image.get_rect()
        
        # 每个外星人最初都在屏幕左上角附近。
        self.rect.x = self.rect.width
        self.rect.y = -self.rect.height
        
        #存储外星人的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.settings = ai_game.settings
        
    def update(self):
        """向右和向下移动外星人"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        self.y += self.settings.fleet_drop_speed
        self.rect.y = self.y
        
    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True。"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
            