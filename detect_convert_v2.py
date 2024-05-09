import time
import pyautogui
import cv2
import numpy
import re

try:
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
                    if result:
                        start = time.time()
                        (cards, cardsConvert), lastCards = parse(), cards
                        # print(f"{cards=}")
                        end = time.time()
                        if cards.replace("0","5")!=lastCards.replace("0","5"):
                            start = time.time()
                            result = decide(cards)
                            steadyLocation = location
                            end = time.time()
                            if result == False:
                                time.sleep(0.05)
                                break
                            else:
                                if result != None:
                                    with open('cards',"w") as fo:
                                        fo.write(cardsConvert)
                            # print(f"Time spent on screenshotting: {end-start:.2f}s")
                            # print(f"Time spent on parsing: {end-start:.2f}s")
                            # print(f"Time spent on deciding: {end-start:.2f}s")
                        else:
                            if get_handcards(cards)==False:
                                break
                    time.sleep(0.05)
                    # print("+")
        
    def locate():
        try:
            imgPath = 'img/'
            imFull = pyautogui.screenshot()
            imFull.save(imgPath+"screenshot_full.png")

            target = cv2.imread("img/screenshot_full.png")
            template = cv2.imread("img/mj/top.png")
            theight, twidth = template.shape[:2]
            result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)
            cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # strmin_val = str(min_val)
            # cv2.rectangle(target,min_loc,(min_loc[0]+twidth,min_loc[1]+theight),(0,0,225),2)
            # title = "MatchResult----MatchingValue="+strmin_val
            # cv2.namedWindow(title,cv2.WINDOW_NORMAL)
            # cv2.imshow(title,target)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            print(min_loc,(min_loc[0]+twidth,min_loc[1]+theight))
        except:
            print("Error with locate()")
            raise KeyboardInterrupt
            return False
        else:
            return (min_loc[0]-30, min_loc[1]-50, twidth+250, theight+250)
    def screenshot(a,b,c,d):
        try:
            imgPath = 'img/'
            imPartial = pyautogui.screenshot(region=(a,b,c,d))
            imPartial.save(imgPath+"screenshot_partial.png")
        except:
            print("Error with screenshot()")
            raise KeyboardInterrupt
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
        
    def decide(cards):    
        if cards:
            result = get_handcards(cards)
            if result:
                print("\n"*3)
                print(cards)
                handcards = HandCards(get_handcards(cards))
                if handcards.shanten() < 0:
                    print('和了')
                elif handcards.shanten() == 0:
                    print('聴牌')
                    handcards.print_jinzhang()
                else:
                    print('{}向聴'.format(handcards.shanten()))
                    handcards.print_jinzhang()
                return True
            else:
                return result
        
    def get_handcards(string):
        # 检查输入是否合法，并读取手牌内容.
        # 若输入不合法，输出错误提示并返回False.
        # 若尚未摸牌，输出None
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
        if num == 13:
            # print('牌数量13张！')
            return None
        if num != 14:
            # print('牌数量错误！手牌数必须为14张！')
            return False
        for tp in 'mpsz':
            for i in set(carddict[tp]):
                if carddict[tp].count(i) > 4:
                    break
            else:
                continue
            # print('牌数量错误！单种牌不得多于4张！')
            break
        else:
            return carddict
        return False
    
except KeyboardInterrupt:
    print("Program end.")
    
