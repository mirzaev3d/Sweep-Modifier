### 🛠️ Sweep Modifier (v2.0.0) – Documentation

**Author:** Abbos Mirzaev

**Blender Version:** 3.0+

**Category:** Modifier (Geometry Nodes)

**Location:**

- **Modifiers Tab → Generate Section**
- **Pie Menu:** `Ctrl + Shift + Q` (when a Mesh or Curve is selected)

---

<div align="left">
      <a href="[https://www.youtube.com/watch?v=5yLzZikS15k](https://youtu.be/lfTAdxE1cmk?si=D9Vzs0E4Lmnosqdz)">
         <img src="[https://img.youtube.com/vi/5yLzZikS15k/0.jpg](https://assets.superhivemarket.com/store/product/236044/image/xlarge_og-305229b5354d71de0e19686251fc3889.png)" style="width:100%;">
      </a>
</div>

---

### 📄 Description

The **Sweep Modifier** addon allows users to non-destructively apply a powerful Geometry Nodes-based sweep effect to any mesh or curve object. It automates the process of importing and applying a pre-designed node group from a local `.blend` file, making advanced procedural modeling more accessible.

Perfect for generating extruded profiles along curves, procedural rails, pipes, or custom profiles — all controlled via Blender’s modifier stack.

---

### 🧰 Features

✅ Adds a **Sweep Modifier** using Geometry Nodes

✅ Appears inside the **Modifier panel > Generate** section

✅ Includes a **Pie Menu** for quick access (`Ctrl + Shift + Q`)

✅ Auto-loads the Geometry Node group from a local `.blend` file

✅ Clean, non-destructive, and reversible

✅ Supports both **Mesh** and **Curve** objects

✅ Uses **PROP_PROJECTED** modifier icon for visual distinction

---

### 📦 Installation

1. Download the `.zip` addon file (e.g., `Sweep_Modifier_Addon_v2.zip`).
2. In Blender, go to **Edit > Preferences > Add-ons**.
3. Click **Install…**, select the ZIP file, and enable **Sweep Modifier**.

---

### 🧩 Asset Setup (Optional but Recommended)

1. Open the `Sweep Modifier.blend` file in Blender.
2. In the **Geometry Node Editor**, select the "Sweep Modifier" node group.
3. Press `F4` → **Mark as Asset**.
4. Save and close the file.
5. Go to **Edit > Preferences > File Paths > Asset Libraries**.
6. Click the `+` icon to add the folder containing the `.blend` file as an **Asset Library**.
7. Restart Blender.

Now the node group will be available from the Asset Browser if needed.

---

### 🧪 How to Use

### 📌 Method 1: From the Modifiers Panel

1. Select a **Mesh** or **Curve** object.
2. In the **Properties Panel**, open the **Modifiers tab**.
3. Scroll down to the **Generate section**.
4. Click **Sweep Modifier** (icon: 🧭).
5. The Geometry Nodes modifier is added with the sweep node group preloaded.

### 📌 Method 2: Using the Pie Menu

1. Select a **Mesh** or **Curve** in the 3D Viewport.
2. Press `Ctrl + Shift + Q` to open the **Sweep Modifier Pie Menu**.
3. Select “Add Sweep Modifier”.

---

### 🔄 Customization

Once the modifier is added:

- Open the **Modifier stack**.
- You will see a **Geometry Nodes** modifier labeled “Sweep Modifier”.
- You can expose inputs/outputs in the node group to control:
    - Profile shape
    - Curve path
    - Width, thickness, taper, etc.

For advanced customization, edit the **Sweep Modifier** node group in the **Geometry Nodes Editor**.

---

### 🧹 Uninstallation

1. Go to **Edit > Preferences > Add-ons**.
2. Search for **Sweep Modifier**, uncheck it, and click **Remove**.
3. Optionally, delete the associated asset library path from File Paths.

---
