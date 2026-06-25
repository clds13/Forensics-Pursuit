################################################################################
## Parking Lot Evidence Collection - Knife Collection Subscene
##
## This file implements the clickable knife evidence-collection step. Clicking
## the bloody knife in the parking lot enters this subscene, where the player:
##
##   PRESUMPTIVE TEST FOR BLOOD (Kastle-Meyer)
##     1. Add methanol to the swab (makes the dried blood adhesive)
##     2. Swab the bloodstain on the knife (click the knife)
##     3. Add phenolphthalein to the swab
##     4. Add hydrogen peroxide to the swab
##     5. The swab turns pink immediately -> the substance is blood
##
##   COLLECT AND PACKAGE (only after blood is confirmed)
##     1. Grab a fresh, pre-moistened (wet) swab from the swab pack
##     2. Swab the dried bloodstain on the knife (click the knife)
##     3. Place the swab into a plastic vial / capsule
##     4. Place the vial into a paper evidence bag and label it
##     5. Seal the bag with tamper-evident tape
##
## The tools live in the Level Template inventory side bar (screen inventory).
## Each tool is "usable"; using it runs the matching function below, which only
## advances the sequence when it is the correct next step (otherwise it gives a
## hint). The knife itself is the click target for the two "swab" steps.
################################################################################


## State #######################################################################
##
## knife_step tracks progress through the sequence. The values map directly onto
## the numbered steps documented above:
##   0  need methanol on swab          (presumptive)
##   1  need to swab the knife
##   2  need phenolphthalein
##   3  need hydrogen peroxide
##   4  blood confirmed (transient)
##   5  need a fresh wet swab           (packaging)
##   6  need to swab the dried stain
##   7  need to place swab in the vial
##   8  need to bag and label
##   9  need to seal with tamper tape
##   10 blood collection complete
##
## Fingerprinting steps:
##   20 need to dust with powder        (fingerprinting)
##   21 need to photograph the print
##   22 need to place scale next to print
##   23 need to lift with fingerprint tape
##   24 need to place on backing card
##   25 fingerprinting complete
##
## Final packaging (only after both blood AND fingerprint complete):
##   30 need to dry the knife          (final packaging)
##   31 need to place in paper bag
##   32 need to label the bag
##   33 need to seal with tamper tape
##   34 final packaging complete
default knife_step = 0
# Which swab image is currently shown in the workspace ("" hides it).
default knife_swab_img = "clean swab"
# Current instruction text shown at the top of the knife workspace.
default knife_instruction = ""
# Reagent/tool currently selected to be applied on the swab.
default knife_pending_swab_action = ""
# Visual packaging states used by the workspace display.
default knife_vial_state = 0
default knife_bag_state = 0
default knife_display_image = "knife_fingerprint_blurry"
default knife_scale_placed = False
default knife_lifted_print = False
default knife_backing_card_done = False
# Whether the player can interact with the workspace / inventory right now.
default knife_interactions_enabled = False
# Enables the smaller Nina dialogue treatment for this subscene only.
default knife_dialogue_style = False
# Track completion of each procedure.
default blood_collected = False
default fingerprint_collected = False
# Whether the knife has been fully collected (used by the parking lot screen).
default knife_collected = False


## Tool action functions #######################################################
##
## These are wired up as the "action" of each inventory item in
## jsons/knife_tools.json. They run when the player uses the item from the
## inventory side bar. Each one only advances when used in the right order.

