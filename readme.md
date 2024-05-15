The purpose of this tool is to allow quick and easy use of pre-existing Civ VI models in your mod.

It does this by searching through your Civ VI install, absorbing any Units.artdef file.

To use this tool, you will need to edit the config.json file and change the value denoted by "civ_install" to your
civ install directory, for example "C:/Steam/Steamapps/common/Sid Meier's Civilization VI". You need double quotes around
I signified there.

You will also need to specify your new units name, and what unit it should copy in the same file.
Under units_specified is a list where you can set what your new unit on the left should be assigned to the civ unit on the right.

To actually run the script, run run.bat on windows, or run.sh on mac or linux. For the latter, you will also need to run:

>>>chmod +x run_main.sh

in your terminal, in the project directory.


You can also have a look at the full list of units available to make your unit look like by setting "show_all_possible_units" to True.

Once the script has run, you should have a new file called Units.artdef. You can then import that into your modbuddy project to build
the .dep file for your mod.

Note: there are some scenario-only units that are importable, but will not show up in game, as the assets for them
are not loaded.