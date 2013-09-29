FTL_editor
==========

A toolset to edit FTL savegame (Faster Than Light )


Death is part of fun. That is tru. but they are another thing that could to be fun… cheat… :-)

This tool allow to edit savegame and set amount of:
- life
- fuel
- missile
- drore
- scrap

Usage
==========

Launch FTL game and start a new game.
Into hangar choose your ship and difficulty… click to start.
Press escape and choose 'Save and Exit'.

Now you can use FTL_editor, They are two mode:
- interactive mode:
Run FTL_editor without argument. The tool will ask what do you want to set.

```
$ ./FTL_editor
Current health: 30
Current fuel: 16
Current drone: 0
Current missile: 0
Current scrap: 10
1/ Set Health
2/ Set Fuel
3/ Set number of drones
4/ Set number of missiles
5/ Set number of Scrap
6/ Exit
choice: 2
Current fuel: 16
fuel:500
1/ Set Health
2/ Set Fuel
3/ Set number of drones
4/ Set number of missiles
5/ Set number of Scrap
6/ Exit
choice: 6
```
- directly from commad line:
By using argument to set amount

```
$ ./FTL_editor --life 30 --fuel 500 --drone 500 --missile 500 --scrap 5000
```
