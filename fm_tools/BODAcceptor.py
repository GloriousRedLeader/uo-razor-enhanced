# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-01-11
# Use at your own risk. 

from System.Collections.Generic import List
from System import Byte, Int32
import sys
from Scripts.fm_core.core_mobiles import get_yellows_in_range
from Scripts.fm_core.core_items import BOD_STATIC_ID
from Scripts.fm_core.core_items import BOD_BOOK_STATIC_ID

# Accepts bods from NPC vendors if you are too lazy to click like me
# Just stand near them, turn this on, and let it rip.
# You can the bods automatically placed into a BOD book if you wish.
# (it uses color to do this).
# You can use this in conjunction with the run_bod_builder tool for
# maximum boddage.

placeInBodBook = True

NPC_BOD_GUMP_ID =  0x9bade6ea
BOD_BOOK_GUMP_ID =  0x54f555df
ALLOWED_SUFFIXES = ["scribe", "alchemist", "carpenter", "bowyer", "tinker", "tailor", "blacksmith", "cook"]

# Looks up nearby npcs and attempts to accept BODs
while True:
    Gumps.CloseGump(BOD_BOOK_GUMP_ID)
    Misc.Pause(500)

    npcs = get_yellows_in_range(4)
    for npc in npcs:
        for prop in npc.Properties:
            res = any(s in prop.ToString() for s in ALLOWED_SUFFIXES)
            if res == True:
                Misc.UseContextMenu(npc.Serial,"Bulk Order Info",3000)
                Misc.Pause(1000)
                gid = Gumps.CurrentGump()

                if gid is not None and gid != 0:
                    Gumps.SendAction(gid, 1)
                    print("gid {}".format(gid))
                else:
                    print("No bods")
                
                if Gumps.HasGump(BOD_BOOK_GUMP_ID):
                    Gumps.CloseGump(BOD_BOOK_GUMP_ID)
                    Misc.Pause(500)                    
    
    if placeInBodBook:
        bods = Items.FindAllByID(itemid = BOD_STATIC_ID,color = -1, container = Player.Backpack.Serial, range = 1)
        for bod in bods:
            bodBook = Items.FindByID(itemid = BOD_BOOK_STATIC_ID, color = bod.Hue, container = Player.Backpack.Serial, range = 3)
            if bodBook is not None:
                Items.Move(bod.Serial, bodBook.Serial, 1)
                Misc.Pause(650)
