# bikepad
The emulator controller system from bicycle ANT+ sensor to the controller of Xbox 360.
The dual player include weighted balance feature that generate the _offset_ signal for controller and make one of the player has less _push_button_ signal, thus, less speed for racing car game.

The dev_cmd contains the source code for:
- ANT+ sensor receiving
- Middle ware for singal translatation, weighted balance calculation, and rewrapping package
- Controller emulator code using GIMX library

The dev_with_GUI contains the GUI frontend and existed code in dev_cmd
