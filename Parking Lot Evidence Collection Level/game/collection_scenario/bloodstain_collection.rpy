################################################################################
## Parking Lot Evidence Collection - Bloodstain Collection Subscene
##
## This subscene mirrors the knife presumptive blood-test workflow:
##   1. Add methanol on swab
##   2. Swab the suspected stain
##   3. Add phenolphthalein
##   4. Add hydrogen peroxide
##
## Difference from the knife sequence: this stain is NOT blood.
## The swab does not turn pink after peroxide is added.
################################################################################


## State #######################################################################
default bloodstain_step = 0
# Which swab image is currently shown in the bloodstain workspace.
default bloodstain_swab_img = ""
# Current instruction shown in the bloodstain workspace header.
default bloodstain_instruction = ""
# Reagent currently selected to be applied on the swab.
default bloodstain_pending_swab_action = ""
# Test units available for preliminary blood testing.
default bloodstain_test_units = 3
# Whether the bloodstain interaction is complete.
default bloodstain_collected = False


## Tool action functions #######################################################
init python:

    def _bs_get(name, fallback=None):
        return getattr(store, name, fallback)

    def _bs_set(name, value):
        setattr(store, name, value)

    def _bloodstain_wrong(hint):
        renpy.notify(hint)

    def _bloodstain_select_for_swab(expected_step, action_name, instruction, wrong_hint):
        if _bs_get("bloodstain_step", 0) == expected_step:
            _bs_set("bloodstain_pending_swab_action", action_name)
            _bs_set("bloodstain_instruction", instruction)
            renpy.notify("Selected. Now click the swab.")
        else:
            _bloodstain_wrong(wrong_hint)

    def bloodstain_use_methanol():
        _bloodstain_select_for_swab(
            0,
            "methanol",
            "Methanol selected. Click the swab to wet it.",
            "That isn't the next step right now.",
        )

    def bloodstain_use_phenol():
        _bloodstain_select_for_swab(
            2,
            "phenol",
            "Phenolphthalein selected. Click the swab to apply it.",
            "Add phenolphthalein only after the swab has touched the stain.",
        )

    def bloodstain_use_peroxide():
        _bloodstain_select_for_swab(
            3,
            "peroxide",
            "Hydrogen peroxide selected. Click the swab to apply it.",
            "Hydrogen peroxide is the last reagent in the test.",
        )

    def bloodstain_swab_target():
        if _bs_get("bloodstain_step", 0) == 1:
            renpy.jump("bloodstain_step_swabbed")
        else:
            _bloodstain_wrong("That isn't the correct step for swabbing the stain.")

    def bloodstain_apply_to_swab():
        action = _bs_get("bloodstain_pending_swab_action", "")

        if action == "methanol" and _bs_get("bloodstain_step", 0) == 0:
            _bs_set("bloodstain_pending_swab_action", "")
            renpy.jump("bloodstain_step_methanol")
        elif action == "phenol" and _bs_get("bloodstain_step", 0) == 2:
            _bs_set("bloodstain_pending_swab_action", "")
            renpy.jump("bloodstain_step_phenol")
        elif action == "peroxide" and _bs_get("bloodstain_step", 0) == 3:
            _bs_set("bloodstain_pending_swab_action", "")
            renpy.jump("bloodstain_step_peroxide_negative")
        elif action:
            _bloodstain_wrong("That reagent can't be applied at this stage.")
        else:
            _bloodstain_wrong("Select a tool first, then click the swab.")

    def bloodstain_load_presumptive_tools():
        toolbox.reset_inventory()

        # Reuse the knife tool visuals/descriptions, but bind bloodstain actions.
        source = knife_tools
        toolbox.add_to_inventory(Item(source["Methanol"].name, source["Methanol"].image_name, source["Methanol"].description, True, bloodstain_use_methanol))
        toolbox.add_to_inventory(Item(source["Phenolphthalein"].name, source["Phenolphthalein"].image_name, source["Phenolphthalein"].description, True, bloodstain_use_phenol))
        toolbox.add_to_inventory(Item(source["Hydrogen Peroxide"].name, source["Hydrogen Peroxide"].image_name, source["Hydrogen Peroxide"].description, True, bloodstain_use_peroxide))


