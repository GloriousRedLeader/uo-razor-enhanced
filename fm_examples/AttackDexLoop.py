# Razor Enhanced Scripts for Ultima Online by
#	GRL  
#	https://github.com/GloriousRedLeader/uo-razor-enhanced
#	2024-03-26
# Use at your own risk. 

# This is the good stuff. This is a nice melee loop that will run in the background.
# Point your dex character at mobs and watch them die. Plenty of options for a lot of
# playstyles. Feel free to customize it even more. 
from Scripts.fm_core.core_attack import run_dex_loop

Misc.SendMessage("Starting Dex Loop")

# This will use weapon secondary ability every 1 second, use discord,
# use consecrate weapon and divine fury every 10 seconds. Read up on all the options
# available by opening the function.
run_dex_loop(
    specialAbilityType = 2,
    specialAbilityDelayMs = 1000,
    useDiscord = 1,
    discordDelayMs = 10000,
    useConsecrateWeapon = 1,
    consecrateWeaponDelayMs = 10000,
    useDivineFury = 1,
    divineFuryDelayMs = 10000,
    useHonor = 0
)