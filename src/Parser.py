
from __future__ import annotations
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'.'))

from builtins import print
from typing import Type
import re
from collections import namedtuple
from src.Regex import Character, Operator


opinfo = namedtuple('Operator', 'precedence associativity')
operator_info = {
    "|": opinfo(0, "left"),
    "concat": opinfo(0, "left"),
    "*": opinfo(1, "R"),
}
operator_list=["*", "concat","|"]



def getPriority(C):
    if (C == '|'):
        return 1
    if(C == 'concat'):
        return 2
    elif (C == '*'):
        return 3
    return 0


def getList(char1, char2):
    list=[]
    for i in range(ord(char1), ord(char2)+1):
        list.append(chr(i))
    return list


def addOperator(list):
    output=[]
    output.append("(")
    for i in range(len(list)):
        output.append(list[i])
        output.append("|")
    output.pop()

    output.append(")")
    return output



def tokenize2(string):
    input = re.sub(r'\s+', "", string)
    
    output = []
    state = ""
    buf = ""
    justInterval=0

    if input[0]=="[" and input[len(input)-1]=="]" and len(input)==5:
        justInterval=1
    

    if input=="eps":
        output.append(input)
        return output

    i=0
    while (i<len(input)):

        #print("input[i]:", input[i])
    
        if input[i]=="[":
            list=[]
            i+=1
            start=input[i]
            i+=2 #-
            stop=input[i]
            i+=2
            list=addOperator(getList(start,stop))

            if justInterval==1:
                list.pop()
                list = list[1:]
          
            output+=list

        if i==len(input):
            return output    
        
        if input[i] ==')':
           
            if len(output)>0 and output[len(output)-1]=="concat":
                output.pop()
            
            output.append(input[i])

            if state!="left_par":
                output.append("concat") 
            state="left_par"
            i+=1
            continue

        if input[i] =='(':
            if len(output)>0 and output[len(output)-1]!="concat" and output[len(output)-1] not in operator_list and state!="right_par":
                output.append("concat")
            output.append(input[i])
                

            if len(output)==0:
                output.append(input[i])

            state="right_par"
            i+=1
            continue
            

        if input[i].isalpha() or input[i].isdigit():
            state="letter"
            output.append(input[i])
            output.append("concat")
        else:
            state="op";

           
            if len(output)>0 and output[len(output)-1]=="concat":
                output.pop();
            output.append(input[i])

            if input[i]=="*":
                output.append("concat")

        i+=1

   
    if output[len(output)-1]=="concat":
        output.pop();

    return output




def replaceEps(list):
    for i in range(len(list)):
        if list[i]=="<":
            print("kdhgs")
            list[i]="eps"
    return list


#a+==a a*
#[a-b]+=[a-b][a-b]*
def plus(string):
    modified_output=[]
    output_string=""

    input = re.sub(r'\s+', "", string)

    for i in range(len(string)):
        if input[i]!="+":
            modified_output.append(input[i])
        else:
            if input[i-1]!="]":
                modified_output.append(input[i-1])
                modified_output.append("*")
            else:
                modified_output.append(input[i-5])
                modified_output.append(input[i-4])
                modified_output.append(input[i-3])
                modified_output.append(input[i-2])
                modified_output.append(input[i-1])
                modified_output.append("*")




    for i in range(len(modified_output)):
        output_string+=modified_output[i]

    return output_string



#s="0?" # 0 | eps
#s=[0-9]?   [0-9]|eps
def qmark(string):
    modified_output=[]
    output_string=""

    input = re.sub(r'\s+', "", string)

    for i in range(len(input)):

        if input[i]=="?":
            modified_output.append("|")
            modified_output.append("<")
        else:
            modified_output.append(input[i])
    
    for i in range(len(modified_output)):
        output_string+=modified_output[i]

    return output_string


 

