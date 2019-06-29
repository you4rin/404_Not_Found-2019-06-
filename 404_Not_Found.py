import pygame as pg
import sys
import os

from math import sin,cos,pi,sqrt as ms,hypot as mh
from random import random as rr

###스크린 크기&초당 틱 수
screen=(360,470)
FPS=60

###클래스 정의하는 자리

##플레이어(깡통) 클래스 정의
class Can(pg.sprite.Sprite):
    def __init__(s,position):
        pg.sprite.Sprite.__init__(s)
        s.image=pg.image.load('./Can.png').convert()
        s.image.set_colorkey((255,255,255))
        s.rect=s.image.get_rect()
        s.rect.center=(screen[0]//3, (screen[1]-40)//2)
        s.atk=15
        s.x=s.rect.x
        s.y=s.rect.y


    def update(s):
        s.rect.x=int(s.x)
        s.rect.y=int(s.y)

##적(자석) 클래스 정의
class Magnet(pg.sprite.Sprite):
    def __init__(s,position):
        pg.sprite.Sprite.__init__(s)
        s.image=pg.image.load('./Magnet.png').convert()
        s.image.set_colorkey((255,255,255))
        s.rect=s.image.get_rect()
        s.rect.center=(2*screen[0]//3, (screen[1]-40)//2)
        s.hp=5000
        s.x=s.rect.x
        s.y=s.rect.y
        s.mask = pg.mask.from_surface(s.image)

    def update(s):
        s.rect.x=int(s.x)
        s.rect.y=int(s.y)

##코인 클래스 정의
class Coin(pg.sprite.Sprite):
    def __init__(s):
        pg.sprite.Sprite.__init__(s)
        s.image=pg.image.load('./Coin.png').convert()
        s.image.set_colorkey((255,255,255))
        s.rect=s.image.get_rect()
        s.rect.center=(int(rr()*360), int(rr()*360))
        s.x=s.rect.x
        s.y=s.rect.y

        #자석, 플레이어 주변에는 소환되지 않도록
        for dodge in tGs:
            check=0
            while check==0:
                if abs(dodge.x-s.x)>20 or abs(dodge.y-s.y)>20:
                    check=1
                else:
                    s.rect.center=(int(rr()*360), int(rr()*360))
                    
    def update(s):
        pass

##총알 발사대 클래스 정의
class Launcher(pg.sprite.Sprite):
    def __init__(s):
        pg.sprite.Sprite.__init__(s)
        s.image=pg.Surface((10,10))
        s.rect=pg.draw.circle(s.image,(0,200,200),(5,5),5)
        s.rect.center=(player.x+35,player.y+15)
        s.x=s.rect.x
        s.y=s.rect.y
        s.deg=0

    def update(s):
        #방향키에 따라 방향이 바뀌도록
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            s.deg+=2

        if key[pg.K_RIGHT]:
            s.deg-=2

        s.rect.x=int(s.x)
        s.rect.y=int(s.y)
        
 ##총알 클래스 정의
class Bullet(pg.sprite.Sprite):
    def __init__(s):
        pg.sprite.Sprite.__init__(s)
        s.image=pg.image.load('./bullet.png').convert()
        s.image.set_colorkey((255,255,255))
        s.rect=s.image.get_rect()
        s.rect.center=launcher.rect.center
        s.x=s.rect.x
        s.y=s.rect.y
        s.deg=launcher.deg
        s.mask = pg.mask.from_surface(s.image)

    def update(s):
        s.rect.x=int(s.x)
        s.rect.y=int(s.y)
        
###클래스 정의 끝

pg.init()
os.environ['SDL_VIDEO_WINDOW_POS']="{},{}".format(50,50)

game_font1=pg.font.SysFont('MalgunGothic',15)
game_font2=pg.font.SysFont('MalgunGothic',40)
game_font3=pg.font.SysFont('MalgunGothic',60)

howto1='이동: 마우스 우클릭'
howto1_surface=game_font1.render(howto1,True,(200,0,0))
howto1_rect=howto1_surface.get_rect()
howto1_rect.topleft=(10,397)

howto2='조준: 좌우 방향키           발사: 스페이스바'
howto2_surface=game_font1.render(howto2,True,(200,0,0))
howto2_rect=howto2_surface.get_rect()
howto2_rect.topleft=(10,420)

howto3='공격력 강화: q(3$ 소모)   인력 약화: w(3$ 소모)'
howto3_surface=game_font1.render(howto3,True,(200,0,0))
howto3_rect=howto3_surface.get_rect()
howto3_rect.topleft=(10,443)

window=pg.display.set_mode(screen)
clock=pg.time.Clock()
pg.time.set_timer(pg.USEREVENT+1,200)
pg.time.set_timer(pg.USEREVENT+3,15000)
pg.time.set_timer(pg.USEREVENT+4,2000)
pg.time.set_timer(pg.USEREVENT+5,2000)

mouse_pos=[-1,-1]
isclicked=False

money=0

player=Can((screen[0]//3, (screen[1]-40)//2))
player_Group=pg.sprite.Group()
player_Group.add(player)
pGs=player_Group.sprites()
player_timealive=True

launcher=Launcher()
launcher_Group=pg.sprite.Group()
launcher_Group.add(launcher)

level=1
power=1

bullet_Group=pg.sprite.Group()
cooltime=False

enemy_Group=pg.sprite.Group()
e1=Magnet((2*screen[0]//3, (screen[1]-40)//2))
MAXHP=e1.hp
e1_timealive=True
enemy_Group.add(e1)
eGs=enemy_Group.sprites()

tGs=pGs+eGs

coin_Group=pg.sprite.Group()
coin_Group.add(Coin())

UI1=pg.Surface((360,30))
UI1_rect=pg.draw.rect(UI1,(125,125,125),(0,0,360,30))
UI1_rect.topleft=(0,360)

UI2=pg.Surface((360,80))
UI2_rect=pg.draw.rect(UI2,(175,175,175),(0,0,360,80))
UI2_rect.topleft=(0,390)

ending='Congratulations :)'
ending_surface=game_font2.render(ending,True,(200,200,0))
ending_rect=ending_surface.get_rect()
ending_rect.center=(180,180)

defeat='GAME OVER'
defeat_surface=game_font3.render(defeat,True,(200,0,0))
defeat_rect=defeat_surface.get_rect()
defeat_rect.center=(180,180)

nomoney='돈이 부족합니다.'
nomoney_surface=game_font1.render(nomoney,True,(200,0,0))
nomoney_rect=nomoney_surface.get_rect()
nomoney_rect.topleft=(10,335)

lowlevel='레벨이 너무 낮습니다.'
lowlevel_surface=game_font1.render(lowlevel,True,(200,0,0))
lowlevel_rect=lowlevel_surface.get_rect()
lowlevel_rect.topleft=(10,335)

notenough=False
levellow=False
win=False
lose=False

###게임 루프

while True:
    window.fill((0, 0, 0))

    status='돈: %d$         레벨: %d         공격력: %d'%(money,level,player.atk)
    status_surface=game_font1.render(status,True,(0,0,200))
    status_rect=howto3_surface.get_rect()
    status_rect.topleft=(10,365)

    hpbar=pg.Surface((24,4))
    hpbar_rect=pg.draw.rect(hpbar,(int(255-255*(e1.hp/MAXHP)),int(255*(e1.hp/MAXHP)),0),(0,0,int(24*e1.hp/MAXHP),4))
    hpbar_rect.topleft=(e1.x+3,e1.y-12)

    ##이벤트
    for event in pg.event.get():
        #종료
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()

        #이동
        if event.type==pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2]:
            mouse_pos[0]=event.pos[0]-10
            mouse_pos[1]=event.pos[1]-20
            isclicked=True

        if event.type==pg.KEYDOWN:
            #스페이스를 누르면 발사되도록
            if event.key==pg.K_SPACE and not cooltime and player.alive():
                cooltime=True
                bullet_Group.add(Bullet())

            #q를 누르면 플레이어 공격력 강화하도록
            if event.key==pg.K_q and money>=3 and player.alive():
                money-=3
                player.atk+=3

            elif event.key==pg.K_q and player.alive():
                notenough=True

            #w를 누르면 자석 인력이 약화되도록
            if event.key==pg.K_w and money>=3 and power>1 and player.alive():
                money-=3
                power-=0.2
                level-=1

            elif event.key==pg.K_w and money<3 and player.alive():
                notenough=True

            elif event.key==pg.K_w and power==1 and player.alive():
                levellow=True

        #게임 종료시 - 자석, 코인 소멸
        if event.type==pg.USEREVENT:
            pg.time.delay(700)
            enemy_Group.empty()
            coin_Group.empty()

        #발사 쿨타임 초기화
        if event.type==pg.USEREVENT+1:
            cooltime=False

        if event.type==pg.USEREVENT+2:
            pg.time.delay(700)
            player_Group.empty()
            coin_Group.empty()
            launcher_Group.empty()
            bullet_Group.empty()

        if event.type==pg.USEREVENT+3:
            power+=0.2
            level+=1

        if event.type==pg.USEREVENT+4:
            notenough=False

        if event.type==pg.USEREVENT+5:
            levellow=False

    if not player.alive() and player_timealive:
        launcher_Group.empty()
        player_timealive=False
        pg.event.post(pg.event.Event(pg.USEREVENT))

    if not e1.alive() and e1_timealive:
        e1_timealive=False
        pg.event.post(pg.event.Event(pg.USEREVENT+2))

    if pg.sprite.groupcollide(player_Group, enemy_Group, True, False, pg.sprite.collide_mask):
        lose=True

    ##플레이어가 코인을 먹으면, 보유한 돈이 증가하고, 코인이 새로운 위치에 소환되도록
    if pg.sprite.groupcollide(player_Group, coin_Group, False, True, pg.sprite.collide_mask):
        money+=1
        coin_Group.add(Coin())        

    ##마우스 우클릭 시, 이동하도록 하는 구간
    for player in player_Group:
        if isclicked:
            dist=mh(player.x-mouse_pos[0],player.y-mouse_pos[1])
            if dist<=10:
                player.x=mouse_pos[0]
                player.y=mouse_pos[1]
            elif player.y+(mouse_pos[1]-player.y)*10/dist<=360:
                player.x+=(mouse_pos[0]-player.x)*10/dist
                player.y+=(mouse_pos[1]-player.y)*10/dist
            else:
                player.x+=(mouse_pos[0]-player.x)*10/dist
                player.y=360

            launcher.x=player.x+10+25*cos(launcher.deg)
            launcher.y=player.y+15-25*sin(launcher.deg)

    ##자석이 플레이어를 일정한 속도로 당기도록 하는 구간
    for enemy in enemy_Group:
        
        dist=mh(player.x-e1.x,player.y-e1.y)
        player.x+=(e1.x-player.x)*power/dist
        player.y+=(e1.y-player.y)*power/dist
        
        launcher.x=player.x+10+25*cos(launcher.deg/180*pi)
        launcher.y=player.y+15-25*sin(launcher.deg/180*pi)

    ##총알이 이동하는 구간
    for bullet in bullet_Group:
        if not 0<bullet.x<360 or not 0<bullet.y<360:
            bullet.kill()
        bullet.x+=5*cos(bullet.deg/180*pi)
        bullet.y-=5*sin(bullet.deg/180*pi)

        #총알이 자석에 닿으면, 총알이 사라지도록
        if pg.sprite.collide_mask(bullet, e1):
            bullet.kill()
            e1.hp-=player.atk
            if e1.hp<=0:
                e1.hp=0
                e1.kill()
                win=True

    ##화면 상태 업데이트하는 구간
    isclicked=False

    if player.alive() or e1.alive():
        window.blit(UI1,UI1_rect)
        window.blit(UI2,UI2_rect)
        window.blit(hpbar,hpbar_rect)
        window.blit(howto1_surface,howto1_rect)
        window.blit(howto2_surface,howto2_rect)
        window.blit(howto3_surface,howto3_rect)
        window.blit(status_surface,status_rect)

    if notenough:
        window.blit(nomoney_surface,nomoney_rect)

    if levellow:
        window.blit(lowlevel_surface,lowlevel_rect)
        
    if win and not player.alive():
        window.blit(ending_surface,ending_rect)

    if lose and not e1.alive():
        window.blit(defeat_surface,defeat_rect)
    
    player.update()
    player_Group.draw(window)
    
    enemy_Group.update()
    enemy_Group.draw(window)
    
    coin_Group.update()
    coin_Group.draw(window)

    launcher_Group.update()
    launcher_Group.draw(window)

    bullet_Group.update()
    bullet_Group.draw(window)

    pg.display.update()
    pg.display.flip()
    clock.tick(FPS)
