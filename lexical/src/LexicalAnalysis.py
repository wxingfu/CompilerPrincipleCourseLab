# author：wxingfu,uestc

fIn = open('test.pas', 'r+')
fOut = open('test.dyd', 'w+')
fError = open('testLex.err', 'a+')

# 逐个字符读取，写入列表
symbolList = []
for sym in fIn.read():
    symbolList.append(sym)

# 添加'\0'做文件结束标志
symbolList.append('\0')

# 符号表长度
length = len(symbolList)

# print(symbolList)
# print(len(symbolList))
# for idx in range(len(symbolList)):
#     print(str(idx) + ' ' + symbolList[idx])

# 定义状态
State = {'state_0': 0, 'state_1': 1, 'state_2': 2, 'state_3': 3,
         'state_4': 4, 'state_5': 5, 'state_6': 6, 'state_7': 7,
         'state_8': 8, 'state_9': 9, 'state_10': 10, 'state_11': 11,
         'state_12': 12, 'state_13': 13, 'state_14': 14, 'state_15': 15,
         'state_16': 16, 'state_17': 17, 'state_18': 18, 'state_19': 19,
         'state_20': 20, 'state_21': 21
         }

# 关键字,种别
KeyWords = {'begin': 1, 'end': 2, 'integer': 3, 'if': 4,
            'then': 5, 'else': 6, 'function': 7, 'read': 8, 'write': 9}

# 符号，种别
Symbols = {'=': 12, '<>': 13, '<=': 14, '<': 15, '>=': 16,
           '>': 17, '-': 18, '*': 19, ':=': 20, '(': 21,
           ')': 22, ';': 23}

# 全局变量，用于拼接多个字符
symStr = ''
# 全局变量，初始状态
state = 0
# 全局变量，初始下标
idx = 0
# 全局变量，初始行
line = 1


# 是否是字母
def isLetter(param):
    if ('a' <= param <= 'z') or ('A' <= param <= 'Z'):
        return True
    else:
        return False


# 是否是数字
def isDigit(param):
    if '0' <= param <= '9':
        return True
    else:
        return False


# 输出格式
def outToFile(str1, str2):
    return ' ' * (16 - len(str1)) + str1 + ' ' + str2 + '\n'


