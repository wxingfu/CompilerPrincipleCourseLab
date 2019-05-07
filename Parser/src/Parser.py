# author：wxingfu,uestc

# from complier.parser import Lexical as Lex
import imp

Lex = imp.load_source('LexicalMain', 'Lexical.py')

# 各个文件
fDys = open('test.dys', 'w+')
fPro = open('test.pro', 'w+')
fVar = open('test.var', 'w+')
fParserErr = open('testParser.err', 'a+')
# 关键字
Keys = Lex.KeyWords
# 操作符
Op = Lex.Operator
# 标识符、常数、换行和结尾的种别
spCode = {'id': 10, 'const': 11, 'EOLN': 24, 'EOF': 25}
# 关系运算符
RelationOp = {'=': 12, '<>': 13, '<=': 14, '<': 15, '>=': 16, '>': 17}
# 变量类型
VarKind = {'param': 0, 'var': 1}
# 变量名列表
VarList = []
# 过程名表
ProcList = []
# 层次
level = 0
# 行数
line = 1
# VarList下标
idx = 0
# 参数偏移量(相对于第一个)
offset1 = 0
# 变量偏移量(相对于第一个)
offset2 = 0
# 符号，初始为空
sym = ''
# 符号种别，初始为0，即不存在
sym_type = 0
# 初始过程名
procName = 'M'
# 表示变量用途，定义或使用
varDefOrUse = {'def': 0, 'use': 1}
# 变量定义表,用于判断变量是否定义
varDefList = []


# 更新当前符号
def advance():
    global sym, line, idx, sym_type
    # 不是文件结尾则继续
    if Lex.output[idx][0] != spCode['EOF']:
        sym = Lex.output[idx][0]
        sym_type = Lex.output[idx][1]
        line = Lex.output[idx][2]
        # 打印分析的符号
        print(idx, sym, sym_type, line)
        idx += 1


# 保持当前符号
def back(n):
    global idx
    idx -= n
    advance()


# 错误输出
def error(line_num, err):
    er = '***LINE:' + str(line_num) + ' ' * 2 + err + '\n'
    print(er)
    fParserErr.write(er)


# 查重
def checkVar(name, proc, kind):
    size = len(VarList)
    # 变量表为空可直接添加
    if size == 0:
        return True
    # 标识符的名称、所属过程和种类都相同则不添加
    for i in range(size):
        if name == VarList[i][0] and proc == VarList[i][1] \
                and kind == VarList[i][2]:
            return False
    return True


# 添加变量或参数
def addVar(def_use, v_name, v_proc, v_kind):
    global offset1, offset2
    # 参数
    if v_kind == 0:
        if checkVar(v_name, v_proc, v_kind):
            # 添加参数
            VarList.append((v_name, v_proc, VarKind['param'], 'unknown', level, offset1))
            offset1 += 1
        else:
            error(line, 'repeat defined ' + v_name)
    # 变量
    if v_kind == 1:
        # 是否是定义
        if def_use == varDefOrUse['def']:
            varDefList.append(v_name)
            # 查重
            if checkVar(v_name, v_proc, v_kind):
                # 添加变量
                VarList.append((v_name, v_proc, VarKind['var'], 'integer', level, offset2))
                offset2 += 1
            else:
                error(line, 'repeat defined ' + v_name)
        # 是否在变量定义表里
        elif v_name not in varDefList:
            error(line, 'Undefined ' + v_name)


def isProc(name):
    tmp_name = []
    for i in range(len(ProcList)):
        # 取出过程名
        tmp_name.append(ProcList[i][0])
    # 检查是否为过程名
    if name in tmp_name:
        return True
    return False


# 过程名查重
def checkProc(name):
    size = len(ProcList)
    # 过程表为空可直接添加
    if size == 0:
        return True
    # 过程表中存在则不添加
    for i in range(size):
        if name == ProcList[i][0]:
            return False
    return True


# 添加过程名
def addProc(p_name):
    # 去重
    if checkProc(p_name):
        # 添加过程
        ProcList.append((p_name, 'integer', level))


# <程序>→begin <说明语句表>;<执行语句表> end
# <Program>→begin <DeclareStmTable>;<ExecStmTable> end
def Program():
    global sym_type, line, level
    # 添加初始过程名
    addProc(procName)
    # 层级加1
    level += 1
    if sym_type == Keys['begin']:
        advance()
        DeclareStmTable()
        if sym_type == Op[';']:
            advance()
            ExecStmTable()
            if sym_type == Keys['end']:
                advance()
                level -= 1
                return
            else:
                error(line, 'missing \'end\'')
        else:
            error(line, 'missing \';\'')
    else:
        error(line, 'it is not a program')


# <说明语句表>→<说明语句><说明语句表tmp>
# <DeclareStmTable>→<DeclareStatement><DeclareStmTableTmp>
def DeclareStmTable():
    DeclareStatement()
    DeclareStmTableTmp()


