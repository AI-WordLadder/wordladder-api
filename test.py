from collections import deque
from heapq import heappop,heappush

heap = [(-1,0,'eueu',['eiei','eueu']),(0,0,'eiei',['eiei'])]
heappush(heap,(-2,0,'eaea',['eiei','eueu','eaea']))
a = heappop(heap)
print(a)