# 状态转换，词法分析
def Analysis():
    global state, idx, line, symStr
    while True:
        if idx < length:
            # print(idx)
            symbol = symbolList[idx]
            # 状态0
            if state == State['state_0'] and symbol == ' ':
                # 空格处理
                state = State['state_0']
                idx = idx + 1

            elif state == State['state_0'] and symbol == '\n':
                # 换行处理
                state = State['state_0']
                out = outToFile('ELON', str(24))
                print(out, end='')
                fOut.write(out)
                idx = idx + 1
                line = line + 1

            elif state == State['state_0'] \
                    and symbol == '\0' and symbolList[length - 1] == '\0':
                # 文件末尾处理
                state = State['state_0']
                out = outToFile('EOF', str(25))
                print(out, end='')
                fOut.write(out)
                idx = idx + 1

            elif state == State['state_0'] and isLetter(symbol):
                # 字母处理
                state = State['state_1']

            elif state == State['state_0'] and isDigit(symbol):
                # 数字处理
                state = State['state_3']

            elif state == State['state_0'] and symbol == '=':
                # '='处理
                state = State['state_5']

            elif state == State['state_0'] and symbol == '-':
                # '-'处理
                state = State['state_6']

            elif state == State['state_0'] and symbol == '*':
                # '*'处理
                state = State['state_7']

            elif state == State['state_0'] and symbol == '(':
                # '('处理
                state = State['state_8']

            elif state == State['state_0'] and symbol == ')':
                # ')'处理
                state = State['state_9']

            elif state == State['state_0'] and symbol == '<':
                # '<'处理
                state = State['state_10']
                symStr = '{}{}'.format(symStr, symbol)
                idx = idx + 1

            elif state == State['state_0'] and symbol == '>':
                # '>'处理
                state = State['state_14']
                symStr = '{}{}'.format(symStr, symbol)
                idx = idx + 1

            elif state == State['state_0'] and symbol == ':':
                # ':'处理
                state = State['state_17']
                symStr = '{}{}'.format(symStr, symbol)
                idx = idx + 1

            elif state == State['state_0'] and symbol == ';':
                # ';'处理
                state = State['state_20']

            # 状态1
            elif state == State['state_1'] and (isLetter(symbol) or isDigit(symbol)):
                # 标识符或者关键字拼接
                state = State['state_1']
                symStr = '{}{}'.format(symStr, symbol)
                idx = idx + 1

            elif state == State['state_1'] and (not (isLetter(symbol) or isDigit(symbol))):
                # 不是字母或数字的处理
                state = State['state_2']

            # 状态2
            elif state == State['state_2']:
                # 输出分析出的标识符或关键字，并回到状态0
                state = State['state_0']
                if symStr in KeyWords.keys():
                    # 关键字
                    out = outToFile(symStr, str(KeyWords[symStr]))
                    print(out, end='')
                    fOut.write(out)
                else:
                    # 标识符
                    if len(symStr) <= 16:
                        out = outToFile(symStr, '10')
                        print(out, end='')
                        fOut.write(out)
                    else:
                        error = '***LINE:' + str(line) + '  ' \
                                + symStr + ' length more than 16' + '\n'
                        fError.write(error)
                # 置为空以用于拼接下一单词
                symStr = ''

            # 状态3
            elif state == State['state_3'] and isDigit(symbol):
                # 常数处理
                state = State['state_3']
                symStr = '{}{}'.format(symStr, symbol)
                idx = idx + 1

            elif state == State['state_3'] and (not (isDigit(symbol))):
                # 不是常数处理
                state = State['state_4']

            # 状态4
            elif state == State['state_4']:
                # 输出常数并回到状态0
                state = State['state_0']
                out = outToFile(symStr, '11')
                print(out, end='')
                fOut.write(out)
                symStr = ''

            # 状态5
            elif state == State['state_5']:
                # 输出'='
                state = State['state_0']
                out = outToFile(symbol, str(Symbols[symbol]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态6
            elif state == State['state_6']:
                # 输出'-'
                state = State['state_0']
                out = outToFile(symbol, str(Symbols[symbol]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态7
            elif state == State['state_7']:
                # 输出'*'
                state = State['state_0']
                out = outToFile(symbol, str(Symbols[symbol]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态8
            elif state == State['state_8']:
                # 输出'('
                state = State['state_0']
                out = outToFile(symbol, str(Symbols[symbol]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态9
            elif state == State['state_9']:
                # 输出')'
                state = State['state_0']
                out = outToFile(symbol, str(Symbols[symbol]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态10
            elif state == State['state_10'] and symbol == '=':
                # 拼接'<='
                state = State['state_11']
                symStr = '{}{}'.format(symStr, symbol)

            elif state == State['state_10'] and symbol == '>':
                # 拼接'<>'
                state = State['state_12']
                symStr = '{}{}'.format(symStr, symbol)

            elif state == State['state_10']:
                # 既不是'<='也不是'<>'
                state = State['state_13']

            # 状态11
            elif state == State['state_11']:
                # 输出'<='并回到状态0
                state = State['state_0']
                out = outToFile(symStr, str(Symbols[symStr]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态12
            elif state == State['state_12']:
                # 输出'<>'并回到状态0
                state = State['state_0']
                out = outToFile(symStr, str(Symbols[symStr]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态13
            elif state == State['state_13']:
                # 输出错误信息
                state = State['state_0']
                error = '***LINE:' + str(line) + '  ' + 'Non-existent <' + symbol + '\n'
                fError.write(error)
                idx = idx + 1

            # 状态14
            elif state == State['state_14'] and symbol == '=':
                # 拼接'>='
                state = State['state_15']
                symStr = '{}{}'.format(symStr, symbol)

            elif state == State['state_14']:
                # 不是'>='
                state = State['state_16']

            # 状态15
            elif state == State['state_15']:
                # 输出'>='并返回状态0
                state = State['state_0']
                out = outToFile(symStr, str(Symbols[symStr]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态16
            elif state == State['state_16']:
                # 输出错误信息
                state = State['state_0']
                error = '***LINE:' + str(line) + '  ' + 'Non-existent >' + symbol + '\n'
                fError.write(error)
                idx = idx + 1

            # 状态17
            elif state == State['state_17'] and symbol == '=':
                # 拼接':='
                state = State['state_18']
                symStr = '{}{}'.format(symStr, symbol)

            elif state == State['state_17']:
                # 不是':='
                state = State['state_19']

            # 状态18
            elif state == State['state_18']:
                # 输出':='并返回状态0
                state = State['state_0']
                out = outToFile(symStr, str(Symbols[symStr]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态19
            elif state == State['state_19']:
                # 输出错误信息
                state = State['state_0']
                error = '***LINE:' + str(line) + '  ' + 'Non-existent :' + symbol + '\n'
                fError.write(error)
                idx = idx + 1

            # 状态20
            elif state == State['state_20']:
                state = State['state_0']
                out = outToFile(symbol, str(Symbols[symbol]))
                print(out, end='')
                fOut.write(out)
                symStr = ''
                idx = idx + 1

            # 状态21
            else:
                # state == State['state_21']
                state = State['state_0']
                error = '***LINE:' + str(line) + '  ' + 'Non-existent ' + symbol + '\n'
                fError.write(error)
                idx = idx + 1
        else:
            break


if __name__ == "__main__":
    Analysis()
    fIn.close()
    fOut.close()
    fError.close()
