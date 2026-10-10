# Heat Haze - ESPless version

This is a conversion of doodlum's [Heat Haze](https://www.nexusmods.com/newvegas/mods/76286) mod into an ESP-less version. Originally i was going to be extending upon it; however i felt that the haze effect that had been created didn't feel... right. 

## Why?

Originally I was using this mod, but found the configuration options to be a bit lackluser. Also noted that someone in the discussions of the mod was talking about how it was "too close". So I wanted to work on an upgrade.

The main goal of this was following the `ESP-less` trend of this mod; since I'm all for FOSS. Plus i wanted to try my hand at New Vegas modding for the first time that wasn't just "resolve X to work with Y" in `FNVEdit`.

## So what's changed (so far)?

- This has been converted to an ESP-less version for starters, so no need for the `.ESP` file in the main mod.
- Updated mesh to be a bit simpler for what a haze effect essentially is (instead of the spheres)
- Updated to allow for editing the configuration through MCM (optional, but restricts the config values properly)
- Haze intendity modifier / distance setting
- Updated to include FO3 + DLC / FNV DLC weathers that can enable this
- Added a debug wireframe option to show where the effect is in the world

## Installation
- TBA

## Game Plan
1. ~~Convert it to ESP-less version~~ ***Done***
2. ~~Set-up scripts to add variance to the `.nif`~~ ***Done***
3. Optimize the code a little bit
4. ~~Make it a bit more configurable~~ ***Done***
5. ~~Allow it to be controllable / togglable through MCM~~ ***Done***
6. ~~Add a debug mode~~ ***Done***

## AI Disclosure:
I'm not going to deny the usage of AI for working on this; although I wouldn't consider the project to be "one-shot" / "Vibe Coded" by a long stretch. Collaborative, rather than acting as a Manager (I like to think). AI isn't perfect, so it's been used more as a colaborative tool rather than a minion to do my bidding. I haven't committed anything that I blindly implemented or not understood.

I've been testing this on every commit; making sure it's still working as expected.

Ai was used in the following ways:
- Helping me find resources to port the logic over / researching how NVSE plugins are implemented in this fashion.
- Correcting my mistakes in implementation (i.e. reference fixes, reviewing, looking for anything specifically GECK/NVSE related that I didn't necessarily realise) + Debugging nuances.
- Helping me update / modify the [Blender niftools addon](https://github.com/niftools/blender_niftools_addon) to work with recent versions of blender.
- Generating the GitHub release scripts / `build.py` script.

Model used: `Claude Opus 5.5` (Formerly `GPT-6.1 Sol`)
