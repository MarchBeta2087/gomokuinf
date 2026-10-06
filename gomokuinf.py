import pygame
import sys
def cmp2d(obj1,obj2): #先比较“行”，后比较“列”
    if obj1[0]<obj2[0]:
        return -1
    elif obj1[0]>obj2[0]:
        return 1
    else:
        if obj1[1]<obj2[1]:
            return -1
        elif obj1[1]>obj2[1]:
            return 1
        else:
            return 0
def binary_search(obj,arr): #如果obj在arr中，返回obj在arr的所在位置，否则返回obj介于arr的哪个位置和哪个位置之间
    if len(arr) == 0:
        return (0,0,False)
    start=0
    end=len(arr)-1
    if (cmp2d(obj,arr[0]) == -1):
        return (-1,0,False)
    elif (cmp2d(obj,arr[0]) == 0):
        return (0,0,True)
    elif (cmp2d(obj,arr[-1]) == 1):
        return (end,end+1,False)
    elif (cmp2d(obj,arr[-1]) == 0):
        return (end,end,True)
    else:
        while start <= end:
            mid=(start+end)//2
            cmpvalue=cmp2d(arr[mid],obj)
            if cmpvalue == -1:
                start=mid+1
            elif cmpvalue == 1:
                end=mid-1
            else:
                return (mid,mid,True)
        return (end,start,False)
table=[] #这个游戏中的棋盘大小是∞x∞，table这个列表只记录所有棋子的位置和颜色，不记录空位
screen=pygame.display.set_mode((720,720))
status=1
winner=0
sx=0 #屏幕上坐标
sy=0 #屏幕上坐标
zx=0 #屏幕上的(0,0)的实际坐标
zy=0 #屏幕上的(0,0)的实际坐标
rx=0 #实际坐标
ry=0 #实际坐标
block_info=tuple()
fivecenter=(0,0)
while True:
    screen.fill((255,255,255))
    title=""
    if winner:
        title="五子棋∞ "+("黑赢 " if (winner==1) else "白赢 ")+str(zy)+"行"+str(zx)+"列~"+str(zy+14)+"行"+str(zx+14)+"列 光标所处位置："+str(ry)+"行"+str(rx)+"列 五子中心位置："+str(fivecenter[0])+"行"+str(fivecenter[1])+"列"
    else:
        title="五子棋∞ "+("黑 " if (status==1) else "白 ")+str(zy)+"行"+str(zx)+"列~"+str(zy+14)+"行"+str(zx+14)+"列 光标所处位置："+str(ry)+"行"+str(rx)+"列"
    pygame.display.set_caption(title)
    for i in range(15): #这个游戏中的棋盘大小是∞x∞，由于窗口大小有限，屏幕上只能显示一小块（15x15）
        pygame.draw.line(screen,(0,0,0),(24+i*48,0),(24+i*48,720)) #竖线
        pygame.draw.line(screen,(0,0,0),(0,24+i*48),(720,24+i*48)) #横线
    for i in range(15):  #这个游戏中的棋盘大小是∞x∞，由于窗口大小有限，屏幕上只能显示一小块（15x15）
        for j in range(15):
            block_info=binary_search((i+zy,j+zx),table)
            if block_info[2]:
                if table[block_info[0]][2] == 1: #黑子
                    pygame.draw.circle(screen,(0,0,0),(24+j*48,24+i*48),18)
                    pygame.draw.circle(screen,(0,0,0),(24+j*48,24+i*48),18,1)
                elif table[block_info[0]][2] == 2: #白子
                    pygame.draw.circle(screen,(255,255,255),(24+j*48,24+i*48),18)
                    pygame.draw.circle(screen,(0,0,0),(24+j*48,24+i*48),18,1)
    for event in pygame.event.get():
        mpos = pygame.mouse.get_pos()
        sy = mpos[1]//48
        sx = mpos[0]//48
        ry = sy+zy
        rx = sx+zx
        block_info=binary_search((ry,rx),table)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (block_info[2] == False) and (winner == 0):
                    table.insert(block_info[1],(ry,rx,status))
                    if status == 1:
                        status = 2
                    elif status == 2:
                        status = 1
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w) or (event.key == pygame.K_UP):
                zy = zy-1
            elif (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                zx = zx-1
            elif (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):
                zy = zy+1
            elif (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                zx = zx+1
    if winner == 0:
        pygame.draw.rect(screen,(0,0,255),(48*sx,48*sy,48,48),2)
    for i in table:
        center=(i[0],i[1])
        blocklu=(center[0]-2,center[1]-2)
        blockrd=(center[0]+2,center[1]+2)
        searchmin=binary_search(blocklu,table)[1]
        searchmax=binary_search(blockrd,table)[0]
        searchpart=table[searchmin:(searchmax+1)]
        isover=1
        centerstatus=i[2]
        for j in range(-2,3):
            isover=isover*binary_search((center[0],center[1]+j),searchpart)[2] #横行
        if isover:
            issame=1
            for j in range(-2,3):
                issame=issame*(table[searchmin+(binary_search((center[0],center[1]+j),searchpart)[0])][2]==centerstatus) #横行
            if issame:
                dsy=i[0]-zy
                dsx=i[1]-zx
                for p in range(-2,3):
                    if (dsy>=-5) and (dsy<=20) and (dsx>=-5) and (dsx<=20):
                        pygame.draw.rect(screen,(255,0,255),(48*(dsx+p),48*dsy,48,48),2)
                        winner=centerstatus
                        fivecenter=center
        isover=1
        for j in range(-2,3):
            isover=isover*binary_search((center[0]+j,center[1]),searchpart)[2] #纵列
        if isover:
            issame=1
            for j in range(-2,3):
                issame=issame*(table[searchmin+(binary_search((center[0]+j,center[1]),searchpart)[0])][2]==centerstatus) #纵列
            if issame:
                dsy=i[0]-zy
                dsx=i[1]-zx
                for p in range(-2,3):
                    if (dsy>=-5) and (dsy<=20) and (dsx>=-5) and (dsx<=20):
                        pygame.draw.rect(screen,(255,0,255),(48*dsx,48*(dsy+p),48,48),2)
                        winner=centerstatus
                        fivecenter=center
        isover=1
        for j in range(-2,3):
            isover=isover*binary_search((center[0]+j,center[1]+j),searchpart)[2]
        if isover:
            issame=1
            for j in range(-2,3):
                issame=issame*(table[searchmin+(binary_search((center[0]+j,center[1]+j),searchpart)[0])][2]==centerstatus)
            if issame:
                dsy=i[0]-zy
                dsx=i[1]-zx
                for p in range(-2,3):
                    if (dsy>=-5) and (dsy<=20) and (dsx>=-5) and (dsx<=20):
                        pygame.draw.rect(screen,(255,0,255),(48*(dsx+p),48*(dsy+p),48,48),2)
                        winner=centerstatus
                        fivecenter=center
        isover=1
        for j in range(-2,3):
            isover=isover*binary_search((center[0]-j,center[1]+j),searchpart)[2]
        if isover:
            issame=1
            for j in range(-2,3):
                issame=issame*(table[searchmin+(binary_search((center[0]-j,center[1]+j),searchpart)[0])][2]==centerstatus)
            if issame:
                dsy=i[0]-zy
                dsx=i[1]-zx
                for p in range(-2,3):
                    if (dsy>=-5) and (dsy<=20) and (dsx>=-5) and (dsx<=20):
                        pygame.draw.rect(screen,(255,0,255),(48*(dsx-p),48*(dsy+p),48,48),2)
                        winner=centerstatus
                        fivecenter=center
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
