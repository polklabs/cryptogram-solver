from operator import le
import re

base =   "abcdefghijklmnopqrstuvwxyz "
cypher = "__________________________ "
revertToIndex = -1

def testWord(cypher, puzzle):
    return "".join([cypher[base.index(c)] for c in puzzle])

wordDict = dict() #{ [length]: words[] }

print("> Loading Words")
# Load common words first so they're searched first
with open('words_common.txt', 'r') as f:
    wordList = f.read().splitlines()
    for word in wordList:
        wLength = len(word)
        if wLength not in wordDict:
            wordDict[wLength] = dict()
        wordDict[wLength][word] = 1

with open('words_alpha.txt', 'r') as f:
    wordList = f.read().splitlines()
    for word in wordList:
        wLength = len(word)
        if wLength not in wordDict:
            wordDict[wLength] = dict()
        wordDict[wLength][word] = 1

for key in wordDict.keys():
    wordDict[key] = list(wordDict[key])

print("> Loading Puzzle")
#Load Puzzle
puzzle = ""
with open('puzzle.txt', 'r') as f:
    puzzle = f.read().splitlines()[0]

for char in puzzle:
    if char.isupper():
        if char not in base:
            base += (char)
            cypher += (char.lower())

def Solve(cypher, puzzle, wordIndex=0):
    global revertToIndex

    puzzleWords = puzzle.split(" ")
    finalWords = testWord(cypher, puzzle).split(" ")

    if wordIndex == len(puzzleWords):
        print("\n" + " ".join(finalWords))
        goOn = input("Keep Looking [Y/n]: ")
        if goOn.lower() == "n":
            return True
        else:
            print(" ".join([finalWords[i] + "(" + str(i) + ")" for i in range(len(finalWords))]))
            revertToIndex = int(input("Which word is incorrect? "))
            return False
    
    missingWord = puzzleWords[wordIndex]
    wordLength = len(missingWord)
    finalWord = finalWords[wordIndex]

    # Make sure letters don't map to themselves
    for i in range(len(cypher)):
        if base[i] != " " and cypher[i] == base[i]:
            return False

    # Make sure all complete words are words, and all incomplete can be words
    for word in finalWords[wordIndex:]:
        if "_" not in word:
            if word in wordDict[len(word)]:
                continue
            else:
                return False

    for word in finalWords[wordIndex:]:
        _count = word.count("_")
        if _count > 0 and _count < len(word):
            incompleteRegex = re.compile(word.replace("_", "."))
            for w in wordDict[len(word)]:
                if bool(re.match(incompleteRegex, w)):
                    break
            else:
                return False

    
    # Get all words of same length
    possibleWords = wordDict[wordLength]

    # Filter by known mappings
    regex = re.compile(finalWord.replace("_", "."))
    possibleWords = [w for w in possibleWords if bool(re.match(regex, w))]

    if len(possibleWords) <= 0:
        return False

    for possibleWord in possibleWords:
        # Assign mappings
        newCypher = list(cypher)
        for i in range(len(possibleWord)):
            char = possibleWord[i]
            cypherIndex = base.index(missingWord[i])
            newCypher[cypherIndex] = char
            if newCypher.count(char) > 1:
                # Theres too many items for this
                break
        else:
            newCypher = "".join(newCypher)

            # print(testWord(newCypher, puzzle))

            # Next word
            if Solve(newCypher, puzzle, wordIndex+1):
                return True
            else:
                if revertToIndex != -1:
                    if wordIndex != revertToIndex:
                        return False
                    else:
                        revertToIndex = -1

print("> Solving Puzzle")
Solve(cypher, puzzle)