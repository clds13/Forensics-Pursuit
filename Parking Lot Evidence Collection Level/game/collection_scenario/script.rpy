################################################################################
## Parking Lot Evidence Collection - Script
##
## This file contains the establishing scene (Nina briefing the player over the
## rainy parking lot) and the hand-off into the interactive "look around" scene.
##
## All code specific to this level lives under the collection_scenario folder.
## The reusable rain effect, navigation screen and evidence screens live in
## collection_scenario/custom_screens.rpy.
################################################################################

init python:
    import json

    # Tools used in the knife collection subscene are loaded here so they are
    # ready to be dropped into the inventory side bar when the player starts
    # collecting the knife. See collection_scenario/knife_collection.rpy.
    knife_tools = load_items("jsons/knife_tools.json")


# Nina is the forensics mentor character. image="nina" lets the say screen pull
# in the matching side portrait (side nina <expression>) automatically.
define n = Character(name=("Nina"), image="nina")
image parking_lot = "parking_lot.png"


## Navigation state ############################################################
##
## The four cubemap faces we can look at, and which one we are currently facing.
## Turning left/right with the arrow keys cycles through this list.
default parking_lot_directions = ["north", "east", "south", "west"]
default parking_lot_index = 0


## Establishing scene ##########################################################
label start:
    # NOTE: parking_lot.png (the wide establishing shot of the rainy, empty
    # parking lot) should be dropped into game/images/. It is referenced here as
    # the "parking_lot" background, per the scene brief.
    scene parking_lot
    show rain
    show rain_front
    with dissolve

    show nina normal1
    n "We've just gotten a report of a possible sexual assault and murder case. The victim is a young woman."
    show nina talk
    n "By the time officers arrived, the scene was already exposed and the rain had started coming down."
    show nina normal1
    n "Right now, we're in an abandoned parking lot. That means the environment is actively compromising our evidence."
    show nina talk
    n "Rain is our biggest problem. Bloodstains and other biological fluids on asphalt can dilute, spread, or wash away completely."
    show nina thinknote1
    n "So the order you collect evidence matters. Some items will disappear over time if you don't secure them."
    show nina talk
    n "Every action you take costs time, and waiting too long can destroy evidence that we only get one chance to collect."
    show nina normal1
    n "Your priorities are simple: document what you see, collect what the rain will destroy first, and package it properly so it stays usable later."
    show nina talk
    n "If you rush and contaminate evidence, it's just as bad as losing it."
    show nina thinknote1
    n "When you enter the scene, the timer starts. Use your tools carefully, and think before you commit to an action."
    show nina normal1
    n "Use the LEFT and RIGHT arrow keys to look around the parking lot. Let's get to work."

    hide nina
    hide rain_front
    hide rain
    with dissolve


## Interactive look-around scene ###############################################
label investigate:
    # Draw the rainy parking lot the player can turn around in. The screen draws
    # the current cubemap face, the rain, and the evidence for that direction.
    call screen parking_lot_scene