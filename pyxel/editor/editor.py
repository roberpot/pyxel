import os

import numpy as np

import pyxel
from pyxel.ui import Widget

from .editor_constants import EDITOR_HEIGHT, EDITOR_WIDTH


class Editor(Widget):
    """
    Events:
        __on_undo(data)
        __on_redo(data)
    """

    def __init__(self, parent, image_file):
        super().__init__(parent, 0, 0, EDITOR_WIDTH, EDITOR_HEIGHT, is_visible=False)

        image_file = os.path.join(os.path.dirname(__file__), "assets", image_file)
        pyxel.image(3, system=True).load(0, 12, image_file)

        data = pyxel.image(3, system=True).data
        self._image_data = np.copy(data[12 : EDITOR_HEIGHT + 12, 0:EDITOR_WIDTH])

        self._edit_history_list = []
        self._edit_history_index = 0

        self.add_event_handler("show", self.__on_show)
        self.add_event_handler("draw", self.__on_draw)

    @property
    def can_undo(self):
        return self._edit_history_index > 0

    @property
    def can_redo(self):
        return self._edit_history_index < len(self._edit_history_list)

    def undo(self):
        if not self.can_undo:
            return

        self._edit_history_index -= 1
        self.call_event_handler(
            "undo", self._edit_history_list[self._edit_history_index]
        )

    def redo(self):
        if not self.can_redo:
            return

        self.call_event_handler(
            "redo", self._edit_history_list[self._edit_history_index]
        )
        self._edit_history_index += 1

    def add_edit_history(self, data):
        self._edit_history_list = self._edit_history_list[: self._edit_history_index]
        self._edit_history_list.append(data)
        self._edit_history_index += 1

    def __on_show(self):
        data = pyxel.image(3, system=True).data
        data[12 : 12 + EDITOR_HEIGHT, 0:EDITOR_WIDTH] = self._image_data

    def __on_draw(self):
        pyxel.blt(0, 0, 3, 0, 12, EDITOR_WIDTH, EDITOR_HEIGHT, 6)

    def draw_not_implemented_message(self):
        pyxel.rect(78, 83, 163, 97, 11)
        pyxel.rectb(78, 83, 163, 97, 1)
        pyxel.text(84, 88, "NOT IMPLEMENTED YET", 1)
