import random
import requests
import time
import sys
from collections import defaultdict, deque
from typing import List, Dict,Annotated, Optional
from fastapi import FastAPI, HTTPException, Query
from heapq import heappop,heappush
import time
import tracemalloc


# Fetch two random words with the specified length
def fetchRandomWords(length: int) -> List[str]:
    url = f"https://random-word-api.vercel.app/api?words=2&length={length}"
    req = requests.get(url)
    if req.status_code == 200:
        try:
            return req.json()
        except requests.exceptions.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Error decoding JSON response from the random word API")
    else:
        raise HTTPException(status_code=500, detail=f"API request failed with status code {req.status_code}")


# Fetch a list of random words with the specified length
def fetchWordList(length: int) -> List[str]:
    url = f"http://localhost:9001/word?length={length}&number=180000"
    req = requests.get(url)
    if req.status_code == 200:
        return req.json()
    else:
        raise HTTPException(status_code=500, detail="Error: The word list could not be retrieved.")


# Build adjacency list for word transformation patterns
def buildAdjacencyList(wordList: List[str]) -> defaultdict:
    nei = defaultdict(list)
    for word in wordList:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j + 1:]
            nei[pattern].append(word)
    return nei

#find hamming distance between two string:
def heuristic(beginWord : str , endWord: str) -> int:
    hn = 0
    for i in range(len(endWord)):
        if beginWord[i] != endWord[i]:
            hn += 1
    return hn

def fn(gn:int ,hn:int):
    return gn+hn

# A* heuristic search
def aStar (beginWord : str, endWord: str, wordList: List[str])-> Dict:
    if endWord not in wordList:
        return {"optimal":0,"path":[]}

    visited = set([beginWord])
    nei = buildAdjacencyList(wordList)
    startFn = heuristic(beginWord,endWord)
    heap = [(startFn,beginWord,[beginWord])]

    while heap:
        _ , startWord, path = heappop(heap)
        gn = len(path)

        if startWord == endWord:
            return {"optimal":gn,"path":path}
        
        for j in range(len(startWord)):
            pattern = startWord[:j] + "*" + startWord[j + 1:]
            for neiWord in nei[pattern]:
                if neiWord not in visited:
                    visited.add(neiWord)
                    hn = heuristic(neiWord,endWord)
                    heappush(heap,(fn(gn,hn),neiWord,path+[neiWord]))

    return {"optimal":0,"path":[]}
    

# Single-direction BFS
def bfsWordLadder(beginWord: str, endWord: str, wordList: List[str]) -> Dict:
    if endWord not in wordList:
        return {"optimal": 0, "path": []}

    wordList.append(beginWord)
    nei = buildAdjacencyList(wordList)
    visited = set([beginWord])
    queue = deque([(beginWord, [beginWord])])

    while queue:
        word, path = queue.popleft()
        if word == endWord:
            return {"optimal": len(path) - 1, "path": path}
        
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j + 1:]
            for neiWord in nei[pattern]:
                if neiWord not in visited:
                    visited.add(neiWord)
                    queue.append((neiWord, path + [neiWord]))

    return {"optimal": 0, "path": []}

# Bidirectional BFS
def bidirectionalBfsWordLadder(beginWord: str, endWord: str, wordList: List[str]) -> Dict:
    if endWord not in wordList:
        return {"optimal": 0, "path": []}
    
    wordSet = set(wordList)
    front = {beginWord: [beginWord]}
    back = {endWord: [endWord]}
    visited = set()

    while front and back:
        if len(front) > len(back):
            front, back = back, front

        next_front = defaultdict(list)
        for word, path in front.items():
            for j in range(len(word)):
                for i in range(26):
                    newWord = word[:j] + chr(ord('a') + i) + word[j + 1:]
                    if newWord in back:
                        forward_path = path
                        backward_path = back[newWord][::-1]
                        full_path = forward_path + backward_path
                        return {"optimal": len(full_path) - 1, "path": full_path}
                    
                    if newWord in wordSet and newWord not in visited:
                        visited.add(newWord)
                        next_front[newWord] = path + [newWord]

        front = next_front

    return {"optimal": 0, "path": []}


# Measure execution time and memory usage
def measure(func, *args):
    tracemalloc.start()  # Start tracking memory
    start_time = time.time()

    result = func(*args)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage in bytes
    tracemalloc.stop()  # Stop tracking

    return result, end_time - start_time, peak / 1024  # Convert bytes to KB

