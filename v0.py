from tkinter import *
from tkinter.messagebox import *
import time

root = Tk()
#  创建一个Canvas，设置其背景色为白色 
cv = Canvas(root, bg='white', width=720, height=800)
chessname = ["黑车", "黑马", "黑象", "黑仕", "黑将", "黑仕", "黑象", "黑马", "黑车", "黑卒", "黑炮",
             "红车", "红马", "红相", "红仕", "红帅", "红仕", "红相", "红马", "红车", "红兵", "红炮"]
imgs = [PhotoImage(file='bmp/' + chessname[i] + '.png') for i in range(0, 22)]

chessmap = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1] for y in range(9)]
# 定义一个字典
dict_ChessName = {}

LocalPlayer = "红"  # LocalPlayer记录自己是红方还是黑方
first = True  # 区分第一次还是第二次选中的棋子
IsMyTurn = True
rect1 = 0
rect2 = 0
firstChessid = 0


def IsAbleToPut(id, x, y, oldx, oldy):  # 实现判断是否能走棋返回逻辑值，这代码最复杂。
    # oldx, oldy 棋子在棋盘原坐标
    # x, y       棋子移动到棋盘的新坐标
    print(id, "QQQ", dict_ChessName[id])
    qi_name = dict_ChessName[id][1]  # 取字符串第二个字符，"黑将"变成"将"
    # "将" "帅"走棋判断
    if (qi_name == "将" or qi_name == "帅"):
        if ((x - oldx) * (y - oldy) != 0):
            return False;
        if (abs(x - oldx) > 1 or abs(y - oldy) > 1):
            return False;
        if (x < 3 or x > 5 or (y >= 3 and y <= 6)):
            return False;
        return True;

    # "士"走棋判断
    if (qi_name == "士" or qi_name == "仕"):
        if ((x - oldx) * (y - oldy) == 0):
            return False;
        if (abs(x - oldx) > 1 or abs(y - oldy) > 1):
            return False;
        if (x < 3 or x > 5 or (y >= 3 and y <= 6)):
            return False;
        return True;

    # "象"走棋判断
    if (qi_name == "象" or qi_name == "相"):
        if ((x - oldx) * (y - oldy) == 0):
            return False;
        if (abs(x - oldx) != 2 or abs(y - oldy) != 2):
            return False;
        if (y < 5 and qi_name == "相"):  # 过河
            return False;
        if (y >= 5 and qi_name == "象"):  # 过河
            return False;
        i = 0;
        j = 0;  # i,j必须有初始值
        if (x - oldx == 2):
            i = x - 1;
        if (x - oldx == -2):
            i = x + 1;
        if (y - oldy == 2):
            j = y - 1;
        if (y - oldy == -2):
            j = y + 1;
        if (chessmap[i][j] != -1):  # 憋象腿
            return False;
        return True;

    # "马"走棋判断
    if (qi_name == "马" or qi_name == "马"):
        if (abs(x - oldx) * abs(y - oldy) != 2):
            return False;
        if (x - oldx == 2):
            if (chessmap[x - 1][oldy] != -1):  # 蹩马腿
                return False;
        if (x - oldx == -2):
            if (chessmap[x + 1][oldy] != -1):  # 蹩马腿
                return False;
        if (y - oldy == 2):
            if (chessmap[oldx][y - 1] != -1):  # 蹩马腿
                return False;
        if (y - oldy == -2):
            if (chessmap[oldx][y + 1] != -1):  # 蹩马腿
                return False;
        return True;

    # "车"走棋判断
    if (qi_name == "车" or qi_name == "车"):
        # 判断是否直线
        if ((x - oldx) * (y - oldy) != 0):
            return False;
        # 判断是否隔有棋子
        if (x != oldx):
            if (oldx > x):
                t = x;
                x = oldx;
                oldx = t;
            for i in range(oldx, x + 1):
                if (i != x and i != oldx):
                    if (chessmap[i][y] != -1):
                        return False;
        if (y != oldy):
            if (oldy > y):
                t = y;
                y = oldy;
                oldy = t;
            for j in range(oldy, y + 1):
                if (j != y and j != oldy):
                    if (chessmap[x][j] != -1):
                        return False;
        return True;

    # "炮"走棋判断
    if (qi_name == "炮" or qi_name == "炮"):
        swapflagx = False;
        swapflagy = False;
        if ((x - oldx) * (y - oldy) != 0):
            return False;
        c = 0;
        if (x != oldx):
            if (oldx > x):
                t = x;
                x = oldx;
                oldx = t;
                swapflagx = True;
            for i in range(oldx, x + 1):  # for (i = oldx; i <= x; i += 1):
                if (i != x and i != oldx):
                    if (chessmap[i][y] != -1):
                        c = c + 1;

        if (y != oldy):
            if (oldy > y):
                t = y;
                y = oldy;
                oldy = t;
                swapflagy = True;
            for j in range(oldy, y + 1):  # for (j = oldy; j <= y; j += 1):
                if (j != y and j != oldy):
                    if (chessmap[x][j] != -1):
                        c = c + 1;

        if (c > 1):
            return False;  # 与目标处间隔1个以上棋子
        if (c == 0):  # 与目标处无间隔棋子
            if (swapflagx == True):
                t = x;
                x = oldx;
                oldx = t;
            if (swapflagy == True):
                t = y;
                y = oldy;
                oldy = t;
            if (chessmap[x][y] != -1):
                return False;
        if (c == 1):  # 与目标处间隔1个棋子
            if (swapflagx == True):
                t = x;
                x = oldx;
                oldx = t;
            if (swapflagy == True):
                t = y;
                y = oldy;
                oldy = t;
            if (chessmap[x][y] == -1):  # 如果目标处无棋子，则不能走此步
                return False;
        return True;

    # "卒" "兵"走棋判断
    if (qi_name == "卒" or qi_name == "兵"):
        if ((x - oldx) * (y - oldy) != 0):  # 不是直线走棋
            return False;
        if (abs(x - oldx) > 1 or abs(y - oldy) > 1):  # 走多步，不符合兵仅能走一步
            return False;
        if (y >= 5 and (x - oldx) != 0 and qi_name == "兵"):  # 未过河且横向走棋
            return False;
        if (y < 5 and (x - oldx) != 0 and qi_name == "卒"):  # 未过河且横向走棋
            return False;
        if (y - oldy > 0 and qi_name == "兵"):  # 后退
            return False;
        if (y - oldy < 0 and qi_name == "卒"):  # 后退
            return False;
        return True;
    return True;


