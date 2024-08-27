import json
import math

# 寄存器編號的字典
num_of_register = {'A': 0, 'X': 1, 'L': 2, 'B': 3,
                   'S': 4, 'T': 5, 'F': 6, 'PC': 8, 'SW': 9}

# 十六進制轉換的字典
HexDict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
           8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

# 十進制轉換的字典
DecDict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
           '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

# 將二進制轉換為十六進制
def Bin2Hex(Bin):
    Hex = ''
    if (len(Bin) > 4):
        #如果二進制字符串的長度大於4
        fill = (4 - (len(Bin) % 4))
        #進行補0操作，確保每個4位二進制都有對應的十六進制數字。
        if (fill == 4):
            fill = (fill - 4)
        #二進制字符串長度剛好是4的倍數，則將 fill 減4，以確保不添加額外的0。

        Bin = ('0'*fill + Bin)
        #將計算出的 fill 個 0 添加到二進制字符串的前面，進行補充操作。
        for i in range(0, len(Bin), 4):#補充後的二進制字符串，每次取4位一組。
            Hex += Bin2Hex(Bin[i:(i*4+4)])#補充後的二進制字符串，每次取4位一組。
    else:#如果二進制字符串的長度不大於4
        Dec = 0#初始化一個變量 Dec 用於存儲十進制的結果
        for i, digit in enumerate(Bin):#遍歷二進制字符串中的每一位
            Dec += (int(digit) * math.pow(2, (3-i)))
            #將每一位二進制數字轉換為十進制，並根據位置計算其值，然後加到 Dec 中。
        Hex = Dec2Hex(Dec)#將十進制結果轉換為十六進制

    return Hex

# 將十進制轉換為十六進制
def Dec2Hex(Dec: int):
    Hex = ''
    while (Dec >= 16):#十進制數字 Dec 大於等於16
        Hex = (HexDict[Dec % 16] + Hex)
        #將十進制數字 Dec 除以16的餘數轉換為對應的十六進制數字，並將其附加到 Hex 的前面
        Dec //= 16#Dec 為其除以16的商

    Hex = (HexDict[Dec] + Hex)
    #處理最後一位十六進制數字，將其轉換為對應的十六進制字符，並附加到 Hex 的前面
    return Hex

# 將十六進制轉換為十進制
def Hex2Dec(Hex: str):
    Dec = 0
    times = 0 #初始化一個變數 times 用於跟蹤每一位十六進制字符的位置
    while (len(Hex) > 0):#十六進制字符串 Hex 的長度大於0。
        Dec += int(DecDict[Hex[-1]] * math.pow(16, times))
        #將最後一位十六進制字符轉換為對應的十進制數字，乘以16的次方（根據位置），並加到 Dec 上
        Hex = Hex[:-1]
        #去掉十六進制字符串的最後一位
        times += 1

    return Dec

