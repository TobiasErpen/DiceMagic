import sys

class ResultsList(object):
	results = []
	timesRolled = 0

	def __init__(self, list):
		self.results = list

	def AddResult(self, result):
		self.results.append(result)

	def CalculateAverage(self):
		avg = 0
		for result in self.results:
			avg += result.posibility * result.number / 100

		return avg
	def GetTimesRolled(self):
		if self.timesRolled == 0:
			self.timesRolled = 0
			for r in self.results:
				self.timesRolled += r.count
		return self.timesRolled

class Result(object):
	'''
	Represents one result. Is used to store one sum and how many rolls had that result.
	'''
	number = 0
	count = 0
	posibility = 0
	
	def __init__(self, number):
		self.number = number
		
	def CalculatePossibility(self, rolledCount):
		self.posibility = self.count * 100 / rolledCount

def CalculatePosibilities(dieType, diceCount, dropLowest = False, useAdvantage = False, useDisadvantage = False, onesAsTwos = False):
	'''
	Returns a ResultList with all Results. Every Result contains the sum of the dice and how likly it is to come up.

	dieType:		The type of the die ist the number of sides it has.
	diceCount: 		The number of dice rolled.
	dropLowest:		Indicates whether the lowest die of a given roll will be ignored.
	useAdvantage:	Indicates whether only the highest die of a given roll will be used.
	useAdvantage:	Indicates whether only the lowest die of a given roll will be used.
	onesAsTwos:		Indicates whether all ones rolled by a single die will be treaded as a two.
	'''
	if dropLowest and useAdvantage:
		raise Exception("Can not use dropLowest and advantage at the same time.") 
	if dropLowest and useDisadvantage:
		raise Exception("Can not use dropLowest and disadvantage at the same time.")
	if useAdvantage and useDisadvantage:
		raise Exception("Can not use advantage and disadvantage at the same time.")

	
	results = ResultsList([])
	dice = []
	diceSum = diceCount
	for number in range(1, (dieType * diceCount)+1):
		results.AddResult(Result(number))
	
	for number in range(1, diceCount+1):
		dice.append(1)
	
	if dropLowest:
		AddPossibilityToArray(results, diceSum-1)
	elif useAdvantage or useDisadvantage:
		AddPossibilityToArray(results, 1)
	elif onesAsTwos:
		AddPossibilityToArray(results, GetNoOnes(dice))
	else:
		AddPossibilityToArray(results, diceSum)
	
	while diceSum < dieType * diceCount:
		dice = IncreaseDice(dice, dieType)
		
		diceSum = 0
		for die in dice:
			diceSum += die
			
		if dropLowest:
			AddPossibilityToArray(results, diceSum-GetLowest(dice, dieType))
		elif useAdvantage:
			AddPossibilityToArray(results, GetHighest(dice))
		elif useDisadvantage:
			AddPossibilityToArray(results, GetLowest(dice, dieType))
		elif onesAsTwos:
			AddPossibilityToArray(results, GetNoOnes(dice))
		else:
			AddPossibilityToArray(results, diceSum)

	CalculateResultPosibilities(results)

	return results

def IncreaseDice(dice, dieType, pointer = 0):
	'''
	Increases the die, which is at the pointers position, by one. 
	If the targeted die would be increased over the dieType value, the next die will be increased instead and the die at the pointers position will be set to 1.

	pointer:	Position of the cecked die.
	'''
	if pointer == len(dice):
		raise Exception("Dice calculation: pointer out of range.")
	
	if dice[pointer] < dieType:
		dice[pointer] += 1
		return dice
	if dice[pointer] == dieType:
		dice[pointer] = 1
		pointer += 1
		return IncreaseDice(dice, dieType, pointer)

	if dice[pointer] > dieType:
		raise Exception("Die has a to high number")
		
	return dice
	
def AddPossibilityToArray(resultsList, diceSum):
	for result in resultsList.results:
			if result.number == diceSum:
				result.count += 1

def GetLowest(dice, dieType):
	'''
	Returns the value of the lowest die in dice.
	'''
	lowest = dieType
	for die in dice:
		lowest = die if die < lowest else lowest
	return lowest

def GetHighest(dice):
	'''
	Returns the value of the highest die in dice.
	'''
	highest = 1
	for die in dice:
		highest = die if die > highest else highest
	return highest

def GetNoOnes(dice):
	'''
	Returns the sum of all dice treating all ones as twos.
	'''
	result = 0
	for die in dice:
		if 1 == die:
			result += 2
		else:
			result += die
	return result

def CalculateResultPosibilities(resultsList):
	for r in resultsList.results:
		r.CalculatePossibility(resultsList.GetTimesRolled())

def printDice(resultsList):
	'''
	Prints a list of all results with there chance to come up and a visual indicator there of.
	'''
	for r in resultsList.results:
		if r.posibility > 0:
			diagram = "."
			for i in range(0, int(round(r.posibility, 0))):
				diagram += "."
			baseDashes = "	         "
			posibilityAsString = str( "{:.2f}".format(round(r.posibility, 2))) if r.posibility >= 0.005 else "< 0.01"
			dashes = baseDashes[:-1*(len(posibilityAsString) - 3)]
			print(str(r.number) + ":" + dashes + posibilityAsString + "%	" + diagram)
		
	print("Avg:	 	" + str(round(resultsList.CalculateAverage(), 2)))
	print("Dice roles:	" + str(resultsList.GetTimesRolled()))

if __name__ == '__main__':
	diceCount = int(sys.argv[1])
	dieType = int(sys.argv[2])
	dropLowest = "-drop" in sys.argv
	advantage = "-adv" in sys.argv
	disadvantage = "-dis" in sys.argv
	onesAsTwos = "-noOne" in sys.argv

	print(f"Calculating for {diceCount}d{dieType} ...")
	print("Drop lowest die: " + str(dropLowest))
	print("Advantage: " + str(advantage))
	print("Disadvantage: " + str(disadvantage))
	print("Tread ones as twos: " + str(onesAsTwos))
	
	result = CalculatePosibilities(dieType, diceCount, dropLowest, advantage, disadvantage, onesAsTwos)
	printDice(result)