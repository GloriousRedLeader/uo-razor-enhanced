# Razor Enhanced Scripts for Ultima Online by
#	GRL  
#	https://github.com/GloriousRedLeader/uo-razor-enhanced
#	2024-03-26
# Use at your own risk. 

# This one is kind of fun when it works. If you have enough HCI and skill level, you will
# remain in stealth and keep attacking and the mob will have no way to fight back.

from Scripts.fm_core.core_attack import run_ss_loop

Misc.SendMessage("Starting SS Loop")

# Read up on options in the run_ss_loop function!
run_ss_loop(
    ssAbility = 1,
    useHonor = 0
)