# 處理BYTE指令
def BYTE(parms):
    #將參數（'C' 或 'X'）轉換為對應的目標碼
    mode = parms[0]#提取 parms 中的第一個字符，表示 BYTE 指令的模式
    data = parms[2:-1]#去除前兩個字符和最後一個字符
    objCode = '' #初始化一個空字符串 objCode 來存儲最終的目標碼
    if (mode == 'C'):#要處理字符數據
        for i in data:#迴圈跑data中的每個字符
            objCode += (Dec2Hex(ord(i))).zfill(2)
    #將每個字符的 ASCII 值轉換為十六進制，然後補0成為兩位，並添加到 objCode 中
    elif (mode == 'X'):#要處理十六進制數據
        objCode += data #直接將 data 添加到 objCode 中
    else:
        print('BYTE Error')

    location_add = (len(objCode)//2)
    #計算目標碼的長度，即字節數，並將其除以2。
    return location_add, objCode

# 處理WORD指令
def WORD(parms):#接受一個字符串 parms 作為輸入。
    if (int(parms) >= 0):
    #轉換為整數後大於等於0，處理非負整數    
        objCode = Dec2Hex(int(parms)).zfill(6)
 #並將parms 轉換為十進制整數，然後轉換為六位的十六進制，並使用 zfill 函數填充0。
    
    else:#轉換為整數後小於0，表示處理負整數
        full_hex = Hex2Dec('1000000')#：將十六進制數字 '1000000' 轉換為十進制
        objCode = Dec2Hex(full_hex + int(parms)).zfill(6)
        #轉換為六位的十六進制，並使用 zfill 函數填充0。
    location_add = (len(objCode)//2)
    #計算目標碼的長度，即字節數，並將其除以2。
    return location_add, objCode

# 處理RESB指令
def RESB(parms):#接受一個字符串 parms 作為輸入。
    objCode = ' '
    #始化一個空格字符串 objCode，因為 RESB 指令通常不產生實際的目標碼。
    location_add = int(parms)#將參數 parms 轉換為整數
    return location_add, objCode

# 處理RESW指令
def RESW(parms):
    objCode = ' '
    #初始化一個空格字符串 objCode，因RESW指令通常不產生實際的目標碼。
    location_add = (int(parms) * 3)
    #表示需要保留的字數。由於每個字有3個字節，所以將字數乘以3得到需要保留的總字節數
    return location_add, objCode

# 定義寄存器類別
class Register():
    A = False
    X = False
    L = False
    B = False
    S = False
    T = False
    F = False
    PC = False
    SW = False

    # 載入數值到寄存器
    def Load(self, instrucet, parms):
        #parms：指令的參數，即欲載入的數值
        if (instrucet == 'LDA'):
            self.A = parms
        elif (instrucet == 'LDX'):
            self.X = parms
        elif (instrucet == 'LDL'):
            self.L = parms
        elif (instrucet == 'LDB'):
            self.B = parms
        elif (instrucet == 'LDS'):
            self.S = parms
        elif (instrucet == 'LDT'):
            self.T = parms
        elif (instrucet == 'LDF'):
            self.F = parms
    #根據指令名稱，將相應的數值載入到對應的寄存器（A、X、L、B、S、T、F）

    # 清除寄存器數值
    def Clear(self, parms):
        #parms：要清除數值的寄存器名稱，例如 'A'、'X' 等
        if (parms == 'A'):
            self.A = 0
        elif (parms == 'X'):
            self.X = 0
        elif (parms == 'L'):
            self.L = 0
        elif (parms == 'B'):
            self.B = 0
        elif (parms == 'S'):
            self.S = 0
        elif (parms == 'T'):
            self.T = 0
        elif (parms == 'F'):
            self.F = 0
        elif (parms == 'PC'):
            self.PC = 0
        elif (parms == 'SW'):
            self.SW = 0
        #根據寄存器名稱，將對應寄存器的數值設為0

    # 取得寄存器位置
    def Location_of_rigster(self):
        if self.A:
            self.A = self.Parms_computing(self.A)
        #如果 A 寄存器 self.A 的值為真（非零），
        #則使用 Parms_computing 方法計算新的 A 寄存器的數值，然後將其賦值給 self.A"""
        elif self.X:
            self.X = self.Parms_computing(self.X)
        elif self.L:
            self.L = self.Parms_computing(self.L)
        elif self.B:
            self.B = self.Parms_computing(self.B)
        elif self.S:
            self.S = self.Parms_computing(self.S)
        elif self.T:
            self.T = self.Parms_computing(self.T)
        elif self.F:
            self.F = self.Parms_computing(self.F)

    # 計算寄存器數值
    def Parms_computing(self, parms):
        if (parms[0] == '#'):#如果 parms 的第一個字符是 '#'，則將其去掉並返回
            parms = parms[1:]
            return function_[parms]

# 創建寄存器物件
register = Register()

# 讀取輸入檔案
f = open('./Input.txt', 'r')
Input = f.readlines()
f.close()

# 讀取SIC/XE指令集
with open('./instrucetion_SICXE.json', 'r', encoding='utf-8') as j:
#open函式打開病毒取一個名為 instrucetion_SICXE.json 的檔案    
    instrucetion = json.load(j)
    #用來載入 JSON 格式的數據

# 存放函式的字典
function_ = {}

# 解析第一行輸入
temp = Input[0].replace('\n', '').split(' ')
#將 Input 列表中輸入文件的第一行去掉換行符號，然後使用空格分割，存儲為 temp 列表。
if (len(temp) == 3):#如果長度為三，意謂為正確指令格式
    information = [[5, temp[2].zfill(4), temp[0], temp[1], temp[2], ' ']]
    """初始化 information 列表。包含一個子列表，子列表的元素是行號、位置、操作碼、操作數1、操作數2和目標碼。
    temp[2].zfill(4) 的作用是將 temp[2] （通常是操作碼）轉換為4位數的字串，不足的地方使用0填充。
    最後的 ' ' 是目標碼的初始值，表示它還沒有被計算出來。"""
    function_[temp[0]] = Hex2Dec(information[0][4])
    #information[0][4]（目標碼）的十進制表示作為值存儲在 function_ 字典中
else:
    information = [[5, temp[2].zfill(4), '', temp[0], temp[1], ' ']]
    #初始化 information 列表，但將 temp[2].zfill(4) 替換為空字符串，表示目標碼的初始值為空

# 初始化行數與位置
line = 10
location = Hex2Dec(information[0][4])
#它設為 information 列表中第一個指令的目標碼的十進制表示

# 解析其他行輸入
for i in Input[1:]:#跑Input 列表的所有元素，從第二行開始
    line += 5 #

    if (i[0] == '.'): #如果行的第一個字符是點（.），表示這是一條註釋
        information.append([line, '', '.', i.replace(
            '.', '').replace('\n', ''), '', ' '])
        #將相應的信息添加到 information 列表
        continue

    i = i.replace('\n', '').split(' ')
    #去除換行符號，然後使用空格分割行。這樣將行分割為單個單詞，存儲在 i 中

    if (len(i) == 1):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], '', ''])
        #i 的長度為 1，表示只有操作碼，並記錄於information。
    elif (len(i) == 2):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], i[1], ''])
        #i 的長度為 2，表示有操作碼和一個操作數，並記錄於information。
    elif (len(i) == 3):
        information.append(
            [line, Dec2Hex(location).zfill(4), i[0], i[1], i[2], ''])
        #表示有操作碼和兩個操作數，將相應的信息添加到 information
        function_[i[0]] = Dec2Hex(location).zfill(4)

    if (information[-1][3][0] == '+'):
        location += 4
        #如果最後一條指令的操作碼的第一個字符是 '+'，表示這是格式四，增加位置 location 的值 4
    elif (information[-1][3] not in instrucetion['pseudo']):
        location += int(instrucetion['instrucetion'][information[-1][3]][1])
        #最後一條指令的助記碼不在 SIC/XE 擴充集的擬指令中，表示這是一條正常的指令。根據指令的格式，增加位置 location的值。
        if (information[-1][3] == 'CLEAR'):
            register.Clear(information[-1][4])
            #調用 register.Clear(information[-1][4]) 方法，將指定寄存器的值清零。
    else:
        if (information[-1][3] == 'BYTE'):
            location_add, objectCode = BYTE(information[-1][4])
            #調用 BYTE 函數處理，獲取 location_add 和 objectCode
        elif (information[-1][3] == 'RESB'):
            location_add, objectCode = RESB(information[-1][4])
            #調用 RESB 函數處理
        elif (information[-1][3] == 'RESW'):
            location_add, objectCode = RESW(information[-1][4])
            #調用 RESW 函數處理
        elif (information[-1][3] == 'WORD'):
            location_add, objectCode = WORD(information[-1][4])
            #調用 WORD 函數處理
        elif (information[-1][3] == 'BASE'):
            register.Load(information[-2][3], information[-2][4])
            information[-1][1] = ''
            information[-1][5] = ' '
            continue
        #調用 register.Load 方法，將指定寄存器的值設置為上一條指令的操作數。
        #然後，將最後一條指令的位置 information[-1][1] 和目標碼 information[-1][5] 設置為空，並跳過下一輪迴圈。
        elif (information[-1][3] == 'END'):
            information[-1][1] = ''
            objectCode = ' '
        #information[-1][1] 設置為空，並將目標碼 objectCode 設置為空字符串。

        location += location_add#將位置 location 增加上一條指令的地址增量
        information[-1][-1] = objectCode
        #將最後一條指令的目標碼 objectCode 賦值給 information[-1][-1]
        """一條指令被處理完畢後，位置計數器需要更新，以便指向下一條指令的存放位置。
        指令的地址增量（location_add）就是這一條指令佔用的記憶體空間大小。
        通常，每條指令都有固定的大小，因此 location_add 就是該指令的大小。"""

