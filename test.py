import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))

# Make a red surface
surf = pygame.Surface((100, 100))
surf.fill((255, 0, 0))

# Convert surface to raw pixel data
raw_bytes = pygame.image.tostring(surf, "RGB")

# Convert back to surface
restored = pygame.image.tostring(raw_bytes, (100, 100), True)

# Display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    screen.blit(restored, (150, 100))
    pygame.display.flip()

# import tkinter as tk
# from tkinter import colorchooser
# import colorsys
#
#
# def rgb_to_hex(rgb):
#     return "#%02x%02x%02x" % rgb
#
#
# def hex_to_rgb(hex_color):
#     hex_color = hex_color.lstrip("#")
#     return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
#
#
# def generate_harmonies(base_rgb):
#     r, g, b = [x/255.0 for x in base_rgb]
#     h, l, s = colorsys.rgb_to_hls(r, g, b)
#
#     harmonies = {}
#
#     # Complementary
#     h2 = (h + 0.5) % 1.0
#     harmonies["Complementary"] = [
#         base_rgb,
#         tuple(int(x*255) for x in colorsys.hls_to_rgb(h2, l, s))
#     ]
#
#     # Triadic
#     harmonies["Triadic"] = [
#         base_rgb,
#         tuple(int(x*255) for x in colorsys.hls_to_rgb((h + 1/3) % 1.0, l, s)),
#         tuple(int(x*255) for x in colorsys.hls_to_rgb((h + 2/3) % 1.0, l, s))
#     ]
#
#     # Tetradic
#     harmonies["Tetradic"] = [
#         base_rgb,
#         tuple(int(x*255) for x in colorsys.hls_to_rgb((h + 0.25) % 1.0, l, s)),
#         tuple(int(x*255) for x in colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s)),
#         tuple(int(x*255) for x in colorsys.hls_to_rgb((h + 0.75) % 1.0, l, s))
#     ]
#
#     # Analogous
#     harmonies["Analogous"] = [
#         base_rgb,
#         tuple(int(x*255) for x in colorsys.hls_to_rgb((h + 0.08) % 1.0, l, s)),
#         tuple(int(x*255) for x in colorsys.hls_to_rgb((h - 0.08) % 1.0, l, s))
#     ]
#
#     # Monochromatic
#     harmonies["Monochromatic"] = [
#         tuple(int(c*255) for c in colorsys.hls_to_rgb(h, max(0, l-0.2), s)),
#         base_rgb,
#         tuple(int(c*255) for c in colorsys.hls_to_rgb(h, min(1, l+0.2), s))
#     ]
#
#     return harmonies
#
#
# class ColorSystemApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Full Color System")
#         self.color_frames = []
#
#         self.toolbar = tk.Frame(root)
#         self.toolbar.pack(fill="x", pady=5)
#
#         self.add_btn = tk.Button(self.toolbar, text="➕ Add Color Picker", command=self.add_color_picker)
#         self.add_btn.pack(side="left", padx=5)
#
#         self.clear_btn = tk.Button(self.toolbar, text="🗑 Clear All", command=self.clear_all)
#         self.clear_btn.pack(side="left", padx=5)
#
#         self.container = tk.Frame(root)
#         self.container.pack(pady=10, fill="both", expand=True)
#
#     def add_color_picker(self):
#         frame = tk.LabelFrame(self.container, text=f"Color Picker {len(self.color_frames)+1}", padx=5, pady=5)
#         frame.pack(fill="x", pady=5, padx=5)
#
#         pick_btn = tk.Button(frame, text="Pick Color", command=lambda f=frame: self.pick_color(f))
#         pick_btn.pack(side="left")
#
#         self.color_frames.append(frame)
#
#     def pick_color(self, frame):
#         color_code = colorchooser.askcolor(title="Choose Base Color")
#         if color_code:
#             base_rgb = tuple(map(int, color_code[0]))
#             harmonies = generate_harmonies(base_rgb)
#
#             # Clear old widgets
#             for widget in frame.winfo_children():
#                 if not isinstance(widget, tk.Button):
#                     widget.destroy()
#
#             # Show base color
#             tk.Label(frame, text="Base:", width=8).pack(side="left")
#             tk.Label(frame, bg=rgb_to_hex(base_rgb), width=10, height=2, relief="ridge").pack(side="left", padx=3)
#
#             # Show harmonies
#             for name, colors in harmonies.items():
#                 row = tk.Frame(frame)
#                 row.pack(fill="x", pady=2)
#
#                 tk.Label(row, text=name, width=12).pack(side="left")
#
#                 for c in colors:
#                     hex_c = rgb_to_hex(c)
#                     swatch = tk.Label(row, bg=hex_c, width=10, height=2, relief="ridge")
#                     swatch.pack(side="left", padx=2)
#                     tk.Label(row, text=hex_c).pack(side="left", padx=2)
#
#     def clear_all(self):
#         for frame in self.color_frames:
#             frame.destroy()
#         self.color_frames = []
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ColorSystemApp(root)
#     root.mainloop()
