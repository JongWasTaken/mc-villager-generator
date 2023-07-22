# Minecraft Custom Villager Trader Generator
What a mouthful...

## Usage
#### Items
Define custom items by creating json files in the `items/` directory.  
Use `feather-v2.json` as a reference.  
#### Villagers
Define custom villagers by creating json files in the `villagers/` directory.  
Use `magic-trader.json` as a reference.  
#### Generate Villager Spawn Egg
Run `python generate.py villager <VILLAGER_FILE_NAME_WITHOUT_DOT_JSON>` in a terminal.  
Alternatively you may omit the arguments, in which case all villagers get generated.
#### Generate Give Command For Custom Item
Run `python generate.py item <ITEM_FILE_NAME_WITHOUT_DOT_JSON>` in a terminal.  

## License
Licensed under the MIT License.
