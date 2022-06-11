import pygame as pg
import sys
import pprint
import winsound
pp = pprint.PrettyPrinter(indent=2)
import pygame.freetype
import random as ran
ran.seed(9)
import time
import glob

def genMenu():
    global FinputNum
    global RinputNum
    global RowNum
    global inputNum
    global rePlay
    StartButton = pygame.Surface((FontSize*5,int(FontSize*2.5)))
    GradeBar = pygame.Surface((window_weith / 2, FontSize * 5))
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
        if mousePos[0]<= FontSize*10 and mousePos[0]>= FontSize*5 and mousePos[1] <= FontSize*7.5 and\
            mousePos[1] >= FontSize*5:
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
        screen.blit(StartButton,(FontSize*5,FontSize*5))
        screen.blit(GradeBar,(5*FontSize,0))
        pg.display.update()

def write(chars,bar,pos=(0,0),color = (0,0,0)):
    font = pygame.freetype.Font('./字体ttf/SIMYOU.TTF')
    font.render_to(bar,pos, chars[0:], fgcolor=color, size=FontSize)
def writeChar(char,bar,pos=(0,0),color = (0,0,0)):
    # todo
    '''写入单个字符'''
    font = pygame.freetype.Font('./字体ttf/SIMYOU.TTF')
    char_surf = font.render(char,fgcolor=color,size=FontSize)
    char_rect = char_surf[1] # char_rect: (右移(左上角右移),上移(左上角海拔),宽度,高度)
    xpos,ypos = pos[0]+char_rect[0], 0.8*FontSize - char_rect[1]  # 使文本对齐,0.8是个迷
    bar.blit(char_surf[0],(xpos,ypos))


#待测试字符集合
s = r'''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ;,./`1234567890-=[]\'~!@#$%^&*()_+{}|:"<>? '''

if True:  # 读取设置文件
    setFile=open('设置文件.txt','r',encoding='utf-8')
    settings = {}
    setString = setFile.read().split()
    for i in setString:
        settings[i.split(':')[0]] = i.split(':')[1]
    print('settings:',settings)

    
    FontSize = int(settings['FontSize'])          # 字符高度，单位：像素
    window_weith = FontSize*25  # 单位：像素
    endNum = int(settings['endNum']) # 准备打的字符数量
    beepFre = int(settings['beepFre'])
    beepLas = int(settings['beepLas'])
    del setFile,settings,setString

if True:  # 读取打字来源
    ssFile = open(str(glob.glob('type*')[0]),'r',encoding='utf-8')
    ssList = ssFile.read().split()
    del ssFile


white=(255,255,255)
inforBars0=pygame.Surface((window_weith, FontSize))
inforBars0.fill(white)
inforBars1=pygame.Surface((window_weith, FontSize))
inforBars1.fill(white)
inforBars2 = pygame.Surface((window_weith, FontSize))
inforBars2.fill(white)
inforBars3 = pygame.Surface((window_weith, FontSize))
inforBars3.fill(white)
inforBars = [inforBars0,inforBars1,inforBars2,inforBars3]

