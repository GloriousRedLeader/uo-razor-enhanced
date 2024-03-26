from Scripts.fm_core.core_mobiles import get_mobs_exclude_serials
from System.Collections.Generic import List
from System import Byte

# This is a standalone script that will attack the closest gray creature with your weapon.
# That is all.

eligible = get_mobs_exclude_serials(6)

if len(eligible) > 0:
    nearest = Mobiles.Select(eligible,'Nearest')
    if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=6:
        Misc.SendMessage(nearest)
        nearby_enemies_len = len(monster_list(1))
        Player.Attack(nearest)