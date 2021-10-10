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
* bot displays scoreboard of quiz

_To be implemented:_
* Different checks for different answer types

_Maybe one day:_
* Selection from more quizzes  
* Option for quizzes to be started by members without admin
* Time based score calculation

#### example quiz-file
hardcoded path: `data/questions.json`, questions are modelled as json array.
```json
[
  {
    "q": "In which year was python published?", 
    "d": "Name it's first appearance",
    "a": "1991",
    "t": "year"
  },
  {
    "q": "Distance from earth to moon?",
    "d": "Rounded to thousands",
    "a": "384400",
    "t": "integer",
    "tolerance": "3"
    
  }
]
```
##### Supported question types:
* year (just compare the year of a date)
* date (compare the whole date, except time)
* time (compare time, dates ignored)
* word (simply match two words, in lowercase)
* integer (compare two integers with given precision)

_integer comparison allows for an extra tolerance parameter in the json_
    

#### setup
`pip install -r requirements.txt`  
`export TOKEN="your-key"`  
`python3 main.py`

#### optional parameters
| parameter |  description | commandline argument |  
| ------ |  ------ |  ------ |
| `PREFIX="q!"`  | Command prefix | `-t` `--token` |
| `QUESTIONS="data/questions.json"`  | Path the quiz file is located | `-q` `--questions` |
| `LANGUAGE="en"`  | Language dates are processed in | `-l` `--language` |
| `VERSION="unknown"` | Version the bot is running | `-v` `--version` |
| `OWNER_NAME="unknwon"` | Name of the bot owner | `-n` `--owner_name` |
| `OWNER_ID="100000000000000000"` | ID of the bot owner | `-i` `--owner_id` |
| `ALLOWED_DELTA="2.0"`| Time (seconds) the questions stay open after a question was answered | `-d` `--allowed_delta` |  

You can configure those parameters using env-variables or console-args.  

The shown values are the default values that will be loaded if nothing else is specified.


