
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

# Usage. Just run this in the armory area of shadowguard. You will need to loot 
# corrupted phylacteries. Once in your bag it will directed you to the purifying area
# and once purified it will direct to a statue.
    
PULSE_MS = 1000
LOOP_NAME = "SG-Fountain"
CANAL_NAME = "Canal"
CORRUPTED_PHYLACTERY_NAME = "Corrupt Phylactery"
PURIFIED_PHYLACTERY_NAME = "Purified Phylactery"
STATUE_NAME = "Cursed Suit of Armor"
FLAME_NAME = "Purifying Flames"

Player.HeadMessage( 111, "{} [running]".format(LOOP_NAME) )

def pick_up_canal():
    filter = Items.Filter()
    filter.OnGround = 1
    filter.RangeMax = 8
    filter.Name = CANAL_NAME
    items = Items.ApplyFilter(filter)
    item = Items.Select(items,"Nearest")
    if item is not None:
        Items.Message(item, 58, "^ Here ^")
        if Player.DistanceTo(item) < 3:
            Items.Move(item, Player.Backpack.Serial, 1)
            Player.HeadMessage( 58, "{} [looted canal piece]".format(LOOP_NAME) )    
            Misc.Pause(650)


while True:
    pick_up_canal()
    Misc.Pause(PULSE_MS)

sys.exit()

def get_nearest_statue():
    filter = Items.Filter()
    filter.OnGround = 1
    filter.RangeMax = 40
    filter.Name = STATUE_NAME
    items = Items.ApplyFilter(filter)
    return Items.Select(items,"Nearest")
    
def get_flames():
    filter = Items.Filter()
    filter.OnGround = 1
    filter.RangeMax = 40
    filter.Name = FLAME_NAME
    items = Items.ApplyFilter(filter)
    for item in items:
        return item
    
def pick_up_corrupted():
    filter = Items.Filter()
    filter.OnGround = 1
    filter.RangeMax = 8
    filter.Name = CORRUPTED_PHYLACTERY_NAME
    items = Items.ApplyFilter(filter)
    if len(items) > 0:
        for item in items:
            Items.Message(item, 58, "^ Here ^")
            if Player.DistanceTo(item) < 3:
                Items.Move(item, Player.Backpack.Serial, 1)
                Player.HeadMessage( 58, "{} [looted corrupted phylactery]".format(LOOP_NAME) )    
                Misc.Pause(650)
        
while True:
    pick_up_corrupted()
    
    purified = find_first_in_container_by_name(PURIFIED_PHYLACTERY_NAME)
    corrupted = find_first_in_container_by_name(CORRUPTED_PHYLACTERY_NAME)
    
    if purified is not None:
        statue = get_nearest_statue()
        Player.HeadMessage( 58, "{} [go to statue]".format(LOOP_NAME) )
        if statue is not None:
            Items.Message(statue, 58, "^ Here ^")
            if Player.DistanceTo(statue) < 5:
                Items.UseItem(purified)
                Target.WaitForTarget(10000, False)
                Target.TargetExecute(statue)
    elif corrupted is not None:
        flames = get_flames()
        if flames is not None:
            Items.Message(flames, 48, "^ Here ^")
            Player.HeadMessage( 48, "{} [go to brazier]".format(LOOP_NAME) )
            if Player.DistanceTo(flames) <= 2:
                Items.UseItem(corrupted)
                Target.WaitForTarget(10000, False)
                Target.TargetExecute(flames)
    else:
        Player.HeadMessage( 38, "{} [kill enemies, loot phylacteries]".format(LOOP_NAME) )
        Misc.Pause(1000)
        
    Misc.Pause(PULSE_MS)