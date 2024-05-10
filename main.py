import time
import pyautogui
import cv2
import numpy
import re
import mah # mah.py

def check_handcards(string: str):
    # 检查输入是否合法。
    # 若输入不合法，输出错误提示并返回False.
    # 若尚未摸牌，输出13
    # 若已摸牌，返回14
    fullmatch = re.fullmatch(r'(\d+[mps]|[1-7]+z)+', string)
    if not fullmatch:
        # print('无效的输入！')
        return False
    match = re.findall(r'\d+[mps]|[1-7]+z', string)
    carddict = {
        'm':[], 'p':[], 's':[], 'z':[]
    }
    for cards in match:
        type_ = cards[-1]
        for i in cards[:-1]:
            if i == '0':# 红宝牌
                carddict[type_].append(5)
            else:
                carddict[type_].append(int(i))
        carddict[type_].sort()
    num = sum(len(carddict[tp]) for tp in 'mpsz')
    for tp in 'mpsz':
        for i in set(carddict[tp]):
            if carddict[tp].count(i) > 4:
                # print('牌数量错误！单种牌不得多于4张！')
                return False
    if num == 13:
        # print('牌数量13张！')
        return 13
    if num != 14:
        # print('牌数量错误！手牌数必须为14张！')
        return False
    else:
        return 14

def start():
    steadyLocation = ()
    while True:
        if not steadyLocation:
            start = time.time()
            # location = locate()
            # print(f"{location=}")
            location = (363, 1158, 1685, 224)
            end = time.time()
            print(f"Time spent on locating: {end-start:.2f}s")
        else:
            location = steadyLocation
        cards = ""
        if location:
            while True:
                start = time.time()
                result = screenshot(*location)
                end = time.time()
                if result: # 从屏幕中识别出结果
                    start = time.time()
                    (cards, cardsConvert), lastCards = parse(), cards # 读取手牌
                    # print(f"{cards=}")
                    end = time.time()
                    if cards.replace("0","5")!=lastCards.replace("0","5"): # 如果手牌未改变
                        cards_status = check_handcards(cards)
                        if cards_status == False: # 手牌有误
                            time.sleep(0.05)
                            break
                        elif cards_status == 13: # 未摸牌，13张
                            print("\n\n")
                            mah.print_shanten_13(cards) # 求解待牌
                            steadyLocation = location
                            time.sleep(0.05)
                        elif cards_status == 14: # 已摸牌，14张
                            print("\n\n")
                            mah.print_shanten_14(cards) # 求解何切
                            steadyLocation = location
                            time.sleep(0.05)
                        # 将手牌写入文档
                        #     if result != None:
                        #         with open('cards',"w") as fo:
                        #             fo.write(cardsConvert)
                    else: # 如果手牌有改变
                        if check_handcards(cards)==False:
                            break
                else: # 屏摄出错
                    time.sleep(0.05)
                    
   
def screenshot(a,b,c,d):
    try:
        imgPath = 'img/'
        imPartial = pyautogui.screenshot(region=(a,b,c,d))
        imPartial.save(imgPath+"screenshot_partial.png")
    except:
        print("Error with screenshot()")
        return False
    else:
        return True
    
def parse():
    try:
        def detect():
            def detectOneType(templatePath, imshowTarget):
                template = cv2.imread(templatePath)
                theight, twidth = template.shape[:2]
                result = cv2.matchTemplate(imshowTarget,template,cv2.TM_SQDIFF_NORMED)
                numOfloc = 0
                threshold = 0.03
                loc = numpy.where(result<threshold)
                for one in zip(*loc[::-1]):
                    for compare in noDuplicates:
                        if (abs(one[0]-compare[0])<(twidth*0.75)):
                            break
                    else:
                        noDuplicates.append(one)
                        numOfloc = numOfloc + 1
                        # cv2.rectangle(imshowTarget,one,(one[0]+twidth,one[1]+theight),(0,0,225),2)
                return (numOfloc, imshowTarget)
            
            targetPath = "img/screenshot_partial.png"
            imshowTarget = cv2.imread(targetPath)
            
            noDuplicates=[]
            mjs={"m":{},
                "p":{},
                "s":{},
                "z":{}}
            for i in (5,1,2,3,4,6,7):
                templatePath = "img/mj/z"+str(i)+".png"
                num, imshowTarget = detectOneType(templatePath, imshowTarget)
                mjs["z"][i]=mjs["z"].get(i,0)+num
            for i in (1,2,3,4,5,6,7,8,9,0):
                templatePath = "img/mj/m"+str(i)+".png"
                num, imshowTarget = detectOneType(templatePath, imshowTarget)
                mjs["m"][i]=mjs["m"].get(i,0)+num
            for i in (1,2,3,4,5,6,7,8,9,0):
                templatePath = "img/mj/p"+str(i)+".png"
                num, imshowTarget = detectOneType(templatePath, imshowTarget)
                mjs["p"][i]=mjs["p"].get(i,0)+num
            for i in (1,2,3,4,5,6,7,8,9,0):
                templatePath = "img/mj/s"+str(i)+".png"
                num, imshowTarget = detectOneType(templatePath, imshowTarget)
                mjs["s"][i]=mjs["s"].get(i,0)+num
            
            cardText = ""
            is_m = is_p = is_s = is_z = False
            for i in (1,2,3,4,0,5,6,7,8,9):
                cardText = cardText + str(i)*mjs["m"].get(i,0)
                if mjs["m"].get(i,0): is_m = True
            if is_m: cardText = cardText + "m"
            for i in (1,2,3,4,0,5,6,7,8,9):
                cardText = cardText + str(i)*mjs["p"].get(i,0)
                if mjs["p"].get(i,0): is_p = True
            if is_p: cardText = cardText + "p"
            for i in (1,2,3,4,0,5,6,7,8,9):
                cardText = cardText + str(i)*mjs["s"].get(i,0)
                if mjs["s"].get(i,0): is_s = True
            if is_s: cardText = cardText + "s"
            for i in range(1,8):
                cardText = cardText + str(i)*mjs["z"].get(i,0)
                if mjs["z"].get(i,0): is_z = True
            if is_z: cardText = cardText + "z"

            cardTextConvert = ""
            card_m = card_p = card_s = card_z = ""
            # 添加 "m" 类型的牌
            for i in (1, 2, 3, 4, 0, 5, 6, 7, 8, 9):
                card_m += str(i)*mjs["m"].get(i,0)
            # 添加 "p" 类型的牌
            for i in (1, 2, 3, 4, 0, 5, 6, 7, 8, 9):
                card_p += str(i)*mjs["p"].get(i,0)
            # 添加 "s" 类型的牌
            for i in (1, 2, 3, 4, 0, 5, 6, 7, 8, 9):
                card_s += str(i)*mjs["s"].get(i,0)
            # 添加 "z" 类型的牌
            for i in range(1, 8):
                card_z += str(i)*mjs["z"].get(i,0)
            # 检查是否有每种牌类型，并将其添加到 cardTextConvert 中
            if card_m:
                cardTextConvert += "m" + card_m
            if card_p:
                cardTextConvert += "p" + card_p
            if card_s:
                cardTextConvert += "s" + card_s
            if card_z:
                cardTextConvert += "z" + card_z
            # strText = cardText
            # cv2.namedWindow(strText,cv2.WINDOW_NORMAL)
            # cv2.imshow(strText,imshowTarget)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            return (cardText, cardTextConvert)
        
        cardText, cardTextConvert = detect()
    except:
        print("Error with parse()")
        raise KeyboardInterrupt
        return False
    else:
        return (cardText, cardTextConvert)
    
start()