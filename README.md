# 🏗️ Anterio — Architect's Complete Guide

[![Ru](https://img.shields.io/badge/lang-ru-green.svg)](README.ru.md)

Welcome to **Anterio**. This is a hybrid of a professional CAD editor and an atmospheric sandbox.
Here, you don't just place blocks — you work with geometry, vectors, and light physics. The program requires some getting used to, but it gives you complete control over space.

## 📐 1. World Basis: Grid, Chunks, and Precision

The entire world in Anterio obeys a mathematical grid. This guarantees that your walls will always join perfectly, without gaps or seams.

### Precision Modes
*   **Decimeter Grid (0.1 m) — [Standard]:**
    *   Default mode.
    *   Cursor and objects "snap" to invisible nodes every 10 cm.
    *   *Ideal for:* Building walls, creating rooms, rough layout.
*   **Centimeter Grid (0.01 m) — [Hold Ctrl]:**
    *   Press and hold **Ctrl** during any action (building, moving, resizing).
    *   Snap step decreases to 1 cm.
    *   *Ideal for:* Creating thin partitions, decor, eliminating micro-gaps, working with furniture.

### Infinite World
The world is generated in **chunks** (sectors) as you move.
*   The **Global Grid** on the ground is drawn only around you (for optimization), but you can build anywhere — coordinates are infinite.

---

## 🎮 2. Game Modes
Instant switching via the **[TAB]** key.

### 👷 Creative Mode
*   **You are the Architect.** The camera flies freely through walls (noclip).
*   **Interface:** HUD is enabled with tooltips, coordinates, and object dimensions.
*   **Visualization:** Bright daylight. Linear fog (helps feel depth but doesn't obstruct view).
*   **Interaction:** Doors open via **Alt + RMB**.

### 🕯️ Adventure Mode (Walk)
*   **You are the Explorer.** Body physics is enabled. You cannot pass through walls; gravity pulls you down.
*   **Lighting:**
*   **Lamp:** A soft glow (light aura) is created around the player, illuminating the path.
    *   Light radius adjustment: **Mouse Wheel**.
*   **Interaction:** Doors open with a normal **LMB** click.

### ☀️ Sun and Atmosphere Editor
Special mode for adjusting time of day and lighting.
*   **Enter/Exit:** Press **[Ctrl + E]**.
*   **Up/Down Arrows:** Change time of day (sun movement across the sky).
*   **Left/Right Arrows:** Rotate sun orbit (change cardinal directions).
*   **Ctrl + Arrows:** Change Time Speed.

---

## 🕹️ Camera and Movement Controls

### Standard
*   **W / A / S / D** — Move (Fly / Walk).
*   **Space** — Fly Up (Creative) / Jump (Adventure).
*   **Shift** — Fly Down (Creative) / Crouch (Adventure). In Adventure mode, makes steps silent and lowers the camera.
*   **Ctrl** — Sprint / Fast Fly.
*   **Mouse Wheel** — In Creative mode smoothly changes base camera flight speed; in Adventure mode adjusts flashlight brightness.
*   **C** — Switch to **Cine-Cam** mode (see section 9).
*   **F11** — Fullscreen mode.

---

## 🛠️ 3. Construction Tools

**How to select:** Press numbers **[1]...[6]** and **[7]**.
**How to exit:** Press **[Esc]** to drop the tool and return to *Select* mode.

> **💡 Key Mechanic [Q]:**
> When using tools, a "ghost" object is built. Press **[Q]** to change the construction plane or constraint axis (e.g., to draw vertically instead of on the floor).

### **[1] Wall**
Simple tool for erecting partitions.
*   Click 1: Start of wall.
*   Click 2: End of wall.
*   *Result:* Wall is created with thickness specified in settings (*Menu -> New Wall Thickness*).

### **[2] Box**
Create monolithic blocks (foundations, stands, solid buildings). Has two modes:
1.  **"Base + Height" Method:**
    *   Draw a rectangle on the floor (Click 1 → Drag → Click 2).
    *   Release mouse and pull cursor **up**.
    *   Click 3rd time to fix height.
2.  **"3D Diagonal" Method:**
    *   Click point **A** in space (e.g., floor corner).
    *   Click point **B** (e.g., opposite corner under the ceiling).
    *   Block is created instantly between these points.

### **[3] Room**
Works exactly like the **Box** tool (same two methods) but creates **hollow** objects:
*   Generates: Floor, Ceiling, and 4 Walls.
*   Wall thickness is taken from settings.

### **[4] Line / Strip**
Drawing walls by points (polyline mode).
1.  Click LMB to place nodes. "Smart corner" logic is active.
2.  **RMB** — Remove last placed point (Undo).
3.  **Closing the loop:** Click exactly on the very first point. The contour closes, corners automatically "weld" without gaps.
4.  **Finish:** Double click (or press Enter) to finish drawing an open wall and extrude it upwards.
> *   **Smart Angle:** If you approach the start point at an angle (not straight) when closing the loop, and aren't holding *Ctrl*, the tool automatically creates a diagonal corner piece so the wall doesn't look "squashed" in the corner.

### **[5] Cube**
Tool for quick voxel modeling and volume subtraction.
*   **RMB (Right Button):** Add cube. Snaps to surface of other objects.
*   **LMB (Left Button):** Cut cube (Boolean Cut). Creates a recess in the object.
*   **Brush Sizes:**
    *   **Standard:** 1 dm (10 cm).
    *   **Shift:** 0.5 m (Large block).
    *   **Ctrl:** 1 cm (Detailing).

### **[6] Cut**
Powerful boolean operation tool (subtraction).
*   **Windows and Doors:** Hover over a wall. Click two points diagonally — an opening is created.
*   **Basements and Pits:** Click two points **on the ground** (not on an object). A hole is cut in the terrain through which you can fall.
*   **Through Cut ([Alt]):**
    *   Hold **[Alt]** while creating a cut.
    *   The hole cuts not only into the block you are looking at but also through all blocks behind it (or touching it). Ideal for punching passages through thick walls or groups of objects.

### **[7] Slice**
Laser knife for cutting objects into parts.
1.  Hover over an object. A cut plane appears.
2.  **Auto-orientation:** The knife understands if you are cutting a floor or wall and aligns perpendicularly.
3.  **[Q]:** Switches cut direction (longitudinal/transverse) if auto-selection isn't right.
4.  **Click LMB** — Slice object. Now it is two independent halves.
5.  **[Alt] + Click** — Slice the entire **group** of objects or all objects on the cut line.

---

## 🚪 4. Door Constructor [T]

There is no ready-made "door" object in Anterio. You can turn **any** block (or group of blocks) into a door.

### Creation Algorithm:
1.  Select tool **[T]**.
2.  Hover over a block (or grouped object).
3.  **Select Axis:** Move cursor near the edge where hinges should be. The edge highlights **purple**.
    *   *Note:* You can choose vertical edges (door) and horizontal edges (hatch).
4.  **Fix:** Press **LMB**. The axis becomes **red** (locked). Now you can rotate the camera and check if the axis is chosen correctly.
    *   *Mistake?* Press **Esc** to reset axis selection (returns to purple highlight).
5.  **Create:** Press **Enter**. The object becomes an interactive door.

### Advanced Door Functions:
*   **Group Doors:** First select multiple blocks (handle, panel, glass) and group them **[G]**. Then apply tool **[T]** to this group. The whole structure will rotate as one.
*   **Remove Properties:** Select tool **[T]** and click on a finished door. It becomes a normal static wall again.
*   **Fix (Ctrl + T):** If the door opens the wrong way or is out of sync: exit to selection mode (Esc), select the door, and press **Ctrl + T**. This inverts its state.

### How to use:
1.  Alt+RMB in Creative Mode - to open/close.
2.  LMB in Adventure Mode - to open/close.

---

## 🎨 5. Painting and Materials [X]

Press **[X]** to open the materials panel on the right. In this mode, the camera unlocks for UI interaction.

### Parameters:
*   **HSV (Hue, Sat, Val):** Color adjustment.
*   **A (Alpha):** Transparency (0 = invisible, 1 = solid). Use for glass.
*   **E (Emit):** Glow strength. In *Adventure* mode, such blocks emit light.
*   **G (Gloss):** Gloss/Shine. Determines reflections from sun and lamps.
*   **D (Dens):** Density and Physics.
    *   **1.0:** Solid block.
    *   **0.25 ... 0.99:** Liquid (Water). Player swims in this block, movement slows, gravity weakens.
    *   **<0.25:** Ghost/Gas. You can pass freely through the block.
*   **M (Mirr):** Mirror. Turns surface into a mirror (affects performance!).

### Application:
*   **"Full" Checkbox (Paint Entire):**
    *   *On:* Paints the entire cube.
    *   *Off:* Paints only **one face**. (To select a face, in *Select* mode use **Ctrl + Click** on the face).
*   **"Tile" Checkbox:** Enables texture repetition (tiling) instead of stretching it over the whole face.
*   **"Load Texture" Button:** Load image (.png, .jpg, .gif) from disk. Supports animated GIFs!
*   **Ctrl + X (Eyedropper):** Hover over a block in the world and press to copy all its properties (color, texture, physics) to the palette.
*   **Double Tap [X]:** Instantly apply current palette settings to the selected object without opening the menu.

### 🎛️ Texture Editing (UV-Mapping)
While materials window **[X]** is open and a textured object is selected, you can move the image on the surface:
*   **W / A / S / D:** Shift texture vertically and horizontally.
*   **Arrows:** Stretch and compress texture (tiling).
*   **Shift + Keys:** Fast change.
*   **Ctrl + Keys:** Precise adjustment (slow).
*   **[R] / [F]:** Rotate and flip texture (works same as objects).

### 🕒 Material History
At the bottom of the materials panel are colored rectangles ("chips"). This is the history of your last used settings. Click any of them to instantly restore that color and properties.

---

## 🖱️ 6. Selection and Manipulation (Select Mode)

This is the main working mode (like in CAD systems). Press **[Esc]** to switch to it from any tool.

### Selection Methods
1.  **Simple Click LMB:** Selects one object.
2.  **Ctrl + Click:** Add object to selection or remove from it.
3.  **Selection Frame (Hold RMB + Drag Mouse):**
    *   🟦 **Blue Frame (drag left-to-right):** Selects only objects that are **completely** inside the frame. (Logic "Inside").
    *   🟩 **Green Frame (drag right-to-left):** Selects everything the frame even **touches**. (Logic "Touch").

### Transforming Selected
*   **Move (Keyboard Arrows):**
    *   Arrows move object along active axis.
    *   **[Q]** — Change active movement plane. Switches between axes X, Y (Vertical), and Z.
*   **Scale [E]:**
    *   Press **[E]**, then press arrows (works like Push/Pull).
    *   **[Alt] + Arrows:** Uniform scaling of object in all directions (from center).
*   **Delete:** **Delete** key.

### Undo/Redo
*   **Ctrl + Z:** Undo last action.
*   **Ctrl + Y:** Redo cancelled action.

### Rotation and Mirroring (Important!)
In Anterio, rotation happens strictly along axes.
1.  First select transformation axis by pressing **Ctrl + Q** (or just Q). At the bottom of screen, you will see tooltip: *Axis X / Axis Y / Axis Z*.
2.  **[R]:** Rotate selected 90° around selected axis.
3.  **[F]:** Flip mirror-wise along selected axis.

### Grouping
*   **[G]:** Group selected. Objects will be selected with a single click.
*   **[G] (again):** Ungroup (if an existing group is selected).
*   **[C] (Combine):** Attempt to physically combine (weld) two selected cubes into one.

### Copying
*   **Ctrl + C:** Copy selected to clipboard.
*   **Ctrl + V:** Paste. Object "hangs" on cursor. It smartly snaps to surfaces.

---

## 📏 7. Interactive Tape Measure

Anterio automatically shows dimensions (X/Y/Z) of selected object. However, you can use selection tools as a tape measure to measure distance between objects.

**How to measure distance between two walls:**

1.  Go to **Select [Esc]** mode.
2.  Hover cursor over first face, click **LMB** (face highlights with blue grid).
3.  Holding **Ctrl**, click on second face on another object.
4.  When exactly **two faces** are selected, a colored line stretches between their centers showing exact distance and axis offset.

## ⚙️ 8. Menu, Export, and Settings

Press **[Esc]** (if nothing is selected) to open Pause/Menu.
*   **New Wall Thickness:** Slider sets wall thickness for new objects.
*   **Fog Distance:** Draw distance and fog.
*   **FPS Limit:** Frame limiter (On/Off).
*   **Save / Load:** File manager. Supports project formats `.ant`, `.zip`, `.json`.
*   **Export 3D:** Export your scene to popular 3D formats (.obj, .glb, .stl) for use in Blender, Unity, or 3D printing.
*   **Ctrl + Alt + S:** Quick save directly in game.
*   **Language:** Interface language switch button (English / Russian).

---

## 🎥 9. Cine-Cam and Video Render [C]

Anterio features a built-in non-linear camera motion editor for creating smooth cinematic flybys.

1.  Press **[C]** to enter Cine Cam mode.
2.  **Adding Frames:**
    *   Move to desired point.
    *   Press **Enter**. Current position and FOV are saved as a Keyframe.
    *   Fly to another point and press **Enter** again. A trajectory appears between points.
3.  **Editing:**
    *   **LMB** on point on trajectory — select frame.
    *   **Enter** (on selected frame) — overwrite camera position in this frame to current.
    *   **Delete** — delete frame.
    *   **Shift + Left/Right Arrows** — change frame order.
4.  **Smoothness Settings (on selected frame):**
    *   **Up/Down Arrows:** Change duration.
    *   **Ctrl + Up/Down:** Change Ease In/Out.
    *   **Ctrl + Left/Right:** Change trajectory Tension/Smoothing.
5.  **Render:** Press **[C] (inside mode)** or export button to save flyby as video file (.mp4).
6.  **Save Slots:** In camera mode, keys **[1] ... [0]** switch slots. You can record up to 10 different flight paths in one project.

---

## ⌨️ 10. Cheat Sheet

### 🔹 General
| Key | Action |
| :--- | :--- |
| **TAB** | Switch Mode (Build <-> Adventure) |
| **Esc** | Exit to Select / Menu |
| **Ctrl** (hold) | 1 cm Grid (Precision) |
| **Shift** | Fly Down (Creative) / Crouch (Adv) |
| **Q** | Change Axis/Plane (Hor/Vert) |
| **Alt + RMB** | Open Door (Creative) |
| **Ctrl + Z / Y** | Undo / Redo |
| **Ctrl + E** | Sun Editor |
| **C** | Cine-Cam Mode |

### 🔨 Tools
| Key | Tool |
| :--- | :--- |
| **1** | Wall |
| **2** | Box |
| **3** | Room |
| **4** | Strip |
| **5** | Cube (LMB-Cut, RMB-Add) |
| **6** | Cut (+Alt for Through Cut) |
| **7** | Slice |
| **T** | Create Door (Ctrl+T - Invert) |
| **X** | Materials / Eyedropper (Ctrl+X) |
| **Ctrl + Alt + S** | Quick Save |

### 📐 Object Manipulation (Select)
| Key | Action |
| :--- | :--- |
| **LMB** | Select |
| **RMB (drag)** | Selection Frame |
| **Arrows** | Move (along Q axis) |
| **E** | Scale (+Alt Uniform) |
| **Ctrl + Q** | **Select Axis (XYZ) for R/F** |
| **R** | Rotate 90° |
| **F** | Flip (Mirror) |
| **G** | Group |
| **C** | Combine |
| **Ctrl+C / V** | Copy / Paste |
| **Delete** | Delete |
| **WASD / Arrows** | Texture Shift/Scale |