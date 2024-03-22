import clr
clr.AddReference ('System.Windows.Forms')
clr.AddReference('System.Drawing')
import re
from System.Drawing import Color, Font, FontStyle, FontFamily
from System.Drawing import Point
from System.Windows.Forms import TextBox, Keys, KeyPressEventHandler, DataGridView, DataGridViewHeaderBorderStyle
from System.Windows.Forms import DataGridViewCellBorderStyle, ColumnStyle, SizeType, RowStyle, GroupBox
from System.Windows import Forms

# This script is easy. Just bind it to a hotkey in razor and run it. No modifications needed.
# Will display a summary of character stats with some contextual help. Tested on UOEX, UOAlive, 
# and InsaneUO.
#
# The fact that this stuff isnt baked into clients (all the fun weapon hits and thresholds)
# is an absolute outrage and warrants federal investigation. Until then, behold.
class CharacterStats(Forms.Form):
    
    INNER_CONTENT_WIDTH = 700        
    
    def __init__(self):
        #Misc.RemoveSharedValue("character_stats_rule_select")
        #self.stats = self.getStatsFromItems()
        
        self.GROUP_BOX_WIDTH = 750
        
        # Main UI Screen
        self.Width = 810
        self.Height = 1100
        self.Text = 'Character Stats by fatman'
        
        # Server rules box
        self.serverRulesBox = Forms.GroupBox()
        self.serverRulesBox.Text = "Server Rules"
        self.serverRulesBox.Location = Point( 25, 25)
        self.serverRulesBox.Width = self.GROUP_BOX_WIDTH
        self.serverRulesBox.Height = 100      
        self.drawServerRulesBox()
        self.Controls.Add(self.serverRulesBox)
        
        # Hits, Mana, etc. basic stats box
        self.charStatsBox = Forms.GroupBox()
        self.charStatsBox.Text = "Char Stats"
        self.charStatsBox.Location = Point( 25, 150)
        self.charStatsBox.Width = self.GROUP_BOX_WIDTH
        self.charStatsBox.Height = 125
        self.Controls.Add(self.charStatsBox)
        self.drawCharStatsBox()        

        # Resists Box
        self.charResistsBox = Forms.GroupBox()
        self.charResistsBox.Text = "Resists"
        self.charResistsBox.Location = Point( 25, 300)
        self.charResistsBox.Width = self.GROUP_BOX_WIDTH
        self.charResistsBox.Height = 75
        self.drawCharResistsBox()
        self.Controls.Add(self.charResistsBox)
        
        # Main Item Stats, this is the reason were doing this
        self.itemStatsBox = Forms.GroupBox()
        self.itemStatsBox.Text = "Item Stats"
        self.itemStatsBox.Location = Point( 25, 400)
        self.itemStatsBox.Width = self.GROUP_BOX_WIDTH
        self.itemStatsBox.Height = 575
        #self.drawItemStatsBox()
        self.Controls.Add(self.itemStatsBox)
        
        # Close button
        my_button = Forms.Button(Text='CLOSE')
        my_button.Click += self.MyOnClick
        my_button.Location = Point(200, 995)
        my_button.Width = 400
        my_button.Height = 50
        self.Controls.Add(my_button)
    
    def getStatsFromItems(self):
        
        LAYERS = [ "RightHand", "LeftHand", "Shoes", "Pants", "Shirt", "Head", "Gloves", "Ring", "Neck", "Hair", "Waist", "InnerTorso", "Bracelet", "FacialHair", "MiddleTorso", "Earrings", "Arms", "Cloak", "OuterTorso", "OuterLegs", "InnerLegs", "Talisman" ]
        #LAYERS = [ "RightHand", "LeftHand", "Shoes", "Pants", "Shirt", "Head", "Gloves", "Ring", "Neck", "Hair", "Waist", "InnerTorso", "Bracelet", "MiddleTorso", "Earrings", "Arms", "Cloak", "OuterTorso", "OuterLegs", "InnerLegs", "Talisman" ]
        #LAYERS = [ "Ring"]
        
        #WEAPON_LAYERS = [ "RightHand", "LeftHand" ]
        
        # https://www.uoex.net/wiki/Stat_Caps
        # https://uo.com/wiki/ultima-online-wiki/items/magic-item-properties/
        stats = [
        
            # Stats
            { "name": "Strength Bonus", "value": 0, "max": 150, "group_name": "Stats", "description": "Increases your Strength Stat by the number of points on the item"  },
            { "name": "Intelligence Bonus", "value": 0, "max": 150, "group_name": "Stats", "description": "Increases your Intelligence Stat by the number of points on the item."  },
            { "name": "Dexterity Bonus", "value": 0, "max": 150, "group_name": "Stats", "description": "Increases your Dexterity Stat by the number of points on the item"  },
            { "name": "Stamina Increase", "value": 0, "max": 0, "group_name": "Stats", "description": "Increases your maximum stamina by the number of points on the item."  },        
            { "name": "Stamina Regeneration", "value": 0, "max": 24, "max_uoex": 40, "group_name": "Stats", "description": "Increases the rate at which you regain stamina. (0.1 point per second per point of SR.)\n\nUOEX: All regens have a diminshing return rate after 35-40 (see wiki). This is with 120 Focus"  },
            { "name": "Hit Point Increase", "value": 0, "max": 25, "group_name": "Stats", "description": "Increases your maximum hit points by the number of points on the item."  },
            { "name": "Hit Point Regeneration", "value": 0, "max": 18, "max_uoex": 55, "group_name": "Stats", "description": "Increases the rate at which you regain hit points. (0.1 hit point per second per hpr point).\n\nUOEX:  All regens have a diminshing return rate after 50-55 (see wiki)."  },
            { "name": "Mana Increase", "value": 0, "max": 0, "group_name": "Stats", "description": "Increases your maximum mana by the number of points on the item."  },
            { "name": "Mana Regeneration", "value": 0, "max": 0, "max_uoex": 35, "group_name": "Stats", "description": "Increases the rate at which you regain mana, subject to diminishing returns. Can be crafted on Spellbooks, maximum intensity of 1.\n\nUOEX: All regens have a diminshing return rate after 30-35 (see wiki). This is with 120 Meditation and 120 Focus"  },
            
            # Melee
            { "name": "Hit Chance Increase", "value": 0, "max": 45, "max_uoex": 70, "group_name": "Melee", "description": "Increases your chance to hit your opponents. If you before Hit Chance Increase is applied have 50% chance to hit, with 20% Hit Chance Increase you will have 60% chance to hit.\n\nUOEX: 70% HCI nullifies any effect from HLA."  },
            { "name": "Swing Speed Increase", "value": 0, "max": 60, "group_name": "Melee", "description": "Increases the base speed at which you swing your weapon. (Maximum swing speed = 1 swing per 1.25 seconds) Affects hit leech properties  (see footnote)\n\nUOEX: 60% cap from gear. Stamina affects swing speed, not dexterity. With 237 stamina, you will swing all weapons at full speed." },
            { "name": "Damage Increase", "value": 0, "max": 100, "group_name": "Melee", "description": "Increases the base damage you inflict with your weapon.  Can be removed from exceptional crafted items by use of Whetstone of Enervation\n\nUOEX:100% Cap from equipment, uncapped otherwise." },
            { "name": "Defense Chance Increase", "value": 0, "max": 45, "max_uoex": 80, "group_name": "Melee", "description": "Increases your chance to dodge blows. If before DCI is applied you have 50% chance to dodge, with 20% DCI you will have 60% chance to dodge.\n\nUOEX:    Divine Fury lowers DCI by 10%. You need 55% to effectively cap this. 80% nullifies any effect from HLA, combined with the -10% from Divine Fury." },
            { "name": "Reflect Physical Damage", "value": 0, "max": 250, "max_uoex": 0, "group_name": "Melee", "description": "Reflect Physical Damage will reflect a percentage of any kinetic physical damage that is inflicted on you back onto the one who inflicted it.\n\nUOEX: Awesome to have if you can take the hits" },
            
            # Magic
            { "name": "Spell Damage Increase", "value": 0, "max": 250, "max_uoex": 0, "group_name": "Magic", "description": "This property increases the damage for most magical attacks that are casted. While the property is normally caped at 20% in PvP, the cap can be further increased to 25% for focused templates.\nFocus templates have no more than 30 modified skill points in mor than one primary skill such as magery, necromancy, mysticism, ninjitsu, bushido, animal taming, musicianship, chivalry or spellweaving.\nAlso no more than 30 modified skill points in the associated secondary skill such as evaluate intelligence, spirit speaking, focus, imbuing.\nExample: magery/eval/inscrip/wrestle is a ‘pure’ mage and will have 25% sdi, adding another of the primary skills listed here, or a secondary skill not \nassociated with your chosen primary, at above 30 skill points reduces the sdi cap back to 20%. Spell damage increase in PvM is 250%.\nThis property is most commonly found on accessories and spellbooks\n\nUOEX: This uncapped for Player Vs. Monster(PvM), but capped at 15% for Player Vs. Player (PvP)" },
            { "name": "Faster Cast Recovery", "value": 0, "max": 6, "group_name": "Magic", "description": "Shortens waiting time between casting spells.\n\nUOEX: Unsure if cap on wep is 6, but you don't need more." },
            { "name": "Faster Casting", "value": 0, "max": 4, "group_name": "Magic", "description": "Decreases the time required to cast  spells by 0.25 seconds per point. Capped at 2 for magery, necromancy & mysticism and 4 for  chivalry (if magery is below 70 skill) and spellweaving .\n\nUOEX: The spell Protection lowers FC by 2. You cannot go over the cap to compensate." },
            { "name": "Lower Mana Cost", "value": 0, "max": 40, "group_name": "Magic", "description": "Lowers the amount of mana needed to cast a spell or use a special move.\n\nUOEX:    GoC Chest/Sleeves/Boots gives 20% LMC. Follower's Sash give 8%."  },
            { "name": "Lower Reagent Cost", "value": 0, "max": 100, "group_name": "Magic", "description": "Lowers the amount of reagents needed to cast spells, both magery and necromancy. 100% negates the need to carry reagents at all. Tithing points, though unused, are required to be available to cast Chivalry spells.\n\nUOEX: Saves you money on regs/tithing." },        
            { "name": "Enhance Potions", "value": 0, "max": 50, "group_name": "Magic", "description": "Increases the effects of potions when they are used. Poison and nightsight potions are excluded."  },

            # Resistances
            { "name": "Physical Resist", "value": 0, "max": 70, "group_name": "Resistances", "description": "Get to 70" },
            { "name": "Fire Resist", "value": 0, "max": 70, "group_name": "Resistances", "description": "Get to 70" },
            { "name": "Cold Resist", "value": 0, "max": 70, "group_name": "Resistances", "description": "Get to 70" },
            { "name": "Poison Resist", "value": 0, "max": 70, "group_name": "Resistances", "description": "Get to 70" },
            { "name": "Energy Resist", "value": 0, "max": 70, "group_name": "Resistances", "description": "Get to 70" },
            
            # Weapon Hits
            { "name": "Hit Life Leech", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "On every successful hit, converts a percentage of the damage inflicted by the attack into hit points for the wielder.\n(If you hit your target for 50 damage with a 60% Hit Life Leech weapon, you have a chance of healing between 0 (50 * 30% * 1% = 0.15) and 9 (50 * 30% * 60%) hit points.)."  },
            { "name": "Hit Stamina Leech", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit to convert 100% of the damage inflicted on the target into stamina for the wielder.\n(If you hit your target for 50 damage, you have a chance of regaining 50 stamina)."  },
            { "name": "Hit Mana Leech", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "On every successful hit, converts a percentage of the damage inflicted by the attack into mana points for the wielder.\n(If you hit your target for 50 damage with a 60% Hit Mana Leech weapon, you have a chance of recovering between 0 (50 * 40% * 1% = 0.2) and 12 (50 * 40% * 60%) mana.)"  },
            { "name": "Hit Lower Attack", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit to lower the hit chance of the target (HCI -25). Approximate duration, 5-10 seconds.\nThe effect does not stack with itself,  percentage hit chance from items is multiplied, not added. example item 1 has 50% hla, item 2 has 30% hla, total hla = 65%"  },
            { "name": "Hit Lower Defense", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit to lower the defensive capabilities of the target(DCI -25). Approximate duration, 5-10 seconds.\nThe effect does not stack with itself,  percentage hit chance from items is multiplied, not added. example item 1 has 50% hld, item 2 has 30% hld, total hld = 65%  In pvp reduces 35% of the target’s maximum DCI."  },
            { "name": "Hit Magic Arrow", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit to cast the magery spell magic arrow on the target."  },
            { "name": "Hit Harm", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit to cast the magery spell harm on the target."  },
            { "name": "Hit Fireball", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit to cast the magery spell fireball on the target."  },
            { "name": "Hit Lightning", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit to cast the magery spell lightning on the target."  },
            { "name": "Hit Dispel", "value": 0, "max": 0, "group_name": "Weapon Hits", "description": "Has a percentage chance on each hit, based on the wielder’s Tactics skill,  to cast the magery spell dispel on any summoned creature."  },
                        
            # Misc.
            { "name": "Luck", "value": 0, "max": 0, "max_uoex": 7200, "group_name": "Misc", "description": "Potentially increases monster loot in 3 ways; a)number of items; b)number of properties; c)intensity of properties." }
        ]        
        
        # UOEX and potentially other servers (dunno) have an item property called "Resistances" that bundles all resists together into a single line.
        # We need to parse that out and put them in their appropriate category.
        regex = '(--|\d+%)* <basefont color=#FFBCB5>(--|\d+%) <basefont color=#B5CBFF>(--|\d+%)* <basefont color=#B5FFC4>(--|\d+%)* <basefont color=#E1B5FF>(--|\d+%)*<basefont color=#ffffff>'
        pattern = re.compile(regex)
        resistMap = {
            "Physical Resist": 1,
            "Fire Resist": 2,
            "Cold Resist": 3,
            "Poison Resist": 4,
            "Energy Resist": 5
        }
        
        for layer in LAYERS:
            item = Player.GetItemOnLayer(layer)
            if item != None:
                # Special handling of Resistances property
                allResistString = Items.GetPropValueString(item.Serial, 'Resistances')
                #Misc.Pause(100)
                match = pattern.match(allResistString)
                for stat in stats:
                    v = Items.GetPropValue(item.Serial, stat['name'])
                    #s = Items.GetPropValueString(item.Serial, stat['name'])
                    #if v > 0:
                        #print("Item: {} Value: {} String: {}".format(item.Name, v, s))
                    #Misc.Pause(100)
                    #stat['value'] = stat['value'] + Items.GetPropValue(item.Serial, stat['name'])
                    stat['value'] = stat['value'] + v
                    #print("Layer: {} Item: {} Property: {} Value: {} Final Value: {}".format(layer, item.Name, stat['name'], v, stat['value']))
                    if match != None and stat['name'] in resistMap:
                        resistValue = match.group(resistMap[stat['name']])
                        if resistValue != "--":
                            stat['value'] = stat['value'] + int(resistValue.replace("%", ""))
        return stats
                        
    def drawCharStatsBox(self):
        charStatsTable = Forms.TableLayoutPanel()
        charStatsTable.Width = CharacterStats.INNER_CONTENT_WIDTH
        charStatsTable.Height = 85
        charStatsTable.Location = Point(25, 25)
        charStatsTable.ColumnCount = 3  
        charStatsTable.RowCount    = 4  
        charStatsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 33))
        charStatsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 33))
        charStatsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 33))
        
        hitPointsLabel = Forms.Label()
        hitPointsLabel.Text = "Hit Points"
        hitPointsLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charStatsTable.Controls.Add(hitPointsLabel , 0, 0) 
        hitPointsValue = Forms.Label()
        hitPointsValue.Text = str(Player.Hits) + " / " + str(Player.HitsMax)
        charStatsTable.Controls.Add(hitPointsValue , 0, 1) 
        
        staminaLabel = Forms.Label()
        staminaLabel.Text = "Stamina"
        staminaLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charStatsTable.Controls.Add(staminaLabel , 1, 0) 
        staminaValue = Forms.Label()
        staminaValue.Text = str(Player.Stam) + " / " + str(Player.StamMax)
        charStatsTable.Controls.Add(staminaValue , 1, 1) 
        
        manaLabel = Forms.Label()
        manaLabel.Text = "Mana"
        manaLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charStatsTable.Controls.Add(manaLabel , 2, 0) 
        manaValue = Forms.Label()
        manaValue.Text = str(Player.Mana) + " / " + str(Player.ManaMax)
        charStatsTable.Controls.Add(manaValue , 2, 1)
        
        strengthLabel = Forms.Label()
        strengthLabel.Text = "Strength"
        strengthLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charStatsTable.Controls.Add(strengthLabel , 0, 2) 
        strengthValue = Forms.Label()
        strengthValue.Text = str(Player.Str)
        charStatsTable.Controls.Add(strengthValue , 0, 3) 
        
        dexterityLabel = Forms.Label()
        dexterityLabel.Text = "Dexterity"
        dexterityLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charStatsTable.Controls.Add(dexterityLabel , 1, 2) 
        dexterityValue = Forms.Label()
        dexterityValue.Text = str(Player.Dex)
        charStatsTable.Controls.Add(dexterityValue , 1, 3)        
        
        intelligenceLabel = Forms.Label()
        intelligenceLabel.Text = "Intelligence"
        intelligenceLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charStatsTable.Controls.Add(intelligenceLabel , 2, 2) 
        intelligenceValue = Forms.Label()
        intelligenceValue.Text = str(Player.Int)
        charStatsTable.Controls.Add(intelligenceValue , 2, 3) 
        
        self.charStatsBox.Controls.Clear()
        self.charStatsBox.Controls.Add(charStatsTable)
        
    def drawCharResistsBox(self):
        charResistsTable = Forms.TableLayoutPanel()
        charResistsTable.Width = CharacterStats.INNER_CONTENT_WIDTH
        charResistsTable.Height = 40
        charResistsTable.Location = Point(25, 25)
        charResistsTable.ColumnCount = 5  
        charResistsTable.RowCount    = 2  
        charResistsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 20))
        charResistsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 20))
        charResistsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 20))
        charResistsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 20))
        charResistsTable.ColumnStyles.Add(ColumnStyle(SizeType.Percent, 20))
        
        physResLabel = Forms.Label()
        physResLabel.Text = "Physical"
        physResLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charResistsTable.Controls.Add(physResLabel , 0, 0) 
        physResValue = Forms.Label()
        physResValue.Text = str(Player.AR)
        charResistsTable.Controls.Add(physResValue , 0, 1) 
        
        fireResLabel = Forms.Label()
        fireResLabel.Text = "Fire"
        fireResLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charResistsTable.Controls.Add(fireResLabel , 1, 0) 
        fireResValue = Forms.Label()
        fireResValue.Text = str(Player.FireResistance)
        charResistsTable.Controls.Add(fireResValue , 1, 1) 
        
        coldResLabel = Forms.Label()
        coldResLabel.Text = "Cold"
        coldResLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charResistsTable.Controls.Add(coldResLabel , 2, 0) 
        coldResValue = Forms.Label()
        coldResValue.Text = str(Player.ColdResistance)
        charResistsTable.Controls.Add(coldResValue , 2, 1)
        
        poisonResLabel = Forms.Label()
        poisonResLabel.Text = "Poison"
        poisonResLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charResistsTable.Controls.Add(poisonResLabel , 3, 0) 
        poisonResValue = Forms.Label()
        poisonResValue.Text = str(Player.PoisonResistance)
        charResistsTable.Controls.Add(poisonResValue , 3, 1)
        
        energyResLabel = Forms.Label()
        energyResLabel.Text = "Energy"
        energyResLabel.Font = Font(FontFamily.GenericSansSerif, 10.0, FontStyle.Bold)
        charResistsTable.Controls.Add(energyResLabel , 4, 0) 
        energyResValue = Forms.Label()
        energyResValue.Text = str(Player.EnergyResistance)
        charResistsTable.Controls.Add(energyResValue , 4, 1)
        
        self.charResistsBox.Controls.Clear()
        self.charResistsBox.Controls.Add(charResistsTable)  
  
    def drawServerRulesBox(self):

        serverRulesLabel = Forms.Label()
        serverRulesLabel.Text = "Pick a server that most closely resemebles yours. This isnt really important. It just gives a hint as to the max allowed value for an item property. Some servers have more relaxed rules as to what is allowed. You can always just edit this python script and change them yourself."
        serverRulesLabel.Width = CharacterStats.INNER_CONTENT_WIDTH
        serverRulesLabel.Height = 30
        serverRulesLabel.Location = Point( 20, 20)
        
        self.ruleRadioNormal = Forms.RadioButton()
        self.ruleRadioNormal.Text = "Normal Rules"
        #self.ruleRadioNormal.IsDefault = True
        self.ruleRadioNormal.Checked = True if Misc.ReadSharedValue("character_stats_rule_select") == "Normal Rules" else False
        
        self.ruleRadioNormal.Location = Point(40, 55)
        
        
        self.ruleRadioUOEX = Forms.RadioButton()
        self.ruleRadioUOEX.Text = "UOEX"
        self.ruleRadioUOEX.Checked = True if Misc.ReadSharedValue("character_stats_rule_select") == "UOEX" else False
        self.ruleRadioUOEX.Location = Point(175, 55)
        
        self.ruleRadioNormal.Click += self.RuleSelect
        self.ruleRadioUOEX.Click += self.RuleSelect        
        
        if not self.ruleRadioNormal.Checked and not self.ruleRadioUOEX.Checked:
            self.ruleRadioNormal.Checked = True
        

        self.serverRulesBox.Controls.Clear()
        self.serverRulesBox.Controls.Add(serverRulesLabel)
        self.serverRulesBox.Controls.Add(self.ruleRadioNormal)
        self.serverRulesBox.Controls.Add(self.ruleRadioUOEX)

    def drawItemPropertyGroup(self, stats, groupName, pointX, pointY):
        
        groupNameLabel = Forms.Label()
        groupNameLabel.Text = groupName
        groupNameLabel.Font = Font(FontFamily.GenericSansSerif, 11.0, FontStyle.Bold)
        groupNameLabel.Width = int(CharacterStats.INNER_CONTENT_WIDTH / 2) - 10
        groupNameLabel.Height = 25
        groupNameLabel.Location = Point( pointX - 5, pointY)
        
        COL_TEXT_WIDTH = 175
        COL_VALUE_WIDTH = 100
        
        table = Forms.TableLayoutPanel()
        table.Width = int(CharacterStats.INNER_CONTENT_WIDTH / 2) - 10
        table.Location = Point(pointX, pointY + 25)
        table.ColumnCount = 2;  
        table.ColumnStyles.Add(ColumnStyle(SizeType.Absolute, COL_TEXT_WIDTH))
        table.ColumnStyles.Add(ColumnStyle(SizeType.Absolute, COL_VALUE_WIDTH))
 
        totalItems = 0
        for key, stat in enumerate(stats):
            if stat['group_name'] != groupName:
                continue
            
            table.RowStyles.Add(RowStyle(SizeType.Absolute, 20));  
            labelText = Forms.Label()
            
            labelText.Text = stat['name']
            labelText.Font = Font(FontFamily.GenericSansSerif, 9.0, FontStyle.Regular)
            labelText.Width = COL_TEXT_WIDTH
            table.Controls.Add(labelText , 0, totalItems) 
            
            labelValue = Forms.Label()
            
            if self.ruleRadioUOEX.Checked and "max_uoex" in stat:
                if stat['max_uoex'] > 0:
                    labelValue.Text = str(stat['value']) + " / " + str(stat['max_uoex'])
                else:
                    labelValue.Text = str(stat['value'])                
            else:
                if stat['max'] > 0:
                    labelValue.Text = str(stat['value']) + " / " + str(stat['max'])
                else:
                    labelValue.Text = str(stat['value'])
            
            tooltip = Forms.ToolTip()
            tooltip.ToolTipTitle = stat['name']
            tooltip.AutomaticDelay = 500000
            tooltip.InitialDelay = 250
            
            tooltip.SetToolTip(labelText, stat['description'])
            labelValue.Width = COL_VALUE_WIDTH
            table.Controls.Add(labelValue , 1, totalItems)
            totalItems = totalItems + 1

        table.Height = totalItems * 20
        self.itemStatsBox.Controls.Add(groupNameLabel)         
        self.itemStatsBox.Controls.Add(table)             
        
        
    def drawItemStatsBox(self):
        self.itemStatsBox.Controls.Clear()
        
        hoverHelpLabel = Forms.Label()
        hoverHelpLabel.Text = "Hover over an item property name for more info"
        hoverHelpLabel.Font = Font(FontFamily.GenericSansSerif, 9.0, FontStyle.Italic)
        hoverHelpLabel.Width = int(CharacterStats.INNER_CONTENT_WIDTH)
        hoverHelpLabel.Height = 25
        hoverHelpLabel.Location = Point( 25, 25)
        self.itemStatsBox.Controls.Add(hoverHelpLabel)    

        stats = self.getStatsFromItems()

        #print(stats)
        
        self.drawItemPropertyGroup(stats, "Stats", 25, 50)
        self.drawItemPropertyGroup(stats, "Weapon Hits", 25, 265)
        self.drawItemPropertyGroup(stats, "Misc", 25, 500)
        
        self.drawItemPropertyGroup(stats, "Resistances", 375, 50)
        self.drawItemPropertyGroup(stats, "Magic", 375, 190)
        self.drawItemPropertyGroup(stats, "Melee", 375, 350)
        
    def RuleSelect(self, *args):
        Misc.SetSharedValue("character_stats_rule_select", args[0].Text)
        self.drawItemStatsBox()
        
    def MyOnClick(self, *args):
        self.Finished()
    
    def OnEnter(self, e, args):
        key = args.KeyChar
        if key == Keys.Enter:
            self.Finished()
            
    def Finished(self):
        self.stats = None
        self.Close()

app = CharacterStats()
Forms.Application.Run(app)