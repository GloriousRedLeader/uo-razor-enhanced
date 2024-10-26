
# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_player import find_first_in_container_by_name
from Scripts.fm_core.core_mobiles import get_mobs_exclude_serials

# Usage. Just run this in the bar area of shadowguard. It will pickup nearby bottles
# and chuck them at pirates.

#bottleItemID = 0x099B
itemName = "a bottle of Liquor"
    
Timer.Create( 'pingTimer', 1 )    

PING_TIMER_DELAY_MS = 3000
LOOP_NAME = "SG-Bar"

while True:
    
#    if Timer.Check( 'pingTimer' ) == False:
#        Player.HeadMessage( 111, "{}".format(LOOP_NAME) )
#        Timer.Create( 'pingTimer', PING_TIMER_DELAY_MS )    
    
    bottle = find_first_in_container_by_name(itemName)
    
    if bottle is None:
        
        if Timer.Check( 'pingTimer' ) == False:
            Player.HeadMessage( 111, "{} [need bottle]".format(LOOP_NAME) )
            Timer.Create( 'pingTimer', PING_TIMER_DELAY_MS )
    
        filter = Items.Filter()
        filter.OnGround = 1
        filter.RangeMax = 2
        filter.Name = itemName
        items = Items.ApplyFilter(filter)
        if len(items) > 0:
            for item in items:
                print(item.Position)
                Items.Move(item, Player.Backpack.Serial, 1)
                Player.HeadMessage( 111, "{} [loaded]".format(LOOP_NAME) )
    else:
        if Timer.Check( 'pingTimer' ) == False:
            Player.HeadMessage( 111, "{} [loaded]".format(LOOP_NAME) )
            Timer.Create( 'pingTimer', PING_TIMER_DELAY_MS )
            
        mobs = get_mobs_exclude_serials (5, checkLineOfSight = True, serialsToExclude = [], namesToExclude = [])
        if len(mobs) > 0:
            Items.UseItem(bottle)
            Target.WaitForTarget(3000, True)
            Target.TargetExecute(mobs[0])
            Player.HeadMessage( 111, "{} [throwing bottle]".format(LOOP_NAME) )
    Misc.Pause(1000)