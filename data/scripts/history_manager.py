import pygame
import copy

def copy_image(image):
    return [layer.copy() for layer in image]

class HistoryManager:
    def __init__(self, limit = 30):
        self.undo_stack = []
        self.redo_stack = []
        self.temp = []
        self.limit = limit

    def save_state(self, state):
        snapshot = copy.deepcopy(state)
        self.undo_stack.append(snapshot)

        if len(self.undo_stack) > self.limit:
            self.undo_stack.pop(0)

        self.redo_stack.clear()

    def undo(self, state):
        if self.undo_stack:
            snapshot = copy.deepcopy(state)
            self.redo_stack.append(snapshot)
            snapshot = self.undo_stack.pop()
            print(snapshot, end="\n\n\n")
        return state.copy()

    def redo(self, state):
        if self.redo_stack:
            snapshot = copy.deepcopy(state)
            self.undo_stack.append(snapshot)
            snapshot = self.redo_stack.pop()
            return snapshot.copy()
        return state.copy()
