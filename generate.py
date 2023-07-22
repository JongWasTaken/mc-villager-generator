import os
import json
import sys

def command(cmd):
    return os.popen(cmd).read().strip()

# create folders if not exist
command("mkdir -p ./items/")
command("mkdir -p ./villagers/")

def resolve_text(raw):
    text = "'[{\"text\":\"" + raw["text"] + "\","
    if raw["italic"]:
        text += "\"italic\":true"
    else:
        text += "\"italic\":false"

    if raw["bold"]:
        text += ",\"bold\":true"

    text += "}]'"
    return text

def generate_item(tag):
    itemString = "{id:"
    # {id:feather,Count:1,
    # tag:{display:
    # {Name:'[{"text":"Mystical Feather of Levitation","italic":false}]',
    # Lore:['[{"text":"Holding this item in your offhand will grant you creative flight.","italic":false}]','[{"text":"Skinnable","italic":false,"bold":true}]']
    # },EnableFlight:1}}
    try:
        itemFile = open('./items/' + tag["id"] + '.json')
        item = json.load(itemFile)
        itemFile.close()
    except:
        print("[WARN] no item with identifier " + tag["id"] + " found, assuming the item is vanilla!")
        return "{id:"+tag["id"]+",Count:"+str(tag["count"])+"}";
    itemString += item["item"];
    itemString += ",Count:" + str(tag["count"])
    itemString += ",tag:{display:{Name:"+ resolve_text(item["title"])

    if len(item["description"]) > 0:
        itemString += ",Lore:["
        # foreach description item
        for text in item["description"]:
            itemString += resolve_text(text) + ","
        itemString = itemString[:-1]
        itemString += "]"
    itemString += "}," # close display tag
    for nbt in item["tags"]:
        if type(nbt["value"]) == type(1):
            itemString += nbt["key"] + ":" + str(nbt["value"]) + ","
        if type(nbt["value"]) == type([""]):
            if nbt["key"] == "Enchantments":
                # Enchantments:[{id:unbreaking,lvl:1}]
                itemString += "Enchantments:["
                for enchantment in nbt["value"]:
                    itemString += "{id:"+enchantment["name"]+",lvl:"+str(enchantment["level"])+"},"
                itemString = itemString[:-1]
                itemString += "],"
    itemString = itemString[:-1]
    itemString += "}}"
    return itemString

def generate_villager(filename):
    try:
        villagerFile = open('./villagers/' + filename + ".json")
        villager = json.load(villagerFile)
        villagerFile.close()
    except:
        print("[ERROR] could not load villager with identifier " + filename + ".json!")
        return;
    print("---- " + filename + ".json ----")
    command = "/give @p wandering_trader_spawn_egg{EntityTag:{id:villager,VillagerData:"
    command += "{type:"+ villager["type"] +",profession:"+ villager["profession"] +",level:99},Offers:{Recipes:["
    for offer in villager["offers"]:
        command += "{" + "maxUses:9999999,priceMultiplier:0,specialPrice:0,rewardExp:false,"
        command += "buy:" + generate_item(offer["buy"]) + ","
        if "buyB" in offer:
            command += "buyB:" + generate_item(offer["buyB"]) + ","
        command += "sell:" + generate_item(offer["sell"])
        command += "},"
    command = command[:-1]
    command += "]},CustomName:'[{\"text\":\""+ villager["title"] +"\"}]',"
    command += "CustomNameVisible:1b,Invulnerable:1b,NoAI:1b,OnGround:1b,PersistenceRequired:1b,Silent:1b},display:{Name:'[{\"text\":\""+ villager["item_name"] +"\",\"italic\":false}]'}} 1"
    print(command)

if len(sys.argv) > 1:
    generate_villager(sys.argv[1])
else:
    #test = {"id": "feather-v2-skin-15", "count": 1}
    #print(generate_item(test))
    #exit(1)
    villagers = command("ls villagers").split("\n")
    for v in villagers:
        generate_villager(v.split(".")[0])
