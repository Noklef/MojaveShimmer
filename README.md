# Mojave Shimmer

***You ever look into the distance, and think there's something... missing?***

This mod aims to add a [Heat Haze](https://en.wikipedia.org/wiki/Mirage#Heat_haze)-like effect into New Vegas. Honestly it's a bare-bones implementation, but an implementation nonetheless (the effect isn't scientifically correct in the slightest)

This took HEAVY inspiration from [doodlum's Heat Haze](https://www.nexusmods.com/newvegas/mods/76286) mod, and has been expanded with new meshes, textures, configuration options, and logic to match more realistic depictions of the effect.

## Why?

The main goal of this was following the `ESP-less` trend of converting a mod; since I'm all for FOSS.
Plus i wanted to try my hand at New Vegas-specific modding for the first time that wasn't just "resolve X to work with Y" in `FNVEdit`.

## Features
- **ESP-less** implementation of a distance Heat Shimmer effect.
- Custom (albeit simple) mesh for displaying the haze effect (literally just a cylinder with custom textures).
- Configurable **intensity**, **distance** and **start / end times** (with a fade in / out) through [MCM Extender](https://www.nexusmods.com/newvegas/mods/93642), or an "Always Enabled" option to ignore the time of day.
- **Debug** option to configure the distance / intensity to your liking in a toxic green colour.
- ***TTW Compatible*** for the most part

## TL;DR on how it works:
- Draws a tall cylinder around the player
- Display the refraction texture effect on that cylinder
- Fades the effect at the start of the day, and out at the end.

## Requirements
- [NVSE](https://www.nexusmods.com/newvegas/mods/67883)
- [JIP LN NVSE](https://www.nexusmods.com/newvegas/mods/58277)
- [Climate Control NVSE](https://www.nexusmods.com/newvegas/mods/77205)
- (Optional) [MCM Extender](https://www.nexusmods.com/newvegas/mods/93642)

## Installation
- TBA

## Compatibility
> ***100% NOT COMPATIBLE WITH [Heat Haze](https://www.nexusmods.com/newvegas/mods/76286), this mod is doing similar to what that one does.***

I'm not 100% sure what works, and what doesn't with this mod...
Guessing ENB don't work it, but it *should* work with NVR (don't quote me on that).

I haven't tested this out 100% with a lot of weather mods, but this heat haze effect shouldn't be an issue with any of them i don't think.

*Should* work with any weather options that have been tagged as **pleasant** (i.e. weather mods, but I haven't tested many yet...)

## AI Disclosure:
I'm not going to deny the usage of AI for working on this; although I wouldn't consider the project to be *"one-shot"* / *"Vibe Coded"* by a long stretch. I'd say collaborative rather than me acting as a manager (i'd like to think at least). AI isn't perfect, so it's been used more as a colaborative tool rather than a minion to do my bidding. I haven't committed anything that I blindly implemented or not understood.

I've been testing this on every commit; making sure it's still working as expected.

Ai was used in the following ways:
- Helping me find resources to port the logic over / researching how NVSE plugins are implemented in this fashion.
- Correcting my mistakes in implementation (i.e. reference fixes, reviewing, looking for anything specifically GECK/NVSE related that I didn't necessarily realise) + Debugging nuances.
- Helping me update / modify the [Blender niftools addon](https://github.com/niftools/blender_niftools_addon) to work with recent versions of Blender.
- Generating the GitHub release scripts / `build.py` script.

Model used: `Claude Opus 5.5` (Formerly `GPT-6.1 Sol`)

## Resources / Credits
- ***doodlum*** for the original [Heat Haze](https://www.nexusmods.com/newvegas/mods/76286) mod & inspiration
- [FNVEdit](https://www.nexusmods.com/newvegas/mods/34703)
- [NIFSkope](https://www.nifskope.com/)
- [GECK Wiki](https://geckwiki.com/) for coming in clutch with knowledge
- [Blender](https://www.blender.org/)
- [Blender niftools addon](https://github.com/niftools/blender_niftools_addon) to convert the model to use in New Vegas
- [Paint.NET](https://www.paint.net/)
