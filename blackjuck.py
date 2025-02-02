import random

CARDS = [
    "H-A", "H-2", "H-3", "H-4", "H-5", "H-6", "H-7", "H-8", "H-9", "H-10", "H-J", "H-Q", "H-K",
    "S-A", "S-2", "S-3", "S-4", "S-5", "S-6", "S-7", "S-8", "S-9", "S-10", "S-J", "S-Q", "S-K",
    "D-A", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7", "D-8", "D-9", "D-10", "D-J", "D-Q", "D-K",
    "C-A", "C-2", "C-3", "C-4", "C-5", "C-6", "C-7", "C-8", "C-9", "C-10", "C-J", "C-Q", "C-K" 
]
BLACKJUCK = 21          
DEALER_PARAMETER = 16   #ディーラの行動パラメータ
SEPARATOR_NUM = 70      #仕切り記号の数
   
cardList = []           # 山札
playerCard = []         # プレイヤーの手札
dealerCard = []         # ディーラの手札
state = 1               # 1:ゲーム続行/ 2:ゲーム終了
motikin = 0   
kakekin = 0   
playerBurst = False     # False:得点がバーストバーストしてない/True:バーストした
dealerBurst = False     # False:得点がバーストバーストしてない/True:バーストした

#持ち金をセット
def motikin_set():
    global motikin
    while True:
        try:
            
            motikin = int(input("プレイヤーの持ち金を入力(正の数)してください："))
            if motikin > 0:
                break
            else:
                print("正の数を入力してください")
                continue
        except ValueError:
            print("正の数を入力してください")
            continue

#掛け金をセット
def kakekin_set():
    global kakekin
    while True:
        try:
            kakekin = int(input(f"持ち金 {motikin:,}/ 掛け金を入力してください："))
            if motikin > 0 and kakekin <= motikin :
                break
            else:
                print("正の数ではないもしくは持ち金が不足しています")
                continue
        except ValueError:
            print("正の数を入力してください")
            continue

#山札のシャッフル
def cardList_shuffle():
    random.shuffle(cardList)

#プレイヤーが1枚引く
def draw_playerCard():
    playerCard.append(cardList.pop(0))

#ディーラが1枚引く
def draw_dealerCard():
    dealerCard.append(cardList.pop(0))

#手札の得点を計算する
def calculate_point(hand):
    numberListInt = []
    AceCount = 0

    #カードナンバーの判定
    for i in range(len(hand)):
        cardNumber = hand[i].split("-")[-1]
        if cardNumber == "A":
            numberListInt.append(11)
            AceCount += 1
        elif cardNumber == "J" or cardNumber == "Q" or cardNumber == "K":
            numberListInt.append(10)
        else:
            numberListInt.append(int(cardNumber))
        
    point = sum(numberListInt)
    
    #エースのカードがある時の処理
    for i in range(AceCount):
        if point > BLACKJUCK:
            point -= 10
            if point <= BLACKJUCK:
                break 
    return point

#ディーラ・プレイヤーの手札の状況を出力
def print_situation():
    print("")
    print("-" * SEPARATOR_NUM)
    print("ディーラ")
    print(f"手札：{len(dealerCard)}枚")
    print("-" * SEPARATOR_NUM)
    print("プレイヤー")
    print(f"手札：{playerCard}")
    print(f"得点：{calculate_point(playerCard)}")
    print("-" * SEPARATOR_NUM)

#ディーラの処理
def dealer_choice():
    global dealerBurst
    dealerBurst = False
    dealerPoint = calculate_point(dealerCard)
    if dealerPoint <= DEALER_PARAMETER:
        draw_dealerCard()
        dealer_choice()
    elif dealerPoint > BLACKJUCK:
        print("ディーラの得点がバーストしました．")
        dealerBurst = True

#プレイヤーによる「勝負するのか、ドローするか」の選択
def player_choice():
    global playerBurst
    playerBurst = False
    while True:
        try:
            if calculate_point(playerCard) <= BLACKJUCK:
                command = int(input("1(勝負する), 2(カードをドローする) のどちらかを選択してください:"))
                if command == 1:
                    break
                elif command == 2:
                    draw_playerCard()
                    print_situation()
                    continue
                else:
                    print("指定の数を入力してください")
                    continue
            else:
                print("プレイヤーの得点がバーストしました．")
                playerBurst = True
                break
        except ValueError:
            print("指定の数を入力してください")
            continue

#最終結果の出力
def print_result():
    global motikin
    dealerPoint = calculate_point(dealerCard)
    playerPoint = calculate_point(playerCard)

    print("")
    print("*" * SEPARATOR_NUM)
    if playerPoint == dealerPoint:
        print("結果:引き分け")
    elif playerBurst == False and dealerBurst == False:
        if playerPoint > dealerPoint:
            print("結果:プレイヤーの勝利!!")
            motikin += kakekin
        else:
            print("結果:プレイヤーの敗北")
            motikin -= kakekin
    elif playerBurst == False and dealerBurst == True:
        print("結果:プレイヤーの勝利!!")
        motikin += kakekin
    elif playerBurst == True and dealerBurst == False:
        print("結果:プレイヤーの敗北")
        motikin -= kakekin
    
    print("-" * SEPARATOR_NUM)
    print("ディーラ")
    print(f"手札：{dealerCard}")
    print(f"得点：{dealerPoint}")
    print("-" * SEPARATOR_NUM)
    print("プレイヤー")
    print(f"手札：{playerCard}")
    print(f"得点：{playerPoint}")
    print("-" * SEPARATOR_NUM)

#ゲームを続けるのか、終了するかの選択
def continue_choice():
    global state
    print("*" * SEPARATOR_NUM)
    if motikin == 0:
        print("持ち金が0になったため終了します")
        state = 2
    else:
        print(f"現在の持ち金:{motikin:,}")
        while True:
            try:
                command = int(input("1(ゲームを続ける), 2(ゲームを終了する) のどちらかを選択してください:"))
                if command == 1:
                    break
                elif command == 2:
                    state = 2
                    break
                else:
                    print("指定の数を入力してください")
                    continue
            except ValueError:
                print("指定の数を入力してください")
                continue
    print("*" * SEPARATOR_NUM)

#1ゲーム
def play_game():
    kakekin_set()

    #変数の初期化
    playerCard.clear()
    dealerCard.clear()
    cardList.clear()
    cardList.extend(CARDS)
    playerBurst = False
    dealerBurst = False
    state = 1
    cardList_shuffle()

    #両者ともにカードを2枚引く
    for i in range(2):
        draw_playerCard()
        draw_dealerCard()
    
    print_situation()
    player_choice()
    if playerBurst == False:
        dealer_choice()
    print_result()

#メイン処理
def main():
    motikin_set()
    while state == 1:
        play_game()
        continue_choice()

main()
