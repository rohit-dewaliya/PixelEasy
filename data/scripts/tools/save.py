import pickle

import pygame

from tkinter import filedialog

from data.scripts.tools.file_manager import write_data, read_file, read_json_file, write_json_file
from data.scripts.canvas import Frame, Layer

def import_image(canvas, error_manager, canvas_surface_resize):
    try:
        save_path = filedialog.askopenfilename(
            title="Import Image",
            defaultextension=".png",
            filetypes=(
                ("Image files", "*.png;*.jpg;*.jpeg"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("All Files", "*.*")
            )
        )


        if save_path:
            image = pygame.image.load(save_path).convert_alpha()
            image_size = (image.get_width(), image.get_height())

            canvas_surface_resize(image_size)

            layer = canvas.image[canvas.selected_layer]
            frame = layer.frames[layer.selected_frame]
            frame.surface.blit(image, (0,0))

            error_manager.add_error("Import complete.", "success")

        if not save_path:
            error_manager.add_error("Can't export this canvas. Error occured.")

    except Exception as e:
        error_manager.add_error(f"Export failed: {e}")
        error_manager.add_error("Export Failed. Can't export this canvas. Error occurred!")


def export_canvas(canvas, error_manager):
    try:
        save_path = filedialog.asksaveasfilename(
            title="Import Image",
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("All Files", "*.*"))
        )

        if not save_path:
            error_manager.add_error("Can't export this canvas. Error occured.")

        total_frames = len(canvas.image[0].frames)

        for frame_index in range(total_frames):
            final_surface = pygame.Surface(canvas.surface_size, pygame.SRCALPHA)

            for layer in canvas.image:
                frame = layer.frames[frame_index]
                final_surface.blit(frame.surface, (0, 0))

            path = save_path.replace(".png", f"_{frame_index + 1}.png")
            pygame.image.save(final_surface, path)

        error_manager.add_error("Export complete. Canvas exported successfully!", "success")

    except Exception as e:
        error_manager.add_error(f"Export failed: {e}")
        error_manager.add_error("Export Failed. Can't export this canvas. Error occurred!")

def get_colors(color_palette):
    return [tuple(color) for  color in color_palette]

def get_canvas_data(canvas):
    data = {}
    for layer in canvas.image:
        layer_data = []
        for frame in layer.frames:
            layer_data.append(str(pygame.image.tobytes(frame.surface, "RGBA")))
        data[layer.name] = layer_data
    return data


def save_project(canvas, color_palette, error_manager):
    try:
        save_path = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("All Files", "*.*"))
        )

        if not save_path:
            error_manager.add_error("Export canceled by user.")
            return

        else:
            color_data = get_colors(color_palette.color_palette_color_manager.color_palette)
            canvas_data = get_canvas_data(canvas)
            data = {
                "color_palette": color_data,
                "canvas": {
                    "size": canvas.surface_size,
                    "layers": canvas_data
                }
            }
            write_json_file(save_path, data)
            error_manager.add_error("Export complete. Canvas exported successfully!", "success")

    except Exception as e:
        print(e)
        # error_manager.add_error(f"Export failed: {e}")
        # error_manager.add_error("Export Failed. Can't export this canvas. Error occurred!")

def import_project(canvas, color_palette, error_manager, frame_manager):
    try:
        load_path = filedialog.askopenfilename(
            title="Import Project",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("All Files", "*.*"))
        )

        if not load_path:
            error_manager.add_error("Export canceled by user.")
            return

        data = read_json_file(load_path)

        color_data = data["color_palette"]
        for color in color_data:
            color_palette.color_palette_color_manager.add_color(tuple(color))

        canvas_data = data["canvas"]
        canvas.surface_size = canvas_data.get("size")

        layer_data = canvas_data.get("layers")

        if layer_data:
            canvas.image = []

            for layer in layer_data:
                frame_data = []
                frames = layer_data[layer]
                for f in frames:
                    frame = Frame(canvas.surface_size)
                    frame.surface = pygame.Surface(frame.surface_size, pygame.SRCALPHA)
                    frame.surface.blit(pygame.image.frombytes(eval(f), frame.surface_size, "RGBA"), (0, 0))
                    frame_data.append(frame)
                l = Layer(canvas.surface_size, layer)
                l.frames = frame_data
                canvas.image.append(l)
                frame_manager.add_layer_rect()

        error_manager.add_error("Import complete. Canvas imported successfully!", "success")

    except Exception as e:
        error_manager.add_error(f"Export failed: {e}")
        error_manager.add_error("Export Failed. Can't export this canvas. Error occurred!")