# <说明语句表tmp>→;<说明语句><说明语句表tmp>│<空>
# <DeclareStmTableTmp>→;<DeclareStatement><DeclareStmTableTmp>|ε
def DeclareStmTableTmp():
    global sym_type, line
    if sym_type == Op[';']:
        advance()
        DeclareStatement()
        DeclareStmTableTmp()

    # elif sym_type == Keys['if']:
    #    # ';'后为'if'则保持为';'
    #    back(2)

    else:
        # 保持当前符号
        back(2)


# <说明语句>→integer <标识符>│integer function <标识符> (<标识符>) ;<函数体>
# <DeclareStatement>→integer <Var>|integer function <Identifier>(<Var>);<Function>
def DeclareStatement():
    global sym_type, line
    if sym_type == Keys['integer']:
        advance()
        if sym_type == Keys['function']:
            FuncDeclaration()
        else:
            Var(varDefOrUse['def'], sym, VarKind['var'])


# <变量>→<字母>│<标识符><字母>│<标识符><数字>
# <Var>→<Letter>|<Identifier><Letter>|<Identifier><Digit>
def Var(def_use, var_name, kind):
    global procName
    addVar(def_use, var_name, procName, kind)
    advance()


# <函数说明>→integer function <标识符> (<变量>) ;<函数体>
# <FuncDeclaration>→integer function <Identifier>(<Var>);<Function>
def FuncDeclaration():
    global sym_type, line, level, procName
    level += 1
    tmp_proc_name = procName
    if sym_type == Keys['function']:
        advance()
        if sym_type == spCode['id']:
            procName = sym
            addProc(procName)
            advance()
            if sym_type == Op['(']:
                advance()
                Var(varDefOrUse['use'], sym, VarKind['param'])
                if sym_type == Op[')']:
                    advance()
                    if sym_type == Op[';']:
                        advance()
                        Function()
                        procName = tmp_proc_name
                        level -= 1
                    else:
                        error(line, 'missing \';\'')
                else:
                    error(line, 'missing \')\'')
            else:
                error(line, 'missing \'(\'')
        else:
            error(line, 'not an identifier')
    else:
        error(line, 'error define function')


# <函数体>→begin <说明语句表>;<执行语句表> end
# <Function>→begin <DeclareStmTable>;<ExecStmTable> end
def Function():
    global sym_type, line, level
    if sym_type == Keys['begin']:
        advance()
        DeclareStmTable()
        if sym_type == Op[';']:
            advance()
            ExecStmTable()
            if sym_type == Keys['end']:
                advance()
            else:
                error(line, 'missing \'end\'')
        else:
            error(line, 'missing \';\'')
    else:
        error(line, 'function error')


# <执行语句表>→<执行语句><执行语句表tmp>
# <ExecStmTable>→<ExecStatement><ExecStmTableTmp>
def ExecStmTable():
    ExecStatement()
    ExecStmTableTmp()


# <执行语句表tmp>→;<执行语句><执行语句表tmp>│<空>
# <ExecStmTableTmp>→;<ExecStatement><ExecStmTableTmp>|ε
def ExecStmTableTmp():
    global sym, line
    if sym == ';':
        advance()
        ExecStatement()
        ExecStmTableTmp()


# <执行语句>→read(<标识符>)│write(<标识符>)│<赋值语句>│if <条件表达式> then <执行语句> else <执行语句>
# <ExecStatement>→read(<Var>)|write(<Var>)|<AssignStatement>|<ConditionStatement>
def ExecStatement():
    global sym, sym_type, line
    if sym_type == Keys['read']:
        advance()
        if sym_type == Op['(']:
            advance()
            Var(varDefOrUse['use'], sym, VarKind['var'])
            if sym_type == Op[')']:
                advance()
            else:
                error(line, 'missing \')\'')
        else:
            error(line, 'missing \'(\'')

    elif sym_type == Keys['write']:
        advance()
        if sym_type == Op['(']:
            advance()
            Var(varDefOrUse['use'], sym, VarKind['var'])
            if sym_type == Op[')']:
                advance()
            else:
                error(line, 'missing \')\'')
        else:
            error(line, 'missing \'(\'')

    elif sym_type == Keys['if']:
        ConditionStatement()

    else:
        AssignStatement()


# <赋值语句>→<变量>:=<算术表达式>
# <AssignStatement>→<Var>:=<ArithmeticExpression>
def AssignStatement():
    global sym, sym_type, line
    Var(varDefOrUse['use'], sym, VarKind['var'])
    if sym_type == Op[':=']:
        advance()
        ArithmeticExpression()


# <算术表达式>→<项><算术表达式tmp>
# <ArithmeticExpression>→<Item><ArithmeticExpressionTmp>
def ArithmeticExpression():
    Item()
    ArithmeticExpressionTmp()