# Utility to check if two words differ by exactly one letter
def is_one_letter_different(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False
    differences = sum(1 for a, b in zip(word1, word2) if a != b)
    return differences == 1

def find_differing_index(word1: str, word2: str) -> Optional[int]:
    if len(word1) != len(word2):
        return None
    differing_indices = [i for i, (a, b) in enumerate(zip(word1, word2)) if a != b]
    return differing_indices[0] if len(differing_indices) == 1 else None


app = FastAPI()

@app.get("/")
def hello_world():
    template ={
                "blind": {
                    "technique": "BFS",
                    "startword": "reseal",
                    "endword": "dubbed",
                    "optimal": 12,
                    "path": ["reseal", "reseat", "resent", "resend", "reseed", "rested", "tested", "tasted", "tauted", "dauted", "daubed", "dabbed", "dubbed"],
                    "space": "0.45 KB",
                    "time": "0.1160 sec"
                },
                "heuristic": {
                    "technique": "A*",
                    "startword": "reseal",
                    "endword": "dubbed",
                    "optimal": 12,
                    "path": [{"word":"reseat","change":2}, {"word":"reseat","change":2}, "resent", "resend", "reseed", "rested", "tested", "tasted", "tauted", "dauted", "daubed", "dabbed", "dubbed"],
                    "space": "0.45 KB",
                    "time": "0.1160 sec"
                }
            }
    return template

@app.get("/check")
def check_word(word: str = Query(..., min_length=1),previous: str = Query(..., min_length=1)):
    try:
        wordList = fetchWordList(len(word))
        if not wordList:
            raise HTTPException(status_code=404, detail=f"No word list found for length {len(word)}.")
        # Check word is in word list
        if word not in wordList:
            return {
                "word": word,
                "valid": False,
                "reason": "Not in word list"
            }
            
        # Check word diff by one letter
        if not is_one_letter_different(word, previous):
            return {
                "word": word,
                "valid": False,
                "message": "Cannot change more than 1 character"
            }
            
        # Find the diff index
        change_index = find_differing_index(word, previous)
        
        # all checks pass
        return {
            "word": word,
            "valid": True,
            "message": f"The word '{word}' is valid.",
            "change": change_index
        }
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/game")
async def game(
    length: Optional[int] = Query(None, ge=3, le=6),
    blind: str = Query("bfs", pattern="^(bfs|bidirectional)$"),
    startWord: Optional[str] = Query(None),
    endWord: Optional[str] = Query(None),
):
    try:
        user_provided_start = startWord is not None
        user_provided_end = endWord is not None

        while True:  # Keep retrying if no valid path is found
            # Determine word length
            if startWord and endWord:
                if len(startWord) != len(endWord):
                    raise HTTPException(
                        status_code=400,
                        detail="StartWord and EndWord must have the same length.",
                    )
                word_length = len(startWord)
            elif startWord:
                word_length = len(startWord)
            elif endWord:
                word_length = len(endWord)
            else:
                word_length = length or 4  # Default length if none provided

            # Fetch word list
            wordList = fetchWordList(word_length)
            if not wordList:
                raise HTTPException(
                    status_code=404,
                    detail=f"No word list found for length {word_length}.",
                )

            # Validate provided words
            if startWord and startWord not in wordList:
                raise HTTPException(
                    status_code=400,
                    detail=f"StartWord '{startWord}' is not in the word list.",
                )

            if endWord and endWord not in wordList:
                raise HTTPException(
                    status_code=400,
                    detail=f"EndWord '{endWord}' is not in the word list.",
                )

            # Generate missing words
            if not startWord:
                startWord, _ = fetchRandomWords(word_length)
            if not endWord:
                _, endWord = fetchRandomWords(word_length)

            print(f"Trying Start Word: {startWord}, End Word: {endWord}")

            # Perform blind search
            if blind == "bfs":
                result, time_taken, memory_used = measure(
                    bfsWordLadder, startWord, endWord, wordList
                )
                technique = "BFS"
            else:
                result, time_taken, memory_used = measure(
                    bidirectionalBfsWordLadder, startWord, endWord, wordList
                )
                technique = "Bidirectional BFS"

            # If no valid path is found, retry **only missing words**
            if result["optimal"] <= 0:
                print("No valid transformation found. Retrying...\n")

                # If both words were user-provided, we cannot regenerate them
                if user_provided_start and user_provided_end:
                    raise HTTPException(
                        status_code=400,
                        detail=f"No valid path found between '{startWord}' and '{endWord}'.",
                    )

                # Regenerate missing words only
                if not user_provided_start:
                    startWord, _ = fetchRandomWords(word_length)
                if not user_provided_end:
                    _, endWord = fetchRandomWords(word_length)

                continue  # Retry with the new values

            # Store results
            blind_result = {
                "technique": technique,
                "startword": startWord,
                "endword": endWord,
                "optimal": result["optimal"],
                "path": result["path"],
                "space": f"{memory_used:.2f} KB",
                "time": f"{time_taken:.4f} sec",
            }

            # Heuristic Search (A* Search)
            result, time_taken, memory_used = measure(
                aStar, startWord, endWord, wordList
            )

            heuristic_result = {
                "technique": "A* Search",
                "startword": startWord,
                "endword": endWord,
                "optimal": result["optimal"],
                "path": result["path"], 
                "space": f"{memory_used:.2f} KB",
                "time": f"{time_taken:.4f} sec",
            }

            return {"blind": blind_result, "heuristic": heuristic_result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )

