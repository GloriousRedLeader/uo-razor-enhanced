# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-02-04
# Use at your own risk. 

from Scripts.fm_core.core_items import INGOT_STATIC_ID 
from Scripts.fm_core.core_items import BOARD_STATIC_ID 
from Scripts.fm_core.core_items import CLOTH_STATIC_ID 
from Scripts.fm_core.core_items import LEATHER_STATIC_ID 
from Scripts.fm_core.core_items import MANDRAKEROOT
from Scripts.fm_core.core_items import BLOODMOSS
from Scripts.fm_core.core_items import SULPHUROUSASH
from Scripts.fm_core.core_items import NIGHTSHADE
from Scripts.fm_core.core_items import BLACKPEARL
from Scripts.fm_core.core_items import SPIDERSILK
from Scripts.fm_core.core_items import GINSENG
from Scripts.fm_core.core_items import GARLIC
from Scripts.fm_core.core_items import PIGIRON
from Scripts.fm_core.core_items import BATWING
from Scripts.fm_core.core_items import NOXCRYSTAL
from Scripts.fm_core.core_items import DAEMONBLOOD
from Scripts.fm_core.core_items import GRAVEDUST
from Scripts.fm_core.core_items import RESOURCE_HUE_DEFAULT
from Scripts.fm_core.core_items import RESOURCE_HUE_DULL_COPPER
from Scripts.fm_core.core_items import RESOURCE_HUE_SHADOW_IRON
from Scripts.fm_core.core_items import RESOURCE_HUE_COPPER
from Scripts.fm_core.core_items import RESOURCE_HUE_BRONZE
from Scripts.fm_core.core_items import RESOURCE_HUE_GOLD
from Scripts.fm_core.core_items import RESOURCE_HUE_AGAPITE
from Scripts.fm_core.core_items import RESOURCE_HUE_VERITE
from Scripts.fm_core.core_items import RESOURCE_HUE_VALORITE
from Scripts.fm_core.core_items import RESOURCE_HUE_BARBED
from Scripts.fm_core.core_items import RESOURCE_HUE_SPINED
from Scripts.fm_core.core_items import RESOURCE_HUE_HORNED
from Scripts.fm_core.core_items import RESOURCE_HUE_OAK
from Scripts.fm_core.core_items import RESOURCE_HUE_ASH
from Scripts.fm_core.core_items import RESOURCE_HUE_YEW
from Scripts.fm_core.core_items import RESOURCE_HUE_HEARTWOOD
from Scripts.fm_core.core_items import RESOURCE_HUE_BLOODWOOD
from Scripts.fm_core.core_items import RESOURCE_HUE_FROSTWOOD
from Scripts.fm_core.core_crafting import RestockItem
from Scripts.fm_core.core_crafting import run_restocker

# Insane UO Specific. Transfer resources from resource box to a commodity box.
# Use this to prepare your box in conjunction with the BODBuilder.
# Automates resource transferring for use.
# See the configuration section below

# Main container that will house a bunch of resources.
# Works well with commodity deed box but can be any container.
commodityBoxSerial = 0x408CC21E

# Set these serials to your InsaneUO resource boxes.
ingotResourceBoxSerial = 0x4003A151
reagentResourceBoxSerial = 0x408F3168
leatherResourceBoxSerial = 0x40E2C44B
woodResourceBoxSerial = 0x402A1002

# Just keeping the peace.
gumpDelayMs = 250

# Main configuration. Set the resources you want to stock here and their amounts.
# Restockable item that lives inside of a specialized resource container.
# Arguments are as follows:
# itemId: Refer to constants, but represents things like item ids for ingots, boards, etc.
# itemHue: Some items have the same id but use different hues (leather, ingots, boards)
# resourceBoxSerial: Inspect your resource box with razor, get the serial, plug it in
# resourceBoxButton: This is the button id of the gump. You can use gump inspector. Starts at 100 and increments up.
# amount: The number of items you want in your commodityDeedBox.
# resourceBoxPage: (Optional) The gump has multiple pages. Starts at 0. Most items are on page 0.
resources = [
    RestockItem(BLACKPEARL, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 100, 10000),
    RestockItem(BLOODMOSS, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 101, 10000),
    RestockItem(GARLIC, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 102, 10000),
    RestockItem(GINSENG, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 103, 10000),
    RestockItem(MANDRAKEROOT, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 104, 10000),
    RestockItem(NIGHTSHADE, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 105, 10000),
    RestockItem(SULPHUROUSASH, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 106, 10000),
    RestockItem(SPIDERSILK, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 107, 10000),
    RestockItem(BATWING, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 108, 10000),
    RestockItem(GRAVEDUST, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 109, 10000),
    RestockItem(DAEMONBLOOD, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 110, 10000),
    RestockItem(NOXCRYSTAL, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 111, 10000),
    RestockItem(PIGIRON, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 112, 10000),
    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_DEFAULT, woodResourceBoxSerial, 107, 10000),
    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_OAK, woodResourceBoxSerial, 108, 10000),
    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_ASH, woodResourceBoxSerial, 109, 10000),
    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_YEW, woodResourceBoxSerial, 110, 10000),
    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_HEARTWOOD, woodResourceBoxSerial, 111, 10000),
    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_BLOODWOOD, woodResourceBoxSerial, 112, 10000),
    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_FROSTWOOD, woodResourceBoxSerial, 113, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_DEFAULT, ingotResourceBoxSerial, 101, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_DULL_COPPER, ingotResourceBoxSerial, 101, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_SHADOW_IRON, ingotResourceBoxSerial, 102, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_COPPER, ingotResourceBoxSerial, 103, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_BRONZE, ingotResourceBoxSerial, 104, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_GOLD, ingotResourceBoxSerial, 105, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_AGAPITE, ingotResourceBoxSerial, 106, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_VERITE, ingotResourceBoxSerial, 107, 10000),
    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_VALORITE, ingotResourceBoxSerial, 108, 10000),
    RestockItem(CLOTH_STATIC_ID, RESOURCE_HUE_DEFAULT, leatherResourceBoxSerial, 111, 10000),
    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_DEFAULT, leatherResourceBoxSerial, 100, 10000),
    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_SPINED, leatherResourceBoxSerial, 101, 10000),
    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_HORNED, leatherResourceBoxSerial, 102, 10000),
    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_BARBED, leatherResourceBoxSerial, 103, 10000)
]

# Stand near resource boxes and load everything from a resource box into a real container.
# This is useful for use in conjunction with the BODBuilder.
# InsaneUO specific.
run_restocker(
    # Green commodity deed box. Can be any container that can hold weight though.
    commodityBoxSerial,
    
    # An array of RestockItem, the resources you want to stock. This is how you configure it.
    # Include only those resources you wish to stock, the hue, the amount, the  gump button id, and page.
    # Page is the page on the gump menu.
    resources,
    
    # Time to wait between item moves. Adjust with caution. Reducing this will increase speed
    # of the script, but you risk disconnects and other issues maintaining state
    itemMoveDelayMs = 1000, 
    
    # (Optional) Timeout between  gump button presses. Configure based on server latency.
    gumpDelayMs = 250
)