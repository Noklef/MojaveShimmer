# Mojave Shimmer

***You ever look into the distance in New Vegas, and think therte's something... missing?*** This mod aims to add a [Heat Haze](https://en.wikipedia.org/wiki/Mirage#Heat_haze)-like effect into New Vegas. Honestly it's a barebones implementation, but an implementation nontheless.

Originally this was a conversion of [doodlum's Heat Haze](https://www.nexusmods.com/newvegas/mods/76286) mod into an `ESP-less` version. But after working on this, it's turned into something a bit different from theirs. A lot of inspiration / implementation notes come from that mod!

## Why?

The main goal of this was following the `ESP-less` trend of converting a mod; since I'm all for FOSS.
Plus i wanted to try my hand at New Vegas-specific modding for the first time that wasn't just "resolve X to work with Y" in `FNVEdit`.

## Features
- `ESP-less` implementation of a distance Heat Shimmer effect.
- Custom (albeit simple) mesh for displaying the haze effect (literally just a cylinder with custom textures).
- Configurable options for `intensity`, `distance`, ~~`start/end times`~~ (TBD) through [MCM Extender](https://www.nexusmods.com/newvegas/mods/93642).
- Debug wireframe option to configure the distance / intensity to your liking.
- *Should* work with any weather options that have been tagged as `pleasant` (I.E. weather mods, but i haven't tested many yet...)
- FNV / TTW Compatible

## TL;DR on how it works:
- Draws a tall cylinder around the player
- Display the refraction texture effect on that cylinder
- Fades the effect at the start of the day, and out at the end.

## Installation
- TBA

## Implementation Plan
1. ~~Convert it to ESP-less version~~ ***Done***
2. ~~Set-up scripts to add variance to the `.nif`~~ ***No need anymore***
3. ~~Optimize the code a little bit~~ ***Done***
4. ~~Make it a bit more configurable~~ ***Done***
5. ~~Allow it to be controllable / togglable through MCM~~ ***Done***
6. ~~Add a debug mode~~ ***Done***
7. Expand out the code with more options

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
- doodlum for the original [Heat Haze](https://www.nexusmods.com/newvegas/mods/76286) mod & inspiration
- [GECK Wiki](https://geckwiki.com/) for coming in clutch with knowledge
- [Blender](https://www.blender.org/)
- [Blender niftools addon](https://github.com/niftools/blender_niftools_addon) to convert the model to use in New Vegas
- [Paint.NET](https://www.paint.net/)