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

#Update:v1.3
#UpdateTime:20/11/17
#UpdateDescribe:增加结束相关函数

#Update:v1.4
#UpdateTime:20/11/18
#UpdateDescribe:增加按钮

#=======================================
import sys 
import time
import pygame
import json

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._alien_capacity()
        self._create_alien()
        self.shot_bool = False
        self.shot_time = 0
        spritelist = []
        self.interval = 2
        self.createtime = time.time()
        #创建Play按钮
        self.play_button = Button(self, "Play")
        
        #创建一个用于存储统计信息的实例并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sb.prep_high_score()
        self.sb.prep_score()
        self.sb.prep_ships()
        self.high_score_image = self.sb.high_score_image
        self._max_score()
        
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._bullet()
                self._update_aliens()
                self._create_fleet()
            self._update_screen()
            
    def _max_score(self):
        """最高分"""
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right -20
        self.high_score_rect.top = 20  
            
    def _check_events(self):
        """响应按键和鼠标事件"""
                
        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                sys.exit()
                
            elif self.event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
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
                
    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.stats = GameStats(self)
            self.sb = Scoreboard(self)
            self.sb.prep_high_score()
            self.sb.prep_score()
            self.high_score_image = self.sb.high_score_image
            self._max_score()
            self.stats.reset_stats()
            self.interval = 2
            self.stats.game_active = True
            self.sb.prep_ships()
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            
            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)
                
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
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
         
        if collisions:
            self.stats.alien_points +=10
        
        if self.shot_bool and (time.time()-self.shot_time)>0.1:
            if len(self.bullets) < self.settings.bullets_allowed:
                self.shot_time = time.time()
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
            
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """创建外星人群"""
        if (time.time() - self.createtime) > self.interval:
            self.createtime = time.time()
            if self.interval >0.8:
                self.interval -= 0.1
            self._alien_capacity()
            self._create_alien()
            self.settings.bullet_width += 0.5
        
    def _alien_capacity(self):
        # 外星人的间距为外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        self.number_aliens_x = available_space_x // (2 * alien_width)
        
    def _create_alien(self):
        """创建一个外星人并将其放在当前行"""
        for alien_number in range(self.number_aliens_x+1):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2* alien_width *alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)
     
    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘
        更新外星人群中所有外星人的位置
        """
        self._check_fleet_edges()
        self.aliens.update()
        
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
        
    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
                
    def _change_fleet_direction(self):
        """改变它们的方向。"""
        self.settings.fleet_direction *= -1 

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()    
        self.aliens.draw(self.screen)
        
        #显示得分
        self.sb.prep_score()
        self.sb.show_score()
        self.screen.blit(self.high_score_image, self.high_score_rect)
        
        #如果游戏处于非活动状态，就绘制Play按钮
        if self.stats.game_active == False:
            self.play_button.draw_button()
            
            
        pygame.display.flip()
        
    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            #将ships_left 减1
            self.stats.ships_left -= 1
        
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
        
            #创建一群新的外星人，并将飞船放到品目底端的中央
            self._create_fleet()
            self.ship.center_ship()
            
            self.sb.prep_ships()
        
            # 暂停
            time.sleep(0.5)
        else:
            if self.sb.high_score < self.stats.alien_points:
                self.sb._remember_score()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            
    def _check_aliens_bottom(self):
        """检查是否有外星人位于屏幕边缘"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break
        
if __name__ == "__main__":
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()