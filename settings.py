# ======================================

#describe:游戏的设置
#author: FarkasG
#CreateTime: #20/11/11#

#Edition: v1.1
#Update:v1.1
#UpdateTime:11/14
#UpdateDescribe:增加子弹设置

#=======================================

class Settings:
    """存储游戏《外星人入侵》中的所有设置的类"""
    
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # 飞船设置
        self.ship_speed = 3
        self.ship_limit = 3
        
        # 子弹设置
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height =15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        
        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 0.3
        # fleet_direction 为1表示右移，为-1表示左移
        self.fleet_direction = 1