init python:

    def knife_route_to_procedure():
        # Route to whichever procedure is not yet done, or to final packaging if both are done.
        if blood_collected and fingerprint_collected:
            # Both procedures complete - go to final packaging
            renpy.jump("knife_final_packaging_start")
        elif blood_collected and not fingerprint_collected:
            # Blood done, fingerprinting remains
            renpy.jump("knife_fingerprint")
        elif fingerprint_collected and not blood_collected:
            # Fingerprinting done, blood remains
            renpy.jump("knife_collect")
        else:
            # Both incomplete; start with blood collection first
            renpy.jump("knife_collect")

    def _knife_wrong(hint):
        # Shared helper for using a tool out of order.
        renpy.notify(hint)

    def _knife_select_for_swab(expected_step, action_name, instruction, wrong_hint):
        # First click selects a reagent; second click (on the swab) applies it.
        if store.knife_step == expected_step:
            store.knife_pending_swab_action = action_name
            store.knife_instruction = instruction
            renpy.notify("Selected. Now click the swab.")
        else:
            _knife_wrong(wrong_hint)

    def knife_use_methanol():
        _knife_select_for_swab(
            0,
            "methanol",
            "Methanol selected. Click the swab to wet it.",
            "That isn't the next step right now.",
        )

    def knife_use_phenol():
        _knife_select_for_swab(
            2,
            "phenol",
            "Phenolphthalein selected. Click the swab to apply it.",
            "Add phenolphthalein only after the swab has touched the stain.",
        )

    def knife_use_peroxide():
        _knife_select_for_swab(
            3,
            "peroxide",
            "Hydrogen peroxide selected. Click the swab to apply it.",
            "Hydrogen peroxide is the last reagent in the test.",
        )

    def knife_use_swabpack():
        if store.knife_step == 5:
            renpy.jump("knife_step_wetswab")
        else:
            _knife_wrong("You only need a fresh swab once the blood is confirmed.")

    def knife_use_vial():
        if store.knife_step == 7:
            store.knife_pending_swab_action = "vial"
            store.knife_instruction = "Plastic vial selected. Click the swab to place it in the vial."
            renpy.notify("Selected. Now click the swab.")
        else:
            _knife_wrong("Collect the stain on a fresh swab before bagging it.")

    def knife_use_bag():
        if store.knife_step == 8:
            store.knife_pending_swab_action = "bag"
            store.knife_instruction = "Paper evidence bag selected. Click the vial to place it in the bag."
            renpy.notify("Selected. Now click the vial.")
        elif store.knife_step == 31:
            store.knife_pending_swab_action = "final_bag"
            store.knife_instruction = "Paper evidence bag selected. Click the knife to place it in the bag."
            renpy.notify("Selected. Now click the knife.")
        else:
            _knife_wrong("The bag is not needed at this stage.")

    def knife_use_tape():
        if store.knife_step == 9:
            store.knife_pending_swab_action = "tape"
            store.knife_instruction = "Tamper tape selected. Click the evidence bag to seal it."
            renpy.notify("Selected. Now click the evidence bag.")
        elif store.knife_step == 32:
            store.knife_pending_swab_action = "final_tape"
            store.knife_instruction = "Tamper tape selected. Click the evidence bag to seal the knife packaging."
            renpy.notify("Selected. Now click the evidence bag.")
        else:
            _knife_wrong("There's nothing sealed to tape shut yet.")

    def knife_swab():
        # The knife itself is the click target for swabbing, fingerprint lifting, and final bagging.
        if store.knife_step == 1:
            renpy.jump("knife_step_swabbed")
        elif store.knife_step == 6:
            renpy.jump("knife_step_swabbed_dry")
        elif store.knife_step == 20 and store.knife_pending_swab_action == "powder":
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_powder")
        elif store.knife_step == 23 and store.knife_pending_swab_action == "lifter":
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_lift")
        elif store.knife_step == 31 and store.knife_pending_swab_action == "final_bag":
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_final_bag")
        else:
            _knife_wrong("That isn't the correct step for interacting with the knife.")

    def knife_apply_to_swab():
        # Applies whichever reagent the player selected to the swab (or places items for fingerprinting).
        action = store.knife_pending_swab_action

        if action == "methanol" and store.knife_step == 0:
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_methanol")
        elif action == "phenol" and store.knife_step == 2:
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_phenol")
        elif action == "peroxide" and store.knife_step == 3:
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_peroxide")
        elif action == "vial" and store.knife_step == 7:
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_vial")
        elif action:
            _knife_wrong("That reagent can't be applied at this stage.")
        else:
            _knife_wrong("Select a tool first, then click to place or apply it.")

    def knife_apply_to_target(target):
        action = store.knife_pending_swab_action

        if target == "vial" and action == "bag" and store.knife_step == 8:
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_bag")
        elif target == "bag" and action == "tape" and store.knife_step == 9:
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_tape")
        elif target == "bag" and action == "final_tape" and store.knife_step == 32:
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_final_tape")
        else:
            _knife_wrong("That isn't the correct target for the selected tool.")

    # Fingerprinting procedure functions
    def knife_use_powder():
        if store.knife_step == 20:
            store.knife_pending_swab_action = "powder"
            store.knife_instruction = "Magnetic powder selected. Click the knife handlebar to dust for fingerprints."
            renpy.notify("Selected. Now click the knife handlebar.")
        else:
            _knife_wrong("The fingerprinting procedure starts with dusting the handlebar.")

    def knife_use_scale():
        if store.knife_step == 22:
            renpy.jump("knife_step_scale")
        else:
            _knife_wrong("Place the scale only after the fingerprint is visible.")

    def knife_use_lifter():
        if store.knife_step == 23:
            store.knife_pending_swab_action = "lifter"
            store.knife_instruction = "Lifting tape selected. Click the fingerprint to lift it."
            renpy.notify("Selected. Now click the fingerprint to lift.")
        else:
            _knife_wrong("The fingerprint must be photographed and labelled before lifting.")

    def knife_use_backing_card():
        if store.knife_step == 24:
            store.knife_pending_swab_action = "backing_card"
            store.knife_instruction = "Backing card selected. Click the lifted tape image to mount it on the card."
            renpy.notify("Selected. Now click the lifted tape image.")
        else:
            _knife_wrong("The fingerprint must be lifted first.")

    def knife_apply_to_lifted_tape():
        if store.knife_step == 24 and store.knife_pending_swab_action == "backing_card":
            store.knife_pending_swab_action = ""
            renpy.jump("knife_step_backing")
        elif store.knife_step == 24:
            _knife_wrong("Select the Backing Card first, then click the lifted tape image.")
        else:
            _knife_wrong("That isn't the correct step for mounting the lifted print.")

    def knife_fingerprint_dust():
        # Click target for dusting the handlebar
        if store.knife_step == 20:
            renpy.jump("knife_step_powder")
        else:
            _knife_wrong("You need to start the fingerprinting procedure first.")


