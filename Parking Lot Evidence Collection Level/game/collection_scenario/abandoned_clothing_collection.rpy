################################################################################
## Parking Lot Evidence Collection - Abandoned Clothing Packaging Subscene
##
## This subscene copies the knife packaging flow structure:
##   1. Place evidence in a paper evidence bag and label it
##   2. Seal with tamper-evident tape
################################################################################


## State #######################################################################
default abandoned_clothing_step = 0
# Instruction text shown at the top of the workspace.
default abandoned_clothing_instruction = ""
# Selected tool waiting to be applied to a target.
default abandoned_clothing_pending_action = ""
# Visual state of the evidence bag.
default abandoned_clothing_bag_state = 0
# Whether this evidence piece has been fully packaged.
default abandoned_clothing_collected = False


## Tool action functions #######################################################
init python:

    def _ac_get(name, fallback=None):
        return getattr(store, name, fallback)

    def _ac_set(name, value):
        setattr(store, name, value)

    def _abandoned_clothing_wrong(hint):
        renpy.notify(hint)

    def abandoned_clothing_use_bag():
        if _ac_get("abandoned_clothing_step", 0) == 0:
            _ac_set("abandoned_clothing_pending_action", "bag")
            _ac_set("abandoned_clothing_instruction", "Paper evidence bag selected. Click the clothing to place it in the bag.")
            renpy.notify("Selected. Now click the clothing.")
        else:
            _abandoned_clothing_wrong("The bag is not needed at this stage.")

    def abandoned_clothing_use_tape():
        if _ac_get("abandoned_clothing_step", 0) == 1:
            _ac_set("abandoned_clothing_pending_action", "tape")
            _ac_set("abandoned_clothing_instruction", "Tamper tape selected. Click the evidence bag to seal it.")
            renpy.notify("Selected. Now click the evidence bag.")
        else:
            _abandoned_clothing_wrong("There's nothing sealed to tape shut yet.")

    def abandoned_clothing_click_item():
        if _ac_get("abandoned_clothing_step", 0) == 0 and _ac_get("abandoned_clothing_pending_action", "") == "bag":
            _ac_set("abandoned_clothing_pending_action", "")
            renpy.jump("abandoned_clothing_step_bag")
        else:
            _abandoned_clothing_wrong("Select the paper evidence bag first, then click the clothing.")

    def abandoned_clothing_click_bag():
        if _ac_get("abandoned_clothing_step", 0) == 1 and _ac_get("abandoned_clothing_pending_action", "") == "tape":
            _ac_set("abandoned_clothing_pending_action", "")
            renpy.jump("abandoned_clothing_step_tape")
        else:
            _abandoned_clothing_wrong("Select tamper-evident tape first, then click the bag.")

    def abandoned_clothing_load_packaging_tools():
        toolbox.reset_inventory()

        source = knife_tools
        toolbox.add_to_inventory(Item(source["Paper Evidence Bag"].name, source["Paper Evidence Bag"].image_name, source["Paper Evidence Bag"].description, True, abandoned_clothing_use_bag))
        toolbox.add_to_inventory(Item(source["Tamper Evident Tape"].name, source["Tamper Evident Tape"].image_name, source["Tamper Evident Tape"].description, True, abandoned_clothing_use_tape))


## Workspace screen ############################################################
screen abandoned_clothing_workspace():
    add "parking_lot_west" at parking_lot_bg

    add "rain"
    add "rain_front"

    if abandoned_clothing_bag_state == 0:
        imagebutton:
            xpos 0.58
            ypos 0.95
            anchor (0.5, 1.0)
            focus_mask True
            sensitive knife_interactions_enabled
            idle Transform("abandoned_clothing", zoom=0.84, yzoom=0.58, alpha=0.82, rotate=-6)
            hover Transform("abandoned_clothing", zoom=0.84, yzoom=0.58, alpha=1.0, rotate=-6, matrixcolor=BrightnessMatrix(0.25))
            hovered Notify("Scattered Clothing")
            unhovered Notify("")
            action Function(abandoned_clothing_click_item)

    if abandoned_clothing_bag_state >= 1:
        imagebutton:
            idle Transform("toolbox-evidence_bag", zoom=2.15)
            hover Transform("toolbox-evidence_bag", zoom=2.15, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.62
            yalign 0.44
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Paper Evidence Bag")
            unhovered Notify("")
            action Function(abandoned_clothing_click_bag)

    if abandoned_clothing_bag_state >= 2:
        add Transform("toolbox-tamper_evident_tape", zoom=1.48, rotate=-14, xalign=0.62, yalign=0.36)


## Subscene flow ###############################################################
label abandoned_clothing_collect:
    $ default_mouse = ''
    $ knife_dialogue_style = True
    $ knife_interactions_enabled = False
    scene parking_lot_west at parking_lot_bg
    show screen abandoned_clothing_workspace
    with dissolve

    n normal1 "This clothing item can hold trace and biological evidence, so we'll package it as-is."
    n talk "Follow chain-of-custody packaging: bag it, label it, then seal it with tamper-evident tape."

    $ abandoned_clothing_step = 0
    $ abandoned_clothing_pending_action = ""
    $ abandoned_clothing_bag_state = 0
    $ abandoned_clothing_instruction = "Use the Paper Evidence Bag, then click the clothing to package it."
    $ abandoned_clothing_load_packaging_tools()
    $ selected_inventory = toolbox
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label abandoned_clothing_step_bag:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ abandoned_clothing_step = 1
    $ abandoned_clothing_bag_state = 1
    $ abandoned_clothing_instruction = "Use the Tamper Evident Tape to seal the bag."
    n normal1 "The clothing is now in a paper evidence bag. Label it with:"
    n talk "Your initials, time collected, location, case number, and exhibit number."
    n normal1 "This preserves chain of custody and keeps the evidence admissible."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label abandoned_clothing_step_tape:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ abandoned_clothing_step = 2
    $ abandoned_clothing_bag_state = 2
    n normal1 "Sealed with tamper-evident tape. The abandoned clothing is now properly packaged."

    python:
        abandoned_clothing_collected = True
        evidence.add_to_inventory(
            Item(
                "Abandoned Clothing (Packaged)",
                "inventory-evidence_bag",
                "Scattered clothing from the parking lot, packaged in a labelled paper evidence bag and sealed with tamper-evident tape.",
            )
        )

    hide screen inventory
    hide screen abandoned_clothing_workspace
    $ knife_dialogue_style = False
    scene parking_lot_west at parking_lot_bg
    with dissolve

    # Return to west-facing view where the hotspot is now cleared.
    $ parking_lot_index = 3
    jump investigate
