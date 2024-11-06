# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-11-05
# Use at your own risk. 

# Drop everything from a container to the ground.AcceptMe

from Scripts.fm_core.core_player import drop_all_items_from_pack_animal_to_floor
#from Scripts.fm_core.core_mobiles import get_friends_by_names

#def drop_all_items_from_pack_animal_to_floor(packAnimalNames = []):
#    currentNum = 1        
#    packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
#    if len(packAnimals) > 0:
#        for packAnimal in packAnimals:
#            for item in Mobiles.FindBySerial( packAnimal.Serial ).Backpack.Contains:
#                Player.HeadMessage(455, "Moving item #{} {}".format(currentNum, item.Name))
#                #Items.DropItemGroundSelf(item, item.Amount)
#                Items.MoveOnGround(item, 0, Player.Position.X - 1, Player.Position.Y + 1, 0)
#                Misc.Pause(650)
#                currentNum = currentNum + 1

drop_all_items_from_pack_animal_to_floor(packAnimalNames = ["two"])