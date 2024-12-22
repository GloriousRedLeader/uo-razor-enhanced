# Trains stealing. Need a pack animal and an item.

packAnimalSerial = Target.PromptTarget("Pick pack animal (must be in guild)")
itemSerial = Target.PromptTarget("Pick item to steal")

packAnimalBackpackSerial = Mobiles.FindBySerial( packAnimalSerial ).Backpack.Serial

Items.UseItem(packAnimalBackpackSerial)
Misc.Pause(650)

while Player.GetSkillValue("Stealing") < Player.GetSkillCap('Stealing'):
    
    item = Items.FindBySerial(itemSerial)
    print("item.Container {}, packAnimalBackpackSerial {}".format(item.Container, packAnimalBackpackSerial))
    if item.Container == packAnimalBackpackSerial:
        Player.UseSkill("Stealing")
        Target.WaitForTarget(300, True)
        Target.TargetExecute(item)
        print("Pausing 10s")
        Misc.Pause(10000)
    else:
        Items.Move(item, packAnimalBackpackSerial, item.Amount)
        print("Moving item back")
        Misc.Pause(1000)