import pygame
from pygame.sprite import Group

from settings import Settings

from game_stats import GameStats

from scoreboard import Scoreboard

from button import Button

from ship import Ship

import game_functions as gf


def run_game():
    # 初始化一个游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()

    # 屏幕大小
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 标题
    pygame.display.set_caption('Alien Invasion')

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一个外星人组
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建play按钮
    play_button = Button(ai_settings, screen, 'play')

    # 开始游戏主循环
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb,
                              ship, aliens, bullets)

            gf.update_aliens(ai_settings, screen, stats, sb,
                             ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats,
                         sb, ship, aliens, bullets, play_button)


run_game()
