### Ultima Online Razor Enhanced Script Library

These are scripts I've either written, liberally modified, or just stored for safekeeping (these are the good ones written by others). They have been tested on a few free shards:

* UOEX
* UOAlive
* InsaneUO

They may or may not work on others.

### Setup

You can safely clone this repo or just manually copy the files into your razord enhanced scripts directory. I have these organized as follows:

RazorInstallDirectory/Scripts

* fm_core -> This is framework stuff I've written (for the most part). These don't do anythign on their own. You'll need to make a script that calls these functions (see fm_examples).
* fm_tools -> Standalone tools and things you can just bind a hotkey and use.
* fm_examples -> Sample usage of core framework. These are what you'd bind to a hotkey.
* fm_train -> Standalone scripts used for training skills.

So basically look through examples and modify those scripts. You can store your scripts in whatever folder you like.

### Usage

Useful things that you'll find here.

A highly configurable **Melee Attack Loop** can be found by looking at *fm_examples/AttackDexLoop.py*. This can be heavily customized, so be sure to read the options available in *fm_core/core_attack.py*.

A **Multi Pet Vet** loop will heal / rez pets around you. Just plug in some serials. See: *fm_examples/PetVetLoop.py*. Turn it on, stand near your pet, and make sure you have bandages.

**Leash Pets** will leash all your pets around you. Just plug in pet serials. See: *fm_examples/LeashAllPets.py*.

**Character Stats** is a standalone tool that will have some details on character stats from item properties. Just bind it to a key and run it when you want to see all your properties like resists, HCI, SDI, etc. Note that it does get a little wonkie sometimes and you'll have to close and re-open your paperdoll. This script will tell you when it needs to be done (has something to do with item caching in the client / razor). You can find this at *fm_tools/CharacterStats.py*.

I found this **Lootmaster** script from Discord on UO Alive. I think its a little easier to use than the Razor Enhanced looter. We really need a public database of loot profiles because they are very time consuming to configure. Find it at *fm_tools/Lootmaster.cs* and set it to auto start. You'll have to do some configuration to make it work. I think there's a link to the original author and maybe a guide on how to use it.

### Credits

I wrote some of this stuff. Others I am just storing for safekeeping. These were acquired via discord or github. All credit goes to original authors.

#### Warning

There are some powerful features here. Use with care. Don't be a jackass.
