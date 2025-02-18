import random
import requests
import time
import sys
from collections import defaultdict, deque
from typing import List, Dict,Annotated
from fastapi import FastAPI, HTTPException, Query
from heapq import heappop,heappush

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
    url = f"https://random-word-api.herokuapp.com/word?length={length}&number=180000"
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
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    memory_usage = sum(sys.getsizeof(obj) for obj in locals().values())
    return result, end_time - start_time, memory_usage / 1024  # Convert memory usage to KB

app = FastAPI()

@app.get("/")
def hello_world():
    template ={
                "technique": "template",
                "startword": "template",
                "endword": "template",
                "optimal": 2,
                "path": ["template","template","template"],
                "space": "2 KB",
                "time": f"{1:.4f} sec"
            }
    return template


@app.get("/game")
async def game(length: int = Query(3, ge=3, le=10), blind: str = Query("bfs", pattern="^(bfs|bidirectional)$"), heuristic: str = Query("bfs", pattern="^(bfs|bidirectional)$")):
    while True:
        # Fetch random words and word list
        startWord, endWord = fetchRandomWords(length)
        wordList = fetchWordList(length)
        print(f"Trying Start Word: {startWord}, End Word: {endWord}")

        # Choose the correct algorithm
        if blind == "bfs":
            result, time_taken, memory_used = measure(bfsWordLadder, startWord, endWord, wordList)
            technique = "BFS"

        elif blind == "astar":
            result,time_taken,memory_used = measure(aStar, startWord, endWord, wordList)
            technique = "A* search"
            
        else:
            result, time_taken, memory_used = measure(bidirectionalBfsWordLadder, startWord, endWord, wordList)
            technique = "Bidirectional BFS"

        # Check if a valid transformation path was found
        if result["optimal"] > 0:
            return {
                "technique": technique,
                "startword": startWord,
                "endword": endWord,
                "optimal": result["optimal"],
                "path": result["path"],
                "space": f"{memory_used:.2f} KB",
                "time": f"{time_taken:.4f} sec"
            }
        else:
            print("No valid transformation found. Retrying...\n")


