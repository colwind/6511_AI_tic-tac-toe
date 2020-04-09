import requests
def creat_game(m,n,s1,s2):
    URL = "http://www.notexponential.com/aip2pgaming/api/index.php"
    headers = {
        "x-api-key": "6896fded1a9b0c6bb60f",
        "userid": "917",
        "User-Agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 "
    }
    payload = {
        "type": "game",
        "teamId1": str(s1),
        "teamId2": str(s2),
        "gameType": "TTT",
        "boardSize": str(m),
        "target": str(n)
    }
    files = [

    ]
    response = requests.request("POST", URL, headers = headers, data = payload, files = files).json()
    # print(response)
    return response

def get_moves(gameId, move_count, size):
    URL = "http://www.notexponential.com/aip2pgaming/api/index.php"
    headers = {
        "x-api-key": "6896fded1a9b0c6bb60f",
        "userid": "917",
        "User-Agent": "Mozilla / 5.0(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 "
    }
    payload = {
        "type": "moves",
        "gameId": gameId,
        "count": move_count
    }
    response = requests.get(URL, params=payload, headers=headers).json()
    # print(response["teamId"])

    response = response["moves"][::-1]


    a = [[0 for i in range(size)] for j in range(size)]
    b = 1
    for res in response:
        moveid = res["moveId"]
        movex = res["moveX"]
        movey = res["moveY"]
        x = int(movex)
        y = int(movey)
        a[x][y] = b
        if b == 1:
            b = -1
        else:
            b = 1
        res = ""
        for i in range(size):
            for j in range(size):
                if a[i][j] == 0:
                    res += "-"
                elif a[i][j] == 1:
                    res += "o"
                else:
                    res += "x"
            res += "\n"
        print(res)

        print(moveid, movex, movey)
    return (int(moveid), int(movex), int(movey))



def make_a_move(gameId, teamId, move):
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
    return (moveid)


size = 12
#
# s = get_moves("1157","40",size)
s = creat_game(12,6,1209,1218)
# s = make_a_move("1093","1209","11,6")