#  s="\' \'\'a\'"
def tokenize(string):
    cleaned = re.sub(r'\s+', "", string)
    
    output = []
    state = ""
    buf = ""

    if cleaned=="eps":
        output.append(cleaned)
        return output

    for char in cleaned:
        print(char)

        if char ==')':
           
            if len(output)>0 and output[len(output)-1]=="concat":
                output.pop()
            
            output.append(char)

            if state!="left_par":
                output.append("concat") 
            state="left_par"
            continue

        if char =='(':
            if len(output)>0 and output[len(output)-1]!="concat" and output[len(output)-1] not in operator_list and state!="right_par":
                output.append("concat")
            output.append(char)
                

            if len(output)==0:
                output.append(char)

            state="right_par"
            continue
            


        if char.isalpha():
            state="letter"
            output.append(char)
            output.append("concat")
        else:
            #print("aici")
            state="op";

            if output[len(output)-1]=="concat":
                output.pop();
            output.append(char)

            if char=="*":
                output.append("concat")
                


    if output[len(output)-1]=="concat":
        output.pop();

    return output






def infixToPrefix(infix):
    # stack for operators.
    operators = []
   
    # stack for operands.
    operands = []
 
    for token in infix:
        if (token == '('): 
            operators.append(token)
 
        elif (token == ')'):
            while (len(operators)!=0 and operators[-1] != '('):
                
                op1=""
                op2=""
                op=""

                # operator
                if len(operators)>0:
                    op = operators[-1]
                    operators.pop()


                if op!= "*":
                    # operand 1
                    if len(operands)>0:
                        op1 = operands[-1]
                        operands.pop()
 
                    # operand 2
                    if len(operands)>0:
                        op2 = operands[-1]
                        operands.pop()

                    tmp = op +" "+op2+" "+ op1
                else:
                    # operand 1
                    if len(operands)>0:
                        op1 = operands[-1]
                        operands.pop()
                    tmp = op+" "+op1
 

                operands.append(tmp)
 
            # Pop opening bracket
            # from stack.
            operators.pop()
 
        elif (token not in operator_list):
            operands.append(token + "")
 
        else:
            while (len(operators)!=0 and getPriority(token) <= getPriority(operators[-1])):
                op1=""
                op2=""
                op=""
                if len(operators)>0:
                    op = operators[-1]
                    operators.pop()
                
                if op!= "*":
                    # operand 1
                    if len(operands)>0:
                        op1 = operands[-1]
                        operands.pop()
 
                    # operand 2
                    if len(operands)>0:
                        op2 = operands[-1]
                        operands.pop()

                    tmp = op +" "+op2 +" "+op1
                else:
                    # operand 1
                    if len(operands)>0:
                        op1 = operands[-1]
                        operands.pop()
                    tmp = op +" "+op1
 

                operands.append(tmp)
            operators.append(token)
 
    while (len(operators)!=0):
        #print(len(operators))
        op1=""
        op2=""
        op=""
        if len(operators)>0:
            op = operators[-1]
            operators.pop()

            
            if op !="*":
                # operand 1
                if len(operands)>0:
                    op1 = operands[-1]
                    operands.pop()
 
                # operand 2
                if len(operands)>0:
                    op2 = operands[-1]
                    operands.pop()

                tmp = op +" "+ op2+" " + op1
            else:
                # operand 1
                if len(operands)>0:
                    op1 = operands[-1]
                    operands.pop()
                tmp = op+" " + op1

            operands.append(tmp)    
 
    return operands[-1]
 





def replaceWords(string):
    cleaned = re.sub(r'\s+', "", string)
    string=string.replace("concat","CONCAT")
    string=string.replace("*","STAR")
    string=string.replace("|","UNION")

    return string


class Parser:
    # This function should:
    # -> Classify input as either character(or string) or operator
    # -> Convert special inputs like [0-9] to their correct form
    # -> Convert escaped characters
    # You can use Character and Operator defined in Regex.py
    @staticmethod
    def preprocess(regex: str) -> list:
        pass

    # This function should construct a prenex expression out of a normal one.
    @staticmethod
    def toPrenex(s: str) -> str:
        #print(tokenize(s))
        
        return replaceWords(infixToPrefix(replaceEps(tokenize2(qmark(plus(s))))))
