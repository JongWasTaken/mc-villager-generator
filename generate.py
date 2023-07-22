import os
import json
import sys

def command(cmd):
    return os.popen(cmd).read().strip()

# create folders if not exist
command("mkdir -p ./items/")
command("mkdir -p ./villagers/")

def resolve_byte(bool):
    if bool:
        return "1b"
    return "0b"

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

def generate_item(tag, giveFormat = False):
    itemString = ""

    if giveFormat:
        temp = tag
        tag = {}
        tag["id"] = temp

    try:
        itemFile = open('./items/' + tag["id"] + '.json')
        item = json.load(itemFile)
        itemFile.close()
    except:
        print("[WARN] no custom item with identifier " + tag["id"] + " found, assuming the item is vanilla!")
        if giveFormat:
            return "/give @p minecraft:" + tag["id"] + " 1"
        else:
            return "{id:"+tag["id"]+",Count:"+str(tag["count"])+"}";

    if not giveFormat:
        itemString += "{id:" + item["item"];
        itemString += ",Count:" + str(tag["count"])
        itemString += ",tag:"
    else:
        itemString += "/give @p minecraft:" + item["item"]
    itemString += "{display:{Name:"+ resolve_text(item["title"])

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
    itemString += "}"

    if not giveFormat:
        itemString += "}"
    else:
        itemString += " 1"
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
        command += "{"
        if "xp" in offer:
            command += "xp:"+ str(offer["xp"]) +","
        else:
            command += "xp:0,"
        if "givexp" in offer:
            command += "rewardExp:"+ str(offer["givexp"]) +","
        else:
            command += "rewardExp:false,"
        if "maxuses" in offer:
            command += "maxUses:"+ str(offer["maxuses"]) +","
        else:
            command += "maxUses:9999999,"
        if "multiplier" in offer:
            command += "priceMultiplier:"+ str(offer["multiplier"]) +","
        else:
            command += "priceMultiplier:0,"
        if "specialprice" in offer:
            command += "specialPrice:"+ str(offer["specialprice"]) +","
        else:
            command += "specialPrice:0,"
        if "demand" in offer:
            command += "demand:"+ str(offer["demand"]) +","
        else:
            command += "demand:0,"
        if "uses" in offer:
            command += "uses:"+ str(offer["uses"]) +","
        else:
            command += "uses:0,"
        command += "buy:" + generate_item(offer["buy"]) + ","
        if "buyB" in offer:
            command += "buyB:" + generate_item(offer["buyB"]) + ","
        command += "sell:" + generate_item(offer["sell"])
        command += "},"
    command = command[:-1]
    command += "]},CustomName:"+ resolve_text(villager["title"]) +","
    if "showcustomname" in villager:
        command += "CustomNameVisible:"+ resolve_byte(villager["showcustomname"]) +","
    else:
        command += "CustomNameVisible:1b,"
    if "invulnerable" in villager:
        command += "Invulnerable:"+ resolve_byte(villager["invulnerable"]) +","
    else:
        command += "Invulnerable:1b,"
    if "noai" in villager:
        command += "NoAI:"+ resolve_byte(villager["noai"]) +","
    else:
        command += "NoAI:1b,"
    if "onground" in villager:
        command += "OnGround:"+ resolve_byte(villager["noai"]) +","
    else:
        command += "OnGround:1b,"
    if "silent" in villager:
        command += "Silent:"+ resolve_byte(villager["silent"]) +","
    else:
        command += "Silent:1b,"
    if "persistant" in villager:
        command += "PersistenceRequired:"+ resolve_byte(villager["persistant"]) +","
    else:
        command += "PersistenceRequired:1b,"
    command = command[:-1]
    command += "},display:{Name:"+resolve_text(villager["item_name"])+"}} 1"
    print(command)

if len(sys.argv) > 2:
    if sys.argv[1] == "villager":
        generate_villager(sys.argv[2])
    if sys.argv[1] == "item":
        print(generate_item(sys.argv[2],True))
else:
    print("[WARN] No arguments given, generating all villagers!")
    #test = {"id": "feather-v2-skin-15", "count": 1}
    #print(generate_item(test))
    #exit(1)
    villagers = command("ls villagers").split("\n")
    for v in villagers:
        generate_villager(v.split(".")[0])