## Helpers for loading the right toolbox per phase #############################

init python:

    def knife_load_presumptive_tools():
        toolbox.reset_inventory()
        for item_name in ("Methanol", "Phenolphthalein", "Hydrogen Peroxide"):
            toolbox.add_to_inventory(knife_tools[item_name])

    def knife_load_packaging_tools():
        toolbox.reset_inventory()
        for item_name in ("Swab Pack", "Plastic Vial", "Paper Evidence Bag", "Tamper Evident Tape"):
            toolbox.add_to_inventory(knife_tools[item_name])

    def knife_load_fingerprinting_tools():
        toolbox.reset_inventory()
        for item_name in ("Magnetic Powder", "Fingerprint Scale", "Fingerprint Tape", "Backing Card"):
            toolbox.add_to_inventory(knife_tools[item_name])

    def knife_load_final_packaging_tools():
        toolbox.reset_inventory()
        for item_name in ("Paper Evidence Bag", "Tamper Evident Tape"):
            toolbox.add_to_inventory(knife_tools[item_name])


## Workspace screen ############################################################
##
## A close-up of the knife with the swab beside it. The inventory side bar is
## shown separately (show screen inventory) so the player can use tools. The
## knife is a click target (with focus_mask so only the blade is clickable) for
## the two swabbing steps.

image knife_workspace_bg = "parking_lot_down.png"

