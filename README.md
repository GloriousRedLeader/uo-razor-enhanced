### Ultima Online Razor Enhanced Script Library

These are scripts I've either written, liberally modified, or just stored for safekeeping (these are the good ones written by others). They have been tested on a few free shards:

* UOAlive
* InsaneUO

They may or may not work on others.

### Setup

You can safely clone this repo or just manually copy the files into your razord enhanced scripts directory. I have these organized as follows:

RazorInstallDirectory/Scripts

* fm_core -> This is framework stuff I've written (for the most part). These don't do anything on their own. You'll need to make a script that calls these functions (see fm_examples).
* fm_tools -> This is the stuff you'll use. It doesn't really matter where you put your scripts, but you can reference these as examples. Most of this stuff uses my framework (the files in *fm_core*).
* fm_train -> Standalone scripts used for training skills.

So basically look through *fm_tools* and modify those scripts. You can store your scripts in whatever folder you like.

### Usage

Useful things you'll find:

A highly configurable **Melee Attack Loop** can be found by looking at *fm_tools/DexLoop.py*.

A rather inefficient **Caster Attack Loop** found at *fm_tools/CasterLoop*.

A couple of resource gathering scripts. **Use with caution**. Don't break any rules.

**Character Stats** is a standalone tool that will have some details on character stats from item properties. Just bind it to a key and run it when you want to see all your properties like resists, HCI, SDI, etc. Note that it does get a little wonkie sometimes and you'll have to close and re-open your paperdoll. This script will tell you when it needs to be done (has something to do with item caching in the client / razor). You can find this at *fm_tools/CharacterStats.py*. 

**Lootmaster** script from Dorana. Just keeping a copy for posterity.

### Credits

I wrote some of this stuff. Others I am just storing for safekeeping. These were acquired via discord or github. All credit goes to original authors.

#### Warning

There are some powerful features here. Use with care. Don't be a jackass.
