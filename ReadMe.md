# 🎨 PixelEase

PixelEase is a lightweight pixel art editor built with **Python** and **Pygame**.  
It provides simple yet powerful tools to create, edit, and manage pixel art projects with ease.

---

## ✨ Features
- 🖌️ **Drawing Tools** – Pencil, Eraser, Line, Rectangle, Fill paint.
- 🔄 **Transformations** – Rotate, Flip horizontally, Flip vertically, Selection & Move.
- 🎛️ **Canvas Controls** – Move canvas, Zoom, Export & Import images.
- 🎨 **Color Palette Manager** – Add, remove, import/export custom palettes.
- 💾 **Project Management** – Save & Load pixel art projects.
- ⚙️ **Settings & Customization** – Adjust brush size, background, and more.

---
## User Manual
PixelEase is a lightweight pixel-art editor built with Pygame.
This manual explains how to use each tool, along with the keyboard shortcuts.

### 🖱️ Basic Controls

* Left Mouse Button (LMB) → Draw / apply tool action.

* Right Mouse Button (RMB) → Secondary action (like erase, cancel selection).

* Mouse Wheel → Zoom in/out the canvas
* Middle Mouse Button Press - Move the canvas

### ⌨️ Keyboard Shortcuts
#### 🔄 General

* Ctrl + Z → Undo

* Ctrl + Y → Redo

* Ctrl + S → Save file

* Ctrl + O → Import file

* Ctrl + E → Export file

* Esc → Exit to menu / close editor

* Ctrl + , → Open Settings

#### 🖌️ Drawing Tools

* P → Pencil Tool
   - Draw freehand with the selected color.

* E → Eraser Tool
  - Erase pixels (makes them transparent).

* L → Line Tool
  - Click and drag to draw a straight line.

* R → Rectangle Tool
  - Click and drag between two points to draw rectangles.

* C → Circle Tool
  - Click and drag between two points to draw circles.

* F → Fill Paint (Bucket)
  - Click on an area to fill with the selected color.

#### 🔧 Canvas Operations

* M → Move Tool
   - Drag layers or selections around.

* Shift + M → Move Canvas
  - Pan the entire canvas within the viewport.

* H → Flip Horizontally
* V → Flip Vertically
* Ctrl + R → Rotate Canvas / Selection
* Ctrl + Alt + R → Resize Canvas

#### 📦 Selection

* S → Selection Tool
   - Click and drag to select an area.
   - Use Delete to clear selection.
   - Use Ctrl + C / Ctrl + V to copy/paste.

#### 📂 File Operations

* Ctrl + O → Import File (PNG, JPG, etc.)
* Ctrl + S → Save Project (.pxe format or similar).
* Ctrl + E → Export as Image (PNG).

#### ⚙️ Settings & Exit

* Ctrl + , → Open Settings menu.
* Esc → Exit editor.

---
## 📸 Screenshots

---

## 🕹️ Controls
- **Mouse Left Click** – Select tool / Draw / Pick color.
- **Mouse Scroll** – Scroll through menus & palettes.
- **Keyboard Shortcuts** – (optional, if implemented) for faster workflow.

---

## 🚀 Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/PixelEase.git
   cd PixelEase
    ```
2. Install dependencies:
```
pip install pygame
```
3. Run the program:
```
python main.py
```
---
## 🛠️ Tech Stack

* Python 3.x
* Pygame
* Tkinter (for file dialogs & color chooser)

---

## 🤝 Contributing

Pull requests are welcome!
If you’d like to add new tools, improve performance, or suggest UI features, feel free to fork and contribute.

---

## 📜 License

MIT License – free to use and modify.