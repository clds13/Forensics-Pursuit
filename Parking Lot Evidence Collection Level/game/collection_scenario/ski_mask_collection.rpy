################################################################################
## Parking Lot Evidence Collection - Ski Mask Saliva Collection Subscene
##
## Workflow:
##   1. Preliminary saliva test around nose/mouth area
##   2. Swab saliva-rich areas on the mask
##   3. Package and send to the lab
################################################################################


## State #######################################################################
default ski_mask_step = 0
# Tool selected and waiting to be applied.
default ski_mask_pending_action = ""
# Current swab visual shown on the right side of the workspace.
default ski_mask_swab_img = ""
# Packaging visuals.
default ski_mask_vial_state = 0
default ski_mask_bag_state = 0
# Track whether both target areas were swabbed.
default ski_mask_nose_swabbed = False
default ski_mask_mouth_swabbed = False
# During area sampling, the player must click swab first, then mask area.
default ski_mask_swab_armed = False
# Completion flag used by the parking lot screen.
default ski_mask_collected = False


## Tool action functions #######################################################
init python:

    def _sm_get(name, fallback=None):
        return getattr(store, name, fallback)

    def _sm_set(name, value):
        setattr(store, name, value)

    def _ski_mask_wrong(hint):
        renpy.notify(hint)

    def ski_mask_use_saliva_test():
        if _sm_get("ski_mask_step", 0) == 0:
            _sm_set("ski_mask_pending_action", "saliva_test")
            renpy.notify("Selected. Click the mask nose/mouth area to run the preliminary saliva test.")
        else:
            _ski_mask_wrong("Preliminary saliva testing is already done.")

    def ski_mask_use_swabpack():
        if _sm_get("ski_mask_step", 0) == 1:
            _sm_set("ski_mask_pending_action", "")
            renpy.jump("ski_mask_step_take_swab")
        else:
            _ski_mask_wrong("Use a fresh swab after the preliminary saliva test.")

    def ski_mask_use_vial():
        if _sm_get("ski_mask_step", 0) == 4:
            _sm_set("ski_mask_pending_action", "vial")
            renpy.notify("Selected. Click the swab to place it in the vial.")
        else:
            _ski_mask_wrong("Package the swab only after sampling the saliva areas.")

    def ski_mask_use_bag():
        if _sm_get("ski_mask_step", 0) == 5:
            _sm_set("ski_mask_pending_action", "bag")
            renpy.notify("Selected. Click the vial to place it in the evidence bag.")
        else:
            _ski_mask_wrong("The evidence bag is not needed at this stage.")

    def ski_mask_use_tape():
        if _sm_get("ski_mask_step", 0) == 6:
            _sm_set("ski_mask_pending_action", "tape")
            renpy.notify("Selected. Click the evidence bag to seal it.")
        else:
            _ski_mask_wrong("There is nothing ready to seal yet.")

    def ski_mask_click_area(area):
        step = _sm_get("ski_mask_step", 0)
        action = _sm_get("ski_mask_pending_action", "")

        if step == 0 and action == "saliva_test":
            _sm_set("ski_mask_pending_action", "")
            renpy.jump("ski_mask_step_prelim_done")
            return

        if step == 2:
            if not _sm_get("ski_mask_swab_armed", False):
                _ski_mask_wrong("Click the swab first, then click a mask area.")
                return

            if area == "mask":
                if not _sm_get("ski_mask_nose_swabbed", False):
                    area = "nose"
                elif not _sm_get("ski_mask_mouth_swabbed", False):
                    area = "mouth"
                else:
                    _ski_mask_wrong("Both target areas are already swabbed.")
                    return

            if area == "nose":
                if not _sm_get("ski_mask_nose_swabbed", False):
                    _sm_set("ski_mask_nose_swabbed", True)
                    _sm_set("ski_mask_swab_armed", False)
                    _sm_set("ski_mask_swab_img", "red swab")
                    renpy.notify("Nose area swabbed.")
                else:
                    _ski_mask_wrong("Nose area already swabbed. Now swab the mouth area.")
            elif area == "mouth":
                if not _sm_get("ski_mask_mouth_swabbed", False):
                    _sm_set("ski_mask_mouth_swabbed", True)
                    _sm_set("ski_mask_swab_armed", False)
                    _sm_set("ski_mask_swab_img", "red swab")
                    renpy.notify("Mouth area swabbed.")
                else:
                    _ski_mask_wrong("Mouth area already swabbed.")

            if _sm_get("ski_mask_nose_swabbed", False) and _sm_get("ski_mask_mouth_swabbed", False):
                renpy.jump("ski_mask_step_swab_complete")
            return

        _ski_mask_wrong("That isn't the correct step for the mask area.")

    def ski_mask_apply_to_swab():
        step = _sm_get("ski_mask_step", 0)

        if step == 2:
            _sm_set("ski_mask_swab_armed", True)
            renpy.notify("Swab ready. Now click the nose or mouth area on the mask.")
        elif step == 4 and _sm_get("ski_mask_pending_action", "") == "vial":
            _sm_set("ski_mask_pending_action", "")
            renpy.jump("ski_mask_step_vial")
        else:
            _ski_mask_wrong("Select the plastic vial first, then click the swab.")

    def ski_mask_apply_to_target(target):
        step = _sm_get("ski_mask_step", 0)
        action = _sm_get("ski_mask_pending_action", "")

        if target == "vial" and step == 5 and action == "bag":
            _sm_set("ski_mask_pending_action", "")
            renpy.jump("ski_mask_step_bag")
        elif target == "bag" and step == 6 and action == "tape":
            _sm_set("ski_mask_pending_action", "")
            renpy.jump("ski_mask_step_tape")
        else:
            _ski_mask_wrong("That isn't the correct target for the selected tool.")

    def ski_mask_load_tools():
        toolbox.reset_inventory()

        source = knife_tools
        toolbox.add_to_inventory(Item("Saliva Test Reagent", "toolbox-reagent", "Preliminary reagent used to screen suspected saliva-rich areas on the mask.", True, ski_mask_use_saliva_test))
        toolbox.add_to_inventory(Item(source["Swab Pack"].name, source["Swab Pack"].image_name, "Sterile swab used for saliva collection from the ski mask nose/mouth area.", True, ski_mask_use_swabpack))
        toolbox.add_to_inventory(Item(source["Plastic Vial"].name, source["Plastic Vial"].image_name, source["Plastic Vial"].description, True, ski_mask_use_vial))
        toolbox.add_to_inventory(Item(source["Paper Evidence Bag"].name, source["Paper Evidence Bag"].image_name, source["Paper Evidence Bag"].description, True, ski_mask_use_bag))
        toolbox.add_to_inventory(Item(source["Tamper Evident Tape"].name, source["Tamper Evident Tape"].image_name, source["Tamper Evident Tape"].description, True, ski_mask_use_tape))


