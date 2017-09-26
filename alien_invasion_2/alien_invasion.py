import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #  初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(ai_settings,screen)
    # 创建一个子弹编组
    bullets = Group()
    # 创建一个外星人
    # alien = Alien(ai_settings,screen)
    # 创建一个外星人编组
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 创建一个用于绘制按钮的实例
    play_button = Button(ai_settings,screen,"Play")
    # 创建一个积分牌
    sb = Scoreboard(ai_settings,screen,stats)

    # 开始游戏主循环
    while True:

        gf.check_events(ai_settings,screen,ship,bullets,stats,
                    play_button,aliens)

        # if stats.game_active:
        #     ship.update()
        #     gf.update_bullet(bullets, aliens, ai_settings, screen, ship)
        #     gf.update_aliens(aliens,screen,ai_settings,ship,stats,bullets)

        gf.update_screen(ai_settings,screen,ship,bullets,aliens,stats,sb)
        # gf.update_aliens(aliens)


run_game()
