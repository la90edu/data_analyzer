class Colors:
    colors = {
        "current": "#FF5733",
        "global_color": "#33FF57",
        "research": "#5733FF"
    }

    @classmethod
    def get_color(cls, color_name):
        return cls.colors.get(color_name, None)

    @classmethod
    def set_color(cls, color_name, color_value):
        if color_name in cls.colors:
            cls.colors[color_name] = color_value
        else:
            raise KeyError(f"{color_name} is not a valid color key.")

    @classmethod
    def get_all_colors(cls):
        return cls.colors

    @property
    def current(self):
        return self.colors["current"]

    @property
    def global_color(self):
        return self.colors["global_color"]

    @property
    def research(self):
        return self.colors["research"]