## Workspace screen ############################################################
screen bloodstain_workspace():
    add "parking_lot_east" at parking_lot_bg

    add "rain"
    add "rain_front"

    imagebutton:
        xpos 0.25
        ypos 0.955
        anchor (0.5, 1.0)
        focus_mask True
        sensitive knife_interactions_enabled
        idle Transform("bloodstain", zoom=0.88, yzoom=0.42, alpha=0.90)
        hover Transform("bloodstain", zoom=0.88, yzoom=0.42, alpha=1.0, matrixcolor=BrightnessMatrix(0.25))
        hovered Notify("Bloodstain")
        unhovered Notify("")
        action Function(bloodstain_swab_target)

    if bloodstain_swab_img != "":
        imagebutton:
            idle Transform(bloodstain_swab_img, zoom=0.5)
            hover Transform(bloodstain_swab_img, zoom=0.5, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.92
            yalign 0.5
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Swab")
            unhovered Notify("")
            action Function(bloodstain_apply_to_swab)


## Subscene flow ###############################################################
label bloodstain_collect:
    $ default_mouse = ''
    $ knife_dialogue_style = True
    $ knife_interactions_enabled = False
    scene parking_lot_east at parking_lot_bg
    show screen bloodstain_workspace
    with dissolve

    n normal1 "This stain looks like blood, so we'll run a preliminary blood test before making assumptions."
    n talk "You have 3 preliminary test units. We'll use one unit for this stain."
    n normal1 "Follow the same Kastle-Meyer order: methanol, swab, phenolphthalein, then hydrogen peroxide."
    with dissolve

    $ bloodstain_step = 0
    $ bloodstain_swab_img = "clean swab"
    $ bloodstain_pending_swab_action = ""
    $ bloodstain_instruction = "Use the Methanol from your toolbox to wet the swab."
    $ bloodstain_load_presumptive_tools()
    $ selected_inventory = toolbox
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label bloodstain_step_methanol:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ bloodstain_step = 1
    $ bloodstain_pending_swab_action = ""
    $ bloodstain_instruction = "Click the bloodstain to swab it."
    n normal1 "Methanol added. The swab is ready to lift residue from the stain."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label bloodstain_step_swabbed:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ bloodstain_step = 2
    $ bloodstain_swab_img = "red swab"
    $ bloodstain_pending_swab_action = ""
    $ bloodstain_instruction = "Use the Phenolphthalein on the swab."
    n normal1 "The swab picked up red residue. Now add phenolphthalein."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label bloodstain_step_phenol:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ bloodstain_step = 3
    $ bloodstain_pending_swab_action = ""
    $ bloodstain_instruction = "Use the Hydrogen Peroxide on the swab."
    n normal1 "Phenolphthalein applied. Add hydrogen peroxide for the reaction check."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label bloodstain_step_peroxide_negative:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ bloodstain_pending_swab_action = ""
    $ bloodstain_step = 4
    $ bloodstain_swab_img = "red swab"
    $ bloodstain_test_units = max(0, bloodstain_test_units - 1)
    $ bloodstain_instruction = "No pink reaction observed."

    n normal1 "No pink color change."
    n talk "Negative presumptive result: this stain is not blood."
    n normal1 "We'll document it as a blood-like stain and continue with other evidence."
    $ renpy.notify("Preliminary blood test units remaining: %d" % bloodstain_test_units)

    python:
        bloodstain_collected = True
        evidence.add_to_inventory(
            Item(
                "Bloodstain Test Swab (Negative)",
                "red swab",
                "Swab from a suspected bloodstain in the parking lot. Kastle-Meyer presumptive test was negative (no pink reaction).",
            )
        )

    hide screen inventory
    hide screen bloodstain_workspace
    $ knife_dialogue_style = False
    scene parking_lot_east at parking_lot_bg
    with dissolve

    # Return to east-facing view where the bloodstain hotspot is now cleared.
    $ parking_lot_index = 1
    jump investigate
