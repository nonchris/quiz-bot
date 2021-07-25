# A quiz bot 
A small discord bot for handling moderated quizzes.  

#### how it works
* read questions from json
* start a quiz using `start`
* wait for answers
    - bot sends message for first correct answer and wil
    - members with the correct answer will be registered
    - the bot will wait for a configurable time until the question can't be answered
* call next question with `next`
* play until all questions asked or just as long as you want use `end` to end a quiz

_To be implemented:_  
* Statistics of quiz
* Different checks for different answer types

_Maybe one day:_
* Selection from more quizzes  
* Option for quizzes to be started by members without admin

#### example quiz-file
hardcoded path: `data/questions.json`, questions are modelled as json array.
```json
[
  {
    "q": "Question", 
    "d": "Additional description",
    "a": "Answer",
    "t": "type, eg data or number"
  },
  {
    "q": "Next question..."
  }
]
```
    

#### setup
`pip install -r requirements.txt`  
`export TOKEN="your-key"`  
`python3 main.py`

#### optional env variables
| parameter |  description |
| ------ |  ------ |
| `export Prefix="q!"`  | Command prefix |
| `export VERSION="unknown"` | Version the bot is running |
| `export OWNER_NAME="unknwon"` | Name of the bot owner |
| `export OWNER_ID="100000000000000000"` | ID of the bot owner |

The shown values are the default values that will be loaded if nothing else is specified.


