# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

GOLD_STATIC_IDS = [0x0EED]

DEADLY_POISON_POT_IDS = [0x0F0A]

DAGGER_STATIC_IDS = [0x0F52]

AXE_STATIC_IDS = [0x0F49, 0x0F47]

LOG_STATIC_IDS = [0x1BDD]

#TREE_STATIC_IDS = [3221, 3222, 3225, 3227, 3228, 3229, 3210, 3238, 3240, 3242, 3243, 3267, 3268, 3272, 3273, 3274, 3275, 3276, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3365, 3367, 3381, 3383, 3384, 3394, 3395, 3417, 3440, 3461, 3476, 3478, 3480, 3482, 3484, 3486, 3488, 3490, 3492, 3496]
TREE_STATIC_IDS = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0C8A, 0x0CA6,
    0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CC9, 0x0CCA, 0x0CCB,
    0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
    0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
    0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
    0x0D98, 0x0D9A, 0x0D9C, 0x0D9E, 0x0DA0, 0x0DA2, 0x0DA4, 0x0DA8 ]

BOARD_STATIC_IDS = [0x1BD7]

INSTRUMENT_STATIC_IDS = [ 
    0x0E9C, # drum
    0x2805, # flute
    0x0EB3, # lute
    0x0EB2, # lap harp
    0x0EB1, # standing harp
    0x0E9E, # tambourine
    0x0E9D, # tambourine (tassle)
]
    
MINER_TOOLS_STATIC_IDS = [0x0F39, 0x0E86]

ORE_STATIC_IDS = [0x19B7, 0x19BA, 0x19B8, 0x19B9, 0x0000, 0x0415, 0x045F, 0x06D8, 0x0455, 0x06B7, 0x097E, 0x07D2, 0x0544 ]

INGOT_STATIC_IDS = [0x1BF2]

STONE_STATIC_IDS = [0x1779]

SAND_STATIC_IDS = [0x423A]

MANDRAKEROOT = 0x0F86
BLOODMOSS = 0x0F7B
SULPHUROUSASH = 0x0F8C
NIGHTSHADE = 0x0F88
BLACKPEARL = 0x0F7A
SPIDERSILK = 0x0F8D
GINSENG = 0x0F85
GARLIC = 0x0F84
PIGIRON = 0x0F8A
BATWING = 0x0F78
NOXCRYSTAL = 0x0F8E
DAEMONBLOOD = 0x0F7D
GRAVEDUST = 0x0F8F

REAGENT_STATIC_IDS = [MANDRAKEROOT, BLOODMOSS, SULPHUROUSASH, NIGHTSHADE, BLACKPEARL, SPIDERSILK, GINSENG, GARLIC, PIGIRON, BATWING, NOXCRYSTAL, DAEMONBLOOD, GRAVEDUST]

ALCHEMY_TOOL_STATIC_IDS = [0x0E9B]

KEG_STATIC_IDS = [0x1940]

EMPTY_BOTTLE_STATIC_ID = 0x0F0E

POISON_POTION_STATIC_ID = 0x0F0A

WRAITH_FORM_SCROLL_ID = 0x226F

FISH_STATIC_IDS = [
    0x4302, # Demon Trout
    0x4303, # Bonito
    0x4306, # Cape cod
    0x4307, # Red grouper, Shad, gray snapper, red drum, sunfish, redbelly beam, pumpkinseed sunfish
    
    0x09CC, # Bluefish, Haddock, brook trout
    0x09CD, 
    0x09CE, # Black seabass
    0x09CF, # Fish
    
    0x44C3, # Torpon, bonefish
    0x44C4, # Yellowfin tuna, pike
    0x44C5, # Captain snook
    0x44C6, # Mahi-mahi
    
    0x44D1, # Snow crab, Apple crab
    0x44D2, # Blue crab, Dungeness crab
    0x44D3, # Crusty Lobster
    0x44D4, # Hummer lobster
]

LOBSTER_TRAP_STATIC_IDS = [0x44CF]

DEPLOYED_LOBSTER_TRAP_STATIC_ID = 0x44CB

FISHING_POLE_STATIC_IDS = [0x0DC0]

PET_LEASH_STATIC_IDS = [0x1374]

BOD_STATIC_ID = 0x2258

BOD_BOOK_STATIC_ID = 0x2259

# Corpses are technically items.    
def get_corpses(range = 2):
    filter = Items.Filter()
    filter.OnGround = True
    filter.RangeMax = range
    filter.IsCorpse = True
    return Items.ApplyFilter(filter)
