import copy


class Character:

    template = {
        "hp": int,
        "name": str,
        "stun": int,
        "image path": "image",
        "position": {"x": int, "y": int},
        "actions": [
            {
                "name": str,
                "category": str,
                "input": "?",
                "meter gain whiff": int,
                "available when projectile on screen": bool,
                "frames": [
                    {
                        "frame number": int,
                        "damage": int,
                        "block damage": int,
                        "hitstun": int,
                        "blockstun": int,
                        "hitstop": int,
                        "slowdown": int,
                        "hit pushback": int,
                        "block pushback": int,
                        "attack number": int,
                        "cancellable": "?",
                        "state": str,
                        "move x": int,
                        "move y": int,
                        "high block": bool,
                        "low block": bool,
                        "meter gain hit": int,
                        "meter gain block": int,
                        "stun": int,
                        "spawn projectile": "?",
                        "go to frame": "?",
                        "opponent action": {"action": "?", "x": int, "y": int},
                        "frame position": {"x": int, "y": int},
                        "boxes": [
                            {
                                "box": {
                                    "x0": int,
                                    "x1": int,
                                    "y0": int,
                                    "y1": int,
                                },
                                "type": {
                                    "attack": bool,
                                    "projectile": bool,
                                    "reflect": bool,
                                    "throw": bool,
                                    "attack vulnerable": bool,
                                    "projectile vulnerable": bool,
                                    "throw vulnerable": bool,
                                    "push": bool,
                                },
                            }
                        ],
                        "crop": {"x0": int, "x1": int, "y0": int, "y1": int},
                    }
                ],
            }
        ],
        "projectiles": [
            {
                "name": str,
                "number of hits": int,
                "position": {"x": int, "y": int},
                "move x": int,
                "move y": int,
                "frames": [
                    {
                        "frame number": int,
                        "damage": int,
                        "block damage": int,
                        "hitstun": int,
                        "blockstun": int,
                        "hitstop": int,
                        "slowdown": int,
                        "hit pushback": int,
                        "block pushback": int,
                        "high block": bool,
                        "low block": bool,
                        "meter gain hit": int,
                        "meter gain block": int,
                        "stun": int,
                        "go to frame": "?",
                        "boxes": [{"x0": int, "x1": int, "y0": int, "y1": int}],
                        "crop": {"x0": int, "x1": int, "y0": int, "y1": int},
                    }
                ],
            }
        ],
        "colors": "?",
    }

    action_categories = [
        "other",
        "normal",
        "command normal",
        "throw",
        "special",
        "super",
    ]

    universal_actions = {
        "other": "stand",
        "normal": "light punch",
        "normal": "light kick",
    }

    box_colors = {
        "attack": {"r": 0xFF, "g": 0x00, "b": 0x0},
        "projectile": {"r": 0x00, "g": 0xFF, "b": 0xFF},
        "reflect": {"r": 0xDD, "g": 0xDD, "b": 0xDD},
        "throw": {"r": 0x00, "g": 0x00, "b": 0xFF},
        "attack_vulnerable": {"r": 0x00, "g": 0xFF, "b": 0x00},
        "projectile_vulnerable": {"r": 0xAA, "g": 0x00, "b": 0xFF},
        "throw_vulnerable": {"r": 0xFF, "g": 0x00, "b": 0xFF},
        "push": {"r": 0xFF, "g": 0xFF, "b": 0x00},
    }

    box_types = {
        "attack": False,
        "projectile": False,
        "reflect": False,
        "throw": False,
        "attack_vulnerable": False,
        "projectile_vulnerable": False,
        "throw_vulnerable": False,
        "push": False,
    }

    box_visible = {
        "attack": True,
        "projectile": True,
        "reflect": True,
        "throw": True,
        "attack_vulnerable": True,
        "projectile_vulnerable": True,
        "throw_vulnerable": True,
        "push": True,
    }

    position_color = {"r": 0xFF, "g": 0x20, "b": 0xA0}

    def __init__(self, image="No image selected", character=None):
        self.attributes = self.create_empty_object(Character.template)
        self.attributes["image path"] = image
        if character:
            self.load_character(Character.template, self.attributes, character)
            self.current_action = self.get_action("other", "stand")
        else:
            self.create_action("other", "stand")
            self.current_action = self.get_action("other", "stand")
        self.current_frame = -1
        self.copied_frame = None

    def create_action(self, category, name, **kwargs):
        for i in range(len(self.attributes["actions"])):
            if (
                self.attributes["actions"][i]["category"] == category
                and self.attributes["actions"][i]["name"] == name
            ):
                pass
        action = self.create_empty_object(Character.template["actions"][0])
        action["category"] = category
        action["name"] = name
        self.attributes["actions"].append(action)
        self.current_action = action

    def get_action(self, category, name):
        for i in range(len(self.attributes["actions"])):
            if (
                self.attributes["actions"][i]["category"] == category
                and self.attributes["actions"][i]["name"] == name
            ):
                return self.attributes["actions"][i]
        return None

    def create_animation_frame(self, crop):
        self.current_frame += 1
        self.current_action["frames"].insert(
            self.current_frame,
            self.create_empty_object(self.template["actions"][0]["frames"][0]),
        )
        self.current_action["frames"][self.current_frame]["crop"] = crop

    # Insertion happens at the frame behind the current one
    def insert_animation_frame(self, animation_frame):
        self.current_frame += 1
        self.current_action["frames"].insert(
            self.current_frame,
            animation_frame,
        )

    def delete_animation_frame(self):
        if self.current_frame == -1:
            return
        self.current_action["frames"].pop(self.current_frame)
        if self.current_frame == len(self.current_action["frames"]):
            self.current_frame -= 1

    def copy_animation_frame(self):
        self.copied_frame = copy.deepcopy(
            self.current_action["frames"][self.current_frame]
        )

    def paste_animation_frame(self):
        self.insert_animation_frame(self.copied_frame)
        self.copy_animation_frame()

    def get_current_crop(self):
        if self.current_frame == -1:
            return {"x0": 0, "x1": 0, "y0": 0, "y1": 0}
        return self.current_action["frames"][self.current_frame]["crop"]

    def create_box(self, box):
        if self.current_frame == -1:
            return
        self.current_action["frames"][self.current_frame]["boxes"].append(
            self.create_empty_object(
                self.template["actions"][0]["frames"][0]["boxes"][0]
            )
        )
        self.current_action["frames"][self.current_frame]["boxes"][-1]["box"] = box
        self.current_action["frames"][self.current_frame]["boxes"][-1][
            "type"
        ] = copy.deepcopy(Character.box_types)

    def delete_box(self, index):
        self.current_action["frames"][self.current_frame]["boxes"].pop(index)

    # returns a list of boxes and a color based on its typings
    def get_boxes(self):
        to_return = []
        if self.current_frame == -1:
            return to_return
        for i in range(len(self.current_action["frames"][self.current_frame]["boxes"])):
            to_append = {}
            to_append["box"] = self.current_action["frames"][self.current_frame][
                "boxes"
            ][i]["box"]
            to_append["color"] = {"r": 0, "g": 0, "b": 0}
            num_colors = 0
            for k, v in self.current_action["frames"][self.current_frame]["boxes"][i][
                "type"
            ].items():
                if (
                    self.current_action["frames"][self.current_frame]["boxes"][i][
                        "type"
                    ][k]
                    and Character.box_visible[k]
                ):
                    to_append["color"]["r"] += Character.box_colors[k]["r"]
                    to_append["color"]["g"] += Character.box_colors[k]["g"]
                    to_append["color"]["b"] += Character.box_colors[k]["b"]
                    num_colors += 1
            if num_colors > 0:
                for k, v in to_append["color"].items():
                    to_append["color"][k] = int(to_append["color"][k] / num_colors)
            to_return.append(to_append)
        return to_return

    def set_position(self, position):
        if self.current_frame == -1:
            return
        self.current_action["frames"][self.current_frame]["frame position"] = position

    def get_position(self):
        to_return = {}
        to_return["position"] = self.current_action["frames"][self.current_frame][
            "frame position"
        ]
        to_return["color"] = Character.position_color
        return to_return

    def frame_has_position(self):
        if self.current_frame == -1:
            return False
        if self.current_action["frames"][self.current_frame]["frame position"]:
            return True
        return False

    def frame_position_x(self):
        if self.current_action == -1:
            return 0
        if self.current_action["frames"][self.current_frame]["frame position"]:
            return self.current_action["frames"][self.current_frame]["frame position"][
                "x"
            ]
        else:
            return 0

    def frame_position_y(self):
        if self.current_action == -1:
            return 0
        if self.current_action["frames"][self.current_frame]["frame position"]:
            return self.current_action["frames"][self.current_frame]["frame position"][
                "y"
            ]
        else:
            return 0

    def previous_frame(self):
        if self.current_frame == -1:
            self.current_frame = len(self.current_action["frames"]) - 1
        else:
            self.current_frame -= 1

    def next_frame(self):
        if self.current_frame + 1 >= len(self.current_action["frames"]):
            self.current_frame = -1
        else:
            self.current_frame += 1

    def get_total_frames(self):
        return len(self.current_action["frames"])

    def get_crop_width(self):
        if self.current_frame == -1:
            return 0
        return (
            self.current_action["frames"][self.current_frame]["crop"]["x1"]
            - self.current_action["frames"][self.current_frame]["crop"]["x0"]
        )

    def get_crop_height(self):
        if self.current_frame == -1:
            return 0
        return (
            self.current_action["frames"][self.current_frame]["crop"]["y1"]
            - self.current_action["frames"][self.current_frame]["crop"]["y0"]
        )

    def get_crop_tuple(self):
        if self.current_frame == -1:
            return 0, 0, 0, 0
        return (
            self.current_action["frames"][self.current_frame]["crop"]["x0"],
            self.current_action["frames"][self.current_frame]["crop"]["y0"],
            self.current_action["frames"][self.current_frame]["crop"]["x1"],
            self.current_action["frames"][self.current_frame]["crop"]["y1"],
        )

    def find_largest_crop_dimensions(self):
        largest_width = int(0)
        largest_height = int(0)
        for i in range(len(self.current_action["frames"])):
            current_crop = self.current_action["frames"][i]["crop"]
            if current_crop["x1"] - current_crop["x0"] > largest_width:
                largest_width = current_crop["x1"] - current_crop["x0"]
            if current_crop["y1"] - current_crop["y0"] > largest_height:
                largest_height = current_crop["y1"] - current_crop["y0"]
        return (largest_width, largest_height)

    def find_most_extreme_positions(self):
        largest_x = int(0)
        largest_y = int(0)
        for i in range(len(self.current_action["frames"])):
            current_position = self.current_action["frames"][i]["frame position"]
            if current_position:
                if current_position["x"] > largest_x:
                    largest_x = current_position["x"]
                if current_position["y"] > largest_y:
                    largest_y = current_position["y"]
        return {"x": largest_x, "y": largest_y}

    def load_character(self, template, attributes, character):
        for k, v in character.items():
            if isinstance(v, dict):
                attributes[k] = self.create_empty_object(template[k])
                self.load_character(template[k], attributes[k], v)
            elif isinstance(v, list):
                for i in range(len(v)):
                    attributes[k].append(self.create_empty_object(template[k][0]))
                    self.load_character(template[k][0], attributes[k][i], v[i])
            else:
                attributes[k] = v

    def create_empty_object(self, template):
        to_return = {}
        for k, v in template.items():
            if v == int:
                to_return[k] = 0
            elif v == str:
                to_return[k] = "Not set"
            elif v == "?":
                to_return[k] = v
            elif isinstance(v, dict):
                to_return[k] = None
            elif isinstance(v, list):
                to_return[k] = []
        return to_return

    def image_chosen(self):
        if self.attributes["image path"] != "No image selected":
            return True
        return False
