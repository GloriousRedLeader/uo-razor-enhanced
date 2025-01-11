# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_gathering import run_mining_loop

# Mines an area then steps forward to mine again in a straight line.
# Attempts to smelt ores if you have a fire beetle (provide parameter)
# Attempts to move smelted ore to pack animal (provide parameter)
run_mining_loop(
    # Required. Your fire beetle's name.
    forgeAnimalName = "fire beetle name",
    
    # Required. One or more blue beetle names.
    packAnimalNames = ["your blue beetle name", "your other blue beetle name"]
)
