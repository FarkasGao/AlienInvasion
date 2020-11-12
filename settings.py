# ======================================

#describe:游戏的设置
#author: FarkasG
#CreateTime: #20/11/11#
#Edition: v1.0
#Update:
#UpdateTime:
#UpdateDescribe:

#=======================================

class Settings:
    """存储游戏《外星人入侵》中的所有设置的类"""
    
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)