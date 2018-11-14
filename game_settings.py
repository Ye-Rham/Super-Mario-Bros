class Settings:
    def __init__(self):
        self.screen_width = 768
        self.screen_height = 720
        # NES Resolution = 256 x 240, Aspect ratio = 16:15
        self.scale = {"resolution_width": 256, "resolution_height": 240,
                      "pixel_width": self.screen_width/256, "pixel_height": self.screen_height/240}
        self.scale.update({"tile_width": self.scale["pixel_width"] * 16,
                           "tile_height": self.scale["pixel_height"] * 16})

        self.bg_color = ((148, 148, 255), (0, 0, 0))

        self.current_level = "overworld"
