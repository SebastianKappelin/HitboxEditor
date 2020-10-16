import copy


class Character:

    template = {
        "hp": "positive",
        "name": str,
        "stun": "positive",
        "image path": "image",
        # "position": {"x": int, "y": int},
        "actions": [
            {
                "name": str,
                "airborne": bool,
                "category": "category",
                "input": "?",
                "available when projectile on screen": bool,
                "frames": [
                    {
                        "frame number": "positive",
                        "damage": "positive",
                        "block damage": "positive",
                        "hitstun": "positive",
                        "blockstun": "positive",
                        "hitstop": "positive",
                        "slowdown": "positive",
                        "hit pushback": "positive",
                        "block pushback": "positive",
                        "attack number": "positive",
                        "cancellable": "?",
                        "state": str,
                        "move x": int,
                        "move y": int,
                        "high block": bool,
                        "low block": bool,
                        "meter gain hit": "positive",
                        "meter gain block": "positive",
                        "meter gain whiff": "positive",
                        "stun": "positive",
                        "spawn projectile": "?",
                        "go to frame": "?",
                        "opponent action": {"action": "?", "x": int, "y": int},
                        "position": {"x": int, "y": int},
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
                "number of hits": "positive",
                "move x": int,
                "move y": int,
                "frames": [
                    {
                        "frame number": "positive",
                        "damage": "positive",
                        "block damage": "positive",
                        "hitstun": "positive",
                        "blockstun": "positive",
                        "hitstop": "positive",
                        "slowdown": "positive",
                        "hit pushback": "positive",
                        "block pushback": "positive",
                        "high block": bool,
                        "low block": bool,
                        "meter gain hit": "positive",
                        "meter gain block": "positive",
                        "stun": "positive",
                        "go to frame": "?",
                        "position": {"x": int, "y": int},
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
        "work in progress",
    ]

    universal_actions = [
        {
            "category": "other",
            "name": "stand",
        },
        {
            "category": "other",
            "name": "crouch",
        },
        {
            "category": "other",
            "name": "walk forward",
        },
        {
            "category": "other",
            "name": "walk backward",
        },
        {
            "category": "other",
            "name": "jump",
        },
        {
            "category": "other",
            "name": "jump forward",
        },
        {
            "category": "other",
            "name": "jump backward",
        },
        {
            "category": "other",
            "name": "stand block",
        },
        {
            "category": "other",
            "name": "crouch block",
        },
        {
            "category": "other",
            "name": "stand hitstun",
        },
        {
            "category": "other",
            "name": "crouch hitstun",
        },
        {
            "category": "other",
            "name": "knock down",
        },
        {
            "category": "other",
            "name": "air reset",
        },
        {
            "category": "other",
            "name": "get up",
        },
        {
            "category": "normal",
            "name": "light punch",
        },
        {
            "category": "normal",
            "name": "light kick",
        },
        {
            "category": "normal",
            "name": "heavy punch",
        },
        {
            "category": "normal",
            "name": "heavy kick",
        },
        {
            "category": "normal",
            "name": "crouch light punch",
        },
        {
            "category": "normal",
            "name": "crouch light kick",
        },
        {
            "category": "normal",
            "name": "crouch heavy punch",
        },
        {
            "category": "normal",
            "name": "crouch heavy kick",
        },
        {
            "category": "normal",
            "name": "jump light punch",
        },
        {
            "category": "normal",
            "name": "jump light kick",
        },
        {
            "category": "normal",
            "name": "jump heavy punch",
        },
        {
            "category": "normal",
            "name": "jump heavy kick",
        },
    ]

    default_action = {"category": "work in progress", "name": "default"}
    default_category = "other"

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

    box_template = {
        "attack": bool,
        "projectile": bool,
        "reflect": bool,
        "throw": bool,
        "attack_vulnerable": bool,
        "projectile_vulnerable": bool,
        "throw_vulnerable": bool,
        "push": bool,
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

    visible_objects_template = {
        "attack": bool,
        "projectile": bool,
        "reflect": bool,
        "throw": bool,
        "attack_vulnerable": bool,
        "projectile_vulnerable": bool,
        "throw_vulnerable": bool,
        "push": bool,
        "position": bool,
    }

    visible_objects = {
        "attack": True,
        "projectile": True,
        "reflect": True,
        "throw": True,
        "attack_vulnerable": True,
        "projectile_vulnerable": True,
        "throw_vulnerable": True,
        "push": True,
        "position": True,
    }

    position_color = {"r": 0xFF, "g": 0x20, "b": 0xA0}

    no_image = "No Image Selected"

    def __init__(self, image=None, character=None):
        if character:
            self.attributes = self.load_character(Character.template, character)
        else:
            self.attributes = self.create_empty_object(Character.template)
        if image:
            self.attributes["image path"] = image
        for i in range(len(Character.universal_actions)):
            self.create_action(
                Character.universal_actions[i]["name"],
                Character.universal_actions[i]["category"],
            )
        self.set_default_current_action()
        # self.current_action = self.get_action(
        #     Character.default_action["name"], Character.default_action["category"]
        # )
        # if not self.current_action:
        #     self.current_action = self.create_action(
        #         Character.default_action["name"], Character.default_action["category"]
        #     )
        # self.current_frame = -1
        self.copied_frame = None

    def create_action(self, name, category, **kwargs):
        for i in range(len(self.attributes["actions"])):
            if (
                self.attributes["actions"][i]["name"] == name
                and self.attributes["actions"][i]["category"] == category
            ):
                return None
        action = self.create_empty_object(Character.template["actions"][0])
        action["category"] = category
        action["name"] = name
        for k, v in kwargs.items():
            action[k] = v
        self.attributes["actions"].append(action)
        # self.current_action = action
        # return self.current_action
        return action

    def delete_action(self, name, category):
        for i in range(len(self.attributes["actions"])):
            if (
                self.attributes["actions"][i]["name"] == name
                and self.attributes["actions"][i]["category"] == category
            ):
                if self.current_action == self.attributes["actions"].pop(i):
                    self.set_default_current_action()
                    # self.current_action = self.get_action(
                    #     Character.default_action["name"],
                    #     Character.default_action["category"],
                    # )
                    # if not self.current_action:
                    #     self.current_action = self.create_action(
                    #         Character.default_action["name"],
                    #         Character.default_action["category"],
                    #     )
                return True
        return False

    def get_action(self, name, category):
        for i in range(len(self.attributes["actions"])):
            if (
                self.attributes["actions"][i]["name"] == name
                and self.attributes["actions"][i]["category"] == category
            ):
                self.current_frame = -1
                return self.attributes["actions"][i]
        return None

    # def set_current_action(self, name, category):
    #     self.current_action = self.get_action(name, category)
    #     if not self.current_action:
    #         self.current_action = self.set_default_current_action()

    def set_current_action(self, action):
        self.current_action = action
        self.current_frame = -1

    def set_default_current_action(self):
        self.current_action = self.get_action(
            Character.default_action["name"], Character.default_action["category"]
        )
        if not self.current_action:
            self.current_action = self.create_action(
                Character.default_action["name"], Character.default_action["category"]
            )
        self.current_frame = -1

    def create_animation_frame(self, crop):
        if not self.current_action:
            return
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
        if self.all_box_types_inactive():
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
                    and Character.visible_objects[k]
                ):
                    to_append["color"]["r"] += Character.box_colors[k]["r"]
                    to_append["color"]["g"] += Character.box_colors[k]["g"]
                    to_append["color"]["b"] += Character.box_colors[k]["b"]
                    num_colors += 1
            if num_colors == 0:
                continue
            if num_colors > 0:
                for k, v in to_append["color"].items():
                    to_append["color"][k] = int(to_append["color"][k] / num_colors)
            to_return.append(to_append)
        return to_return

    def set_position(self, position):
        if self.current_frame == -1:
            return
        self.current_action["frames"][self.current_frame]["position"] = position

    def get_position(self):
        return self.current_action["frames"][self.current_frame]["position"]

    def get_position_and_color(self):
        to_return = {}
        to_return["position"] = self.current_action["frames"][self.current_frame][
            "position"
        ]
        to_return["color"] = Character.position_color
        return to_return

    def is_position_visible(self):
        return Character.visible_objects["position"]

    def frame_has_position(self):
        if self.current_frame == -1:
            return False
        if self.current_action["frames"][self.current_frame]["position"]:
            return True
        return False

    def frame_position_x(self):
        if self.current_frame == -1:
            return 0
        if self.current_action["frames"][self.current_frame]["position"]:
            return self.current_action["frames"][self.current_frame]["position"]["x"]
        else:
            return 0

    def frame_position_y(self):
        if self.current_frame == -1:
            return 0
        if self.current_action["frames"][self.current_frame]["position"]:
            return self.current_action["frames"][self.current_frame]["position"]["y"]
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

    # The first frame is shown as 1.
    def get_current_frame_number(self):
        return self.current_frame + 1

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
            current_position = self.current_action["frames"][i]["position"]
            if current_position:
                if current_position["x"] > largest_x:
                    largest_x = current_position["x"]
                if current_position["y"] > largest_y:
                    largest_y = current_position["y"]
        return {"x": largest_x, "y": largest_y}

    def load_character(self, template, character):
        to_return = self.create_empty_object(template)
        for k, v in character.items():
            # if k not in to_return:
            #     continue  # If attributes not in template shouldn't be loaded.
            if isinstance(v, dict):
                to_return[k] = self.load_character(template[k], v)
            elif isinstance(v, list):
                for i in range(len(v)):
                    to_return[k].append(self.load_character(template[k][0], v[i]))
            else:
                to_return[k] = v
        return to_return

    def create_empty_object(self, template):
        to_return = {}
        for k, v in template.items():
            if v == int:
                to_return[k] = 0
            elif v == "positive":
                to_return[k] = 0
            elif v == str:
                to_return[k] = "Not set"
            elif v == bool:
                to_return[k] = False
            elif v == "category":
                to_return[k] = Character.default_category
            elif v == "image":
                to_return[k] = Character.no_image
            elif v == "?":
                to_return[k] = v
            elif isinstance(v, dict):
                to_return[k] = None
            elif isinstance(v, list):
                to_return[k] = []
        return to_return

    def image_chosen(self):
        if self.attributes["image path"] != Character.no_image:
            return True
        return False

    #
    # def has_current_action(self):
    #     if self.current_action:
    #         return True
    #     return False

    def number_of_actions(self):
        return len(self.attributes["actions"])

    def get_all_actions(self):
        return self.attributes["actions"]

    def get_current_action(self):
        return self.current_action

    def get_action_name(self, action):
        return action["name"]

    def get_action_category(self, action):
        return action["category"]

    def get_action_input(self, action):
        return action["input"]

    def get_action_total_frames(self, action):
        return len(action["frames"])

    def get_attributes(self):
        return self.attributes

    def get_current_animation_frame(self):
        return self.current_action["frames"][self.current_frame]

    def get_animation_frame_template(self):
        return Character.template["actions"][0]["frames"][0]

    def apply_changes(self, to_change, changes):
        for k, v in changes.items():
            to_change[k] = v

    # Prevents actions from getting the same name-category pair
    def try_apply_action_changes(self, to_change, changes):
        for i in range(len(self.attributes["actions"])):
            if (
                self.attributes["actions"][i]["name"] == changes["name"]
                and self.attributes["actions"][i]["category"] == changes["category"]
            ) and (
                changes["name"] != to_change["name"]
                or changes["category"] != to_change["category"]
            ):
                return None
        for k, v in changes.items():
            to_change[k] = v
        return to_change

    def get_action_template(self):
        return Character.template["actions"][0]

    def all_box_types_inactive(self):
        for k, v in Character.box_types.items():
            if v:
                return False
        return True