# 計算寄存器位置
register.Location_of_rigster()
"""檢查每一個寄存器（A、X、L、B、S、T、F）檢查是否為非零。如果某個寄存器包含值，就調用 Parms_computing 
方法對該值進行計算。對 Parms_computing 的調用是對帶有 '#' 前綴的數值進行處理。"""

# 解析指令並生成目標碼
for now_index, infor in enumerate(information):
#跑information 列表的循環，現在是now_index
    infor = infor.copy()
#對 infor 進行了一次複製。這是為了防止修改 infor 的內容對原始列表的元素產生影響。
#在循環內的後續代碼中，可以對 infor 進行修改而不影響原始列表中對應位置的元素。
    next_index = now_index
#next_index 初始化為 now_index。用於跟蹤下一條非空指令的索引

    if infor[5] == '':#為空，表示該行指令的目標機器碼還未生成。
        if (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '2'):
            #檢查指令的格式是否為2。
            infor[4] = infor[4].split(',')#按逗號分割
            if (len(infor[4]) == 2):#如果操作數分割後的長度為2，表示指令有兩個寄存器操作數。
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}{num_of_register[infor[4][1]]}'
            #根據指令的機器碼格式，將兩個寄存器的編號轉換為目標機器碼。
            else:
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}0'
                #如果操作數只有一個，則生成相應的目標機器碼

        elif (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '3'):
            #檢查指令的格式是否為3
            if (infor[3] == 'RSUB'):#如果指令是RSUB
                information[now_index][5] = '4F0000'
            #直接將目標機器碼設為'4F0000'
                continue

            next_index += 1#將 next_index 增加1，跳過註解行
            while information[next_index][1] == '':
                #略過可能的註解行，確保找到下一個非註解的行。
                next_index += 1

            register.PC = information[next_index][1]
            #設定程式計數器 PC 的值為下一條指令的地址。

            """以下是nixbpe的換算"""

            if (infor[4][0] == '@'):
                infor[4] = infor[4][1:]
                n, i = 1, 0
            #指令的位址部分以 '@' 開頭，表示使用間接位址，將 n 設為1，i 設為0。
            elif (infor[4][0] == '#'):
                infor[4] = infor[4][1:]
                n, i = 0, 1
            #指令的位址部分以 '#' 開頭，表示使用即時位址，將 n 設為0，i 設為1
            else:
                n, i = 1, 1
            #以上條件都不滿足，表示使用直接位址，將 n 設為1，i 設為1

            if ',X' in infor[4]:
                infor[4] = infor[4].replace(',X', '')
                x = 1
            #位址部分包含 ',X'，表示使用相對位址，將 x 設為1，否則設為0。
            else:
                x = 0

            if (infor[3][0] == '+'):
                infor[3] = infor[3][1:]
                e = 1
            #指令以 '+' 開頭，表示使用擴展格式，將 e 設為1，否則設為0。
            else:
                e = 0

            opcode = f'{instrucetion["instrucetion"][infor[3]][0]}0'
            #根據指令的操作碼，生成操作碼部分的機器碼，並附加 '0'

            #這一部分的程式碼處理了擴展格式指令（e 為 1）的情況
            b, p = 0, 0
            if e:#e 為 1 表示使用相對位址
                if (not n and i and (infor[4].isdigit())):
                #判斷確保了相對位址（n 為 0，i 為 1），並且地址部分是數字
                    address = Dec2Hex(int(infor[4])).zfill(5)
                #即時相對位址，將地址部分（即數字）轉換為十六進制，然後填充為 5 位。
                else: #地址部分不是即時數值，那麼它可能是一個符號，需要透過 function_ 字典查找其對應的值。
                    address = function_[infor[4]].zfill(5)#找到符號對應的值，同樣填充為 5 位

                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{address}'
                #將上述計算得到的地址部分和其他標誌組合成最終的碼。
            
            else:#檢查是否為即時位址（Immediate Addressing），同時檢查地址部分是否為數字
                if (not n and i and (infor[4].isdigit())):                    
                #檢查 n 是否為 False，即檢查是否使用直接位址（Immediate Addressing）。n 是指令格式中的 n 位元，當 n 為 0 時表示使用直接位址
                #檢查 i 是否為 True，即檢查是否使用即時位址（Immediate Addressing）。i 是指令格式中的 i 位元，當 i 為 1 時表示使用即時位址
                #最後檢查 infor[4] 是否為數字。infor[4] 包含指令的地址部分。
                    disp = Dec2Hex(int(infor[4])).zfill(3)
                #將 infor[4] 轉換為整數後，將整數轉換為十六進制,當字符串的位數不足3位，則在左側使用零進行填充。
                else:#處理非即時位址（e 為 0）的情況
                    disp = (
                        Hex2Dec(function_[infor[4]]) - Hex2Dec(register.PC))
                    #相對於 register.PC 的位址偏移 disp。它使用了指令中的目標地址 function_[infor[4]] 減去當前的 register.PC
                    if x:
                        disp -= register.X
                    #檢查指令中是否有索引位（X），將 register.X 的值減去 disp，對應的內存位置需要加上位移
                    if ((disp >= 4096) or ((disp <= -4096))):#檢查 disp 是否大於等於 4096 或小於等於 -4096
                        b, p = 1, 0
                        disp = (
                            Hex2Dec(function_[infor[4]]) - Hex2Dec(register.B))
                    #disp 的計算涉及將 function_[infor[4]] 的十六進制地址轉換為十進制，然後減去 register.B 的地址
                        if x:
                            disp -= register.X
                    
                    ##檢查指令中是否有索引位（X），將 register.X 的值減去 disp，對應的內存位置需要加上位移
                    else:
                        b, p = 0, 1
                    '''表示可以使用 PC 相對位址或絕對位址。此時，b 被設為0，p 被設為1
                    如果 disp 為負數，將其轉換為正數形式，並且不超過3位十六進制'''

                    if (disp < 0):
                        disp = Dec2Hex(disp + Hex2Dec('1000')).zfill(3)
                    else:
                        disp = Dec2Hex(disp).zfill(3)

                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{disp[-3:]}'
                '''計算指令的前三個十六進制數字。它將 opcode 與一些標誌（n、i、x、b、p、e）的二進制值相加，
                然後將其轉換為十六進制，並使用 zfill(3) 確保結果是三位數'''
                #disp[-3:]: 該部分取 disp 的最後三個字符。由於前面已經確保了 disp 是三位的十六進制數字
# 輸出結果
print(" %-10s %-10s %-10s %-10s %-10s %-17s" %
      ('Line', 'Location', '', 'Original', '', 'Object code'))
#%-10s: 這表示一個長度為 10 的左對齊的字串欄位
for i in information:
    if (i[2] == '.'):
        print(" %-10s %-10s %-10s %-39s" % (i[0], i[1], i[2], i[3]))
    else:
        print(" %-10s %-10s %-10s %-10s %-10s %-17s" %
              (i[0], i[1], i[2], i[3], i[4], i[5]))
#一行的第三個元素 i[2] 是點（'.'），表示這是一個註解，那麼只印出前四個元素；否則，印出所有六個元素