class HandCards:
    def __init__(self, carddict):
        self.carddict = carddict
        self.num = sum(len(carddict[tp]) for tp in 'mpsz')
        
    def taatsucount(self):
        # 计算手牌中的面子、搭子、对子数，并返回一个三元元组
        toitsu, taatsu, mentsu = (0, 0, 0)
        carddict_cpy = {
            'm':self.carddict['m'].copy(),
            'p':self.carddict['p'].copy(),
            's':self.carddict['s'].copy(),
            'z':self.carddict['z'].copy()
        }
        # 创建原手牌的拷贝以进行删除操作，防止破坏原手牌
        # 因为一个面子能使向听数-2，选择先计算面子的贪心算法
        # step 1: 顺子
        for tp in 'mps':
            for i in range(1, 8):
                if i in carddict_cpy[tp]:
                    if i + 1 in carddict_cpy[tp] and i + 2 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 1)
                        carddict_cpy[tp].remove(i + 2)
                        mentsu += 1
        # step 2: 刻子
        for tp in 'mpsz':
            for i in range(1, 10):#不存在的89z不影响
                if carddict_cpy[tp].count(i) >= 3:
                    carddict_cpy[tp].remove(i)
                    carddict_cpy[tp].remove(i)
                    carddict_cpy[tp].remove(i)
                    # 4张字牌额外删除1张以便step5的检验
                    if tp == 'z' and carddict_cpy[tp].count(i) == 1:
                        carddict_cpy[tp].remove(i)
                    mentsu += 1
        # step 3: 对子
        toitsu_dict = {'m':[], 'p':[], 's':[]}# 用于解决step3.1的问题
        for tp in 'mps':
            for i in range(1, 10):
                if carddict_cpy[tp].count(i) == 2:
                    carddict_cpy[tp].remove(i)
                    carddict_cpy[tp].remove(i)
                    toitsu_dict[tp].append(i)
                    toitsu += 1
        for i in range(1, 8):
            if carddict_cpy['z'].count(i) == 2:
                carddict_cpy['z'].remove(i)
                carddict_cpy['z'].remove(i)
                toitsu += 1
        # step 3.1: 解决类似2446的问题
        for tp in 'mps':
            for i in toitsu_dict[tp]:
                if toitsu == 0:
                    break
                neighbor = [i - 2, i - 1, i + 1, i + 2]
                if sum(carddict_cpy[tp].count(j) for j in neighbor) >= 2:
                    # 删除其中的两个，改为搭子
                    count = 2
                    for j in neighbor:
                        if count == 0:
                            break
                        if j in carddict_cpy[tp]:
                            carddict_cpy[tp].remove(j)
                            count -= 1
                    toitsu -= 1
                    taatsu += 2
        # step 4: 搭子
        for tp in 'mps':
            for i in range(1, 9):
                if i in carddict_cpy[tp]:
                    if i + 1 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 1)
                        taatsu += 1
                    elif i + 2 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 2)
                        taatsu += 1
        # step 5: 剩余手牌检验
        # 若剩余的手牌均不存在靠张，将其删除
        # 若删除后手牌数+block数小于5（一般为4），则向听数+1
        # 数牌一般不存在完全没有靠张的情况，故只讨论字牌
        # 我们在step2中的操作已经完成了删除无效字牌的操作
        if mentsu + toitsu + taatsu + sum(len(carddict_cpy[tp]) for tp in 'mpsz') < 5:
            taatsu -= 1# 对函数本身而言这会导致搭子数计算错误，但能让向听数计算正确
        return (toitsu, taatsu, mentsu)
    
    def shanten(self):
        # 计算手牌的向听数
        # case 1: 国士无双
        st_kokushi = 13
        if self.num == 14:
            carddict_cpy = {
                'm':self.carddict['m'].copy(),
                'p':self.carddict['p'].copy(),
                's':self.carddict['s'].copy(),
                'z':self.carddict['z'].copy()
            }
            for tp in 'mps':
                if 1 in carddict_cpy[tp]:
                    st_kokushi -= 1
                    carddict_cpy[tp].remove(1)
                if 9 in carddict_cpy[tp]:
                    st_kokushi -= 1
                    carddict_cpy[tp].remove(9)
            for i in range(1,8):
                if i in carddict_cpy['z']:
                    st_kokushi -= 1
                    carddict_cpy['z'].remove(i)
            if carddict_cpy['z']:
                st_kokushi -= 1
            else:
                for tp in 'mps':
                    if 1 in carddict_cpy[tp] or 9 in carddict_cpy[tp]:
                        st_kokushi -= 1
                        break
                    
        # case 2: 七对
        toitsu = 0
        dragon = 0 # 
        if self.num == 14:
            for tp in 'mpsz':
                for i in range(1,10):
                    if i in self.carddict[tp] and self.carddict[tp].count(i) == 4:
                        dragon += 1
                    elif i in self.carddict[tp] and self.carddict[tp].count(i) >= 2:
                        toitsu += 1
                        
        # case 2.1: 塞满了，例如11112222333344z
        if toitsu + 2 * dragon == 7:
            st_chitoi = 2 * dragon - 1
        else:
            st_chitoi = 6 - toitsu - dragon
            
        # case 3: 一般形
        tuple_ = self.taatsucount()
        block = sum(tuple_)
        toitsu, taatsu, mentsu = tuple_
        if toitsu == 0:
            st_ippan = 8 - 2 * mentsu - taatsu + max(0, block - 4)
        else:
            st_ippan = 8 - 2 * mentsu - taatsu - toitsu + max(0, block - 5)

        return min(st_kokushi, st_chitoi, st_ippan)
    
    def jinzhang(self, card_num, card_tp):
        # 计算打某张牌的具体的进张以及进张数
        ret_str = ''
        num = 0
        carddict_cpy = {
            'm':self.carddict['m'].copy(),
            'p':self.carddict['p'].copy(),
            's':self.carddict['s'].copy(),
            'z':self.carddict['z'].copy()
        }
        handcards_cpy = HandCards(carddict_cpy)
        for tp in 'mpsz':
            handcards_cpy.carddict[card_tp].remove(card_num)
            for i in range(1,10):
                if tp == 'z' and i > 7:
                    break
                if self.carddict[tp].count(i) == 4:
                    continue
                handcards_cpy.carddict[tp].append(i)
                handcards_cpy.carddict[tp].sort()
                if handcards_cpy.shanten() < self.shanten():
                    ret_str += str(i)
                    ret_str += tp
                    num += 4 - self.carddict[tp].count(i)
                handcards_cpy.carddict[tp].remove(i)
            handcards_cpy.carddict[card_tp].append(card_num)
        return (ret_str, num)
    
    def print_jinzhang(self):
        strlist = []
        for tp in 'mpsz':
            set_ = set(self.carddict[tp])
            for card_num in set_:
                drawcard, num = self.jinzhang(card_num, tp)
                if num > 0:
                    discard = str(card_num) + tp
                    strlist.append((discard, drawcard, num))
        # 将输出按一定顺序排列
        strlist.sort(key = lambda tuple_: tuple_[0][0])
        strlist.sort(key = lambda tuple_: tuple_[0][1])
        strlist.sort(key = lambda tuple_: tuple_[2], reverse = True)
        for tuple_ in strlist:
            str_ = '打' + tuple_[0] + '共{1}枚 摸{0}'.format(tuple_[1], tuple_[2])
            print(str_)

start()

# References:
# https://blog.csdn.net/qq_30622831/article/details/81638521
# https://blog.csdn.net/c_lanxiaofang/article/details/126412158
# https://zhuanlan.zhihu.com/p/417146130
# https://blog.csdn.net/jndingxin/article/details/124569885
# https://tenhou.net/2/?q=111m234067p88999s
# https://blog.csdn.net/qq_51273457/article/details/113100157 !
# https://github.com/ultralytics/ultralytics
# https://zhuanlan.zhihu.com/p/654306620
# https://blog.csdn.net/m0_37579176/article/details/116950903
# https://blog.csdn.net/zhuisui_woxin/article/details/84400439 !
# https://www.bilibili.com/video/BV1GC4y15736/
# https://www.bilibili.com/video/BV1eX4y1j7ce/
# 2024/3/1
