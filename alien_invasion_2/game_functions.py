import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button

def check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens):
    """检测鼠标和键盘事件"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens)
            # print(event.key)

        elif event.type == pygame.KEYUP:
            check_keyup_events(ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button,mouse_x,mouse_y,stats,aliens,bullets,ai_settings,screen,ship)


def check_play_button(play_button,mouse_x,mouse_y,stats,aliens,bullets,ai_settings,screen,ship):
    """在玩家单击Play时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:

        start_game(stats,aliens,bullets,ai_settings,screen,ship)

    # elif


def start_game(stats,aliens,bullets,ai_settings,screen,ship):
    # 重置游戏动态属性
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏的统计信息
    stats.reset_stats()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人,并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    stats.game_active = True

def check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens):

        if event.key == pygame.K_RIGHT:
             ship.moving_right = True

        elif event.key == pygame.K_LEFT:
             ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            # 创建一颗子弹并将其加入到编组的bullets中
            fire_bullet(ai_settings,bullets,screen,ship)

        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_p:
            start_game(stats,aliens,bullets,ai_settings,screen,ship)



def check_keyup_events(ship):

        ship.moving_right = False
        ship.moving_left = False


def update_screen(ai_settings,screen,ship,bullets,aliens,stats,sb):
    """更新屏幕上的图像，并切换到新屏幕"""
    play_button = Button(ai_settings, screen, "Play")
    screen.fill(ai_settings.bg_color)

    if stats.game_active:
        update_ship(ship)
        update_bullet(bullets,aliens,ai_settings, screen, ship)
        update_aliens(aliens,screen,ai_settings,ship,stats,bullets)
        update_score(sb)

    if not stats.game_active:
        play_button.draw_button()
        # update_ship(ship)
        # update_score(sb)
        # screen.fill(ai_settings.bg_color_blue)
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_score(sb):
    sb.show_score()


def update_ship(ship):
    ship.blitme()
    ship.update()


def fire_bullet(ai_settings,bullets,screen,ship):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullet(bullets,aliens,ai_settings, screen, ship):
    # 在外星人和飞船后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()  # 对每个精灵调用 draw_bullet()

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(bullets, aliens, ai_settings, screen, ship)


def check_bullet_alien_collisions(bullets,aliens,ai_settings,screen,ship):
    # 检查是否有子弹击中了外星人
    # 如击中,则删除相应子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)


def get_number_aliens_x(ai_settings,alien_width):
    """计算一行能容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    numbers_aliens_x = int(available_space_x / (2 * alien_width))
    return numbers_aliens_x


def get_numbers_rows(ai_settings,alien_height,ship_height):
    """计算屏幕能容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                           (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
        # 创建一个外星人并加入当前行
        alien = Alien(ai_settings, screen)
        alien_width = alien.rect.width
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    # 外星人间距为外星人的宽度
    alien = Alien(ai_settings,screen)
    numbers_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_numbers_rows(ai_settings,ship.rect.height,alien.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(numbers_aliens_x):
            # 创建一个外星人并加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,row_number)


def check_fleet_edges(aliens,ai_settings):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():  # 遍历外星人群
        if alien.check_edges():
            change_fleet_direction(aliens,ai_settings)
            break


def change_fleet_direction(aliens,ai_settings):
    """将整群外星人往下移动,并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1 # 改变方向

def ship_hit(stats,aliens,bullets,ai_settings,screen,ship):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 1:

        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人,并将飞船放到屏幕最底端
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(screen,aliens,stats,bullets,ai_settings,ship):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats,aliens,bullets,ai_settings,screen,ship)
            break


def update_aliens(aliens,screen,ai_settings,ship,stats,bullets):
    aliens.draw(screen)  # 对编组调用draw  pygame自动绘制编组的每个元素
    aliens.update()
    """检测是否有外星人位于屏幕边缘,及时更新外星人位置"""
    check_fleet_edges(aliens,ai_settings)

    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(stats,aliens,bullets,ai_settings,screen,ship)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(screen,aliens,stats,bullets,ai_settings,ship)








