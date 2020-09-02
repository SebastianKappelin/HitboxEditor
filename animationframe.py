from imageframe import ImageFrame


class AnimationFrame:

    hitboxes_visible = True
    hurtboxes_visible = True
    throwboxes_visible = True
    proximityboxes_visible = True
    pushboxes_visible = True
    position_visible = True

    hitbox_color = "#ff0000"
    hurtbox_color = "#00ff00"
    throwbox_color = "#0000ff"
    pushbox_color = "#ffff00"
    position_color = "#ff00ff"

    def __init__(self, crop=None):
        # box-coords/crop = (left, up, right, down)
        # position = (x, y)
        self.hitboxes = []
        self.hurtboxes = []
        self.throwboxes = []
        self.pushboxes = []
        self.position = None
        self.crop = crop

    def get_boxes(self):
        boxes = []
        if AnimationFrame.hitboxes_visible:
            for i in range(len(self.hitboxes)):
                boxes.append(
                    {
                        "box": self.hitboxes[i],
                        "color": AnimationFrame.hitbox_color,
                    }
                )
        if AnimationFrame.hurtboxes_visible:
            for i in range(len(self.hurtboxes)):
                boxes.append(
                    {
                        "box": self.hurtboxes[i],
                        "color": AnimationFrame.hurtbox_color,
                    }
                )
        if AnimationFrame.throwboxes_visible:
            for i in range(len(self.throwboxes)):
                boxes.append(
                    {
                        "box": self.throwboxes[i],
                        "color": AnimationFrame.throwbox_color,
                    }
                )
        if AnimationFrame.pushboxes_visible:
            for i in range(len(self.pushboxes)):
                boxes.append(
                    {
                        "box": self.pushboxes[i],
                        "color": AnimationFrame.pushbox_color,
                    }
                )
        return boxes

    def get_position(self):
        if AnimationFrame.position_visible and self.position:
            return {
                "x": self.position[0],
                "y": self.position[1],
                "color": AnimationFrame.position_color,
            }
        else:
            return None

    def get_width(self):
        if self.crop:
            return self.crop["x1"] - self.crop["x0"]
        else:
            return 0

    def get_height(self):
        if self.crop:
            return self.crop["y1"] - self.crop["y0"]
        else:
            return 0

    def to_string(self):
        pass