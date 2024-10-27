
# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_player import find_first_in_container_by_name
from Scripts.fm_core.core_player import find_in_container_by_id
from Scripts.fm_core.core_mobiles import get_mobs_exclude_serials
from System.Collections.Generic import List
from Scripts.fm_core.core_rails import go_to_tile
import re

# Usage. Just run this in the bar area of shadowguard. It will pickup nearby bottles
# and chuck them at pirates.

PING_TIMER_DELAY_MS = 3000
LOOP_NAME = "SG-Orchard"
APPLE_PROPERTY_REGEX = r"An Enchanted Apple of ([A-Za-z]*)"
APPLE_ID = 0x09D0
PULSE_MS = 1000
VIRTUE_MAP = {
    "Compassion": "Despise",
    "Honor": "Shame",
    "Honesty": "Deceit",
    "Humility": "Pride",
    "Justice": "Wrong",
    "Sacrafice": "Covetous",
    "Spirituality": "Hythloth",
    "Valor": "Destard",
    "Despise": "Compassion",
    "Shame": "Honor",
    "Deceit": "Honesty",
    "Pride": "Humility",
    "Wrong": "Justice",
    "Covetous": "Sacrafice",
    "Hythloth": "Spirituality",
    "Destard": "Valor"
}

trees = []

def get_apple_from_bag():
    global VIRTUE_MAP
    apple = find_in_container_by_id(APPLE_ID, Player.Backpack)
    if apple is not None:
        for prop in apple.Properties:
            res = re.search(APPLE_PROPERTY_REGEX, prop.ToString())
            if res is not None:
                virtue = res.group(1)
                return { "Item": apple, "Virtue": virtue, "TargetTreeVirtue": VIRTUE_MAP[virtue] }

def set_trees():
    filter = Items.Filter()
    filter.OnGround = 1
    filter.RangeMax = 40
    filter.Name = "cypress tree"
    items = Items.ApplyFilter(filter)  
    i = 0
    for item in items:
        treeExists = False
        for tree in trees:
            if tree["Serial"] == item.Serial:
                treeExists = True
        if not treeExists:
            trees.append({ "Item": item, "Serial": item.Serial, "Position": item.Position, "Virtue": None, "Alive": True })
            print("Add tree to map ({})".format(len(trees)))
    return len(trees)

# returns exact tree or a random one to try, might as well not waste the cycle
def get_tree_for_apple(apple):
    randomTree = None
    for tree in trees:
        if tree["Virtue"] == apple["TargetTreeVirtue"]:
            return tree, False
        else:
            randomTree = tree
    return randomTree, True
            
def set_tree_dead(virtue):
    global VIRTUE_MAP
    for tree in trees:
        if tree["Virtue"] == virtue or tree["Virtue"] == VIRTUE_MAP[virtue]:    
            tree["Alive"] = False
        
def get_tree_to_pick_apple():
    for tree in trees:
        if tree["Virtue"] is None and tree["Alive"] == True:
            return tree

Player.HeadMessage( 111, "{} [starting]".format(LOOP_NAME) )

while True:
    set_trees()
        
    apple = get_apple_from_bag()
    if apple is not None:
        tree, isRandom = get_tree_for_apple(apple)
        if tree is not None:
            if isRandom == True:
                Player.HeadMessage( 38, "{} [go to tree]".format(LOOP_NAME) )
                Items.Message(tree["Item"], 38, "^ Here ^")
            else:
                Player.HeadMessage( 58, "{} [go to tree]".format(LOOP_NAME) )
                Items.Message(tree["Item"], 58, "^ Here ^")
            Items.UseItem(apple["Item"])
            Target.WaitForTarget(10000, False)
            Journal.Clear()
            Target.TargetExecute(tree["Item"])
            if Journal.Search("Your throw releases powerful magics and destroys the tree!"):
                set_tree_dead(apple["Virtue"])
                Player.HeadMessage( 38, "{} [killed a tree]".format(LOOP_NAME) )
        else:
            Player.HeadMessage( 111, "{} [wait 30 seconds]".format(LOOP_NAME) )
    else:
        tree = get_tree_to_pick_apple()
        if tree is None:
            Player.HeadMessage( 111, "{} [no more trees]".format(LOOP_NAME) )
            break
        
        while True:
            Player.HeadMessage( 58, "{} [go to tree]".format(LOOP_NAME) )
            Items.Message(tree["Item"], 58, "^ Here ^")
            Items.UseItem(tree["Item"])

            apple = get_apple_from_bag()
            if apple is not None:
                tree["Virtue"] = apple["Virtue"]
                break
            Misc.Pause(PULSE_MS)
    Misc.Pause(PULSE_MS)