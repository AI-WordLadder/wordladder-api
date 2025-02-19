# 📖 Word Ladder API

**Word Ladder API** — Blind Search & Heuristic Search using FastAPI (Python 3.10+)

----------

## 🚀 Installation

Install the necessary libraries:


`pip install uvicorn fastapi` 

## ▶️ Run the Server

Use `uvicorn` to start the server:

`uvicorn main:app` 

----------


## 📌 Available Path Endpoint

**`GET /game`**

### Query Parameters
| Parameter | Type   | Description                                        | Default    | Options                      |
|-----------|--------|----------------------------------------------------|------------|-----------------------------|
| `length`  | Number | Defines the length of the game path (range: 3-6)   | `3`        | `3`- `6`          |
| `blind`   | String | Search technique to be used                        | `"bfs"`    | `"bfs"`, `"bidirectional"`  |

---

## 📄 Body Response Example
```json
{
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
    "technique": "A* Search",
    "startword": "reseal",
    "endword": "dubbed",
    "optimal": 12,
    "path": ["reseal", "reseat", "resent", "resend", "reseed", "rested", "tested", "tasted", "tauted", "dauted", "daubed", "dabbed", "dubbed"],
    "space": "0.45 KB",
    "time": "0.1160 sec"
  }
}
```

## 🔎 Notes

-   **`optimal`**: Number of steps in the optimal path from `startword` to `endword`.
-   **`space`**: Memory usage for the search process.
-   **`time`**: Time taken to find the path in seconds.
