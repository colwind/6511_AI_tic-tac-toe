import time
import requests

class Node():
    def __init__(self):
        self.bestChild = None
        self.child = []
        self.p = None
        self.mark = 0

    def setPoint(self, r):
        self.p = r

    def addChild(self, r):
        self.child.append(r)

    def getLastChild(self):
        return self.child[-1]

class game():
    def __init__(self, m, n, aifirst, deep):
        self.size = m
        self.win_number = n
        self.aiFirst = aifirst
        self.chessBoard = [[0 for _ in range(self.size)] for __ in range(self.size)] # 1:black -1:white
        self.isBlack = False # chess color
        self.toJudge = {}
        self.dr = [-1,1,-1,1,0,0,-1,1]
        self.dc = [1,-1,-1,1,-1,1,0,0]
        self.MAXN = 2147483647
        self.MINN = -1 * self.MAXN
        self.searchDeep = deep # dfs deep
        self.isFinished = False
        self.iniChessBoard()

    def putChess(self, x, y):
        if self.isBlack:
            self.chessBoard[y][x] = 1
        else:
            self.chessBoard[y][x] = -1
        if self.isEnd(x,y):
            if self.isBlack:
                s = "black wins"
            else:
                s = "white wins"
            # print(s)
            self.isBlack = True
            # self.iniChessBoard()
            return
        else:
            p = (x,y)
            if p in self.toJudge:
                self.toJudge.pop(p)
                # del(self.toJudge[p])
            for i in range(8):
                now = (p[0] + self.dc[i], p[1] + self.dr[i])
                if (0 <= now[0] and now[0] < self.size and 0 <= now[1] and now[1] < self.size and self.chessBoard[now[1]][now[0]] == 0):
                    self.toJudge[now] = 1

    def iniChessBoard(self):
        self.toJudge.clear()
        # initial chessboard
        for i in range(self.size):
            for j in range(self.size):
                self.chessBoard[i][j] = 0
        # ai first
        # ri = (self.size + 1) // 2
        # self.chessBoard[ri][ri] = 1
        # self.findtoJudge(ri,ri)
        self.isBlack = False

    def findtoJudge(self, x, y):
        for i in range(8):
            if (0 <= x + self.dc[i] and x + self.dc[i] < self.size and 0 <= y + self.dr[i] and y + self.dr[i] < self.size):
                now = (x+self.dc[i],y+self.dr[i])
                if now not in self.toJudge:
                    self.toJudge[now] = 1

    def myAI(self):
        node = Node()
        self.dfs(0, node, self.MINN, self.MAXN, None)
        """
        小朋友，你是不是有许多问号
        """
        now = node.bestChild.p
        # del(self.toJudge[now])
        # post_move = self.make_a_move(,,)
        # return post_move
        self.putChess(now[0],now[1])
        self.isBlack = False
        return ",".join(map(str,[now[0],now[1]]))

    def getMark(self):
        MAXN = 2147483647
        res = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.chessBoard[i][j] != 0:
                    # COLUMS
                    flag1 = False
                    flag2 = False
                    x = j
                    y = i
                    cnt = 1
                    col = x - 1
                    row = y
                    while col >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        col -= 1
                    if (col >= 0 and self.chessBoard[row][col] == 0):
                        flag1 = True
                    col = x + 1
                    row = y
                    while col < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        col += 1
                    if (col < self.size and self.chessBoard[row][col] == 0):
                        flag2 = True
                    if flag1 and flag2:
                        res += self.chessBoard[i][j] * cnt * cnt * 5
                    elif flag1 or flag2:
                        res += self.chessBoard[i][j] * cnt * cnt/(self.win_number-1)
                    if cnt >= self.win_number:
                        res = MAXN * self.chessBoard[i][j]
                        return res

                    # ROWS
                    col = x
                    row = y - 1
                    cnt = 1
                    flag1 = False
                    flag2 = False
                    while row >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        row -= 1
                    if (row >= 0 and self.chessBoard[row][col] == 0):
                        flag1 = True
                    col = x
                    row = y + 1
                    while row < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        row += 1
                    if (row < self.size and self.chessBoard[row][col] == 0):
                        flag2 = True
                    if flag1 and flag2:
                        res += self.chessBoard[i][j] * cnt * cnt * 5
                    elif flag1 or flag2:
                        res += self.chessBoard[i][j] * cnt * cnt/(self.win_number-1)
                    if cnt >= self.win_number:
                        res= MAXN * self.chessBoard[i][j]
                        return res

                    # left diagonal
                    col = x - 1
                    row = y - 1
                    cnt = 1
                    flag1 = False
                    flag2 = False
                    while col >= 0 and row >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        col -=1
                        row -= 1
                    if col >= 0 and row >= 0 and self.chessBoard[row][col] == 0:
                        flag1 = True
                    col = x + 1
                    row = y + 1
                    while col < self.size and row < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        row += 1
                        col += 1
                    if col < self.size and row < self.size and self.chessBoard[row][col] == 0:
                        flag2 = True
                    if flag1 and flag2:
                        res += self.chessBoard[i][j] * cnt * cnt * 5
                    elif flag1 or flag2:
                        res += self.chessBoard[i][j] * cnt * cnt /(self.win_number-1)
                    if cnt >= self.win_number:
                        res = MAXN * self.chessBoard[i][j]
                        return res

                    # right diagonal
                    col = x + 1
                    row = y - 1
                    cnt = 1
                    flag1 = False
                    flag2 = False
                    while col < self.size and row >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        col += 1
                        row -= 1
                    if col < self.size and row >= 0 and self.chessBoard[row][col] == 0:
                        flag1 = True
                    col = x - 1
                    row = y + 1
                    while col >= 0 and row < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
                        cnt += 1
                        row += 1
                        col -= 1
                    if col >= 0 and row < self.size and self.chessBoard[row][col] == 0:
                        flag2 = True
                    if flag1 and flag2:
                        res += self.chessBoard[i][j] * cnt * cnt * 5
                    elif flag1 or flag2:
                        res += self.chessBoard[i][j] * cnt * cnt /(self.win_number-1)
                    if cnt >= self.win_number:
                        res = MAXN * self.chessBoard[i][j]
                        return res
        return res

    def isEnd(self, x, y):
        # colums
        cnt = 1
        col = x - 1
        row = y
        while col >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            col -= 1
        col = x + 1
        while col < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            col += 1
        if cnt >= self.win_number:
            self.isFinished = True
            return True
        # rows
        col = x
        row = y - 1
        cnt = 1
        while row >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            row -= 1
        row = y + 1
        while row < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            row += 1
        if cnt >= self.win_number:
            self.isFinished = True
            return True
        # left diagonal
        col = x - 1
        row = y - 1
        cnt = 1
        while col >= 0 and row >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            col -= 1
            row -= 1
        col = x + 1
        row = y + 1
        while col < self.size and row < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            row += 1
            col += 1
        if cnt >= self.win_number:
            self.isFinished = True
            return True
        # right diagonal
        col = x + 1
        row = y - 1
        cnt = 1
        while col < self.size and row >= 0 and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            col += 1
            row -= 1
        col = x - 1
        row = y + 1
        while col >= 0 and row < self.size and self.chessBoard[row][col] == self.chessBoard[y][x]:
            cnt += 1
            row += 1
            col -= 1
        if cnt >= self.win_number:
            self.isFinished = True
            return True
        return False


        # alpha beta dfs

    def dfs(self, deep, root, alpha, beta, p):
        MAXN = 2147483647
        if (deep == self.searchDeep):
            root.mark = self.getMark()
            return
        judgeSet = [] #  ArrayList < Point >
        for i in self.toJudge:
            judgeSet.append(i)
        for i in judgeSet:
            now = i
            node = Node()
            node.setPoint(now)
            root.addChild(node)
            if now in self.toJudge:
                flag = True
            else:
                flag = False

            if deep % 2 == 1:
                self.chessBoard[now[1]][now[0]] = -1
            else:
                self.chessBoard[now[1]][now[0]] = 1

            if self.isEnd(now[0], now[1]):
                root.bestChild = node
                root.mark = MAXN * self.chessBoard[now[1]][now[0]]
                self.chessBoard[now[1]][now[0]] = 0
                return
            flags = [True for _ in range(8)]
            for i in range(8):
                next = (now[0] + self.dc[i], now[1] + self.dr[i])
                if (0 <= now[0] + self.dc[i] and now[0] + self.dc[i] < self.size and 0 <= now[1] + self.dr[i] and now[1] + self.dr[i] < self.size and self.chessBoard[next[1]][next[0]] == 0):
                    if next not in  self.toJudge:
                        self.toJudge[next] = 1
                        # print(next)
                        # print()
                    else:
                        flags[i] = False
                    """
                    退位
                    """
                else:
                    flags[i] = False

            if flag:
                self.toJudge.pop(now)
                # del(self.toJudge[now])
            self.dfs(deep+1,root.getLastChild(),alpha,beta,now)
            self.chessBoard[now[1]][now[0]]=0
            if flag:
                self.toJudge[now] = 1
            for i in range(8):
                if flags[i]:
                    delet = (now[0] + self.dc[i], now[1] + self.dr[i])
                    # print(self.toJudge)
                    # print(delet)
                    self.toJudge.pop(delet)
                    # del(self.toJudge[delet])
            # alpha beta pruning
            # min layer
            if deep % 2 == 1:
                if not root.bestChild or root.getLastChild().mark < root.bestChild.mark:
                    root.bestChild = root.getLastChild()
                    root.mark = root.bestChild.mark
                    if root.mark <= self.MINN:
                        root.mark += deep
                    beta = min(root.mark, beta)
                if root.mark <= alpha:
                    return
            # max layer
            else:
                if not root.bestChild or root.getLastChild().mark > root.bestChild.mark:
                    root.bestChild = root.getLastChild()
                    root.mark = root.bestChild.mark
                    if root.mark == self.MAXN:
                        root.mark -= deep
                    alpha = max(root.mark,alpha)
                if root.mark >= beta:
                    return
        # if deep == 0:
        #     print("******************** deep==0 **********************\n")

    def debug(self):
        for i in range(self.size):
            s = " ".join(map(str,self.chessBoard[i]))
            print(s)

    def make_a_move(self, gameId, teamId, move):
        URL = "http://www.notexponential.com/aip2pgaming/api/index.php"
        headers = {
            "x-api-key": "16f3ecbbb20e7ae3f30d",
            "userid": "922",
            "User-Agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 "
        }
        files = [

        ]
        payload = {
            "type": "move",
            "gameId": gameId,
            "teamId": teamId,
            "move": move
        }
        # response = requests.post(URL, params=payload, headers=headers).json()
        response = requests.request("POST", URL, headers=headers, data=payload, files=files).json()
        print(response)
        moveid = response["moveId"]
        code = response["code"]
        print(moveid, code)
        return moveid

    def get_moves(self, gameId, move_count):
        URL = "http://www.notexponential.com/aip2pgaming/api/index.php"
        headers = {
            "x-api-key": "16f3ecbbb20e7ae3f30d",
            "userid": "922",
            "User-Agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 "
        }
        payload = {
            "type": "moves",
            "gameId": gameId,
            "count": move_count
        }
        response = requests.get(URL, params=payload, headers=headers).json()
        # print(response["teamId"])
        res = response["moves"][0]

        moveid = res["moveId"]
        movex = res["moveX"]
        movey = res["moveY"]
        print(moveid, movex, movey)
        return (int(moveid), int(movex), int(movey))

    def print_chessboard(self):
        res = " "
        for i in range(self.size):
            i = i % 10
            res += str(i)
        res += "\n"
        for i in range(self.size):
            res += str(i % 10)
            for j in range(self.size):
                if self.chessBoard[i][j] == 0:
                    res += "-"
                elif self.chessBoard[i][j] == 1:
                    res += "o"
                else:
                    res += "x"
            res += "\n"
        print (res)


