# Freemocap Visualizer
Add-on to visualize the Freemocap Blender output. Some of its features:
1. One-click base elements visibility toggle.
2. Add motion paths to the joint markers and center of mass.
3. Add Center of Mass (COM) vertical projection with custom colors.
4. Add animated joint angles with mesh and text with angle value. Can set custom colors.
5. Add animated Base of Support (BOS) polygon based on points of contact and a z threshold.

# Requirements
Make sure that the scipy and shapely python modules are installed in your Blender's python folder.
If they are not installed you will get a "ModuleNotFoundError: No module named scipy/shapely" when installing the addon.
To install the scipy and shapely packages run this commands inside your Blender python folder:
`python -m pip install scipy`
`python -m pip install shapely`

For example:

`C:\Program Files\Blender Foundation\Blender 3.6\3.6\python\bin> .\python.exe -m pip install scipy`.

`C:\Program Files\Blender Foundation\Blender 3.6\3.6\python\bin> .\python.exe -m pip install shapely`.

# Installation
Install as a regular *.zip add-on in Edit->Preferences-Add-ons.

# Notes
The addon doesn't consider all possible use combinations. So errors might happen when using the functions multiple times.
Is better to undo the functions instead of deleting the meshes and create them again.

Addon captures:

![image](https://github.com/ajc27-git/freemocap_tools/assets/36526931/cf05f630-dcbc-43d0-bc91-9fe5539b1f2b)

![image](https://github.com/ajc27-git/freemocap_tools/assets/36526931/5dc5a5c6-a0b4-4f18-8a27-03855343143a)