screen knife_workspace():
    # The scene background is set on the master layer (scene knife_workspace_bg),
    # so this screen must NOT paint a fullscreen solid here - doing so would
    # cover the inventory side bar shown underneath it.

    # The knife stays visible during the blood workflow, the fingerprinting
    # workflow, and the pre-bag final packaging phase. Once bagging starts,
    # the bag becomes the center-stage object instead.
    if (knife_step < 8 or (20 <= knife_step < 25) or (30 <= knife_step < 32)) and not knife_lifted_print and not knife_backing_card_done:
        imagebutton:
            xalign 0.55
            yalign 0.5
            focus_mask True
            sensitive knife_interactions_enabled
            idle Transform(knife_display_image, zoom=1.1)
            hover Transform(knife_display_image, zoom=1.1, matrixcolor=BrightnessMatrix(0.2))
            hovered Notify("Knife")
            unhovered Notify("")
            action Function(knife_swab)

    if knife_scale_placed:
        add Transform("scalebar", xzoom=0.27, yzoom=-0.27, rotate=63, xalign=0.685, yalign=0.44)
    if knife_lifted_print:
        imagebutton:
            idle Transform("tape_print_scalebar", zoom=1.3, rotate=-8)
            hover Transform("tape_print_scalebar", zoom=1.3, rotate=-8, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.3
            yalign 0.6
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Lifted print")
            unhovered Notify("")
            action Function(knife_apply_to_lifted_tape)

    if knife_backing_card_done:
        # Left card: pushed further left (760 -> 620)
        add Transform("complete_backing_card_front", zoom=0.28, rotate=2, anchor=(0.5, 0.5), xpos=620, ypos=250)
        
        # Right card: pushed further right (1160 -> 1300)
        add Transform("complete_backing_card_r", zoom=0.28, rotate=-2, anchor=(0.5, 0.5), xpos=1300, ypos=250)
    
    # The swab currently in use, if any.
    if knife_swab_img != "" and knife_step < 8:
        imagebutton:
            idle Transform(knife_swab_img, zoom=0.5)
            hover Transform(knife_swab_img, zoom=0.5, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.92
            yalign 0.5
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Swab")
            unhovered Notify("")
            action Function(knife_apply_to_swab)

    # Packaging visuals and clickable targets.
    if knife_step == 8 and knife_vial_state >= 2:
        imagebutton:
            idle Transform("toolbox-tube", zoom=2.0)
            hover Transform("toolbox-tube", zoom=2.0, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.62
            yalign 0.44
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Plastic Vial")
            unhovered Notify("")
            action Function(knife_apply_to_target, "vial")

    if knife_bag_state >= 1 and (8 <= knife_step <= 10 or knife_step >= 32):
        imagebutton:
            idle Transform("toolbox-evidence_bag", zoom=2.15)
            hover Transform("toolbox-evidence_bag", zoom=2.15, matrixcolor=BrightnessMatrix(0.18))
            xalign 0.62
            yalign 0.44
            focus_mask True
            sensitive knife_interactions_enabled
            hovered Notify("Paper Evidence Bag")
            unhovered Notify("")
            action Function(knife_apply_to_target, "bag")

    if knife_bag_state >= 2 and (8 <= knife_step <= 10 or knife_step >= 32):
        add Transform("toolbox-tamper_evident_tape", zoom=1.48, rotate=-14, xalign=0.62, yalign=0.36)


## Subscene flow ###############################################################

label knife_fingerprint:
    $ default_mouse = ''
    $ knife_dialogue_style = True
    $ knife_interactions_enabled = False
    # Clear stale packaging visuals before the screen is shown.
    $ knife_vial_state = 0
    $ knife_bag_state = 0
    $ knife_swab_img = ""
    scene knife_workspace_bg
    show screen knife_workspace
    with dissolve

    n normal1 "Before we bag the knife, we need to collect any fingerprints from the handlebar."
    n talk "We'll use a magnetic powder to reveal latent prints, then lift and preserve them on a backing card."
    with dissolve

    # Start the fingerprinting procedure.
    $ knife_step = 20
    $ knife_swab_img = ""
    $ knife_pending_swab_action = ""
    $ knife_vial_state = 0
    $ knife_bag_state = 0
    $ knife_display_image = "knife_fingerprint_blurry"
    $ knife_scale_placed = False
    $ knife_lifted_print = False
    $ knife_backing_card_done = False
    $ knife_instruction = "Use the Magnetic Powder from your toolbox to dust the handlebar."
    $ knife_load_fingerprinting_tools()
    $ selected_inventory = toolbox
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


# --- Fingerprinting procedure ----
label knife_step_powder:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 21
    $ knife_pending_swab_action = ""
    $ knife_display_image = "knife_fingerprint_clear"
    $ knife_instruction = "Fingerprints revealed. Photograph complete."
    n normal1 "Magnetic powder applied. The latent fingerprints on the handlebar are now visible."
    n talk "The print is documented with a photograph showing the scale reference."
    n normal1 "Now we place the scale reference label beside the fingerprint."
    
    # Auto-advance to scale placement (no separate tool for photography).
    $ knife_step = 22
    $ knife_instruction = "Use the Fingerprint Scale next to the visible print."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_scale:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 23
    $ knife_pending_swab_action = ""
    $ knife_scale_placed = True
    $ knife_instruction = "Use the Fingerprint Tape to lift the print from the handlebar."
    n normal1 "Scale positioned beside the fingerprint. Now we lift the fingerprint with the clear lifting tape."
    n talk "Be careful to get the entire print on the tape without smudging it."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_lift:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 24
    $ knife_pending_swab_action = ""
    $ knife_scale_placed = False
    $ knife_lifted_print = True
    $ knife_instruction = "Use the Backing Card, then click the lifted tape image to mount the print on the card."
    n normal1 "Print lifted successfully. The tape is now holding the dusted fingerprint."
    n talk "Now we transfer this to a backing card for preservation and documentation."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_backing:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_backing_card_done = True
    $ knife_lifted_print = False
    $ knife_display_image = "knife_fingerprint_clear"
    n normal1 "Fingerprint preserved on the backing card. The collection is complete."
    n talk "We've filled in all required backing card details: case information, exhibit ID, date/time, and collector initials."

    # Mark fingerprinting as complete and return to parking lot
    $ fingerprint_collected = True
    $ knife_step = 25
    n normal1 "Both the blood sample and the fingerprint have been collected. Let's go back and package the knife for transport."
    hide screen inventory
    hide screen knife_workspace
    $ knife_dialogue_style = False
    scene knife_workspace_bg
    with dissolve
    $ parking_lot_index = 0
    jump investigate


label knife_collect:
    $ default_mouse = ''
    $ knife_dialogue_style = True
    $ knife_interactions_enabled = False
    scene knife_workspace_bg
    show screen knife_workspace
    with dissolve

    n normal1 "This is the knife we spotted. Before we collect anything, we need to confirm that the red staining is actually blood."
    n talk "We'll run a Kastle-Meyer presumptive test. Order matters, so follow each step carefully."
    with dissolve

    # Start the presumptive test.
    $ knife_step = 0
    $ knife_display_image = "knife_fingerprint_blurry"
    $ knife_swab_img = "clean swab"
    $ knife_pending_swab_action = ""
    $ knife_vial_state = 0
    $ knife_bag_state = 0
    $ knife_instruction = "Use the Methanol from your toolbox to wet the swab."
    $ knife_load_presumptive_tools()
    $ selected_inventory = toolbox
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


# --- Presumptive test ---------------------------------------------------------
label knife_step_methanol:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 1
    $ knife_pending_swab_action = ""
    $ knife_instruction = "Click the knife to swab the bloodstain."
    n normal1 "Methanol added. That makes the dried blood adhere to the swab so we can lift a sample."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_swabbed:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 2
    $ knife_swab_img = "red swab"
    $ knife_pending_swab_action = ""
    $ knife_instruction = "Use the Phenolphthalein on the swab."
    n normal1 "Good - the swab picked up the red staining. Now add the phenolphthalein."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_phenol:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 3
    $ knife_pending_swab_action = ""
    $ knife_instruction = "Use the Hydrogen Peroxide on the swab."
    n normal1 "Phenolphthalein is on. The last reagent is hydrogen peroxide."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_peroxide:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_swab_img = "pink swab"
    $ knife_pending_swab_action = ""
    n normal1 "It turned pink immediately."
    n talk "A bright pink reaction is a positive result - this is blood. Now we collect it properly."

    # Move into the packaging phase with a fresh set of tools.
    $ knife_step = 5
    $ knife_swab_img = ""
    $ knife_instruction = "Use the Swab Pack to take out a fresh wet swab."
    $ knife_load_packaging_tools()
    n normal1 "The knife is already dry, so this is a dried stain. We collect a dried stain with a fresh, pre-moistened swab."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)


# --- Collect and package ------------------------------------------------------
label knife_step_wetswab:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 6
    $ knife_swab_img = "clean swab"
    $ knife_instruction = "Click the knife to swab the dried bloodstain."
    n normal1 "That swab is pre-moistened, so it'll lift the dried blood. Swab the stain on the knife."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_swabbed_dry:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 7
    $ knife_swab_img = "red swab"
    $ knife_vial_state = 1
    $ knife_instruction = "Use the Plastic Vial, then click the swab to place it in the vial."
    n normal1 "Sample collected. Next, we transfer the swab into a plastic vial."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_vial:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 8
    $ knife_swab_img = ""
    $ knife_vial_state = 2
    $ knife_instruction = "Use the Paper Evidence Bag, then click the vial to package it."
    n normal1 "The swab is now sealed in the vial. We can package that vial in a paper evidence bag."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_bag:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 9
    $ knife_bag_state = 1
    $ knife_instruction = "Use the Tamper Evident Tape to seal the bag."
    n normal1 "Label the bag with your initials, the time, the location, the case number, and the exhibit number."
    n talk "That label is our chain of custody - skip it and the evidence can be thrown out in court."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_tape:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_bag_state = 2
    n normal1 "Sealed with tamper-evident tape. The blood sample is now properly packaged."

    # Mark blood collection as complete and return to parking lot
    $ blood_collected = True
    $ knife_step = 10
    n normal1 "Now you need to collect the fingerprints from the handlebar. Go back to the parking lot and process those."
    hide screen inventory
    hide screen knife_workspace
    $ knife_dialogue_style = False
    scene knife_workspace_bg
    with dissolve
    $ parking_lot_index = 0
    jump investigate


label knife_final_packaging_start:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 30
    $ knife_swab_img = ""
    $ knife_display_image = "bloody_knife"
    $ knife_scale_placed = False
    $ knife_lifted_print = False
    $ knife_backing_card_done = False
    $ knife_vial_state = 0
    $ knife_bag_state = 0
    $ knife_pending_swab_action = ""
    $ knife_instruction = "Both procedures complete. The knife must dry before final packaging."
    scene knife_workspace_bg
    show screen knife_workspace
    with dissolve
    n normal1 "Both the blood and fingerprint evidence have been collected and preserved."
    n talk "Now we need to package the knife itself for transport to the lab."
    n normal1 "First, we let the knife dry completely. No moisture should be present."
    $ renpy.pause(0.8)
    $ renpy.notify("Knife drying...")
    $ renpy.pause(1.2)
    $ renpy.notify("Knife dry.")
    n normal1 "The knife is dry and ready for packaging. Let's place it in a paper evidence bag."
    $ knife_step = 31
    $ knife_load_final_packaging_tools()
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_final_bag:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_step = 32
    $ knife_bag_state = 1
    $ knife_instruction = "Label the bag with your initials, the time, the location, the case number, and the exhibit number."
    n normal1 "The knife is now in the paper evidence bag. Label it with:"
    n talk "Your initials, time collected, location, case number, and exhibit number."
    n normal1 "This establishes the complete chain of custody for the evidence."
    $ knife_interactions_enabled = True
    show screen inventory
    $ renpy.pause(hard=True)

label knife_step_final_tape:
    $ knife_interactions_enabled = False
    hide screen inventory
    $ knife_bag_state = 2
    $ knife_step = 33
    n normal1 "Sealed with tamper-evident tape. The knife is now fully packaged and ready for transport."
    n normal1 "Excellent work. You've successfully collected both blood and fingerprint evidence from the knife."
    n talk "Both samples are now preserved in a chain of custody-compliant manner."

    # Record all collected evidence and end the subscene.
    python:
        knife_collected = True
        knife_step = 34
        evidence.add_to_inventory(
            Item(
                "Knife (Packaged)",
                "inventory-evidence_bag",
                "The knife, fully packaged in a labelled, tamper-sealed paper bag. Contains both dried bloodstain (preserved via swab) and handlebar fingerprint evidence.",
            )
        )

    hide screen inventory
    hide screen knife_workspace
    $ knife_dialogue_style = False
    scene knife_workspace_bg
    with dissolve

    # Return to the parking lot, facing the knife's direction (north).
    $ parking_lot_index = 0
    jump investigate