battle = 1      # 1: play with API; 0: play with Human
isAifirst = 1   # 1:AI first 0:AI second
size = 12       # set the cheeboard size: 12*12
n = 6           # the target number of win
searchdeep = 3  # set the search tree deep
if battle:
    gameid = "1404"
    teamid = "1209"
    g = game(size, n, isAifirst, searchdeep)
    wait_time = 5
    total_time = 0
    if isAifirst:
        ri = (size + 1) // 2
        g.chessBoard[ri][ri] = 1
        g.findtoJudge(ri,ri)
        move = str(ri)+","+str(ri)
        last_moveid = g.make_a_move(gameid,teamid,move)
        g.print_chessboard()

        while 1:
            (moveid,movex,movey) = g.get_moves(gameid,"1")
            if moveid == last_moveid:
                time.sleep(wait_time)
                total_time += wait_time
                print(total_time)
            else:
                total_time = 0
                g.putChess(int(movex), int(movey))
                g.isBlack = True

                print("api: " + str(movex) + "," + str(movey))
                g.print_chessboard()
                move = g.myAI()
                last_moveid = g.make_a_move(gameid,teamid,move)
                print("me: " + str(last_moveid))
                g.print_chessboard()

    else:
        (moveid,movex,movey) = g.get_moves(gameid,"1")
        g.isBlack = False
        g.putChess(int(movex), int(movey))
        g.findtoJudge(movex, movey)
        g.isBlack = True
        print("api: " + str(movex) + "," + str(movey))
        g.print_chessboard()
        move = g.myAI()
        last_moveid = g.make_a_move(gameid, teamid, move)
        print("me: " + str(last_moveid))
        g.print_chessboard()
        while 1:
            (moveid, movex, movey) = g.get_moves(gameid, "1")
            if moveid == last_moveid:
                time.sleep(wait_time)
                total_time += wait_time
                print(total_time)
            else:
                total_time = 0
                g.putChess(int(movex), int(movey))
                g.isBlack = True

                print("api: " + str(movex) + "," + str(movey))
                g.print_chessboard()
                move = g.myAI()
                last_moveid = g.make_a_move(gameid, teamid, move)
                print("me: " + str(last_moveid))
                g.print_chessboard()