## Workspace screen ############################################################
screen ski_mask_workspace():
    add "parking_lot_south" at parking_lot_bg

    add "rain"
    add "rain_front"

    # Base ski mask object remains only until vial placement is complete.
    if ski_mask_bag_state == 0 and ski_mask_step < 5:
        imagebutton:
            idle Transform("ski_mask", zoom=1.3, rotate=7)
            hover Transform("ski_mask", zoom=1.3, rotate=7, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.57
            yalign 0.77
            focus_mask True
            sensitive knife_interactions_enabled and (ski_mask_step == 0 or (ski_mask_step == 2 and ski_mask_swab_armed))
            hovered Notify("Ski mask target")
            unhovered Notify("")
            action Function(ski_mask_click_area, "mask")

        # Nose-area saliva target.
        button:
            xpos 1040
            ypos 570
            xsize 120
            ysize 80
            background None
            focus_mask True
            sensitive knife_interactions_enabled and ski_mask_step == 2
            hovered Notify("Mask nose area")
            unhovered Notify("")
            action Function(ski_mask_click_area, "nose")

        # Mouth-area saliva target.
        button:
            xpos 980
            ypos 640
            xsize 220
            ysize 90
            background None
            focus_mask True
            sensitive knife_interactions_enabled and ski_mask_step == 2
            hovered Notify("Mask mouth area")
            unhovered Notify("")
            action Function(ski_mask_click_area, "mouth")

    # Swab in use.
    if ski_mask_swab_img != "" and ski_mask_step < 5:
        imagebutton:
            idle Transform(ski_mask_swab_img, zoom=0.5)
            hover Transform(ski_mask_swab_img, zoom=0.5, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.92
            yalign 0.5
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Swab")
            unhovered Notify("")
            action Function(ski_mask_apply_to_swab)

    # Packaging visuals and targets.
    if ski_mask_step == 5 and ski_mask_vial_state >= 2:
        imagebutton:
            idle Transform("toolbox-tube", zoom=2.0)
            hover Transform("toolbox-tube", zoom=2.0, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.62
            yalign 0.44
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Plastic Vial")
            unhovered Notify("")
            action Function(ski_mask_apply_to_target, "vial")

    if ski_mask_bag_state >= 1:
        imagebutton:
            idle Transform("toolbox-evidence_bag", zoom=2.15)
            hover Transform("toolbox-evidence_bag", zoom=2.15, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.62
            yalign 0.44
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Paper Evidence Bag")
            unhovered Notify("")
            action Function(ski_mask_apply_to_target, "bag")

    if ski_mask_bag_state >= 2:
        add Transform("toolbox-tamper_evident_tape", zoom=1.48, rotate=-14, xalign=0.62, yalign=0.36)


## Subscene flow ###############################################################
label ski_mask_collect:
    $ default_mouse = ''
    $ knife_dialogue_style = True
    $ knife_interactions_enabled = False
    scene parking_lot_south at parking_lot_bg
    show screen ski_mask_workspace
    with dissolve

    n normal1 "This ski mask may contain saliva around the nose and mouth opening."
    n talk "We'll do a preliminary saliva screen first, then swab those areas and package the sample for lab submission."

    $ ski_mask_step = 0
    $ ski_mask_pending_action = ""
    $ ski_mask_swab_img = ""
    $ ski_mask_vial_state = 0
    $ ski_mask_bag_state = 0
    $ ski_mask_nose_swabbed = False
    $ ski_mask_mouth_swabbed = False
    $ ski_mask_swab_armed = False
    $ ski_mask_load_tools()
    $ selected_inventory = toolbox
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label ski_mask_step_prelim_done:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ ski_mask_step = 1
    n normal1 "Preliminary screen indicates probable saliva around the nose and mouth area."
    n talk "Now collect those areas with a sterile swab."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label ski_mask_step_take_swab:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ ski_mask_step = 2
    $ ski_mask_swab_img = "clean swab"
    $ ski_mask_swab_armed = False
    n normal1 "Fresh swab ready. Swab the nose area and the mouth area on the ski mask."
    n talk "For each sample, click the swab first, then click the target area on the mask."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label ski_mask_step_swab_complete:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ ski_mask_step = 4
    $ ski_mask_swab_armed = False
    $ ski_mask_swab_img = "red swab"
    $ ski_mask_vial_state = 1
    n normal1 "Saliva-prone areas swabbed. Place the swab into a plastic vial."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label ski_mask_step_vial:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ ski_mask_step = 5
    $ ski_mask_swab_img = ""
    $ ski_mask_vial_state = 2
    n normal1 "Swab sealed in the vial. Next, place the vial into a paper evidence bag and label it."
    n talk "Include initials, time collected, location, case number, and exhibit number."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label ski_mask_step_bag:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ ski_mask_step = 6
    $ ski_mask_bag_state = 1
    n normal1 "The vial is now in the evidence bag. Seal it with tamper-evident tape."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


label ski_mask_step_tape:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ ski_mask_step = 7
    $ ski_mask_bag_state = 2

    n normal1 "Sealed with tamper-evident tape. The ski mask saliva sample is fully packaged."
    n talk "This sample is now ready to be sent to the lab for confirmatory DNA/saliva analysis."

    python:
        ski_mask_collected = True
        evidence.add_to_inventory(
            Item(
                "Ski Mask Saliva Swab (Packaged)",
                "inventory-evidence_bag",
                "Saliva-area swab from the ski mask nose/mouth region, packaged in a labelled paper evidence bag and sealed for lab submission.",
            )
        )

    hide screen inventory
    hide screen ski_mask_workspace
    $ knife_dialogue_style = False
    scene parking_lot_south at parking_lot_bg
    with dissolve

    # Return to south-facing view where the ski-mask hotspot is now cleared.
    $ parking_lot_index = 2
    jump investigate
