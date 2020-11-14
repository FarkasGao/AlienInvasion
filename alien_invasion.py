import sys 

import pygame

# ======================================

#describe:游戏主体tff
#author: FarkasG
#CreateTime: #20/11/11#
#Edition: v1.2

#Update:v1.1
#UpdateTime:20/11/12
#UpdateDescribe:重构run_game()方法 将其差分成两个辅助方法(helper method):
#                _check_events(), _update_screen()

#Update:v1.2
#UpdateTime:20/11/14
#UpdateDescribe:增加子弹相关方法

#=======================================

from settings import Settings
from ship import Ship

class AlienInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        #设置背景色
        #self.bg_color = (230, 0, 100)
        
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            # 监视键盘和鼠标事件
            # for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        sys.exit()
            
            self._update_screen()
            # 每次循环时都重绘屏幕
            #self.screen.fill(self.settings.bg_color)
            #self.ship.blitme()
            
            # 让最近绘制的屏幕可见。
            #pygame.display.flip()
            
            self.ship.update()
            
    def _check_events(self):
        """响应按键和鼠标事件"""
                
        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                sys.exit()
            elif self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_q:
                    sys.exit()
                self._move(True)
                    
            elif self.event.type == pygame.KEYUP:
                self._move(False)
                
    def _move(self, move_bool):
        """移动"""
        if self.event.key == pygame.K_RIGHT:
            self.ship.moving_right = move_bool
        if self.event.key == pygame.K_LEFT:
            self.ship.moving_left = move_bool
        if self.event.key == pygame.K_UP:
            self.ship.moving_up = move_bool
        if self.event.key == pygame.K_DOWN:  
            self.ship.moving_down = move_bool            
    
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        pygame.display.flip()
        
if __name__ == "__main__":
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()