else: # test
    g = game(size, n, isAifirst, searchdeep)
    g.print_chessboard()
    wait_time = 5
    if isAifirst:
        ri = (size + 1) // 2
        g.chessBoard[ri][ri] = 1
        g.findtoJudge(ri,ri)
        g.print_chessboard()

        while 1:
            movex = input("input x: ")
            movey = input("input y: ")
            g.putChess(int(movex), int(movey))
            g.isBlack = True
            # if g.isFinished:
            #     print("over with api")
            #     break
            print("api: " + str(movex) + "," + str(movey))
            g.print_chessboard()
            move = g.myAI()
            print("AI-----:" + move)
            g.print_chessboard()
            # if g.isFinished:
            #     print("over with me")
            #     break
    else:
        movex = input("input x: ")
        movey = input("input y: ")
        g.isBlack = False
        g.putChess(int(movex), int(movey))
        g.isBlack = True
        print("human: " + str(movex) + "," + str(movey))
        g.print_chessboard()
        move = g.myAI()
        g.print_chessboard()
        if g.isFinished:
            print("over with me")
        while 1:
            movex = input("input x: ")
            movey = input("input y: ")
            g.putChess(int(movex), int(movey))
            g.isBlack = True
            # if g.isFinished:
            #     print("over with api")
            #     break
            print("api: " + str(movex) + "," + str(movey))
            g.print_chessboard()
            move = g.myAI()
            print("AI-----:"+move)
            g.print_chessboard()
            # if g.isFinished:
            #     print("over with me")
            #     break