# ——————————————————————
def callback(event):  # 走棋picBoard_MouseClick
    global LocalPlayer
    global chessmap
    global rect1, rect2  # 选中框图像id
    global firstChessid, secondChessid
    global x1, x2, y1, y2
    global first
    print("clicked at", event.x, event.y, LocalPlayer)
    x = (event.x - 14) // 76  # 换算棋盘坐标
    y = (event.y - 14) // 76
    print("clicked at", x, y, LocalPlayer)

    # if (IsMyTurn == False):
    #   return;

    if (first):  # 第1次单击棋子
        x1 = x;
        y1 = y;
        firstChessid = chessmap[x1][y1]
        if not (chessmap[x1][y1] == -1):
            player = dict_ChessName[firstChessid][0]
            if (player != LocalPlayer):
                print("单击成对方棋子了!");
                return
            print("第1次单击", firstChessid)
            first = False;
            rect1 = cv.create_rectangle(60 + 76 * x - 40, 54 + y * 76 - 38, 60 + 76 * x + 80 - 40,
                                        54 + y * 76 + 80 - 38, outline="red")  # 画选中标记框

    else:  # 第2次单击
        x2 = x;
        y2 = y;
        secondChessid = chessmap[x2][y2]
        # 目标处如果是自己的棋子,则换上次选择的棋子
        if not (chessmap[x2][y2] == -1):
            player = dict_ChessName[secondChessid][0]
            if (player == LocalPlayer):  # 如果是自己的棋子,则换上次选择的棋子
                firstChessid = chessmap[x2][y2]
                print("第2次单击", firstChessid)
                cv.delete(rect1);  # 取消上次选择的棋子标记框
                x1 = x;
                y1 = y;
                # 设置选择的棋子颜色
                rect1 = cv.create_rectangle(60 + 76 * x - 40, 54 + y * 76 - 38, 60 + 76 * x + 80 - 40,
                                            54 + y * 76 + 80 - 38, outline="red")  # 画选中标记框
                print("第2次单击", firstChessid)
                return;
            else:  # 在吃子目标处画框
                rect2 = cv.create_rectangle(60 + 76 * x - 40, 54 + y * 76 - 38, 60 + 76 * x + 80 - 40,
                                            54 + y * 76 + 80 - 38, outline="yellow")  # 目标处画框;
        else:  # 在移动棋子目标处画框
            rect2 = cv.create_rectangle(60 + 76 * x - 40, 54 + y * 76 - 38, 60 + 76 * x + 80 - 40,
                                        54 + y * 76 + 80 - 38, outline="yellow")  # 目标处画框;

        # 目标处没棋子，移动棋子
        print("kkkkk", firstChessid)
        if (chessmap[x2][y2] == " " or chessmap[x2][y2] == -1):  # 目标处没棋子，移动棋子
            print("目标处没棋子，移动棋子", firstChessid, x2, y2, x1, y1)
            if (IsAbleToPut(firstChessid, x2, y2, x1, y1)):  # 判断是否可以走棋
                print("can移动棋子", x1, y1)
                cv.move(firstChessid, 76 * (x2 - x1), 76 * (y2 - y1));
                # ******************************************
                # 在map取掉原CurSelect棋子
                chessmap[x1][y1] = -1;
                chessmap[x2][y2] = firstChessid
                cv.delete(rect1);
                cv.delete(rect2);

                # send
                # send("move" + "|" + idx.ToString() + "|" + (10 - x2).ToString() + "|"
                #    + Convert.ToString(11 - y2) + "|" + StepList[StepList.Count - 1]);
                # CurSelect = 0;
                first = True;
                SetMyTurn(False);  # 该对方了
                # toolStripStatusLabel1.Text = "";
            else:
                # 错误走棋
                print("不符合走棋规则");
                showinfo(title="提示", message="不符合走棋规则")
            return;
        else:
            # 目标处有棋子，可以吃子
            if (not (chessmap[x2][y2] == -1) and IsAbleToPut(firstChessid, x2, y2, x1, y1)):  # 可以吃子
                first = True;
                print("can吃子", x1, y1)
                cv.move(firstChessid, 76 * (x2 - x1), 76 * (y2 - y1));
                # ******************************************
                # 在map取掉原CurSelect棋子
                chessmap[x1][y1] = -1;
                chessmap[x2][y2] = firstChessid
                cv.delete(secondChessid);
                cv.delete(rect1);  # 删除选中标记框
                cv.delete(rect2);  # 删除目标标记框

                if (dict_ChessName[secondChessid][1] == "将"):  # "将"
                    showinfo(title="提示", message="红方你赢了")
                    return;
                if (dict_ChessName[secondChessid][1] == "帅"):  # "帅"
                    showinfo(title="提示", message="黑方你赢了")
                    return;
                # send

                SetMyTurn(False);  # 该对方了
                # toolStripStatusLabel1.Text = "";
            else:  # 不能吃子
                print("不能吃子");
                lable1['text'] = "不能吃子"
                cv.delete(rect2);  # 删除目标标记框


