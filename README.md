
# 📖 Word Ladder API

  

**Word Ladder API** — Blind Search & Heuristic Search using FastAPI (Python 3.10+)

  

----------

  

## 🚀 Installation

  

Install the necessary libraries:

  
  

```bash
pip install uvicorn fastapi
```

  

## ▶️ Run the Server

  

Use `uvicorn` to start the server:

  
```bash
uvicorn main:app
```
  

----------

  
  

## 📌 Available Path Endpoint

 **`GET /`**
 return template response of the game (example in Body Response Example)
 
 **`GET /check`**
#### Query Parameters (Necessary)

**`GET /game`**
| Parameter | Type | Description |
 |------------|--------|-------------| 
 | `word` | String | The word being submitted as the current answer. | 
 | `previous` | String | The word used in the previous step of the game. |

#### Query Parameters (Optional)

| Parameter  | Type   | Description                                            | Default | Options                   |
|------------|--------|--------------------------------------------------------|---------|---------------------------|
| `length`     | Number | Length of the game path (must be between 3 and 6)     | 3       | 3, 4, 5, 6                |
| `blind`      | String | Search technique to be used                           | "bfs"   | "bfs", "bidirectional"    |
| `startWord`  | String | Starting word for the game                            | None    | Any valid word            |
| `endWord`    | String | Target word for the game                              | None    | Any valid word            |

**Note:**  
- If either `startWord` or `endWord` is not found in the word list, the API will return a **400 Bad Request** error.


  

---

  

## 📄 Body Response Example

#### json response of /game
```json
{
  "blind": {
    "technique": "BFS",
    "startword": "poke",
    "endword": "blow",
    "optimal": 6,
    "path": [
      {
        "poke": 0
      },
      {
        "pole": 2
      },
      {
        "bole": 0
      },
      {
        "bolt": 3
      },
      {
        "boot": 2
      },
      {
        "blot": 1
      },
      {
        "blow": 3
      }
    ],
    "space": "1890.75 KB",
    "time": "0.1766 sec"
  },
  "heuristic": {
    "technique": "A* Search",
    "startword": "poke",
    "endword": "blow",
    "optimal": 6,
    "path": [
      {
        "poke": 0
      },
      {
        "pole": 2
      },
      {
        "bole": 0
      },
      {
        "bolt": 3
      },
      {
        "boot": 2
      },
      {
        "blot": 1
      },
      {
        "blow": 3
      }
    ],
    "space": "1351.89 KB",
    "time": "0.0660 sec"
  }
}

```
#### json response of /check
```json
 {
  "word": "sing",
  "valid": false,
  "message": "Cannot change more than 1 character"
} 
```

## 🔎 Notes

  

-  **`optimal`**: Number of steps in the optimal path from `startword` to `endword`.

-  **`space`**: Memory usage for the search process.

-  **`time`**: Time taken to find the path in seconds.
