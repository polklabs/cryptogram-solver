from operator import le
import re

base =   "abcdefghijklmnopqrstuvwxyz "
cypher = "__________________________ "
checks = 0

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
solution = ""
hasSolution = False
with open('puzzle2.txt', 'r') as f:
    lines = f.read().splitlines()
    puzzle = lines[0]
    if len(lines) > 1:
        solution = lines[1]
        hasSolution = True

for char in puzzle:
    if char.isupper():
        if char not in base:
            base += (char)
            cypher += (char.lower())

def getWordIndex(outputWords, wordIndex):
    # Next unsolved word
    # return wordIndex

    # Smallest unsolved word
    # s = sorted(outputWords, key=len)
    # for i in range(len(s)):
    #     if "_" in s[i]:
    #         return outputWords.index(s[i])

    # Largest unsolved word
    # s = sorted(outputWords, key=len)
    # for i in range(len(s)):
    #     if "_" in s[0-(i+1)]:
    #         return outputWords.index(s[0-(i+1)])

    # Word with fewest _ in it
    count = 1000
    index = 0
    for i in range(len(outputWords)):
        if '_' in outputWords[i]:
            if outputWords[i].count('_') < count:
                count = outputWords[i].count('_')
                index = i
    return index

def Solve(cypher, puzzle, wordIndex=0):
    global checks
    checks += 1

    output = testWord(cypher, puzzle)

    puzzleWords = puzzle.split(" ")
    finalWords = output.split(" ")

    print(output)

    if wordIndex == len(puzzleWords) or "_" not in output:
        if hasSolution:
            return output == solution
        else:
            print("\n" + output)
            goOn = input("Keep Looking [Y/n]: ")
            if goOn.lower() == "n":
                return True
            else:
                return False
    
    index = getWordIndex(finalWords, wordIndex)
    missingWord = puzzleWords[index]
    finalWord = finalWords[index]
    wordLength = len(missingWord)

    # Make sure letters don't map to themselves
    for i in range(len(cypher)):
        if base[i] != " " and cypher[i] == base[i]:
            return False

    # Make sure all complete words are words, and all incomplete can be words
    for word in finalWords:
        if "_" not in word:
            if word in wordDict[len(word)]:
                continue
            else:
                return False

    for word in finalWords:
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

            #Make sure all mappings are 1 to 1
            if newCypher.count(char) > 1:
                break
        else:
            newCypher = "".join(newCypher)

            # Next word
            if Solve(newCypher, puzzle, wordIndex+1):
                return True

print("> Solving Puzzle")
Solve(cypher, puzzle)
print(checks)