# ——————————————————————

def SetMyTurn(flag):
    global LocalPlayer
    IsMyTurn = flag
    if LocalPlayer == "红":
        LocalPlayer = "黑"
        lable1['text'] = "轮到黑方走"
    else:
        LocalPlayer = "红"
        lable1['text'] = "轮到红方走"


# ——————————————————————
img1 = PhotoImage(file='bmp/棋盘.png')


def DrawBoard():  # 画棋盘
    p1 = cv.create_image((0, 0), image=img1)
    cv.coords(p1, (360, 400))


# ——————————————————————
def sleep():
    for i in range(0, 10000):
        pass


def LoadChess():  # 加载棋子
    global chessmap
    # 黑方16个棋子
    for i in range(0, 9):
        img = imgs[i]
        id = cv.create_image((60 + 76 * i, 54), image=img)  # 76*76棋盘格子大小
        dict_ChessName[id] = chessname[i];  # 图像对应的是那种棋子
        chessmap[i][0] = id  # 图像id

    for i in range(0, 5):
        img = imgs[9]  # 卒
        id = cv.create_image((60 + 76 * 2 * i, 54 + 3 * 76), image=img)  # 76*76棋盘格子大小
        chessmap[i * 2][3] = id
        dict_ChessName[id] = "黑卒";  # 图像对应的是那种棋子

    img = imgs[10]  # 黑方炮
    id = cv.create_image((60 + 76 * 1, 54 + 2 * 76), image=img)  # 76*76棋盘格子大小
    chessmap[1][2] = id
    dict_ChessName[id] = "黑炮";  # 图像对应的是那种棋子

    id = cv.create_image((60 + 76 * 7, 54 + 2 * 76), image=img)  # 76*76棋盘格子大小
    chessmap[7][2] = id
    dict_ChessName[id] = "黑炮";  # 图像对应的是那种棋子

    # 红方16个棋子
    for i in range(0, 9):
        img = imgs[i + 11]
        id = cv.create_image((60 + 76 * i, 54 + 9 * 76), image=img)  # 76*76棋盘格子大小
        dict_ChessName[id] = chessname[i + 11];  # 图像对应的是那种棋子
        chessmap[i][9] = id  # 图像id

    for i in range(0, 5):
        img = imgs[20]  # 兵
        id = cv.create_image((60 + 76 * 2 * i, 54 + 6 * 76), image=img)  # 76*76棋盘格子大小
        chessmap[i * 2][6] = id  # 图像id
        dict_ChessName[id] = chessname[20];  # 图像对应的是那种棋子

    img = imgs[21]  # 红方炮
    id = cv.create_image((60 + 76 * 1, 54 + 7 * 76), image=img)  # 76*76棋盘格子大小
    chessmap[1][7] = id
    dict_ChessName[id] = "红炮";  # 图像对应的是那种棋子

    id = cv.create_image((60 + 76 * 7, 54 + 7 * 76), image=img)  # 76*76棋盘格子大小
    chessmap[7][7] = id
    dict_ChessName[id] = "红炮";  # 图像对应的是那种棋子


# ——————————————————————
DrawBoard()  # 画棋盘
LoadChess()  # 加载棋子
# ——————————————————————

# print (map1)
print(dict_ChessName)

cv.bind("<Button-1>", callback)
cv.pack()
lable1 = Label(root, fg='red', bg='white', text="红方先走")
lable1['text'] = "红方先走1"
##var = StringVar()
##l = Label(root, fg='red', bg='white',text=var, width=14, height=5)
##var.set("Hey")
lable1.pack()
root.mainloop()



