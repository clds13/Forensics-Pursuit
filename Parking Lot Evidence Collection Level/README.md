## Parking Lot Evidence Collection Level

An evidence collection scene built on top of the Level Template. A young woman has
been assaulted and murdered in an abandoned, empty parking lot, and rain is actively
threatening to wash away the bloodstains and biological fluids on the asphalt. The
player must secure the evidence before the weather destroys it.

### What is implemented

- **Establishing scene** (`game/collection_scenario/script.rpy`, label `start`): the
  rainy parking lot background with Nina briefing the player on the case and the
  importance of evidence-collection order under the rain.
- **Interactive look-around scene** (label `investigate`, screen
  `parking_lot_scene`): a 360-degree view built from the four cubemap faces
  (north/east/south/west). Use the LEFT and RIGHT arrow keys to turn. Each direction
  contains one scattered piece of evidence that highlights (brightens) when hovered.
- **Rain effect** (`game/collection_scenario/custom_screens.rpy`): a `SnowBlossom`
  particle effect using `raindrop.png`, stretched into falling streaks. It is shown
  in both the establishing scene and the interactive scene.

### Assets

The level expects the following images in `game/images/`:

- `parking_lot_north.png`, `parking_lot_east.png`, `parking_lot_south.png`,
  `parking_lot_west.png` - the four cubemap faces (2048x2048).
- `raindrop.png` - the single transparent raindrop used for the rain effect.
- `bloody_knife.png`, `bloodstain.png`, `ski_mask.png`, `abandoned_clothing.png` -
  the scattered evidence.
- `parking_lot.png` - **(still needed)** the wide establishing shot of the rainy,
  empty parking lot used as the background for the opening briefing. Drop this file
  into `game/images/` for the establishing scene to display.