<p align="center">
    <img src="https://github.com/freemocap/freemocap/assets/15314521/da1af7fe-f808-43dc-8f59-c579715d6593" height="240" alt="Project Logo">
</p> 


<h3 align="center">FreeMoCap Blender Addon</h3>



<p align="center">

<a href="https://doi.org/10.5281/zenodo.7233714">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.7233714.svg" alt=DOI-via-Zenodo.org>
  </a>

<a href="https://github.com/psf/black">
    <img alt="https://img.shields.io/badge/code%20style-black-000000.svg" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>

<a href="https://github.com/freemocap/freemocap_blender_addon/releases/latest">
        <img src="https://img.shields.io/github/release/freemocap/freemocap_blender_addon.svg" alt="Latest Release">
    </a>

<a href="https://github.com/freemocap/freemocap/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/license-AGPL-blue.svg" alt="AGPLv3">
    </a>

<a href="https://github.com/freemocap/freemocap/issues">
        <img src="https://img.shields.io/badge/contributions-welcome-ff69b4.svg" alt="Contributions Welcome">
    </a>

<a href="https://github.com/psf/black">
    <img alt="https://img.shields.io/badge/code%20style-black-000000.svg" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>

<a href="https://discord.gg/SgdnzbHDTG">
    <img alt="Discord Community Server" src="https://dcbadge.vercel.app/api/server/SgdnzbHDTG?style=flat">
  </a>


</p>

This is a Blender add-on for loading and visualizing the output of the [freemocap](https://freemocap.org) software. 

The core functionality is run automatically at the end of a standard freemocap recording session, but this add-on allows for manual loading and visualization of the pre-processed `freemocap` recording data in Blender.

![image](https://github.com/freemocap/freemocap_blender_addon/assets/15314521/94d482c1-9fa7-4c66-8354-34cf5707af9f)

# Installation
1. Download the `freemocap_blender_addon.zip` ([from the latest release](https://github.com/freemocap/freemocap_blender_addon/releases/latest))
1. Open [Blender]()
1. `Edit` > `Preferences` > `Add-ons` > `Install...` 
1. Select the `freemocap_blender_addon.zip` (likely from your `Downloads/` folder) 
1. Verify installation by searching `freemocap` in the addon tab and ensuring the box next to `freemocap_blender_addon` is checked

## Usage
> NOTE - *We strongly recommend activating your System Console before running this addon, as it will show oodles of valuable information about the underlying process. On Windows, you can toggle this console on from the `Window` menu in a running instance of Blender. On Mac/Linux, you must **launch** blender from a Terminal by typing `blender` into a terminal after install.*

### Pre-requisites - Data!
You must have should have a fully processed [freemocap](https://freemocap.org) recording folder on your computer somewhere. 

If you are processing a recording from the `freemocap` software, it will probably in in `[path_to_your_home_directory]/freemocap_data/recording_sessions/[recording_name]`

If you have downloaded and processed the `test` data from the `Data` dropdown in the menu bar of the `freemoap` software, the addon should detect that automatically and set that path as the default.

You may download a pre-processed `freemocap_test_data` recording on the [`freemocap==1.3.0` release notes](https://github.com/freemocap/freemocap/releases/download/v1.3.0/):
> https://github.com/freemocap/freemocap/releases/download/v1.3.0/freemocap_test_data_processed_with_freemocap_v1.3.0.zip
    

## Running the skeleton building pipeline
1. In the `3D viewport` window, press `n` to show the sidebar
2. Select the `💀FreeMoCap` tab
3. Set the path to the FreeMoCap recording you want to load (path should point to the directory that contains the `output_data/` and `annotated_videos/` folders)
4. Press the `RUN_ALL` (keep an eye on the terminal window for useful output) 

# 💀✨ Time for skeletons \o/ 
If all went well, there should now be a friendly spooky skeleton in your scene along with the annotated images-as-planes, and a new `.blend` file saved to the specified recording folder named `[recording_folder_name].blend` (i.e. the same way it comes out of a standard `freemocap` recording session) 


___
# Considerations:

- The rig has a TPose as rest pose for easier retargeting.
- For best results, your recording should include a few seconds where the particapant is standing still with their feet clearly visible flat on the ground.
- If the data comes out rotated relative to gravity, it can be globally manipulated using the parent `empty`
 object (usually named `[recording_name]_parent_empty`) in the scene.
- This is a Work-In-Progress with significant refactors/overhauls planned for the near future. You will always be able to re-process old freemocap recordings using new versions of software, but things like naming conventions, armature configuration, etc may change without notice! Save your work often and back up your data often :D 

# Special Thanks
 Special thanks to @ajc27-git for the original work developing this addon and supporting the `freemocap` community! Check out their work at:  https://www.youtube.com/@fluxrenders
 
# Join the FreeMoCap Discord Community for support, feedback, and collaboration!
Click this link to join the our community Discord server - https://discord.gg/XpRQJnqZxf

