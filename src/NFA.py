
from typing import Callable, Generic, TypeVar ,Set, Dict, Tuple, List
import re
from queue import Queue

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'.'))
S = TypeVar("S")
T = TypeVar("T")

class NFA:
    _alphabet:Set[str]
    _initial_state: int
    _final_states:int
    _delta: List[Tuple[int, str, int]]
    _max_int_state: int



    def __init__(self, token):

        if token == 'eps':
            self._alphabet=set()
            self._initial_state=0
            self._max_int_state=0
            self._delta = list()

        elif token != "void":
            self._alphabet=set()
            self._alphabet.add(token)
            self._alphabet.add('eps')

            self._final_states=1
            self._initial_state=0
            self._max_int_state=1
            self._delta = list()
            self._delta.append([ 0, token,  1])
        else:
            self._alphabet=set()
            self._initial_state=0
            self._max_int_state=-1
            self._delta = list()




    def printList(self, tokens):
        print(tokens)


    def createOneTransitionNFA(self, token):
        nfa=NFA(token);
        return nfa;

 
    def increaseStateNrByOne(self, A):
        for x in A._delta:
            x[0]+=1
            x[2]+=1
        
        A._max_int_state+=1
        A._final_states+=1;


    @staticmethod
    def star(A):
        A._delta.append([A._max_int_state,'eps',A._initial_state])
        A.increaseStateNrByOne(A)

        #add new transitions
        A._delta.insert(0, [0,'eps',1])
        A._delta.append([A._max_int_state ,'eps', A._max_int_state+1])
        A._max_int_state+=1
        A._delta.append([0,'eps',A._max_int_state])


        return A;


    @staticmethod
    def upStates(A, nr):
        for x in A._delta:
            x[0]+=nr
            x[2]+=nr
        

        A._initial_state+=nr
        A._max_int_state+=nr
        A._final_states+=nr



    @staticmethod
    def union(A, B):

        A.increaseStateNrByOne(A)

        #add 2 transition to A
        A._delta.insert(0, [0,'eps',1])
        B.upStates(B, A._max_int_state+1)

        A._delta.append([0, 'eps', B._initial_state])
        
        for x in B._delta:
            A._delta.append(x)
        

        A._delta.append([B._max_int_state, 'eps', B._max_int_state+1])
        A._delta.append([A._max_int_state, 'eps', B._max_int_state+1])
        A._max_int_state=B._max_int_state+1

        for x in B._alphabet:
            A._alphabet.add(x)

        return A



    @staticmethod
    def concat(A, B):
         B.upStates(B, A._max_int_state+1)
         A._delta.append([A._max_int_state, 'eps', B._initial_state])

         for transition in B._delta:
            A._delta.append(transition)
        
         for x in B._alphabet:
            A._alphabet.add(x)

         A._max_int_state=B._max_int_state

         return A



    @staticmethod
    def myFunc(tokens):
       
        token=tokens.pop(0)
        if token=="UNION":
            a=NFA.myFunc(tokens)
            b=NFA.myFunc(tokens)
            return NFA.union(a,b)
          

        elif token=="STAR":
            a=NFA.myFunc(tokens)
            return NFA.star(a)

        elif token=="CONCAT":
            a=NFA.myFunc(tokens)
            b=NFA.myFunc(tokens)
            return NFA.concat(a,b)
        else:
            if token=="SPACE":
                return NFA(' ')
            elif token=="AP":
                return NFA("'")
            elif token=="R":
                return NFA("\r")
            elif token=="ENDL":
                return NFA("\n")
            elif token=="NULL":
                return NFA("\0")
            elif token=="TAB":
                return NFA("\t")
            else:
                return NFA(token)


    @staticmethod
    def getDict(A):
        dictA=dict()
        for transition in A._delta:
            key=transition[0]
            ch= transition[1]
            value=transition[2]

            valueTuple=(ch,value)

            if dictA.get(key)!=None:
                dictA[key].append(valueTuple)
            else:
                dictA[key]=list()
                dictA[key].append(valueTuple)
        return dictA



    @staticmethod    
    def word(dictA, finalState, str, state, doneStack):
    
        if str == "" and state == finalState:
            return [state]

        if (str, state) in doneStack:
            return []
        else:
            if len(str) == 0:
                doneStack.append(('esp', state))
            else:
                doneStack.append((str, state))
             
        if state not in dictA:
            return []

        paths = dictA[state]
        matchedPaths = []

        for path in paths:
            if str != "" and path[0] == str[0]:
                for found in NFA.word(dictA, finalState, str[1:], path[1], doneStack):
                    matchedPaths.append(found)
            if path[0] == "eps":
                for found in NFA.word(dictA, finalState, str, path[1], doneStack):
                    matchedPaths.append(found)

        return matchedPaths


      
    @staticmethod    
    def acceptWord(obj, word):
        dictA=obj.getDict(obj)
        listA =list()
        listA=obj.word(dictA,obj._max_int_state,word ,0,[])

        if listA!=[] and listA[0] == obj._max_int_state:
            return True 
        else:
            return False

    
    def accepts(self, str: str) -> bool:
        return self.acceptWord(self, str)


    @staticmethod
    def getTokenList(str):
        tokens=str.split()
        return tokens


    @staticmethod
    def fromPrenex(str: str) -> 'NFA[int]':
        obj=NFA("void")
        str=re.sub("' '","SPACE",str)
        str=re.sub("'''","AP",str)
        str=re.sub("'\r'","R",str)
        str=re.sub("'\n'","ENDL",str)
        str=re.sub("'\0'","NULL",str)
        str=re.sub("'\t'","TAB",str)

        
        tokens=list()
        tokens=obj.getTokenList(str)
        obj=obj.myFunc(tokens)
        return obj


    def map(self, f: Callable[[S], T]) -> 'NFA[T]':
        return self

    def next(self, from_state: S, on_chr: str) -> 'set[S]':
        return []

    def getStates(self) -> 'set[S]':
        return list(range(0, self._max_int_state))
		

    def isFinal(self, state: S) -> bool:
        pass

