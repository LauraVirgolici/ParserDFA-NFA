
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'.'))
from typing import Callable, Generic, TypeVar, Set, Dict, Tuple, List
from NFA import NFA



S = TypeVar("S")
T = TypeVar("T")

class DFA(Generic[S]):
	_alphabet:Set[str]
	_initial_state: int
	_final_states:Set[int]
	_delta:List[Tuple[int, str,int]]
	_max_int_state: int

	

	@staticmethod
	def getDirectEpsilonNeigh(nfa,State):
		neighList=[]
		for transition in nfa._delta:
			if transition[0]==State and transition[1]=='eps':
				neighList.append(transition[2])
		
		return neighList


    
	def uniqueList(L):
		unique=[]
		if L is None:
			return []

		for x in L:
			if x not in unique:
				unique.append(x)
		return unique

  
	@staticmethod
	def epsilonClosure(nfa,State):
		index=1
		closureList=[]

		closureList=DFA.getDirectEpsilonNeigh(nfa,State)
		closureList.insert(0, State)
		closureList=DFA.uniqueList(closureList)

      
        #TODO add initial state
		while index <len(closureList):
			closureList.extend(DFA.getDirectEpsilonNeigh(nfa,closureList[index]))
			closureList=DFA.uniqueList(closureList)
			index+=1

		return closureList



	@staticmethod
	def findCharTr(nfa, list, ch):
		throughCh=[]
		for x in list:
			for transition in nfa._delta:
				if transition[0]== x and transition[1]==ch :
					throughCh.append(transition[2]);
        
		return throughCh



	@staticmethod
	def fromList_toNr(list):
		result=''
		for x in list:
			result+=str(x)
	
		return result


	@staticmethod
	def getFinalStates(list, finalState):	
		chToFind=str(finalState)
		finalStatesList=[]

		for transition in list:
			word=transition[0]
			if word.find(chToFind) != -1:
				finalStatesList.append(transition[0])
		return finalStatesList



	@staticmethod
	def NFAtoDFA(nfa, str):
		startState=[]
		startState=DFA.epsilonClosure(nfa, nfa._initial_state)
		startState.sort()

		DfaList=[]
		currentS=[]
		q = []

		currentS=startState
		q.append(currentS)
		index=0

		while index< len(q):
			currentS=q[index]
			index+=1

			for ch in nfa._alphabet:
				if ch!='eps':
					directNextState=DFA.findCharTr(nfa,currentS,ch)

					nextStateWithEpsList=[]
					for x in directNextState:
						nextStateWithEpsList.extend(DFA.epsilonClosure(nfa,x))

                  
        
					nextStateWithEpsList=DFA.uniqueList(nextStateWithEpsList)
               
					if nextStateWithEpsList!= None or nextStateWithEpsList!=[]:
						nextStateWithEpsList.sort()


					if nextStateWithEpsList not in q:
						if nextStateWithEpsList !=None:
							q.append(nextStateWithEpsList)
                                   

					newState=[currentS, ch ,nextStateWithEpsList]
					if newState not in DfaList:
						DfaList.append(newState)


		deltaList=[]
		for transition in DfaList:
			startStateList=transition[0]
			ch=transition[1]
			nextStateList=transition[2]
			deltaList.append([DFA.fromList_toNr(startStateList), ch, DFA.fromList_toNr(nextStateList)])


		label=0
		StartState=[]
		EndState=[]
		finalStates=set()

		if str=='eps':
			finalStates.add(0)

		for i in range(len(DfaList)):
			
			if type(DfaList[i][0]) ==list:
				if nfa._max_int_state in DfaList[i][0]:
					finalStates.add(label)

				StartState=DfaList[i][0]
			
				for j in range(i,len(DfaList)):
					if DfaList[j][0] ==StartState:
						DfaList[j][0]=label
					if DfaList[j][2] ==StartState:
						DfaList[j][2]=label
				label+=1


			if type(DfaList[i][2]) ==list:
				if nfa._max_int_state in DfaList[i][2]:
					finalStates.add(label)

				EndState=DfaList[i][2]

				for j in range(i,len(DfaList)):
					if DfaList[j][0] ==EndState:
						DfaList[j][0]=label
					if DfaList[j][2] ==EndState:
						DfaList[j][2]=label
				label+=1

		dfa=DFA()
		dfa._delta=DfaList
		dfa._initial_state=0
		dfa._final_states=finalStates
		dfa._alphabet=set()
		dfa._alphabet=nfa._alphabet
		return dfa





	def map(self, f: Callable[[S], T]) -> 'DFA[T]':
		pass

	def next(self, from_state: S, on_chr: str) -> S:
		pass

	def getStates(self) -> 'set[S]':
		pass

	def accepts(self, str: str) -> bool:
		currentState=0
		
		for ch in str:
			if ch not in self._alphabet:
				return False

			for transition in self._delta:
				found=0
				if transition[0]==currentState and transition[1]==ch:
					currentState=transition[2]
					found=1
					break
		
			if found==0:
				return False

		print(currentState)
		if  self.isFinal(currentState):
			return True
		else:
			return False



	def isFinal(self, state: S) -> bool:
		for finalState in self._final_states:
			if state == finalState:
				return True
		return False


	@staticmethod
	def fromPrenex(str: str) -> 'DFA[int]':
		nfa = NFA.fromPrenex(str)

		if str=="void":
			nfa._final_states=-1

		dfa=DFA.NFAtoDFA(nfa, str)
		return dfa




#s = "UNION a b"
#nfa = NFA.fromPrenex(str)
#print(nfa._alphabet)
#print(dfa.accepts("0"))