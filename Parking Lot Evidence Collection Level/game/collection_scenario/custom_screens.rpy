################################################################################
## Parking Lot Evidence Collection - Custom Screens
##
## This file contains all of the custom screens and displayables used in the
## parking lot evidence collection scene:
##   - The rain weather effect (SnowBlossom)
##   - The 360 degree "look around" navigation screen (left/right arrow keys)
##   - The reusable evidence_piece screen used to scatter and highlight evidence
################################################################################


## Rain effect #################################################################
##
## The rain is built with Ren'Py's SnowBlossom particle effect. The raindrop.png
## asset is a single, semi-transparent raindrop. To make it read as realistic
## rain (long streaks falling almost straight down) we:
##   - stretch the drop vertically (yzoom) and thin it out (xzoom) into a streak
##   - tilt it very slightly (rotate) and give it a small horizontal speed so it
##     falls at a believable angle rather than perfectly vertical
##   - give it a high downward yspeed so the streaks fall quickly
##   - use a high count and fast=True so the whole screen is full of rain
##     immediately when the scene appears

image rain_streak = Transform("raindrop.png", xzoom=0.04, yzoom=0.75, alpha=0.42)
image rain = SnowBlossom("rain_streak", count=350, xspeed=(0, 15), yspeed=(1400, 2000), start=0, fast=True)

# A second, closer rain layer makes rainfall visually obvious while keeping
# the base rain behavior realistic.
image rain_front_streak = Transform("raindrop.png", xzoom=0.07, yzoom=1.25, alpha=0.62)
image rain_front = SnowBlossom("rain_front_streak", count=220, xspeed=(3, 22), yspeed=(1650, 2300), start=0, fast=True)


## Background transform ########################################################
##
## The cubemap faces are 2048x2048. This transform scales them so they cover the
## full 1920x1080 screen (cropping the top/bottom evenly) and keeps them centered.

transform parking_lot_bg:
    zoom 0.94
    xalign 0.5
    yalign 0.5


## Evidence piece ##############################################################
##
## A reusable screen for a single scattered piece of evidence on the ground.
## Hovering over the evidence brightens it (a "highlight") using BrightnessMatrix
## - the standard Ren'Py matrixcolor function - and pops up its name via Notify,
## matching the hover feedback used in the other evidence collection levels.
##
##   image_name : the auto-defined image for the evidence asset
##   ev_name    : the human readable name shown when hovered/clicked
##   xpos_, ypos_ : screen-relative position of the evidence on the ground
##   zoom_      : how much to scale the evidence asset down

screen evidence_piece(image_name, ev_name, xpos_, ypos_, zoom_=0.55, yflatten_=0.8, alpha_=0.84, rotate_=0, click_action=None):
    imagebutton:
        xpos xpos_
        ypos ypos_
        anchor (0.5, 1.0)
        focus_mask True

        idle Transform(image_name, zoom=zoom_, yzoom=yflatten_, alpha=alpha_, rotate=rotate_)
        hover Transform(image_name, zoom=zoom_, yzoom=yflatten_, alpha=1.0, rotate=rotate_, matrixcolor=BrightnessMatrix(0.25))

        hovered Notify(ev_name)
        unhovered Notify("")

        action (click_action if click_action is not None else Notify("You spotted the " + ev_name + "."))


## Parking lot look-around screen ##############################################
##
## Displays the cubemap face for the direction the player is currently facing,
## with the rain overlaid on top, and the single piece of evidence that belongs
## to that direction. The player turns left/right with the arrow keys, which
## cycles through north -> east -> south -> west.

screen parking_lot_scene():
    # Background for the current direction.
    add ("parking_lot_" + parking_lot_directions[parking_lot_index]) at parking_lot_bg

    # Rain falls over the scene, exactly as in the establishing shot.
    add "rain"
    add "rain_front"

    # Scatter one piece of evidence per direction, placed on the ground.
    if parking_lot_directions[parking_lot_index] == "north":
        if not knife_collected:
            # Single knife hotspot routes to whichever procedure is not yet done.
            imagebutton:
                xpos 0.65
                ypos 1.08
                anchor (0.5, 1.0)
                focus_mask True
                idle Transform("knife_fingerprint_blurry", zoom=0.78, yzoom=1.08, rotate=25)
                hover Transform("knife_fingerprint_blurry", zoom=0.78, yzoom=1.08, rotate=25, matrixcolor=BrightnessMatrix(0.25))
                hovered Notify("Knife - Click to continue evidence collection")
                unhovered Notify("")
                action Function(knife_route_to_procedure)

    elif parking_lot_directions[parking_lot_index] == "east":
        if not bloodstain_collected:
            use evidence_piece(
                "bloodstain",
                "Bloodstain - Click to test",
                0.25,
                0.955,
                0.88,
                0.42,
                0.90,
                0,
                click_action=Jump("bloodstain_collect"),
            )
    elif parking_lot_directions[parking_lot_index] == "south":
        if not ski_mask_collected:
            use evidence_piece(
                "ski_mask",
                "Ski Mask - Click to process",
                0.44,
                0.94,
                0.55,
                0.60,
                0.86,
                10,
                click_action=Jump("ski_mask_collect"),
            )
    elif parking_lot_directions[parking_lot_index] == "west":
        if not abandoned_clothing_collected:
            use evidence_piece(
                "abandoned_clothing",
                "Scattered Clothing - Click to package",
                0.58,
                0.95,
                0.84,
                0.58,
                0.82,
                -6,
                click_action=Jump("abandoned_clothing_collect"),
            )

    # A small compass hint so the player knows which way they are facing.
    frame:
        background "#0006"
        xalign 0.5
        ypos 30
        padding (20, 8)
        text ("Facing: " + parking_lot_directions[parking_lot_index].capitalize()):
            size 28
            color "#fff"

    # Turn left/right with the arrow keys to look around the parking lot.
    key "K_LEFT" action SetVariable("parking_lot_index", (parking_lot_index - 1) % 4)
    key "K_RIGHT" action SetVariable("parking_lot_index", (parking_lot_index + 1) % 4)
