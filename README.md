### Ultima Online Razor Enhanced Script Library

These are scripts I've either written, liberally modified, or just stored for safekeeping (these are the good ones written by others). They have been tested on a few free shards:

* UOAlive
* InsaneUO

They may or may not work on others.

### Setup

You can safely clone this repo or just manually copy *ALL* of the files into your razord enhanced scripts directory. I have these organized as follows:

RazorInstallDirectory/Scripts

* fm_core -> This is framework stuff I've written (for the most part). These don't do anything on their own. You'll need to make a script that calls these functions (see fm_tools for examples).
* fm_tools -> This is the stuff you'll use. Modify these. Configure them. Bind them to keys.
* fm_train -> Standalone scripts used for training skills.

So basically look through *fm_tools* and modify those scripts. You can store your scripts in whatever folder you like.

### Usage

Useful things you'll find:

A highly configurable **Dexer Attack Loop** that supports some chiv, necro and shield bash stuff. More to come later, I just don't really play other builds.

A rather inefficient **Caster Attack Loop**. Good for mage tamer and InsaneUO specific focused necro caster.

A couple of **resource gathering** scripts. Use with caution. Don't break any rules. Includes fishing on a boat, lumberjacking, and mining.

**BOD Builder** script to automate crafting and filling small bods. Highly configurable. Should support all crafting professions (currently just blacksmithy).

**Move Items** scripts to put things in various containers. I bind about 3 of these to the M key (shift + M,alt + M) lots of use cases.

**Automated character movement** script that uses the rails framework. Several default routes already established. You can easily add your own, it's just a list of x, y coordinates. Use this in conjunction with dexer / caster loops for maximum farming. For the love of all that is holy, use while you're at your machine supervising. You will get banned.

**Character Stats** is a standalone tool that will have some details on character stats from item properties. Just bind it to a key and run it when you want to see all your properties like resists, HCI, SDI, etc. Note that it does get a little wonkie sometimes and you'll have to close and re-open your paperdoll. This script will tell you when it needs to be done (has something to do with item caching in the client / razor). You can find this at *fm_tools/CharacterStats.py*. 

**Shadowguard** script from Dorana. Just keeping a copy. This thing is amazing. Dear god.

**Lootmaster** script from Dorana. Just keeping a copy for posterity.

### Credits

I wrote some of this stuff. Others I am just storing for safekeeping. These were acquired via discord or github. All credit goes to original authors.

#### Warning

There are some powerful features here. Use with care. Don't be a jackass.
