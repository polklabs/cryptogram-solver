import re

checks = 0
bestGuess = ""

def testWord(cypher, puzzle):
    return "".join([cypher[c] for c in puzzle])

print("> Loading Words")
wordDict = dict() #{ [length]: words[] }

def loadDictionary(filename, skip=0):
    with open(filename, 'r') as f:
        for _ in range(skip):
            f.readline()
        wordList = f.read().splitlines()
        for word in wordList:
            word = word.split()[0].lower()
            wLength = len(word)
            if wLength not in wordDict:
                wordDict[wLength] = dict()
            wordDict[wLength][word] = 1

# Load common words first so they're searched first
# loadDictionary('words_common.txt')
# loadDictionary('dictionary.txt')
loadDictionary('SUBTLEXus74286wordstextversion.txt', 1)

for key in wordDict.keys():
    wordDict[key] = list(wordDict[key])

print("> Loading Puzzle")
#Load Puzzle
puzzle = ""
solution = ""
hasSolution = False
with open('pz.txt', 'r') as f:
    lines = f.read().splitlines()
    puzzle = lines[0]
    bestGuess = "_"*len(puzzle)
    if len(lines) > 1:
        solution = lines[1]
        hasSolution = True

# Create Cypher
cypher = dict()
cypher[' '] = ' '
for i in range(ord('a'), ord('z')+1):
    cypher[chr(i)] = '_'
for char in puzzle:
    if char.isupper() and char not in cypher:
        cypher[char] = char.lower()

def getWordIndex(outputWords, wordIndex, type="next"):
    # Next unsolved word
    if type == "next":
        return wordIndex

    # Smallest unsolved word
    if type == "smallest":
        s = sorted(outputWords, key=len)
        for i in range(len(s)):
            if "_" in s[i]:
                return outputWords.index(s[i])

    # Largest unsolved word
    if type == "largest":
        s = sorted(outputWords, key=len)
        for i in range(len(s)):
            if "_" in s[0-(i+1)]:
                return outputWords.index(s[0-(i+1)])

    # Word with fewest _ in it
    if type == "fewest":
        count = 1000
        index = 0
        for i in range(len(outputWords)):
            if '_' in outputWords[i]:
                if outputWords[i].count('_') < count:
                    count = outputWords[i].count('_')
                    index = i
        return index

    # Word with smallest ratio of _ in it
    if type == "ratio":
        count = 100
        index = 0
        for i in range(len(outputWords)):
            if '_' in outputWords[i]:
                ratio = outputWords[i].count('_') / len(outputWords[i]) * 100
                if ratio < count:
                    count = ratio
                    index = i
        return index

def getPossibleWords(finalWord, length):
    # Get all words of same length
    possibleWords = wordDict[length]

    # Filter by known mappings
    regex = re.compile(finalWord.replace("_", "."))
    possibleWords = [w for w in possibleWords if bool(re.match(regex, w))]

    return possibleWords

def Solve(cypher, puzzle, wordIndex=0):
    global checks, bestGuess, wordDict
    checks += 1

    output = testWord(cypher, puzzle)
    if output.count("_") < bestGuess.count("_"):
        bestGuess = output

    puzzleWords = puzzle.split(" ")
    finalWords = output.split(" ")

    print(output)

    if wordIndex == len(puzzleWords) or "_" not in output:
        if hasSolution:
            return output == solution
        else:
            print("\n" + output)
            goOn = input("Keep Looking [Y/n]: ")
            return goOn.lower() == "n"
    
    index = getWordIndex(finalWords, wordIndex, "ratio")
    missingWord = puzzleWords[index]
    finalWord = finalWords[index]
    wordLength = len(missingWord)

    # Make sure letters don't map to themselves
    for key in cypher.keys():
        if key != " " and cypher[key] == key:
            return False

    # Make sure all complete words are words, and all incomplete can be words
    for word in finalWords:
        if "_" not in word:
            missing = True
            if len(word) in wordDict:
                if word in wordDict[len(word)]:
                    missing = False
            if missing:
                return False

    for word in finalWords:
        if "_" in word:
            missing = True
            incompleteRegex = re.compile(word.replace("_", "."))
            if len(word) in wordDict:
                for w in wordDict[len(word)]:
                    if bool(re.match(incompleteRegex, w)):
                        missing = False
                        break
            if missing:
                return False
    
    possibleWords = getPossibleWords(finalWord, wordLength)

    for possibleWord in possibleWords:
        # Assign mappings
        newCypher = cypher.copy()
        for i in range(len(possibleWord)):
            char = possibleWord[i]
            newCypher[missingWord[i]] = char

            #Make sure all mappings are 1 to 1
            if list(newCypher.values()).count(char) > 1:
                break
        else:
            # Next word
            if Solve(newCypher, puzzle, wordIndex+1):
                return True
    return False

print("> Solving Puzzle")
Solve(cypher, puzzle)
print(checks)