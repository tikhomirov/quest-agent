# Quest Agent

An AI agent that plays interactive fiction games using large language models and TextWorld.

## Generating Treasure Hunter Games

You can generate Treasure Hunter games using TextWorld's CLI tools. These games involve navigating randomly generated mazes to find specific objects.

### Example Command

```bash
uv run tw-make tw-treasure_hunter --level 5 --output tw_games/treasure_hunter_level5.z8
```

### Difficulty Levels

Difficulty levels are defined as follows:

* **Level 1 to 10**: mode easy, nb. rooms = 5, quest length ranging from 1 to 5 as the difficulty increases
* **Level 11 to 20**: mode medium, nb. rooms = 10, quest length ranging from 2 to 10 as the difficulty increases  
* **Level 21 to 30**: mode hard, nb. rooms = 20, quest length ranging from 3 to 20 as the difficulty increases

Where the different modes correspond to:

* **Easy**: rooms are all empty except where the two objects are placed. Also, connections between rooms have no door
* **Medium**: adding closed doors and containers that might need to be open in order to find the object
* **Hard**: adding locked doors and containers (necessary keys will in the inventory) that might need to be unlocked (and open) in order to find the object

Once generated, run the agent with your game:

```bash
uv run agent games/treasure_hunter_level5.z8 --model gpt-4o-mini
```