# <算术表达式tmp> → - <项><算术表达式tmp> │<空>
# <ArithmeticExpressionTmp>→-<Item><ArithmeticExpressionTmp>|ε
def ArithmeticExpressionTmp():
    global sym, line
    if sym == '-':
        advance()
        Item()
        ArithmeticExpressionTmp()


# <项>→<因子><项tmp>
# <Item>→<Factor><ItemTmp>
def Item():
    Factor()
    ItemTmp()


# <项tmp>→*<因子><项tmp>│<空>
# <ItemTmp>→*<Factor><ItemTmp>|ε
def ItemTmp():
    global sym_type, line
    if sym_type == Op['*']:
        advance()
        Factor()
        ItemTmp()


# <因子>→<变量>│<常数>│<函数调用>
# <Factor>→<Var>|<Constant>|<FuncCall>
def Factor():
    global sym_type, sym
    if sym_type == spCode['id']:
        # 判断是否是一个过程名
        if isProc(sym):
            advance()
            FuncCall()
        else:
            Var(varDefOrUse['use'], sym, VarKind['var'])
    if sym_type == spCode['const']:
        advance()


# <函数调用>→<标识符>(<算数表达式>)
# <FuncCall>→<Var>(<ArithmeticExpression>)
def FuncCall():
    global sym_type, sym
    if sym_type == Op['(']:
        advance()
        ArithmeticExpression()
        if sym_type == Op[')']:
            advance()
        else:
            error(line, 'error: missing \')\'')
    else:
        error(line, 'error: missing \'(\'')


# <条件语句>→if <条件表达式> then <执行语句> else <执行语句>
# <ConditionStatement>→if <ConditionExpression> then <ExecStatement> else <ExecStatement>
def ConditionStatement():
    global sym_type, sym, line
    if sym_type == Keys['if']:
        advance()
        ConditionExpression()
        if sym_type == Keys['then']:
            advance()
            ExecStatement()
            if sym_type == Keys['else']:
                advance()
                ExecStatement()
            else:
                error(line, 'error: lack \'else\'')
        else:
            error(line, 'error: lack \'then\'')
    else:
        error(line, 'error: not a condition statement')


# <条件表达式>→<算术表达式><关系运算符><算术表达式>
# <ConditionExpression>→<ArithmeticExpression><RelationOperator><ArithmeticExpression>
def ConditionExpression():
    ArithmeticExpression()
    RelationOperator()
    ArithmeticExpression()


# <关系运算符> →<│<=│>│>=│=│<>
# <RelationOperator>→<|<=|>|>=|=|<>
def RelationOperator():
    global sym_type
    if sym_type in RelationOp.values():
        advance()
    else:
        error(line, 'error: not a relation operator')


# 输出语法分析
def outDys():
    for i in range(len(Lex.output)):
        out = ' ' * (16 - len(Lex.output[i][0])) \
              + Lex.output[i][0] + ' ' + str(Lex.output[i][1]) + '\n'
        fDys.write(out)


def outVar():
    blank = ' ' * 4
    header = 'vName' + blank + 'vProc' + blank + 'vKind' + blank \
             + 'vType' + blank + ' ' * 4 + 'vLev' + blank + ' ' * 2 + 'vAdr' + '\n'
    fVar.write(header)
    for i in range(len(VarList)):
        fVar.write('-' * (len(header)) + '\n')
        content = VarList[i][0] + ' ' * 8 + VarList[i][1] + ' ' * 8 + str(VarList[i][2]) + ' ' * 8 + \
                  str(VarList[i][3]) + ' ' * 8 + str(VarList[i][4]) + ' ' * 8 + str(VarList[i][5]) + '\n'
        fVar.write(content)


def outProc():
    blank = ' ' * 4
    header = 'pName' + blank + 'pType' + blank + 'pLev' + blank + 'fAdr' + blank + 'lAdr' + '\n'
    fPro.write(header)
    for i in range(len(ProcList)):
        fPro.write('-' * (len(header)) + '\n')
        content = ProcList[i][0] + ' ' * 6 + ProcList[i][1] + ' ' * 6 + str(ProcList[i][2]) \
                  + ' ' * 6 + str(VarList[0][5]) + ' ' * 6 + str(VarList[len(VarList) - 1][5]) + '\n'
        fPro.write(content)


def delELON():
    i = 0
    while True:
        if i < len(Lex.output):
            if Lex.output[i][0] == 'ELON':
                del Lex.output[i]
                i = i - 1
            i = i + 1
        else:
            break
    print(Lex.output)
    print(len(Lex.output))


def ParserMain():
    # 词法分析
    Lex.LexicalMain()
    print(Lex.output)
    # 删除List中的'ELON'
    delELON()
    # 开始语法分析
    advance()
    Program()
    outDys()
    outVar()
    outProc()


if __name__ == '__main__':
    ParserMain()
    fDys.close()
    fPro.close()
    fVar.close()
    fParserErr.close()