gray = (200,200,200)
typeBar0 = pygame.Surface((window_weith, FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar0.fill(gray)
typeBar1 = pygame.Surface((window_weith, FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar1.fill(gray)
typeBar2 = pygame.Surface((window_weith, FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar2.fill(gray)
typeBar3 = pygame.Surface((window_weith, FontSize))    #窗口中灰色的部分，用来显示用户打出的字符
typeBar3.fill(gray)
typeBars = [typeBar0, typeBar1, typeBar2, typeBar3]

pg.init()

screen=pg.display.set_mode((window_weith, 2*FontSize* len(inforBars)))  #窗口矩形
pg.display.set_caption("打字练习")


inputNum = 0                            #记录用户打出的字符的‘位置’，inputNum=第n+1个
RowNum = 0                              #RowNum:记录用户打出的字符在第几行

showString = ''                         #未来展示在inforBars的字符
cha_num_row = int(window_weith / (FontSize / 2))   # cha_num_row:每行的字符数量

finishOneLine = False

notStarted = True
RinputNum = 0                           #记录用户打出了多少个正确字符
FinputNum = 0                           #记录用户打出了多少个错误字符

rePlay = True
FaultChars = []

green = (20,100,20)

while(True):
    if rePlay:
        # 如果重新开始一局或刚开始
        rePlay = False
        FinputNum , RinputNum,RowNum,inputNum = 0,0,0,0
        showString = ''
        notStarted = True
        finishOneLine = False
        FaultChars = []
        for inforBar in inforBars:
            inforBar.fill(white)
        for typeBar in typeBars:
            typeBar.fill(gray)

        showString = ''  # 未来展示在inforBars的字符
        while len(showString) < int(len(inforBars)*cha_num_row):
            showString += ran.choice(ssList)
            showString += ' '
        pass
        for itr, inforBar in enumerate(inforBars):
            infoStr = showString[cha_num_row * itr : cha_num_row*itr + cha_num_row]
            char_pos = 0
            for char in infoStr:
                writeChar(char,inforBar,(char_pos,0))
                char_pos += FontSize/2
            # write(infoStr, inforBar)
        del char_pos,infoStr



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
            # pp.pprint(event.__dict__)
            # pg.display.set_caption("输入了: "+event.unicode)

            if event.unicode not in s or event.unicode == '':
                print('进入 not in s 或 == \'\'')
                pass
            else:
                try:
                    cha_pos = cha_num_row*RowNum+inputNum
                    if event.unicode == showString[cha_pos] :
                        print('进入打对了:'+str(event.unicode)) # 测试代码
                        writeChar(event.unicode, typeBars[RowNum], (FontSize / 2 * inputNum, 0), color=green)
                        inputNum += 1
                        RinputNum += 1

                    elif event.unicode == 'v' and showString[cha_pos] == 'ü':
                        print('进入ü') # 测试代码
                        writeChar('ü', typeBars[RowNum], (FontSize / 2 * inputNum, 0), green)
                        inputNum += 1
                        RinputNum += 1
                    else:
                        print('进入 打错') # 测试代码
                        winsound.Beep(beepFre,beepLas)
                        FaultChars.append(showString[cha_pos])
                        FinputNum += 1

                except Exception as e:
                    print('进入 except') # 测试
                    print(e)
                    pass
    if RinputNum >= endNum:
        # 如果打完了
        try:
            print('time cost:', time.time() - time_start, 's')
            print('字符数:', RinputNum)
            print('速度：', int(60 * RinputNum / (time.time() - time_start)), '字符/分钟')
            print('正确率：', 100 * round((RinputNum - FinputNum) / RinputNum, 4), '%')
        except:
            pass
        genMenu()

    if inputNum == cha_num_row:        #如果 待打字符的位置到了一行的最后的位置：
        RowNum += 1
        inputNum = 0                     #用户待打字符位置重新指向0
        if RowNum >= len(typeBars):
            # 如果 打到了最底部
            RowNum = 0

            for var in inforBars:
                var.fill(white)
            for var in typeBars:
                var.fill(gray)

            showString = ''  # 未来展示在inforBars的字符
            while len(showString) < int(len(inforBars)*cha_num_row):
                showString += ran.choice(ssList)
                showString += ' '
            for itr, inforBar in enumerate(inforBars):
                write(showString[cha_num_row * itr:cha_num_row\
                            * itr + cha_num_row], inforBar)

    black = (0,0,0)
    screen.fill(black)
    for idx,var in enumerate(inforBars):
        screen.blit(var,(0,idx*2*FontSize))
    for idx,var in enumerate(typeBars):
        screen.blit(var,(0,FontSize+idx*2*FontSize))
    pg.draw.line(screen,black,(FontSize/2*inputNum,FontSize*(2*RowNum+1)),(FontSize/2*inputNum,FontSize*(2*RowNum+2)))
    pg.display.update()
