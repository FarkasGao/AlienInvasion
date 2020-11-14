import sys 
import time
import pygame

# ======================================

#describe:游戏主体
#author: FarkasG
#CreateTime: #20/11/11#
#Edition: v1.2

#Update:v1.1
#UpdateTime:20/11/12
#UpdateDescribe:重构run_game()方法 将其差分成两个辅助方法(helper method):
#                _check_events(), _update_screen()

#Update:v1.2
#UpdateTime:20/11/14
#UpdateDescribe:增加子弹相关函数

#Update:
#UpdateTime:
#UpdateDescribe:

#=======================================

from settings import Settings
from ship import Ship
from bullet import Bullet

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
        self.bullets = pygame.sprite.Group()
        self.shot_bool = False
        self.shot_time = 0
        
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._bullet()
            self._update_screen()
            
    def _check_events(self):
        """响应按键和鼠标事件"""
                
        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                sys.exit()
            elif self.event.type == pygame.KEYDOWN:
                self._move(True)
                if self.event.key == pygame.K_q:
                    sys.exit()
                if self.event.key ==pygame.K_SPACE:
                    self.shot_bool = True
                    
            elif self.event.type == pygame.KEYUP:
                self._move(False)
                if self.event.key == pygame.K_SPACE:
                    self.shot_bool = False
                
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
          
    def _bullet(self):
        """管理子弹"""
        self.bullets.update()
        
        if self.shot_bool and (time.time()-self.shot_time)>0.1:
            if len(self.bullets) < self.settings.bullets_allowed:
                self.shot_time = time.time()
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
            
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
           
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()    
        pygame.display.flip()
        
if __name__ == "__main__":
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()