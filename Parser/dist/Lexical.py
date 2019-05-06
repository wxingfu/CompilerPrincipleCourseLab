"""
报告截止时间：十五周周五之前
可以修改源文件，体现出错处理
"""

fPas = open('test.pas', 'r+')
fDyd = open('test.dyd', 'w+')
fLexErr = open('testLex.err', 'a+')

charList = [char for char in fPas.read()]
charList.append('\0')
size = len(charList)
# print(charList)

State = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
         10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

KeyWords = {'begin': 1, 'end': 2, 'integer': 3, 'if': 4,
            'then': 5, 'else': 6, 'function': 7, 'read': 8, 'write': 9}

Operator = {'=': 12, '<>': 13, '<=': 14, '<': 15, '>=': 16,
            '>': 17, '-': 18, '*': 19, ':=': 20, '(': 21, ')': 22, ';': 23}

# 记录二元式以及行
output = []
# 记录错误以及行
outLexErr = []
# 全局变量，用于拼接多个字符
tmp_str = ''
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


# 状态转换，词法分析
def Analysis():
    global state, idx, line, tmp_str
    while True:
        if idx < size:
            char = charList[idx]
            # 状态0
            if state == State[0] and char == ' ':
                # 空格处理
                state = State[0]
                idx = idx + 1

            elif state == State[0] and char == '\n':
                # 换行处理
                state = State[0]
                output.append(('ELON', 24, line))
                idx = idx + 1
                line = line + 1

            elif state == State[0] \
                    and char == '\0' \
                    and charList[size - 1] == '\0':
                # 文件末尾处理
                state = State[0]
                output.append(('EOF', 25, line))
                idx = idx + 1

            elif state == State[0] and isLetter(char):
                # 字母处理
                state = State[1]

            elif state == State[0] and isDigit(char):
                # 数字处理
                state = State[3]

            elif state == State[0] and char == '=':
                # '='处理
                state = State[5]

            elif state == State[0] and char == '-':
                # '-'处理
                state = State[6]

            elif state == State[0] and char == '*':
                # '*'处理
                state = State[7]

            elif state == State[0] and char == '(':
                # '('处理
                state = State[8]

            elif state == State[0] and char == ')':
                # ')'处理
                state = State[9]

            elif state == State[0] and char == '<':
                # '<'处理
                state = State[10]
                tmp_str = '{}{}'.format(tmp_str, char)
                idx = idx + 1

            elif state == State[0] and char == '>':
                # '>'处理
                state = State[14]
                tmp_str = '{}{}'.format(tmp_str, char)
                idx = idx + 1

            elif state == State[0] and char == ':':
                # ':'处理
                state = State[17]
                tmp_str = '{}{}'.format(tmp_str, char)
                idx = idx + 1

            elif state == State[0] and char == ';':
                # ';'处理
                state = State[20]

            # 状态1
            elif state == State[1] \
                    and (isLetter(char) or isDigit(char)):
                # 标识符或者关键字拼接
                state = State[1]
                tmp_str = '{}{}'.format(tmp_str, char)
                idx = idx + 1

            elif state == State[1] \
                    and (not (isLetter(char) or isDigit(char))):
                # 不是字母或数字的处理
                state = State[2]

            # 状态2
            elif state == State[2]:
                # 输出分析出的标识符或关键字，并回到状态0
                state = State[0]
                if tmp_str in KeyWords.keys():
                    # 关键字
                    output.append((tmp_str, KeyWords[tmp_str], line))
                else:
                    # 标识符
                    if len(tmp_str) <= 16:
                        output.append((tmp_str, 10, line))
                    else:
                        outLexErr.append((line, tmp_str + 'length more than 16'))
                # 置为空以用于拼接下一单词
                tmp_str = ''

            # 状态3
            elif state == State[3] and isDigit(char):
                # 常数处理
                state = State[3]
                tmp_str = '{}{}'.format(tmp_str, char)
                idx = idx + 1

            elif state == State[3] and (not (isDigit(char))):
                # 不是常数处理
                state = State[4]

            # 状态4
            elif state == State[4]:
                # 输出常数并回到状态0
                state = State[0]
                output.append((tmp_str, 11, line))
                tmp_str = ''

            # 状态5
            elif state == State[5]:
                # 输出'='
                state = State[0]
                output.append((char, Operator[char], line))
                tmp_str = ''
                idx = idx + 1

            # 状态6
            elif state == State[6]:
                # 输出'-'
                state = State[0]
                output.append((char, Operator[char], line))
                tmp_str = ''
                idx = idx + 1

            # 状态7
            elif state == State[7]:
                # 输出'*'
                state = State[0]
                output.append((char, Operator[char], line))
                tmp_str = ''
                idx = idx + 1

            # 状态8
            elif state == State[8]:
                # 输出'('
                state = State[0]
                output.append((char, Operator[char], line))
                tmp_str = ''
                idx = idx + 1

            # 状态9
            elif state == State[9]:
                # 输出')'
                state = State[0]
                output.append((char, Operator[char], line))
                tmp_str = ''
                idx = idx + 1

            # 状态10
            elif state == State[10] and char == '=':
                # 拼接'<='
                state = State[11]
                tmp_str = '{}{}'.format(tmp_str, char)

            elif state == State[10] and char == '>':
                # 拼接'<>'
                state = State[12]
                tmp_str = '{}{}'.format(tmp_str, char)

            elif state == State[10]:
                # 既不是'<='也不是'<>'
                state = State[13]

            # 状态11
            elif state == State[11]:
                # 输出'<='并回到状态0
                state = State[0]
                output.append((tmp_str, Operator[tmp_str], line))
                tmp_str = ''
                idx = idx + 1

            # 状态12
            elif state == State[12]:
                # 输出'<>'并回到状态0
                state = State[0]
                output.append((tmp_str, Operator[tmp_str], line))
                tmp_str = ''
                idx = idx + 1

            # 状态13
            elif state == State[13]:
                # 输出错误信息
                state = State[0]
                outLexErr.append((line, 'Non-existent <' + char))
                idx = idx + 1

            # 状态14
            elif state == State[14] and char == '=':
                # 拼接'>='
                state = State[15]
                tmp_str = '{}{}'.format(tmp_str, char)

            elif state == State[14]:
                # 不是'>='
                state = State[16]

            # 状态15
            elif state == State[15]:
                # 输出'>='并返回状态0
                state = State[0]
                output.append((tmp_str, Operator[tmp_str], line))
                tmp_str = ''
                idx = idx + 1

            # 状态16
            elif state == State[16]:
                # 输出错误信息
                state = State[0]
                outLexErr.append((line, 'Non-existent >' + char))
                idx = idx + 1

            # 状态17
            elif state == State[17] and char == '=':
                # 拼接':='
                state = State[18]
                tmp_str = '{}{}'.format(tmp_str, char)

            elif state == State[17]:
                # 不是':='
                state = State[19]

            # 状态18
            elif state == State[18]:
                # 输出':='并返回状态0
                state = State[0]
                output.append((tmp_str, Operator[tmp_str], line))
                tmp_str = ''
                idx = idx + 1

            # 状态19
            elif state == State[19]:
                # 输出错误信息
                state = State[0]
                outLexErr.append((line, ': match error ' + char))
                idx = idx + 1

            # 状态20
            elif state == State[20]:
                state = State[0]
                output.append((char, Operator[char], line))
                tmp_str = ''
                idx = idx + 1

            # 状态21
            else:
                # state == State[21]
                state = State[0]
                outLexErr.append((line, 'Non-existent ' + char))
                idx = idx + 1
        else:
            break


# 二元式输出
def outDyd():
    for i in range(len(output)):
        out = ' ' * (16 - len(output[i][0])) \
              + output[i][0] + ' ' + str(output[i][1]) + '\n'
        fDyd.write(out)


def outLexicalErr():
    for i in range(len(outLexErr)):
        error = '***LINE:' + str(outLexErr[i][0]) + '  ' + outLexErr[i][1] + '\n'
        fLexErr.write(error)


def LexicalMain():
    Analysis()
    print('词法分析完成...')
    outDyd()
    print('输出二元式...')
    outLexicalErr()
    print('输出词法分析错误信息...')
    # print(output)
    fPas.close()
    fDyd.close()
    fLexErr.close()


# 测试
if __name__ == "__main__":
    LexicalMain()
