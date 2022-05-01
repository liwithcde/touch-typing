import pygame as pg
import sys
import pprint
import winsound
pp = pprint.PrettyPrinter(indent=2)
import pygame.freetype
import random as ran
import time
import glob
def genMenu():
    global FinputNum
    global RinputNum
    global RowNum
    global inputNum
    global rePlay
    StartButton = pygame.Surface((100,50))
    GradeBar = pygame.Surface((weith/2,FontSize*5))
    GradeBar.fill((255,255,255))
    s1 = '错误个数：'+str(FinputNum)
    s2 = '正确率：' + str(round(100*(RinputNum-FinputNum)/RinputNum,2))+'%'
    s3 = '时间：' + str(round(time.time() - time_start))+'s'
    s4 = '速度：' + str(round(60*RinputNum/(time.time()-time_start),2))+'字符/分钟'
    s5 = '错误字母：'+ str(''.join(FaultChars))
    with open('统计数据.txt','a') as f:
        f.write(time.ctime()+' '+s1+' '+s2+' '+s3+' ' +s4+' '+s5+'\n')
    write(s1,GradeBar,pos=(0,0))
    write(s2,GradeBar,pos=(0,FontSize))
    write(s3,GradeBar,pos=(0,2*FontSize))
    write(s5,GradeBar,pos=(0,3*FontSize))
    write(s4,GradeBar,pos=(0,4*FontSize))

    StartisPressed = False
    while(True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        StartButton.fill((180, 180, 0))

        mousePos = pg.mouse.get_pos()
        if mousePos[0]<= 200 and mousePos[0]>= 100 and mousePos[1] <= 150 and\
            mousePos[1] >= 100:
            if pg.mouse.get_pressed()[0] == 1:
                StartButton.fill((255, 255, 0))
                StartisPressed = True
            else:
                if StartisPressed == True:
                    rePlay = True
                    return
                else:
                    StartButton.fill((225,225,0))

        write('开始', StartButton,pos=(15,10))
        screen.fill((0,0,0))
        screen.blit(StartButton,(100,100))
        screen.blit(GradeBar,(5*FontSize,0))
        pg.display.update()
def write(chars,bar,pos=(0,0),color = (0,0,0)):
    font = pygame.freetype.Font('./字体ttf/SIMYOU.TTF', 20)
    font.render_to(bar,pos, chars[0:], color, size=FontSize)




s = 'abcdefghijklmnopqrstuvwxyz;,./ '    #待测试字符集合

with open('设置文件.txt','r',encoding='utf-8') as setFile:
    settings = {}
    setString = setFile.read().split()
    for i in setString:
        settings[i.split(':')[0]] = i.split(':')[1]
    print('settings:',settings)

    weith = int(settings['windowWeight'])
    FontSize = int(settings['FontSize'])
    endNum = int(settings['endNum'])
    beepFre = int(settings['beepFre'])
    beepLas = int(settings['beepLas'])

with open(str(glob.glob('type*')[0]),'r',encoding='utf-8') as ssFile:
    ssList = ssFile.read().split()
    print(ssList)



inforBar0=pygame.Surface((weith,FontSize))
inforBar0.fill((255,255,255))
inforBar1=pygame.Surface((weith,FontSize))
inforBar1.fill((255,255,255))
inforBar2 = pygame.Surface((weith,FontSize))
inforBar2.fill((255,255,255))
inforBar3 = pygame.Surface((weith,FontSize))
inforBar3.fill((255,255,255))
inforBar = [inforBar0,inforBar1,inforBar2,inforBar3]

typeBar0 = pygame.Surface((weith,FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar0.fill((200,200,200))
typeBar1 = pygame.Surface((weith,FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar1.fill((200,200,200))
typeBar2 = pygame.Surface((weith,FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar2.fill((200,200,200))
typeBar3 = pygame.Surface((weith,FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar3.fill((200,200,200))
typeBar = [typeBar0,typeBar1,typeBar2,typeBar3]

pg.init()

screen=pg.display.set_mode((weith,80*len(inforBar)))  #窗口是一个左右1000，上下400的矩形
pg.display.set_caption("Pygame游戏")


inputNum = 0                            #记录用户打出的字符的‘位置’，inputNum=第n+1个
RowNum = 0                              #RowNum:记录用户打出的字符在第几行

showString = ''                         #未来展示在inforBar的字符
while len(showString)<int(2*4*weith/FontSize):
    showString += ran.choice(ssList)
    showString += ' '
for itr,var in enumerate(inforBar):
    write(showString[int(weith/(FontSize/2))*itr:int(weith/(FontSize/2))*itr+int(weith/(FontSize/2))], var)

finishOneLine = False



notStarted = True
RinputNum = 0                           #记录用户打出了多少个正确字符
FinputNum = 0                           #记录用户打出了多少个错误字符

rePlay = True
FaultChars = []
while(True):
    if rePlay:
        rePlay = False
        FinputNum , RinputNum,RowNum,inputNum = 0,0,0,0
        showString = ''
        notStarted = True
        finishOneLine = False
        FaultChars = []
        for var in inforBar:
            var.fill((255, 255, 255))
        for var in typeBar:
            var.fill((200, 200, 200))

        showString = ''  # 未来展示在inforBar的字符
        while len(showString) < int(2 * len(inforBar) * weith / FontSize):
            showString += ran.choice(ssList)
            showString += ' '
        for itr, var in enumerate(inforBar):
            write(showString[int(weith / (FontSize / 2)) * itr:int(weith / (FontSize / 2)) \
                                                               * itr + int(weith / (FontSize / 2))], var)


    for event in pg.event.get():
        if event.type == pg.QUIT:
            try:
                print('time cost:',time.time()-time_start,'s')
                print('字符数:',RinputNum)
                print('速度：',int(60*RinputNum/(time.time()-time_start)),'字符/分钟')
                print('正确率：',100*round((RinputNum-FinputNum)/RinputNum,4),'%')
            except:
                pass
            sys.exit()
        if event.type == pg.KEYDOWN:
            if notStarted:
                time_start = time.time()
                notStarted = False
            else:
                pass
            pp.pprint(event.__dict__)
            if event.unicode not in s or event.unicode == '':
                pass
            else:
                try:
                    if event.unicode == showString[int(weith/(FontSize/2))*RowNum+inputNum] :
                        write(event.unicode,typeBar[RowNum],(FontSize/2*inputNum,0),(20,100,20))
                        inputNum += 1
                        RinputNum += 1
                    elif event.unicode == 'v' and showString[int(weith/(FontSize/2))*RowNum+inputNum] == 'ü':
                        write('ü', typeBar[RowNum], (FontSize/2* inputNum, 0), (20, 100, 20))
                        inputNum += 1
                        RinputNum += 1
                    else:
                        winsound.Beep(beepFre,beepLas)
                        FaultChars.append(showString[int(weith/(FontSize/2))*RowNum+inputNum])
                        FinputNum += 1

                except:
                    pass
    if RinputNum >= endNum:
        try:
            print('time cost:', time.time() - time_start, 's')
            print('字符数:', RinputNum)
            print('速度：', int(60 * RinputNum / (time.time() - time_start)), '字符/分钟')
            print('正确率：', 100 * round((RinputNum - FinputNum) / RinputNum, 4), '%')
        except:
            pass
        finally:
            genMenu()
    if inputNum == int(2*weith/FontSize):        #如果 待打字符的位置到了一行的最后的位置：
        RowNum += 1
        inputNum = 0                     #用户待打字符位置重新指向0
        if RowNum >= len(typeBar):
            RowNum = 0

            for var in inforBar:
                var.fill((255,255,255))
            for var in typeBar:
                var.fill((200,200,200))

            showString = ''  # 未来展示在inforBar的字符
            while len(showString) < int(2 * len(inforBar) * weith / FontSize):
                showString += ran.choice(ssList)
                showString += ' '
            for itr, var in enumerate(inforBar):
                write(showString[int(weith/(FontSize/2)) * itr:int(weith/(FontSize/2))\
                            * itr + int(weith / (FontSize / 2))], var)


    screen.fill((0,0,0))
    for idx,var in enumerate(inforBar):
        screen.blit(var,(0,idx*2*FontSize))
    for idx,var in enumerate(typeBar):
        screen.blit(var,(0,FontSize+idx*2*FontSize))
    pg.draw.line(screen,(0,0,0),(FontSize/2*inputNum,FontSize*(2*RowNum+1)),(FontSize/2*inputNum,FontSize*(2*RowNum+2)))
    pg.display.update()
