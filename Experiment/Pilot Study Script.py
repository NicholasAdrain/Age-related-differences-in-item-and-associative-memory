#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ─── Imports ─────────────────────────────────────────────────────────────────
import os
import csv
import random
from psychopy import visual, core, event, gui, data, logging

# ─── Experiment Mode Toggle ──────────────────────────────────────────────────
# Set one of the following modes:
#   "both"         – runs both item memory tasks
#   "item"         – runs only the object experiment
#   "scene"        – runs only the scene experiment
#   "pam_objects"  – runs only the PAM object-pairs condition
#   "pam_scenes"   – runs only the PAM scene-pairs condition
#   "pam_itemscene"– runs only the PAM item-scene-pairs condition
#   "pam_all"      – runs all three PAM conditions in sequence (with breaks)
#   "all"          – runs everything: item, scene, then all three PAM conditions

EXPERIMENT_MODE = "pam_all"

# ─── Experiment Settings ─────────────────────────────────────────────────────
FIXATION_DUR              = 0.5
RESPONSE_TIMEOUT          = 3.0
PRACTICE_NOCUE_TIMEOUT    = 3.0
PRACTICE_FEEDBACK_TIMEOUT = 12.0
SPACE_TIMEOUT             = 60.0
SPACE_COUNTDOWN_START     = 10
MAX_WRONG_PER_ITEM        = 3
FULLSCREEN                = True
BACKGROUND                = "white"
TEXT_COLOUR               = "black"
IMAGE_SIZE                = (500, 500)

# PAM-specific settings
PAM_PAIR_IMAGE_SIZE = (420, 420)   # each image in a side-by-side pair
PAM_PAIR_EXPOSURE   = 6.0          # seconds per pair during encoding
PAM_PAIR_GAP        = 40           # horizontal gap (px) between pair images

# Item experiment keys / labels
# NOTE: The labels Man-Made and Natural were switched out for 'Metal' and 'No Metal',
# However, the original keys are still being used.
KEY_MANMADE   = "f"
KEY_NATURAL   = "j"
LABEL_MANMADE = "Metal"
LABEL_NATURAL = "No Metal"

# Scene experiment keys / labels
KEY_INDOOR    = "f"
KEY_OUTDOOR   = "j"
LABEL_INDOOR  = "Indoor"
LABEL_OUTDOOR = "Outdoor"

BTN_BLUE = "#3a7ca5"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAM_BASE_DIR = os.path.join(BASE_DIR, "PAM_memory")


# ─── Helper: load a labelled folder ──────────────────────────────────────────
#Scans for folders

def load_labelled_folder(base_dir, labels):
    result = []
    for label in labels:
        folder = os.path.join(base_dir, label)
        if not os.path.isdir(folder):
            raise FileNotFoundError(
                f"Expected subfolder not found: {folder}\n"
                f"Please create it and add your stimuli images."
            )
        for fname in sorted(os.listdir(folder)):
            if fname.lower().endswith((".jpg", ".png", ".jpeg")):
                result.append({
                    "image":   os.path.join(label, fname),
                    "correct": label,
                })
    return result


# ─── ITEM Experiment Stimuli ──────────────────────────────────────────────────

ITEM_LABELS  = ["Metal", "Not Metal"]
SCENE_LABELS = ["Indoor", "Outdoor"]

ITEM_MEMORY_DIR           = os.path.join(BASE_DIR, "item_memory")
STIMULI_DIR               = os.path.join(ITEM_MEMORY_DIR, "stimuli")
PRACTICE_DIR              = os.path.join(ITEM_MEMORY_DIR, "practice")
PRACTICE_NOCUE_DIR        = os.path.join(ITEM_MEMORY_DIR, "practice_nocue")
SCENE_PRACTICE_NOCUE_DIR  = os.path.join(ITEM_MEMORY_DIR, "practice_nocue_scenes")
REC_PRACTICE_DIR          = os.path.join(ITEM_MEMORY_DIR, "recognition_practice")

STIMULUS_LIST          = load_labelled_folder(STIMULI_DIR,       ITEM_LABELS)
PRACTICE_FEEDBACK_LIST = load_labelled_folder(PRACTICE_DIR,      ITEM_LABELS)
PRACTICE_NOCUE_LIST    = load_labelled_folder(PRACTICE_NOCUE_DIR, ITEM_LABELS)

# ─── SCENE Experiment Stimuli ─────────────────────────────────────────────────
SCENE_STIMULI_DIR      = os.path.join(ITEM_MEMORY_DIR, "stimuli_scenes")
SCENE_PRACTICE_DIR     = os.path.join(ITEM_MEMORY_DIR, "practice_scenes")
SCENE_REC_PRACTICE_DIR = os.path.join(ITEM_MEMORY_DIR, "rec_practice_scenes")
SCENE_REC_NEW_DIR      = os.path.join(ITEM_MEMORY_DIR, "recognition_new_scenes")

SCENE_REC_NEW_LIST = [
    {"image": fname, "correct": "new"}
    for fname in sorted(os.listdir(SCENE_REC_NEW_DIR))
    if fname.lower().endswith((".jpg", ".jpeg", ".png"))
]

SCENE_STIMULUS_LIST          = load_labelled_folder(SCENE_STIMULI_DIR,       SCENE_LABELS)
SCENE_PRACTICE_FEEDBACK_LIST = load_labelled_folder(SCENE_PRACTICE_DIR,      SCENE_LABELS)
SCENE_PRACTICE_NOCUE_LIST    = load_labelled_folder(SCENE_PRACTICE_NOCUE_DIR, SCENE_LABELS)

# ─── Catch Trials ────────────────────────────────────────────────────────────
CATCH_TRIALS = [
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Metal)",
     "target_key": "f", "correct_label": "Metal"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (Not Metal)",
     "target_key": "j", "correct_label": "No Metal"},

]
CATCH_TIMEOUT = 3.0

REC_CATCH_TRIALS = [
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
]

SCENE_CATCH_TRIALS = [
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Indoor)",
     "target_key": "f", "correct_label": "Indoor"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (Outdoor)",
     "target_key": "j", "correct_label": "Outdoor"},
]

SCENE_REC_CATCH_TRIALS = [
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},

]

# ─── PAM Stimulus Paths ───────────────────────────────────────────────────────
PAM_OBJ_PAIRS_DIR  = os.path.join(PAM_BASE_DIR, "pam_objects", "pairs")
PAM_OBJ_PRAC_DIR   = os.path.join(PAM_BASE_DIR, "pam_objects", "practice")
PAM_SC_PAIRS_DIR   = os.path.join(PAM_BASE_DIR, "pam_scenes",  "pairs")
PAM_SC_PRAC_DIR    = os.path.join(PAM_BASE_DIR, "pam_scenes",  "practice")
PAM_IS_PAIRS_DIR   = os.path.join(PAM_BASE_DIR, "pam_itemscene", "pairs")
PAM_IS_PRAC_DIR    = os.path.join(PAM_BASE_DIR, "pam_itemscene", "practice")

PAM_OBJ_PAIR_LIST = [
    {"image_a": "bacon.png",              "image_b": "postalmailbox01.png"},
    {"image_a": "moon.png",               "image_b": "tongs01b.jpg"},
    {"image_a": "cabbage.jpg",            "image_b": "downhillski.jpg"},
    {"image_a": "mailbox01.png",          "image_b": "radish01.jpg"},
    {"image_a": "locker.jpg",             "image_b": "softcheese.jpg"},
    {"image_a": "fortunecookie.jpg",      "image_b": "sink.jpg"},
    {"image_a": "bleachers.png",          "image_b": "crayon.png"},
    {"image_a": "potato02b.jpg",          "image_b": "zipper.jpg"},
    {"image_a": "cauliflower01.png",      "image_b": "safe.jpg"},
    {"image_a": "carrot01.png",           "image_b": "kneepad01c.jpg"},
    {"image_a": "computerkeyboard02.png", "image_b": "icecube02.png"},
    {"image_a": "feather03a.jpg",         "image_b": "waterfountain02.jpg"},
    {"image_a": "cookiecutter.jpg",       "image_b": "onion.jpg"},
    {"image_a": "coffeemachine.jpg",      "image_b": "necklace.png"},
    {"image_a": "camera01a.png",          "image_b": "celery.png"},
    {"image_a": "baseballbat.png",        "image_b": "ginger.png"},
    {"image_a": "masquerademask01.png",   "image_b": "microwave.png"},
    {"image_a": "puzzlepiece.jpg",        "image_b": "whisk.png"},
    {"image_a": "bridge.png",             "image_b": "lipstick02a.jpg"},
    {"image_a": "blackberry.png",         "image_b": "stepladder.jpg"},
    {"image_a": "toysoldier01b.jpg",      "image_b": "xylophone.jpg"},
    {"image_a": "lighthouse.png",         "image_b": "paperclip03.png"},
    {"image_a": "bagel01.png",            "image_b": "laptop01a.png"},
    {"image_a": "blender.png",            "image_b": "windshieldwiper02.png"},
]

PAM_OBJ_PRACTICE_LIST = [
    {"image_a": "armchair.jpg",    "image_b": "balloons.jpg"},
    {"image_a": "basketball.jpg",  "image_b": "bicycle_bell.jpg"},
    {"image_a": "blanket.jpg",     "image_b": "nest.jpg"},
]

PAM_OBJ_REC_CATCH_TRIALS = [
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
]

PAM_SC_PAIR_LIST = [
    {"image_a": "fountain_A.jpg",         "image_b": "waiting_room_A.jpg"},
    {"image_a": "locker_room_A.jpg",       "image_b": "shopping_center_B.jpg"},
    {"image_a": "road_B.jpg",              "image_b": "home_office_B.jpg"},
    {"image_a": "airplane_interior_B.jpg", "image_b": "river_B.jpg"},
    {"image_a": "stage_B.jpg",             "image_b": "beach_B.jpg"},
    {"image_a": "gas_pump_B.jpg",          "image_b": "bedroom_B.jpg"},
    {"image_a": "garden_B.jpg",            "image_b": "restaurant_B.jpg"},
    {"image_a": "kiosk_A.jpg",             "image_b": "lake_B.jpg"},
    {"image_a": "library_B.jpg",           "image_b": "flower_shop_A.jpg"},
    {"image_a": "kitchen_B.jpg",           "image_b": "pool_B.jpg"},
    {"image_a": "castle_B.jpg",            "image_b": "movie_theater_A.jpg"},
    {"image_a": "waves.jpg",               "image_b": "gymnasium_B.jpg"},
    {"image_a": "field_A.jpg",             "image_b": "bar_A.jpg"},
    {"image_a": "living_room_B.jpg",       "image_b": "classroom_A.jpg"},
    {"image_a": "beach_A.jpg",             "image_b": "dentist_B.jpg"},
    {"image_a": "flower_shop_B.jpg",       "image_b": "building_stairs_B.jpg"},
    {"image_a": "balcony.jpg",             "image_b": "market_B.jpg"},
    {"image_a": "waiting_room_B.jpg",      "image_b": "street_B.jpg"},
    {"image_a": "train_station_B.jpg",     "image_b": "vegetable_garden_B.jpg"},
    {"image_a": "car_interior_A.jpg",      "image_b": "toy_store_B.jpg"},
    {"image_a": "terrace_A.jpg",           "image_b": "elevator_B.jpg"},
    {"image_a": "backyard_B.jpg",          "image_b": "pharmacy_B.jpg"},
    {"image_a": "toilet_B.jpg",            "image_b": "shopping_center_A.jpg"},
    {"image_a": "garage_B.jpg",            "image_b": "library_A.jpg"},
]

PAM_SC_PRACTICE_LIST = [
    {"image_a": "sc_prac_pair_01a.jpg", "image_b": "sc_prac_pair_01b.jpg"},
    {"image_a": "sc_prac_pair_02a.jpg", "image_b": "sc_prac_pair_02b.jpg"},
    {"image_a": "sc_prac_pair_03a.jpg", "image_b": "sc_prac_pair_03b.jpg"},
]

PAM_SC_REC_CATCH_TRIALS = [
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
]

PAM_IS_PAIR_LIST = [
    {"image_a": "fork.jpg",                "image_b": "stationary_store_A.jpg"},
    {"image_a": "pen.jpg",                 "image_b": "toilet_A.jpg"},
    {"image_a": "belt.jpg",                "image_b": "toy_store_A.jpg"},
    {"image_a": "water_bottle.jpg",        "image_b": "hair_salon_A.jpg"},
    {"image_a": "vacuum_cleaner.jpg",      "image_b": "lake_A.jpg"},
    {"image_a": "comb.jpg",                "image_b": "restaurant_A.jpg"},
    {"image_a": "hairdryer.jpg",           "image_b": "train_station_A.jpg"},
    {"image_a": "salt_shaker.jpg",         "image_b": "circus_A.jpg"},
    {"image_a": "wool_cap.jpg",            "image_b": "pool_A.jpg"},
    {"image_a": "keychain.jpg",            "image_b": "dentist_A.jpg"},
    {"image_a": "safety_pin.jpg",          "image_b": "market_A.jpg"},
    {"image_a": "airplane_belt.jpg",       "image_b": "garden_A.jpg"},
    {"image_a": "clothesline.jpg",         "image_b": "museum_B.jpg"},
    {"image_a": "lighter.jpg",             "image_b": "childrens_room_A.jpg"},
    {"image_a": "blackboard_eraser.jpg",   "image_b": "airport_B.jpg"},
    {"image_a": "wine_cork.jpg",           "image_b": "playground_A.jpg"},
    {"image_a": "battery.jpg",             "image_b": "sky_A.jpg"},
    {"image_a": "drawing_compass.jpg",     "image_b": "basketball_field_A.jpg"},
    {"image_a": "hose.jpg",                "image_b": "bedroom_A.jpg"},
    {"image_a": "mannequin.jpg",           "image_b": "vegetable_garden_A.jpg"},
    {"image_a": "beach_bucket.jpg",        "image_b": "bakery_A.jpg"},
    {"image_a": "domino_piece.jpg",        "image_b": "road_A.jpg"},
    {"image_a": "digital_piano.jpg",       "image_b": "parking_lot_A.jpg"},
    {"image_a": "feather.jpg",             "image_b": "pastry_shop_B.jpg"},
    {"image_a": "slippers.jpg",            "image_b": "theater_A.jpg"},
    {"image_a": "watering_can.jpg",        "image_b": "building_stairs_A.jpg"},
    {"image_a": "tennis_ball.jpg",         "image_b": "kitchen_A.jpg"},
    {"image_a": "3d_glasses.jpg",          "image_b": "elevator_A.jpg"},
    {"image_a": "shovel.jpg",              "image_b": "pharmacy_A.jpg"},
    {"image_a": "brush_tool.jpg",          "image_b": "car_interior_B.jpg"},
]

PAM_IS_PRACTICE_LIST = [
    {"image_a": "is_prac_pair_01a.jpg", "image_b": "is_prac_pair_01b.jpg"},
    {"image_a": "is_prac_pair_02a.jpg", "image_b": "is_prac_pair_02b.jpg"},
    {"image_a": "is_prac_pair_03a.png", "image_b": "is_prac_pair_03b.jpg"},
]

PAM_IS_REC_CATCH_TRIALS = [
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  J  (New)",
     "target_key": "j", "correct_label": "new"},
    {"prompt": "ATTENTION CHECK\n\nFor this trial, please press  F  (Old)",
     "target_key": "f", "correct_label": "old"},
]

# --- Participant Info Dialog --------------------------------------------------
exp_info = {
    "Participant ID": "",
    "Session":        "1",
}
dlg = gui.DlgFromDict(exp_info, title="Item Memory Task - Encoding", sortKeys=False)
if not dlg.OK:
    core.quit()
exp_info["date"] = data.getDateStr()

# --- Data Logging ---------------------------------------------------------
os.makedirs(os.path.join("data", "item_memory"), exist_ok=True)
os.makedirs(os.path.join("data", "PAM_memory"), exist_ok=True)

item_filename = os.path.join(
    "data", "item_memory",
    f"sub-{exp_info['Participant ID']}_ses-{exp_info['Session']}_encoding_{exp_info['date']}"
)
pam_filename = os.path.join(
    "data", "PAM_memory",
    f"sub-{exp_info['Participant ID']}_ses-{exp_info['Session']}_encoding_{exp_info['date']}"
)

logging.LogFile(item_filename + ".log", level=logging.EXP)
logging.console.setLevel(logging.WARNING)

exp_handler = data.ExperimentHandler(
    name="ItemMemoryEncoding",
    version="5.0",
    extraInfo=exp_info,
    dataFileName=item_filename,
)

pam_exp_handler = data.ExperimentHandler(
    name="PAMEncoding",
    version="5.0",
    extraInfo=exp_info,
    dataFileName=pam_filename,
)
# --- Results Accumulator ---------------------------------------------------
results_store = {
    "item": {
        "encoding_trials":    [],
        "catch_encoding":     [],
        "recognition_trials": [],
        "catch_recognition":  [],
    },
    "scene": {
        "encoding_trials":    [],
        "catch_encoding":     [],
        "recognition_trials": [],
        "catch_recognition":  [],
    },
    "pam_objects": {
        "encoding_pairs":     [],
        "recognition_trials": [],
        "catch_recognition":  [],
    },
    "pam_scenes": {
        "encoding_pairs":     [],
        "recognition_trials": [],
        "catch_recognition":  [],
    },
    "pam_itemscene": {
        "encoding_pairs":     [],
        "recognition_trials": [],
        "catch_recognition":  [],
    },
}

# --- Validate Stimuli --------------------------------------------------------
def validate_list(stim_list, folder, list_name, valid_labels):
    for entry in stim_list:
        p = os.path.join(folder, entry["image"])
        if not os.path.isfile(p):
            raise FileNotFoundError(f"[{list_name}] Image not found: {p}")
        if entry["correct"].lower() not in [lbl.lower() for lbl in valid_labels]:
            raise ValueError(
                f"[{list_name}] Invalid correct answer '{entry['correct']}' for {entry['image']}"
            )

def validate_pair_list(pair_list, folder, list_name):
    for entry in pair_list:
        for key in ("image_a", "image_b"):
            p = os.path.join(folder, entry[key])
            if not os.path.isfile(p):
                raise FileNotFoundError(f"[{list_name}] Image not found: {p}")

validate_list(PRACTICE_FEEDBACK_LIST,       PRACTICE_DIR,            "PRACTICE_FEEDBACK_LIST",       ITEM_LABELS)
validate_list(PRACTICE_NOCUE_LIST,          PRACTICE_NOCUE_DIR,      "PRACTICE_NOCUE_LIST",          ITEM_LABELS)
validate_list(STIMULUS_LIST,                STIMULI_DIR,             "STIMULUS_LIST",                ITEM_LABELS)
validate_list(SCENE_PRACTICE_FEEDBACK_LIST, SCENE_PRACTICE_DIR,      "SCENE_PRACTICE_FEEDBACK_LIST", SCENE_LABELS)
validate_list(SCENE_PRACTICE_NOCUE_LIST,    SCENE_PRACTICE_NOCUE_DIR,"SCENE_PRACTICE_NOCUE_LIST",    SCENE_LABELS)
validate_list(SCENE_STIMULUS_LIST,          SCENE_STIMULI_DIR,       "SCENE_STIMULUS_LIST",          SCENE_LABELS)


# --- Window ------------------------------------------------------------------
win = visual.Window(
    size=[1024, 768], fullscr=FULLSCREEN, screen=0,
    winType="pyglet", allowGUI=False,
    color=BACKGROUND, colorSpace="named", units="pix",
)
win.mouseVisible = False

# --- Shared Stimulus Objects -------------------------------------------------
fixation    = visual.TextStim(win, text="+", height=60, color=TEXT_COLOUR, bold=True)
img_stim    = visual.ImageStim(win, image=None, size=IMAGE_SIZE, pos=(0, 20), units="pix")

# PAM pair image stimuli (side-by-side)
_pair_x        = PAM_PAIR_IMAGE_SIZE[0] // 2 + PAM_PAIR_GAP // 2
img_pair_left  = visual.ImageStim(win, image=None, size=PAM_PAIR_IMAGE_SIZE,
                                  pos=(-_pair_x, 0), units="pix")
img_pair_right = visual.ImageStim(win, image=None, size=PAM_PAIR_IMAGE_SIZE,
                                  pos=( _pair_x, 0), units="pix")

BTN_Y = -310
BTN_W = 200
BTN_H = 55

btn_left = visual.Rect(
    win, width=BTN_W, height=BTN_H,
    pos=(-140, BTN_Y), fillColor=BTN_BLUE, lineColor="white", lineWidth=2,
)
btn_left_label = visual.TextStim(
    win, text=f"F  -  {LABEL_MANMADE}", height=22, color="white",
    pos=(-140, BTN_Y), bold=True,
)
btn_right = visual.Rect(
    win, width=BTN_W, height=BTN_H,
    pos=(140, BTN_Y), fillColor=BTN_BLUE, lineColor="white", lineWidth=2,
)
btn_right_label = visual.TextStim(
    win, text=f"J  -  {LABEL_NATURAL}", height=22, color="white",
    pos=(140, BTN_Y), bold=True,
)

practice_heading = visual.TextStim(
    win, text="Practice Example",
    height=35, color="black", bold=True,
    pos=(0, win.size[1] // 2 - 100),
)
practice_instruction = visual.TextStim(
    win,
    text="Please select whether the following objects visually contain metal "
         "by using the [F] and [J] keys on your keyboard.",
    height=30, color=TEXT_COLOUR,
    pos=(0, win.size[1] // 2 - 200), wrapWidth=700, alignText="center",
)
scene_practice_instruction = visual.TextStim(
    win,
    text="Please select whether the following scenes are taking place indoors or outdoors "
         "by using the [F] and [J] keys on your keyboard.",
    height=30, color=TEXT_COLOUR,
    pos=(0, win.size[1] // 2 - 200), wrapWidth=700, alignText="center",
)

pam_practice_heading = visual.TextStim(
    win, text="Practice Example",
    height=35, color="black", bold=True,
    pos=(0, win.size[1] // 2 - 60),
)
pam_practice_instruction = visual.TextStim(
    win,
    text="Try to imagine the following pairs of images interacting with one another.",
    height=28, color=TEXT_COLOUR,
    pos=(0, win.size[1] // 2 - 130), wrapWidth=800, alignText="center",
)

catch_prompt = visual.TextStim(
    win, text="", height=32, color="black",
    wrapWidth=800, alignText="center",
)

feedback_text = visual.TextStim(
    win, text="", height=48, bold=True,
    pos=(0, 0), wrapWidth=700, alignText="center",
)

REC_BTN_Y = -290
REC_BTN_W = 240
REC_BTN_H = 60
REC_SUB_Y = REC_BTN_Y - 42

btn_old = visual.Rect(
    win, width=REC_BTN_W, height=REC_BTN_H,
    pos=(-160, REC_BTN_Y), fillColor=BTN_BLUE, lineColor="white", lineWidth=2,
)
btn_old_label = visual.TextStim(
    win, text="F  -  Old", height=22, color="white",
    pos=(-160, REC_BTN_Y), bold=True,
)
btn_old_sublabel = visual.TextStim(
    win, text="Previously presented", height=16, color="black",
    pos=(-160, REC_SUB_Y), italic=True,
)

btn_new = visual.Rect(
    win, width=REC_BTN_W, height=REC_BTN_H,
    pos=(160, REC_BTN_Y), fillColor=BTN_BLUE, lineColor="white", lineWidth=2,
)
btn_new_label = visual.TextStim(
    win, text="J  -  New", height=22, color="white",
    pos=(160, REC_BTN_Y), bold=True,
)
btn_new_sublabel = visual.TextStim(
    win, text="Not previously presented", height=16, color="black",
    pos=(160, REC_SUB_Y), italic=True,
)

rec_key_reminder = visual.TextStim(
    win,
    text="Based on the items you were just shown, please select whether the following "
         "items are OLD or NEW by using the [F] and [J] keys on your keyboard.",
    height=30, color=TEXT_COLOUR,
    pos=(0, win.size[1] // 2 - 200), wrapWidth=700, alignText="center",
)
scene_rec_key_reminder = visual.TextStim(
    win,
    text="Based on the scenes you were just shown, please select whether the following "
         "scenes are OLD or NEW by using the [F] and [J] keys on your keyboard.",
    height=30, color=TEXT_COLOUR,
    pos=(0, win.size[1] // 2 - 200), wrapWidth=700, alignText="center",
)
pam_rec_key_reminder = visual.TextStim(
    win,
    text="Based on the images you were just shown, please select whether the following "
         "images are OLD or NEW by using the [F] and [J] keys on your keyboard.",
    height=30, color=TEXT_COLOUR,
    pos=(0, win.size[1] // 2 - 200), wrapWidth=700, alignText="center",
)

countdown_stim = visual.TextStim(
    win, text="", height=28, color="white", bold=True,
    pos=(win.size[0] // 2 - 125, win.size[1] // 2 - 40),
    alignText="right",
)

end_text = visual.TextStim(
    win,
    text=(
        "Well done!\n\n"
        "You have completed the first half of the experiment.\n\n"
        "You can now take a 2-minute break before the experiment continues.\n\n"
        "After 2 minutes, you will automatically be moved to the next task.\n\n"
        "If you would like to end your break early, press SPACE to continue."
    ),
    height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
)

global_clock = core.Clock()


# --- Helpers -------------------------------------------------------------
def check_escape():
    if "escape" in event.getKeys(["escape"]):
        win.close()
        core.quit()

def clear_buffers():
    win.clearBuffer(); win.flip()
    win.clearBuffer(); win.flip()

def draw_buttons_default():
    btn_left.fillColor  = BTN_BLUE
    btn_right.fillColor = BTN_BLUE
    btn_left.draw();  btn_left_label.draw()
    btn_right.draw(); btn_right_label.draw()

def draw_buttons_confirmed(side):
    btn_left.fillColor  = "yellow" if side == "left"  else BTN_BLUE
    btn_right.fillColor = "yellow" if side == "right" else BTN_BLUE
    btn_left.draw();  btn_left_label.draw()
    btn_right.draw(); btn_right_label.draw()
    btn_left.fillColor  = BTN_BLUE
    btn_right.fillColor = BTN_BLUE

def draw_rec_buttons_default():
    btn_old.fillColor = BTN_BLUE
    btn_new.fillColor = BTN_BLUE
    btn_old.draw(); btn_old_label.draw(); btn_old_sublabel.draw()
    btn_new.draw(); btn_new_label.draw(); btn_new_sublabel.draw()

def draw_rec_buttons_confirmed(side):
    btn_old.fillColor = "yellow" if side == "old" else BTN_BLUE
    btn_new.fillColor = "yellow" if side == "new" else BTN_BLUE
    btn_old.draw(); btn_old_label.draw(); btn_old_sublabel.draw()
    btn_new.draw(); btn_new_label.draw(); btn_new_sublabel.draw()
    btn_old.fillColor = BTN_BLUE
    btn_new.fillColor = BTN_BLUE

def draw_image_screen(confirmed_side=None):
    img_stim.draw()
    if confirmed_side:
        draw_buttons_confirmed(confirmed_side)
    else:
        draw_buttons_default()

def draw_practice_image_screen(show_heading=False, confirmed_side=None, scene_mode=False):
    if show_heading:
        practice_heading.draw()
        if scene_mode:
            scene_practice_instruction.draw()
        else:
            practice_instruction.draw()
    img_stim.draw()
    if confirmed_side:
        draw_buttons_confirmed(confirmed_side)
    else:
        draw_buttons_default()

def draw_rec_practice_screen(show_heading=False, confirmed_side=None,
                              scene_mode=False, pam_mode=False):
    if show_heading:
        practice_heading.draw()
        if pam_mode:
            pam_rec_key_reminder.draw()
        elif scene_mode:
            scene_rec_key_reminder.draw()
        else:
            rec_key_reminder.draw()
    img_stim.draw()
    if confirmed_side:
        draw_rec_buttons_confirmed(confirmed_side)
    else:
        draw_rec_buttons_default()

def show_fixation():
    clear_buffers()
    fixation.draw()
    win.flip()
    fix_t = global_clock.getTime()
    core.wait(FIXATION_DUR)
    return fix_t

def wait_for_space(stim_obj, timeout=SPACE_TIMEOUT, countdown_from=SPACE_COUNTDOWN_START):
    stim_obj.draw()
    win.flip()
    onset = global_clock.getTime()
    event.clearEvents()
    while True:
        check_escape()
        elapsed   = global_clock.getTime() - onset
        remaining = timeout - elapsed
        if remaining <= 0:
            break
        keys = event.getKeys(keyList=["space"])
        if keys:
            break
        stim_obj.draw()
        if remaining <= countdown_from:
            secs_left = int(remaining) + 1
            countdown_stim.setText(f"Continuing in {secs_left}...")
            countdown_stim.draw()
        win.flip()
        core.wait(0.01)
    win.flip()
    core.wait(0.3)

def show_break_screen(duration=120):
    """Show a timed break screen; participant can press SPACE to end early."""
    break_stim = visual.TextStim(
        win,
        text=(
            "Well done!\n\n"
            "Please take a short break.\n\n"
            "The next task will begin automatically after 2 minutes.\n\n"
            "Press SPACE at any time to continue early."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(break_stim, timeout=duration, countdown_from=30)


# Recognition trial sequences -------------------------------
def build_encoding_sequence(stim_list, catch_list, stimuli_dir=None):
    image_trials = [{"trial_type": "image", "folder": stimuli_dir, **s} for s in stim_list]
    random.shuffle(image_trials)
    n_image = len(image_trials)
    n_catch = len(catch_list)
    catch_positions = sorted(random.sample(range(1, n_image + 1), k=min(n_catch, n_image)))
    sequence  = []
    catch_idx = 0
    for i, t in enumerate(image_trials):
        sequence.append(t)
        if catch_idx < n_catch and i + 1 == catch_positions[catch_idx]:
            sequence.append({"trial_type": "catch", **catch_list[catch_idx]})
            catch_idx += 1
    while catch_idx < n_catch:
        sequence.append({"trial_type": "catch", **catch_list[catch_idx]})
        catch_idx += 1
    return sequence

def build_recognition_sequence(stim_list, stimuli_dir, new_item_template,
                                new_item_dir, n_new, catch_list):
    rec_trials   = []
    seen_images  = set()

    # OLD items
    for item in stim_list:
        if item["image"] not in seen_images:
            rec_trials.append({"image": item["image"], "status": "old", "folder": stimuli_dir})
            seen_images.add(item["image"])

    # NEW items
    if new_item_template is None:
        new_files = sorted([
            f for f in os.listdir(new_item_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])
        for fname in new_files:
            if fname not in seen_images:
                rec_trials.append({"image": fname, "status": "new", "folder": new_item_dir})
                seen_images.add(fname)
    else:
        for i in range(1, n_new + 1):
            fname = new_item_template.format(i)
            if fname not in seen_images:
                rec_trials.append({"image": fname, "status": "new", "folder": new_item_dir})
                seen_images.add(fname)

    random.shuffle(rec_trials)

    n_rec_image = len(rec_trials)
    n_rec_catch = len(catch_list)
    positions   = sorted(random.sample(range(1, n_rec_image + 1),
                                       k=min(n_rec_catch, n_rec_image)))
    sequence  = []
    catch_idx = 0
    for i, t in enumerate(rec_trials):
        sequence.append(t)
        if catch_idx < n_rec_catch and i + 1 == positions[catch_idx]:
            sequence.append({"trial_type": "catch", **catch_list[catch_idx]})
            catch_idx += 1
    while catch_idx < n_rec_catch:
        sequence.append({"trial_type": "catch", **catch_list[catch_idx]})
        catch_idx += 1
    return sequence


# --- Block runners ------------------------------------------------------------------

def run_practice_feedback_block(prac_list, prac_dir, scene_mode=False):
    wrong_counts = {item["image"]: 0 for item in prac_list}
    queue        = prac_list.copy()
    first_shown  = False
    noun         = "scene" if scene_mode else "item"

    while queue:
        prac_item      = queue.pop(0)
        img_path       = os.path.join(prac_dir, prac_item["image"])
        correct_answer = prac_item["correct"].lower()
        show_heading   = not first_shown
        first_shown    = True

        fix_t = show_fixation()
        img_stim.setImage(img_path)
        draw_practice_image_screen(show_heading=show_heading, scene_mode=scene_mode)
        win.flip()

        onset    = global_clock.getTime()
        deadline = onset + PRACTICE_FEEDBACK_TIMEOUT
        response = rt = method = None
        event.clearEvents()

        while global_clock.getTime() < deadline:
            check_escape()
            if response is None:
                keys = event.getKeys(
                    keyList=[KEY_INDOOR, KEY_OUTDOOR] if scene_mode
                    else [KEY_MANMADE, KEY_NATURAL],
                    timeStamped=global_clock)
                if keys:
                    k, kt  = keys[0]
                    response = ("indoor" if k == KEY_INDOOR else "outdoor") if scene_mode \
                               else ("metal" if k == KEY_MANMADE else "not metal")
                    rt     = kt - onset
                    method = "keyboard"
                    break
            core.wait(0.001)

        clear_buffers()
        no_response = response is None

        if no_response:
            feedback_text.setText("No response given.")
            feedback_text.color = "#ff4444"
            wrong_counts[prac_item["image"]] += 1
            if wrong_counts[prac_item["image"]] < MAX_WRONG_PER_ITEM:
                queue.append(prac_item)
            accuracy = 0
        elif response == correct_answer:
            feedback_text.setText("Correct!")
            feedback_text.color = "#00dd00"
            accuracy = 1
        else:
            feedback_text.setText(f"Incorrect -- this {noun} will appear again.")
            feedback_text.color = "#FF0000"
            wrong_counts[prac_item["image"]] += 1
            if wrong_counts[prac_item["image"]] < MAX_WRONG_PER_ITEM:
                queue.append(prac_item)
            accuracy = 0

        feedback_text.draw()
        win.flip()
        core.wait(1.2)

        exp_handler.addData("block",          "practice_feedback")
        exp_handler.addData("trial_type",     "practice_feedback")
        exp_handler.addData("image_file",     prac_item["image"])
        exp_handler.addData("correct_answer", correct_answer)
        exp_handler.addData("response",       response if response else "no response")
        exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
        exp_handler.addData("accuracy",       accuracy)
        exp_handler.addData("input_method",   method if method else "no response")
        exp_handler.addData("wrong_count",    wrong_counts[prac_item["image"]])
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)


def run_practice_nocue_block(prac_list, prac_dir, header_stim, scene_mode=False):
    wait_for_space(header_stim)
    img_stim.pos = (0, 60)

    for prac_item in prac_list:
        img_path       = os.path.join(prac_dir, prac_item["image"])
        correct_answer = prac_item["correct"].lower()

        fix_t = show_fixation()
        img_stim.setImage(img_path)
        draw_image_screen()
        win.flip()

        onset    = global_clock.getTime()
        deadline = onset + PRACTICE_NOCUE_TIMEOUT
        response = rt = method = None
        event.clearEvents()

        while global_clock.getTime() < deadline:
            check_escape()
            if response is None:
                keys = event.getKeys(
                    keyList=[KEY_INDOOR, KEY_OUTDOOR] if scene_mode
                    else [KEY_MANMADE, KEY_NATURAL],
                    timeStamped=global_clock)
                if keys:
                    k, kt  = keys[0]
                    response = ("indoor" if k == KEY_INDOOR else "outdoor") if scene_mode \
                               else ("metal" if k == KEY_MANMADE else "not metal")
                    rt     = kt - onset
                    method = "keyboard"
            side = "left" if response in ("metal", "indoor") else "right" if response else None
            draw_image_screen(confirmed_side=side)
            win.flip()
            core.wait(0.001)

        acc = int(response == correct_answer) if response else 0
        exp_handler.addData("block",          "practice_nocue")
        exp_handler.addData("trial_type",     "practice_nocue")
        exp_handler.addData("image_file",     prac_item["image"])
        exp_handler.addData("correct_answer", correct_answer)
        exp_handler.addData("response",       response if response else "no response")
        exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
        exp_handler.addData("accuracy",       acc)
        exp_handler.addData("input_method",   method if method else "no response")
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)


def run_recognition_practice_block(rec_prac_list, scene_mode=False, pam_mode=False):
    wrong_counts = {item["image"]: 0 for item in rec_prac_list}
    random.shuffle(rec_prac_list)
    queue       = rec_prac_list.copy()
    first_shown = False
    noun        = "scene" if scene_mode else "item"

    img_stim.pos = (0, 20)

    while queue:
        prac         = queue.pop(0)
        show_heading = not first_shown
        first_shown  = True

        fix_t = show_fixation()
        img_stim.setImage(os.path.join(prac["folder"], prac["image"]))
        draw_rec_practice_screen(show_heading=show_heading, scene_mode=scene_mode,
                                 pam_mode=pam_mode)
        win.flip()

        onset    = global_clock.getTime()
        deadline = onset + PRACTICE_FEEDBACK_TIMEOUT
        response = rt = method = None
        event.clearEvents()

        while global_clock.getTime() < deadline:
            check_escape()
            if response is None:
                keys = event.getKeys(
                    keyList=[KEY_MANMADE, KEY_NATURAL], timeStamped=global_clock)
                if keys:
                    k, kt    = keys[0]
                    response = "old" if k == KEY_MANMADE else "new"
                    rt       = kt - onset
                    method   = "keyboard"
                    break
            core.wait(0.001)

        clear_buffers()
        no_response = response is None

        if no_response:
            feedback_text.setText("No response given.")
            feedback_text.color = "#FF0000"
            wrong_counts[prac["image"]] += 1
            if wrong_counts[prac["image"]] < MAX_WRONG_PER_ITEM:
                queue.append(prac)
            accuracy = 0
        elif response == prac["status"]:
            feedback_text.setText("Correct!")
            feedback_text.color = "#00dd00"
            accuracy = 1
        else:
            label = "shown earlier" if prac["status"] == "old" else f"a new {noun}"
            feedback_text.setText(f"Incorrect - this {noun} was {label}.")
            feedback_text.color = "#ff4444"
            wrong_counts[prac["image"]] += 1
            if wrong_counts[prac["image"]] < MAX_WRONG_PER_ITEM:
                queue.append(prac)
            accuracy = 0

        feedback_text.draw()
        win.flip()
        core.wait(1.5)

        exp_handler.addData("block",          "recognition_practice")
        exp_handler.addData("trial_type",     "recognition_practice")
        exp_handler.addData("image_file",     prac["image"])
        exp_handler.addData("correct_status", prac["status"])
        exp_handler.addData("response",       response if response else "no response")
        exp_handler.addData("accuracy",       accuracy if not no_response else 0)
        exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
        exp_handler.addData("input_method",   method if method else "no response")
        exp_handler.addData("wrong_count",    wrong_counts[prac["image"]])
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)


def run_encoding_main(trial_sequence, exp_label, results_key, scene_mode=False):
    img_stim.pos = (0, 60)
    global_clock.reset()
    catch_counter = 0

    for seq_idx, trial in enumerate(trial_sequence):
        check_escape()

        if trial["trial_type"] == "catch":
            catch_counter += 1
            correct_label = trial["correct_label"]
            fix_t = show_fixation()
            clear_buffers()

            catch_prompt.setText(trial["prompt"])
            catch_prompt.draw()
            btn_left.draw();  btn_left_label.draw()
            btn_right.draw(); btn_right_label.draw()
            win.flip()
            catch_onset = global_clock.getTime()
            deadline    = catch_onset + CATCH_TIMEOUT

            response = rt = method = None
            event.clearEvents()

            while global_clock.getTime() < deadline:
                check_escape()
                if response is None:
                    keys = event.getKeys(
                        keyList=[KEY_INDOOR, KEY_OUTDOOR] if scene_mode
                        else [KEY_MANMADE, KEY_NATURAL],
                        timeStamped=global_clock)
                    if keys:
                        k, kt  = keys[0]
                        response = ("indoor" if k == KEY_INDOOR else "outdoor") if scene_mode \
                                   else ("metal" if k == KEY_MANMADE else "not metal")
                        rt     = kt - catch_onset
                        method = "keyboard"

                if response is not None:
                    side = "left" if response in ("metal", "indoor") else "right"
                    btn_left.fillColor  = "yellow" if side == "left"  else BTN_BLUE
                    btn_right.fillColor = "yellow" if side == "right" else BTN_BLUE
                catch_prompt.draw()
                btn_left.draw();  btn_left_label.draw()
                btn_right.draw(); btn_right_label.draw()
                btn_left.fillColor  = BTN_BLUE
                btn_right.fillColor = BTN_BLUE
                win.flip()
                core.wait(0.001)

            accuracy = int(response == correct_label.lower()) if response else 0
            results_store[results_key]["catch_encoding"].append({
                "catch_num":     catch_counter,
                "prompt":        trial["prompt"].replace("\n\n", " | "),
                "correct_label": correct_label,
                "response":      response if response else "no response",
                "accuracy":      accuracy,
            })

            exp_handler.addData("block",          exp_label)
            exp_handler.addData("seq_position",   seq_idx + 1)
            exp_handler.addData("trial_type",     "catch")
            exp_handler.addData("image_file",     "")
            exp_handler.addData("correct_answer", correct_label)
            exp_handler.addData("response",       response if response else "no response")
            exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
            exp_handler.addData("accuracy",       accuracy)
            exp_handler.addData("input_method",   method if method else "no response")
            exp_handler.addData("attempt",        1)
            exp_handler.addData("img_onset",      "")
            exp_handler.addData("fix_onset",      fix_t)
            exp_handler.nextEntry()
            win.flip(); core.wait(0.3)
            continue

        # Image trial
        img_path       = os.path.join(trial.get("folder", STIMULI_DIR), trial["image"])
        correct_answer = trial["correct"].lower()
        fix_t = show_fixation()
        img_stim.setImage(img_path)
        draw_image_screen()
        win.flip()
        onset    = global_clock.getTime()
        deadline = onset + RESPONSE_TIMEOUT

        response = rt = method = None
        event.clearEvents()

        while global_clock.getTime() < deadline:
            check_escape()
            if response is None:
                keys = event.getKeys(
                    keyList=[KEY_INDOOR, KEY_OUTDOOR] if scene_mode
                    else [KEY_MANMADE, KEY_NATURAL],
                    timeStamped=global_clock)
                if keys:
                    k, kt  = keys[0]
                    response = ("indoor" if k == KEY_INDOOR else "outdoor") if scene_mode \
                               else ("metal" if k == KEY_MANMADE else "not metal")
                    rt     = kt - onset
                    method = "keyboard"
            side = "left" if response in ("metal", "indoor") else "right" if response else None
            draw_image_screen(confirmed_side=side)
            win.flip()
            core.wait(0.001)

        accuracy = int(response == correct_answer) if response else 0
        results_store[results_key]["encoding_trials"].append({
            "image":          trial["image"],
            "correct_answer": correct_answer,
            "response":       response if response else "no response",
            "accuracy":       accuracy,
        })

        exp_handler.addData("block",          exp_label)
        exp_handler.addData("seq_position",   seq_idx + 1)
        exp_handler.addData("trial_type",     "image")
        exp_handler.addData("image_file",     trial["image"])
        exp_handler.addData("correct_answer", correct_answer)
        exp_handler.addData("response",       response if response else "no response")
        exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
        exp_handler.addData("accuracy",       accuracy)
        exp_handler.addData("input_method",   method if method else "no response")
        exp_handler.addData("attempt",        1)
        exp_handler.addData("img_onset",      onset)
        exp_handler.addData("fix_onset",      fix_t)
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)


def run_distractor():
    distract_intro = visual.TextStim(
        win,
        text=(
            "Before continuing, please complete a short arithmetic task.\n\n"
            "Simple addition problems will appear on the screen.\n"
            "Please type the correct answer to each problem using the number keys, "
            "and then press ENTER to continue.\n\n"
            "Take your time and do your best.\n\n"
            "Press SPACE to begin."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(distract_intro)

    DISTRACT_DURATION = 60
    start_time    = global_clock.getTime()
    problem_text  = visual.TextStim(win, text="", height=40, color=TEXT_COLOUR)
    response_box  = visual.TextStim(win, text="", height=40, color="blue", pos=(0, -80))

    while global_clock.getTime() - start_time < DISTRACT_DURATION:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        correct_answer = a + b
        problem_text.setText(f"{a} + {b} = ?")
        typed = ""

        while True:
            check_escape()
            problem_text.draw()
            response_box.setText(typed)
            response_box.draw()
            win.flip()
            keys = event.getKeys()
            if keys:
                k = keys[0]
                if k in ["return", "enter"] and typed:
                    break
                elif k == "backspace":
                    typed = typed[:-1]
                elif k.isdigit():
                    typed += k
            if global_clock.getTime() - start_time >= DISTRACT_DURATION:
                break

        exp_handler.addData("block",          "distractor")
        exp_handler.addData("trial_type",     "arithmetic")
        exp_handler.addData("problem",        f"{a}+{b}")
        exp_handler.addData("correct_answer", correct_answer)
        exp_handler.addData("response",       typed if typed else "no response")
        exp_handler.addData("accuracy",       int(typed == str(correct_answer)))
        exp_handler.nextEntry()
        if global_clock.getTime() - start_time >= DISTRACT_DURATION:
            break

    win.flip(); core.wait(0.3)


def run_recognition_main(rec_trial_sequence, exp_label, results_key):
    img_stim.pos  = (0, 60)
    catch_counter = 0

    for seq_idx, trial in enumerate(rec_trial_sequence):
        check_escape()

        if trial.get("trial_type") == "catch":
            catch_counter += 1
            correct_label  = trial["correct_label"]
            fix_t = show_fixation()
            clear_buffers()

            catch_prompt.setText(trial["prompt"])
            catch_prompt.draw()
            btn_old.draw(); btn_old_label.draw(); btn_old_sublabel.draw()
            btn_new.draw(); btn_new_label.draw(); btn_new_sublabel.draw()
            win.flip()
            catch_onset = global_clock.getTime()
            deadline    = catch_onset + CATCH_TIMEOUT

            response = rt = method = None
            event.clearEvents()

            while global_clock.getTime() < deadline:
                check_escape()
                if response is None:
                    keys = event.getKeys(
                        keyList=[KEY_MANMADE, KEY_NATURAL], timeStamped=global_clock)
                    if keys:
                        k, kt    = keys[0]
                        response = "old" if k == KEY_MANMADE else "new"
                        rt       = kt - catch_onset
                        method   = "keyboard"
                if response is not None:
                    draw_rec_buttons_confirmed(response)
                else:
                    draw_rec_buttons_default()
                catch_prompt.draw()
                win.flip()
                core.wait(0.001)

            accuracy = int(response == correct_label) if response else 0
            results_store[results_key]["catch_recognition"].append({
                "catch_num":     catch_counter,
                "prompt":        trial["prompt"].replace("\n\n", " | "),
                "correct_label": correct_label,
                "response":      response if response else "no response",
                "accuracy":      accuracy,
            })

            exp_handler.addData("block",          exp_label + "_recognition")
            exp_handler.addData("seq_position",   seq_idx + 1)
            exp_handler.addData("trial_type",     "catch")
            exp_handler.addData("image_file",     "")
            exp_handler.addData("correct_status", correct_label)
            exp_handler.addData("response",       response if response else "no response")
            exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
            exp_handler.addData("accuracy",       accuracy)
            exp_handler.addData("input_method",   method if method else "no response")
            exp_handler.addData("fix_onset",      fix_t)
            exp_handler.nextEntry()
            win.flip(); core.wait(0.3)
            continue

        # Recognition image trial
        fix_t    = show_fixation()
        img_path = os.path.join(trial["folder"], trial["image"])
        img_stim.setImage(img_path)
        img_stim.draw()
        draw_rec_buttons_default()
        win.flip()

        onset    = global_clock.getTime()
        response = rt = None
        event.clearEvents()

        while response is None:
            check_escape()
            keys = event.getKeys(keyList=[KEY_MANMADE, KEY_NATURAL],
                                 timeStamped=global_clock)
            if keys:
                k, kt    = keys[0]
                response = "old" if k == KEY_MANMADE else "new"
                rt       = kt - onset
            img_stim.draw()
            if response is not None:
                draw_rec_buttons_confirmed(response)
            else:
                draw_rec_buttons_default()
            win.flip()
            core.wait(0.001)

        accuracy = int(response == trial["status"])
        results_store[results_key]["recognition_trials"].append({
            "image":    trial["image"],
            "status":   trial["status"],
            "response": response,
            "accuracy": accuracy,
        })

        exp_handler.addData("block",          exp_label + "_recognition")
        exp_handler.addData("seq_position",   seq_idx + 1)
        exp_handler.addData("trial_type",     "recognition")
        exp_handler.addData("image_file",     trial["image"])
        exp_handler.addData("correct_status", trial["status"])
        exp_handler.addData("response",       response)
        exp_handler.addData("accuracy",       accuracy)
        exp_handler.addData("response_rt",    round(rt, 4))
        exp_handler.addData("input_method",   "keyboard")
        exp_handler.addData("fix_onset",      fix_t)
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)
        
def draw_pair(show_heading=False):
    if show_heading:
        pam_practice_heading.draw()
        pam_practice_instruction.draw()
    img_pair_left.draw()
    img_pair_right.draw()


def run_pam_practice_block(prac_list, prac_dir, exp_label):
    first_shown = False
    for pair_idx, pair in enumerate(prac_list):
        path_a = os.path.join(prac_dir, pair["image_a"])
        path_b = os.path.join(prac_dir, pair["image_b"])
        show_heading = not first_shown
        first_shown  = True
        fix_t = show_fixation()
        img_pair_left.setImage(path_a)
        img_pair_right.setImage(path_b)
        draw_pair(show_heading=show_heading)
        win.flip()
        onset = global_clock.getTime()
        while global_clock.getTime() - onset < PRACTICE_FEEDBACK_TIMEOUT:
            check_escape()
            draw_pair(show_heading=show_heading)
            win.flip()
            core.wait(0.001)
        clear_buffers()
        exp_handler.addData("block",      exp_label + "_pam_practice")
        exp_handler.addData("trial_type", "pam_practice_pair")
        exp_handler.addData("pair_num",   pair_idx + 1)
        exp_handler.addData("image_a",    pair["image_a"])
        exp_handler.addData("image_b",    pair["image_b"])
        exp_handler.addData("fix_onset",  fix_t)
        exp_handler.addData("img_onset",  onset)
        exp_handler.nextEntry()
        win.flip(); core.wait(0.3)


def run_pam_encoding_main(pair_list, pairs_dir, exp_label, results_key):
    random.shuffle(pair_list)
    for pair_idx, pair in enumerate(pair_list):
        check_escape()
        path_a = os.path.join(pairs_dir, pair["image_a"])
        path_b = os.path.join(pairs_dir, pair["image_b"])
        fix_t = show_fixation()
        img_pair_left.setImage(path_a)
        img_pair_right.setImage(path_b)
        draw_pair(show_heading=False)
        win.flip()
        onset = global_clock.getTime()
        while global_clock.getTime() - onset < PAM_PAIR_EXPOSURE:
            check_escape()
            draw_pair(show_heading=False)
            win.flip()
            core.wait(0.001)
        results_store[results_key]["encoding_pairs"].append({
            "pair_num": pair_idx + 1,
            "image_a":  pair["image_a"],
            "image_b":  pair["image_b"],
        })
        exp_handler.addData("block",        exp_label)
        exp_handler.addData("seq_position", pair_idx + 1)
        exp_handler.addData("trial_type",   "pam_pair")
        exp_handler.addData("image_a",      pair["image_a"])
        exp_handler.addData("image_b",      pair["image_b"])
        exp_handler.addData("fix_onset",    fix_t)
        exp_handler.addData("img_onset",    onset)
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)


def build_pam_pair_recognition_sequence(pair_list, pairs_dir, n_targets=12, catch_list=None):
    if catch_list is None:
        catch_list = []

    N = len(pair_list)
    if N < n_targets * 2:
        raise ValueError(
            f"Need at least {n_targets * 2} pairs to create {n_targets} OLD "
            f"and {n_targets} recombined NEW trials with no repeated images. "
            f"Only {N} pairs available."
        )

   # Shuffle trials
    all_indices = list(range(N))
    random.shuffle(all_indices)
    old_idx  = all_indices[:n_targets]           # pairs shown intact as OLD
    new_idx  = all_indices[n_targets:n_targets * 2]  # pairs broken up for NEW

    rec_trials = []

    # OLD trials — shown exactly as encoded
    for idx in old_idx:
        p = pair_list[idx]
        rec_trials.append({
            "trial_type": "pair",
            "image_a": p["image_a"],
            "image_b": p["image_b"],
            "status":  "old",
            "folder":  pairs_dir,
        })

    # Recombined trials
    new_pairs = [pair_list[idx] for idx in new_idx]
    a_images  = [p["image_a"] for p in new_pairs]
    b_images  = [p["image_b"] for p in new_pairs]
    b_images_rotated = b_images[1:] + b_images[:1]
    original_pairs = {(p["image_a"], p["image_b"]) for p in pair_list}
    max_rotations  = len(b_images)
    rotation       = 1
    while rotation < max_rotations:
        b_rotated = b_images[rotation:] + b_images[:rotation]
        if not any((a, b) in original_pairs for a, b in zip(a_images, b_rotated)):
            b_images_rotated = b_rotated
            break
        rotation += 1

    for a, b in zip(a_images, b_images_rotated):
        rec_trials.append({
            "trial_type": "pair",
            "image_a": a,
            "image_b": b,
            "status":  "recombined",
            "folder":  pairs_dir,
        })

    random.shuffle(rec_trials)

    # Interleave catch trials
    n_rec     = len(rec_trials)
    n_catch   = len(catch_list)
    positions = sorted(random.sample(range(1, n_rec + 1), k=min(n_catch, n_rec))) if n_catch else []
    sequence  = []
    catch_idx = 0
    for i, t in enumerate(rec_trials):
        sequence.append(t)
        if catch_idx < n_catch and i + 1 == positions[catch_idx]:
            sequence.append({"trial_type": "catch", **catch_list[catch_idx]})
            catch_idx += 1
    while catch_idx < n_catch:
        sequence.append({"trial_type": "catch", **catch_list[catch_idx]})
        catch_idx += 1
    return sequence


def run_pam_pair_recognition_main(rec_pair_sequence, exp_label, results_key):
    catch_counter = 0
    for seq_idx, trial in enumerate(rec_pair_sequence):
        check_escape()
        if trial.get("trial_type") == "catch":
            catch_counter += 1
            correct_label = trial["correct_label"]
            fix_t = show_fixation()
            clear_buffers()
            catch_prompt.setText(trial["prompt"])
            catch_prompt.draw()
            btn_old.draw(); btn_old_label.draw(); btn_old_sublabel.draw()
            btn_new.draw(); btn_new_label.draw(); btn_new_sublabel.draw()
            win.flip()
            catch_onset = global_clock.getTime()
            deadline    = catch_onset + CATCH_TIMEOUT
            response = rt = method = None
            event.clearEvents()
            while global_clock.getTime() < deadline:
                check_escape()
                if response is None:
                    keys = event.getKeys(keyList=[KEY_MANMADE, KEY_NATURAL], timeStamped=global_clock)
                    if keys:
                        k, kt    = keys[0]
                        response = "old" if k == KEY_MANMADE else "new"
                        rt       = kt - catch_onset
                        method   = "keyboard"
                if response is not None:
                    draw_rec_buttons_confirmed(response)
                else:
                    draw_rec_buttons_default()
                catch_prompt.draw()
                win.flip()
                core.wait(0.001)
            accuracy = int(response == correct_label) if response else 0
            results_store[results_key]["catch_recognition"].append({
                "catch_num":     catch_counter,
                "prompt":        trial["prompt"].replace("\n\n", " | "),
                "correct_label": correct_label,
                "response":      response if response else "no response",
                "accuracy":      accuracy,
            })
            exp_handler.addData("block",          exp_label + "_recognition")
            exp_handler.addData("seq_position",   seq_idx + 1)
            exp_handler.addData("trial_type",     "catch")
            exp_handler.addData("correct_status", correct_label)
            exp_handler.addData("response",       response if response else "no response")
            exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
            exp_handler.addData("accuracy",       accuracy)
            exp_handler.addData("input_method",   method if method else "no response")
            exp_handler.addData("fix_onset",      fix_t)
            exp_handler.nextEntry()
            win.flip(); core.wait(0.3)
            continue
        fix_t  = show_fixation()
        img_pair_left.setImage(os.path.join(trial["folder"], trial["image_a"]))
        img_pair_right.setImage(os.path.join(trial["folder"], trial["image_b"]))
        img_pair_left.draw()
        img_pair_right.draw()
        draw_rec_buttons_default()
        win.flip()
        onset    = global_clock.getTime()
        response = rt = None
        event.clearEvents()
        while response is None:
            check_escape()
            keys = event.getKeys(keyList=[KEY_MANMADE, KEY_NATURAL], timeStamped=global_clock)
            if keys:
                k, kt    = keys[0]
                response = "old" if k == KEY_MANMADE else "new"
                rt       = kt - onset
            img_pair_left.draw()
            img_pair_right.draw()
            if response is not None:
                draw_rec_buttons_confirmed(response)
            else:
                draw_rec_buttons_default()
            win.flip()
            core.wait(0.001)
        accuracy = int(response == ("old" if trial["status"] == "old" else "new"))
        results_store[results_key]["recognition_trials"].append({
            "image_a":  trial["image_a"],
            "image_b":  trial["image_b"],
            "status":   trial["status"],
            "response": response,
            "accuracy": accuracy,
        })
        exp_handler.addData("block",          exp_label + "_recognition")
        exp_handler.addData("seq_position",   seq_idx + 1)
        exp_handler.addData("trial_type",     "recognition_pair")
        exp_handler.addData("image_a",        trial["image_a"])
        exp_handler.addData("image_b",        trial["image_b"])
        exp_handler.addData("correct_status", trial["status"])
        exp_handler.addData("response",       response)
        exp_handler.addData("accuracy",       accuracy)
        exp_handler.addData("response_rt",    round(rt, 4))
        exp_handler.addData("input_method",   "keyboard")
        exp_handler.addData("fix_onset",      fix_t)
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)

def run_full_pam_condition(
    condition_label,
    exp_label,
    results_key,
    pair_list,
    pairs_dir,
    prac_list,
    prac_dir,
    rec_catch_list,
    instructions_text,
    transition_text,
):
    instr_stim = visual.TextStim(
        win, text=instructions_text,
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(instr_stim)

    run_pam_practice_block(prac_list, prac_dir, exp_label)

    prac_done_stim = visual.TextStim(
        win,
        text=(
            "Well done!\n\n"
            "Following presentation of the scenes, you will complete an arithmetic "
            "and memory task.\n\n"
            "For the memory task, you will be shown a images of pairs on the screen.\n\n"
            "For each pair, decide whether it was shown earlier in the experiment (OLD) or whether it was not (NEW).\n\n"
            "Some pairs have been mixed and are different from what you saw before (NEW).\n\n"
            "You will now be shown a practice example of the task.\n\n"
            "   \n\n"
            "Press  SPACE  to continue."
        ),
        height=28, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(prac_done_stim)

    prac_rec_list = [
        {
            "trial_type": "pair",
            "image_a": prac_list[0]["image_a"],
            "image_b": prac_list[0]["image_b"],
            "status":  "old",
            "folder":  prac_dir,
        },
        {
            "trial_type": "pair",
            "image_a": prac_list[1]["image_a"],
            "image_b": prac_list[2]["image_b"],
            "status":  "recombined",
            "folder":  prac_dir,
        },
        {
            "trial_type": "pair",
            "image_a": prac_list[2]["image_a"],
            "image_b": prac_list[1]["image_b"],
            "status":  "recombined",
            "folder":  prac_dir,
        },
    ]
    random.shuffle(prac_rec_list)
    first_shown = True

    for prac in prac_rec_list:
        fix_t = show_fixation()
        img_pair_left.setImage(os.path.join(prac["folder"], prac["image_a"]))
        img_pair_right.setImage(os.path.join(prac["folder"], prac["image_b"]))
        draw_pair(show_heading=False)
        if first_shown:
            pam_practice_heading.draw()
            rec_prac_instr = visual.TextStim(
                win,
                text="Has this exact pair been shown before (OLD) or is the combination NEW?",
                height=26, color=TEXT_COLOUR,
                pos=(0, win.size[1] // 2 - 130), wrapWidth=800, alignText="center",
            )
            rec_prac_instr.draw()
        draw_rec_buttons_default()
        win.flip()
        first_shown = False

        onset    = global_clock.getTime()
        deadline = onset + PRACTICE_FEEDBACK_TIMEOUT
        response = rt = method = None
        event.clearEvents()

        while global_clock.getTime() < deadline:
            check_escape()
            if response is None:
                keys = event.getKeys(
                    keyList=[KEY_MANMADE, KEY_NATURAL], timeStamped=global_clock)
                if keys:
                    k, kt    = keys[0]
                    response = "old" if k == KEY_MANMADE else "new"
                    rt       = kt - onset
                    method   = "keyboard"
                    break
            core.wait(0.001)

        clear_buffers()
        correct = "old" if prac["status"] == "old" else "new"
        if response is None:
            feedback_text.setText("No response given.")
            feedback_text.color = "#FF0000"
            accuracy = 0
        elif response == correct:
            feedback_text.setText("Correct!")
            feedback_text.color = "#00dd00"
            accuracy = 1
        else:
            label = "shown before" if prac["status"] == "old" else "not shown before"
            feedback_text.setText(f"Incorrect — this exact pair was {label}.")
            feedback_text.color = "#ff4444"
            accuracy = 0

        feedback_text.draw()
        win.flip()
        core.wait(1.5)

        exp_handler.addData("block",          exp_label + "_rec_practice")
        exp_handler.addData("trial_type",     "pam_rec_practice")
        exp_handler.addData("image_a",        prac["image_a"])
        exp_handler.addData("image_b",        prac["image_b"])
        exp_handler.addData("correct_status", prac["status"])
        exp_handler.addData("response",       response if response else "no response")
        exp_handler.addData("accuracy",       accuracy)
        exp_handler.addData("response_rt",    round(rt, 4) if rt else "")
        exp_handler.addData("input_method",   method if method else "no response")
        exp_handler.nextEntry()
        win.flip(); core.wait(0.2)

    main_start_stim = visual.TextStim(
        win,
        text=(
            "Great work!\n\n"
            "The practice is now complete.\n\n"
            "The main task will now begin.\n\n"
            "Please answer as quickly and accurately as possible.\n\n"
            "Press SPACE when you are ready to start."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(main_start_stim)

    run_pam_encoding_main(pair_list.copy(), pairs_dir, exp_label, results_key)

    run_distractor()

    trans_stim = visual.TextStim(
        win, text=transition_text,
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(trans_stim)

    rec_sequence = build_pam_pair_recognition_sequence(
        pair_list, pairs_dir,
        n_targets  = min(12, len(pair_list)),
        catch_list = rec_catch_list,
    )
    run_pam_pair_recognition_main(rec_sequence, exp_label, results_key)

        
        
# ─── ITEM Experiment ──────────────────────────────────────────────────

if EXPERIMENT_MODE in ("both", "item", "all"):

    btn_left_label.setText(f"F  -  {LABEL_MANMADE}")
    btn_right_label.setText(f"J  -  {LABEL_NATURAL}")

    instructions = visual.TextStim(
        win,
        text=(
            "Welcome!\n\n"
            "In this task you will be shown a series of objects.\n\n"
            "Your task will be to decide whether each object visually contains metal.\n\n"
            "Please pay attention to each presented object - "
            "you will later be tested on your memory of the objects.\n\n"
            "You will now be shown a practice example of the task.\n\n"
            "Press  SPACE  to continue."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(instructions)

    img_stim.pos = (0, 20)

    # Practice A
    run_practice_feedback_block(PRACTICE_FEEDBACK_LIST, PRACTICE_DIR, scene_mode=False)

    # Practice B
    prac_b_header = visual.TextStim(
        win,
        text=(
            "Now try without feedback.\n\n"
            "Each image will appear for a few seconds - just like in the real task.\n\n"
            "Press  SPACE  to continue."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=800, alignText="center",
    )
    run_practice_nocue_block(PRACTICE_NOCUE_LIST, PRACTICE_NOCUE_DIR, prac_b_header,
                             scene_mode=False)

    # Transition
    transition_screen = visual.TextStim(
        win,
        text=(
            "Well done!\n\n"
            "Following presentation of the objects, you will complete an arithmetic "
            "and memory task.\n\n"
            "In the memory task, you will be shown a series of objects on the screen. "
            "Some of these objects will have been shown earlier in the experiment (OLD), "
            "and some will be new (NEW).\n\n"
            "For each object, you must decide whether the object is OLD or NEW.\n\n"
            "You will now be shown a practice example of the task.\n\n"
            "Press  SPACE  to continue."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(transition_screen)

    # Recognition practice
    REC_PRACTICE_LIST = [
        {"image": "prac_01.jpg",      "status": "old", "folder": PRACTICE_DIR},
        {"image": "prac_02.jpg",      "status": "new", "folder": PRACTICE_DIR},
        {"image": "rec_prac_new.jpg", "status": "new", "folder": REC_PRACTICE_DIR},
    ]
    run_recognition_practice_block(REC_PRACTICE_LIST, scene_mode=False)

    rec_prac_done = visual.TextStim(
        win,
        text=(
            "Great work!\n\n"
            "The practice is now complete.\n\n"
            "The main experiment will now begin.\n\n"
            "Please answer as quickly and accurately as possible.\n\n"
            "Press  SPACE  when you are ready to start."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(rec_prac_done)

    # Main encoding
    item_encoding_sequence = build_encoding_sequence(
        STIMULUS_LIST, CATCH_TRIALS, stimuli_dir=STIMULI_DIR)
    run_encoding_main(item_encoding_sequence, exp_label="main",
                      results_key="item", scene_mode=False)

    run_distractor()

    # Recognition
    item_rec_sequence = build_recognition_sequence(
        STIMULUS_LIST, STIMULI_DIR,
        None, os.path.join(ITEM_MEMORY_DIR, "recognition_new"),
        len(STIMULUS_LIST), REC_CATCH_TRIALS,
    )
    rec_test_intro = visual.TextStim(
        win,
        text=(
            "You will now complete a memory test.\n\n"
            "In this task, you will be shown a series of objects on the screen.\n\n"
            "For each object, decide whether it was shown earlier in the experiment "
            "(OLD) or whether it was not (NEW).\n\n"
            "Press F for OLD\n"
            "Press J for NEW\n\n"
            "Press SPACE to begin."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(rec_test_intro)
    run_recognition_main(item_rec_sequence, exp_label="item", results_key="item")

    if EXPERIMENT_MODE in ("both", "all"):
        wait_for_space(end_text, timeout=120, countdown_from=30)


# ─── Scene Experiment ──────────────────────────────────────────────────

if EXPERIMENT_MODE in ("both", "scene", "all"):

    btn_left_label.setText(f"F  –  {LABEL_INDOOR}")
    btn_right_label.setText(f"J  –  {LABEL_OUTDOOR}")

    scene_instructions = visual.TextStim(
        win,
        text=(
            "In this task you will be shown a series of scenes.\n\n"
            "This task will be identical to the previous task except you will need to "
            "decide whether each scene is taking place indoors or outdoors.\n\n"
            "Please pay attention to each presented scene – "
            "you will later be tested on your memory of the scenes.\n\n"
            "You will now be shown a practice example of the task.\n\n"
            "Press  SPACE  to continue."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(scene_instructions)

    img_stim.pos = (0, 20)

    # Scene Practice A
    run_practice_feedback_block(SCENE_PRACTICE_FEEDBACK_LIST, SCENE_PRACTICE_DIR,
                                scene_mode=True)

    # Scene Practice B
    scene_prac_b_header = visual.TextStim(
        win,
        text=(
            "Now try without feedback.\n\n"
            "Each scene will appear for a few seconds — just like in the real task.\n\n"
            "Press  SPACE  to continue."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=800, alignText="center",
    )
    run_practice_nocue_block(SCENE_PRACTICE_NOCUE_LIST, SCENE_PRACTICE_NOCUE_DIR,
                             scene_prac_b_header, scene_mode=True)

    # Scene Transition
    scene_transition = visual.TextStim(
        win,
        text=(
            "Well done!\n\n"
            "Following presentation of the scenes, you will complete an arithmetic "
            "and memory task.\n\n"
            "For the memory task, you will be shown a series of scenes on the screen. "
            "Some of these scenes will have been shown earlier in the experiment (OLD), "
            "and some will be new (NEW).\n\n"
            "For each scene, you must decide whether the scene is OLD or NEW.\n\n"
            "You will now be shown a practice example of the task.\n\n"
            "Press  SPACE  to continue."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(scene_transition)

    # Scene Recognition Practice
    SCENE_REC_PRACTICE_LIST = [
        {"image": "scene_prac_01.jpg",       "status": "old", "folder": SCENE_PRACTICE_DIR},
        {"image": "scene_rec_prac_new02.jpg","status": "new", "folder": SCENE_REC_PRACTICE_DIR},
        {"image": "scene_rec_prac_new.jpg",  "status": "new", "folder": SCENE_REC_PRACTICE_DIR},
    ]
    run_recognition_practice_block(SCENE_REC_PRACTICE_LIST, scene_mode=True)

    scene_prac_done = visual.TextStim(
        win,
        text=(
            "Great work!\n\n"
            "The practice is now complete.\n\n"
            "The main experiment will now begin.\n\n"
            "Please answer as quickly and accurately as possible.\n\n"
            "Press  SPACE  when you are ready to start."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(scene_prac_done)

    # Main scene encoding
    scene_encoding_sequence = build_encoding_sequence(
        SCENE_STIMULUS_LIST, SCENE_CATCH_TRIALS, stimuli_dir=SCENE_STIMULI_DIR)
    run_encoding_main(scene_encoding_sequence, exp_label="scene_main",
                      results_key="scene", scene_mode=True)

    run_distractor()

    # Scene recognition
    scene_rec_sequence = build_recognition_sequence(
        SCENE_STIMULUS_LIST, SCENE_STIMULI_DIR,
        None, SCENE_REC_NEW_DIR,
        len(SCENE_STIMULUS_LIST), SCENE_REC_CATCH_TRIALS,
    )
    scene_rec_intro = visual.TextStim(
        win,
        text=(
            "You will now complete a memory test.\n\n"
            "In this task, you will be shown a series of scenes on the screen.\n\n"
            "For each scene, decide whether it was shown earlier in the experiment "
            "(OLD) or whether it was not (NEW).\n\n"
            "Press F for OLD\n"
            "Press J for NEW\n\n"
            "Press SPACE to begin."
        ),
        height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
    )
    wait_for_space(scene_rec_intro)
    run_recognition_main(scene_rec_sequence, exp_label="scene", results_key="scene")

    if EXPERIMENT_MODE == "all":
        show_break_screen(duration=120)


# ─── PAM Object pairs ──────────────────────────────────────────────────

if EXPERIMENT_MODE in ("pam_objects", "pam_all", "all"):

    btn_left_label.setText("F  –  Old")
    btn_right_label.setText("J  –  New")

    run_full_pam_condition(
            condition_label  = "PAM Object Pairs",
            exp_label        = "pam_objects",
            results_key      = "pam_objects",
            pair_list        = PAM_OBJ_PAIR_LIST,
            pairs_dir        = PAM_OBJ_PAIRS_DIR,
            prac_list        = PAM_OBJ_PRACTICE_LIST,
            prac_dir         = PAM_OBJ_PRAC_DIR,
            rec_catch_list   = PAM_OBJ_REC_CATCH_TRIALS,
            
            instructions_text = (
            "In the next task, you will be shown pairs of objects on the screen.\n\n"
            "Each pair will be displayed for a few seconds.\n\n"
            "Your task is to try to imagine the two objects interacting with one another.\n\n"
            "There are no buttons to press while the pairs are being presented.\n\n"
            "You will later complete an arithmetic task and be tested on your memory of the pairs.\n\n"
            "   \n\n"
            "You will now be shown a practice example of the task.\n\n"
            "      \n\n"
            "Press  SPACE  to continue."
        ),
        transition_text   = (
            "You will now complete a memory test.\n\n"
            "In this task, you will be shown a pictures of pairs on the screen.\n\n"
            "For each pair, decide whether it was shown earlier in the experiment (OLD) or whether it was not (NEW).\n\n"
            "Some pairs have been mixed and are different from what you saw before (NEW).\n\n"
            "Press F for OLD\n"
            "Press J for NEW\n\n"
            "    \n\n"
            "Press SPACE to begin."
        ),
    )

    if EXPERIMENT_MODE in ("pam_all", "all"):
        show_break_screen(duration=120)

# ─── PAM Scene pairs  ──────────────────────────────────────────────────

if EXPERIMENT_MODE in ("pam_scenes", "pam_all", "all"):

    btn_left_label.setText("F  –  Old")
    btn_right_label.setText("J  –  New")

    run_full_pam_condition(
            condition_label  = "PAM Scene Pairs",
            exp_label        = "pam_scenes",
            results_key      = "pam_scenes",
            pair_list        = PAM_SC_PAIR_LIST,
            pairs_dir        = PAM_SC_PAIRS_DIR,
            prac_list        = PAM_SC_PRACTICE_LIST,
            prac_dir         = PAM_SC_PRAC_DIR,
            rec_catch_list   = PAM_SC_REC_CATCH_TRIALS,
            
        instructions_text = (
            "In the next task, you will be shown pairs of scenes on the screen.\n\n"
            "Each pair will be displayed for a few seconds.\n\n"
            "Your task is to try to imagine the two scenes interacting with one another.\n\n"
            "There are no buttons to press while the pairs are being presented.\n\n"
            "You will later complete an arithmetic task and be tested on your memory of the pairs.\n\n"
            "   \n\n"
            "You will now be shown a practice example of the task.\n\n"
            "      \n\n"
            "Press  SPACE  to continue."

        ),
        transition_text   = (
            "You will now complete a memory test.\n\n"
            "In this task, you will be shown a pictures of pairs on the screen.\n\n"
            "For each pair, decide whether it was shown earlier in the experiment (OLD) or whether it was not (NEW).\n\n"
            "Some pairs have been mixed and are different from what you saw before (NEW).\n\n"
            "Press F for OLD\n"
            "Press J for NEW\n\n"
            "    \n\n"
            "Press SPACE to begin."
        ),
    )

    if EXPERIMENT_MODE in ("pam_all", "all"):
        show_break_screen(duration=120)


# ─── PAM object-scene pairs ──────────────────────────────────────────────────

if EXPERIMENT_MODE in ("pam_itemscene", "pam_all", "all"):

    btn_left_label.setText("F  –  Old")
    btn_right_label.setText("J  –  New")

    run_full_pam_condition(
            condition_label  = "PAM Item-Scene Pairs",
            exp_label        = "pam_itemscene",
            results_key      = "pam_itemscene",
            pair_list        = PAM_IS_PAIR_LIST,
            pairs_dir        = PAM_IS_PAIRS_DIR,
            prac_list        = PAM_IS_PRACTICE_LIST,
            prac_dir         = PAM_IS_PRAC_DIR,
            rec_catch_list   = PAM_IS_REC_CATCH_TRIALS,
        
        instructions_text = (
            "In the next task, you will be shown pairs of images on the screen.\n\n"
            "Each pair will be displayed for a few seconds.\n\n"
            "Your task is to try to imagine the object and scene interacting with one another.\n\n "
            "There are no buttons to press while the pairs are being presented.\n\n"
            "You will later complete an arithmetic task and be tested on your memory of the pairs.\n\n"
            "   \n\n"
            "You will now be shown a practice example of the task.\n\n"
            "      \n\n"
            "Press  SPACE  to continue."

        ),
        transition_text   = (
            "You will now complete a memory test.\n\n"
            "In this task, you will be shown a pictures of pairs on the screen.\n\n"
            "For each pair, decide whether it was shown earlier in the experiment (OLD) or whether it was not (NEW).\n\n"
            "Some pairs have been mixed and are different from what you saw before (NEW).\n\n"
            "Press F for OLD\n"
            "Press J for NEW\n\n"
            "    \n\n"
            "Press SPACE to begin."

        ),
    )


# ─── Output summary file ──────────────────────────────────────────────────

def compute_summary(enc_trials, rec_trials, catch_enc, catch_rec):
    enc_hits     = sum(1 for t in enc_trials if t["accuracy"] == 1)
    enc_misses   = sum(1 for t in enc_trials
                       if t["accuracy"] == 0 and t["response"] != "no response")
    enc_no_input = sum(1 for t in enc_trials if t["response"] == "no response")
    enc_total    = len(enc_trials)
    enc_score    = enc_hits - enc_misses

    rec_hits   = sum(1 for t in rec_trials if t["accuracy"] == 1)
    rec_misses = sum(1 for t in rec_trials if t["accuracy"] == 0)
    rec_total  = len(rec_trials)
    rec_score  = rec_hits - rec_misses

    catch_enc_correct = sum(1 for c in catch_enc if c["accuracy"] == 1)
    catch_enc_total   = len(catch_enc)
    catch_rec_correct = sum(1 for c in catch_rec if c["accuracy"] == 1)
    catch_rec_total   = len(catch_rec)

    return {
        "enc_hits": enc_hits, "enc_misses": enc_misses,
        "enc_no_input": enc_no_input, "enc_total": enc_total, "enc_score": enc_score,
        "rec_hits": rec_hits, "rec_misses": rec_misses,
        "rec_total": rec_total, "rec_score": rec_score,
        "catch_enc_correct": catch_enc_correct, "catch_enc_total": catch_enc_total,
        "catch_rec_correct": catch_rec_correct, "catch_rec_total": catch_rec_total,
    }


def compute_pam_summary(enc_pairs, rec_trials, catch_rec):
    rec_hits   = sum(1 for t in rec_trials if t["accuracy"] == 1)
    rec_misses = sum(1 for t in rec_trials if t["accuracy"] == 0)
    rec_total  = len(rec_trials)
    rec_score  = rec_hits - rec_misses

    catch_rec_correct = sum(1 for c in catch_rec if c["accuracy"] == 1)
    catch_rec_total   = len(catch_rec)

    return {
        "enc_pairs_total":   len(enc_pairs),
        "rec_hits":          rec_hits,
        "rec_misses":        rec_misses,
        "rec_total":         rec_total,
        "rec_score":         rec_score,
        "catch_rec_correct": catch_rec_correct,
        "catch_rec_total":   catch_rec_total,
    }


# ─── Item/Scene summary ───────────────────────────────────────────────────────
item_summary_filename = os.path.join(
    "data", "item_memory",
    f"sub-{exp_info['Participant ID']}_ses-{exp_info['Session']}_summary_{exp_info['date']}.csv"
)

with open(item_summary_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    standard_experiments = []
    if EXPERIMENT_MODE in ("both", "item", "all"):
        standard_experiments.append(("item",  "ITEM EXPERIMENT"))
    if EXPERIMENT_MODE in ("both", "scene", "all"):
        standard_experiments.append(("scene", "SCENE EXPERIMENT"))

    for exp_key, exp_label in standard_experiments:
        enc_trials = results_store[exp_key]["encoding_trials"]
        rec_trials = results_store[exp_key]["recognition_trials"]
        catch_enc  = results_store[exp_key]["catch_encoding"]
        catch_rec  = results_store[exp_key]["catch_recognition"]
        s = compute_summary(enc_trials, rec_trials, catch_enc, catch_rec)

        writer.writerow([f"===== {exp_label} ====="])
        writer.writerow([])
        writer.writerow(["--- ENCODING TASK: OVERALL SUMMARY ---"])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total trials",                  s["enc_total"]])
        writer.writerow(["Hits (correct response)",        s["enc_hits"]])
        writer.writerow(["Misses (wrong response)",        s["enc_misses"]])
        writer.writerow(["No input (no response)",         s["enc_no_input"]])
        writer.writerow(["Overall score (Hits - Misses)",  s["enc_score"]])
        writer.writerow([])
        writer.writerow(["--- RECOGNITION TASK: OVERALL SUMMARY ---"])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total trials",                  s["rec_total"]])
        writer.writerow(["Hits (correct)",                 s["rec_hits"]])
        writer.writerow(["Misses (wrong)",                 s["rec_misses"]])
        writer.writerow(["Overall score (Hits - Misses)",  s["rec_score"]])
        writer.writerow([])
        writer.writerow(["--- CATCH TRIALS: OVERALL SUMMARY ---"])
        writer.writerow(["Phase", "Correct", "Total", "Accuracy (%)"])
        enc_pct = (round(100 * s["catch_enc_correct"] / s["catch_enc_total"], 1)
                   if s["catch_enc_total"] else "N/A")
        rec_pct = (round(100 * s["catch_rec_correct"] / s["catch_rec_total"], 1)
                   if s["catch_rec_total"] else "N/A")
        writer.writerow(["Encoding",    s["catch_enc_correct"], s["catch_enc_total"], enc_pct])
        writer.writerow(["Recognition", s["catch_rec_correct"], s["catch_rec_total"], rec_pct])
        writer.writerow([])
        writer.writerow(["--- ENCODING TASK: PER-IMAGE RESULTS ---"])
        writer.writerow(["Image", "Correct Answer", "Response",
                         "Encoding Correct?", "Recognition Correct?"])
        rec_lookup = {t["image"]: t for t in rec_trials}
        for t in enc_trials:
            rec = rec_lookup.get(t["image"])
            rec_correct = rec["accuracy"] if rec else "N/A (not in recognition)"
            writer.writerow([
                t["image"], t["correct_answer"], t["response"],
                "Yes" if t["accuracy"] == 1 else "No",
                "Yes" if rec_correct == 1 else ("No" if rec_correct == 0 else rec_correct),
            ])
        writer.writerow([])
        writer.writerow(["--- RECOGNITION TASK: NEW ITEMS ---"])
        writer.writerow(["Image", "Status", "Response", "Correct?"])
        for t in rec_trials:
            if t["status"] == "new":
                writer.writerow([t["image"], "new", t["response"],
                                 "Yes" if t["accuracy"] == 1 else "No"])
        writer.writerow([])
        writer.writerow(["--- CATCH TRIALS: ENCODING DETAIL ---"])
        writer.writerow(["Catch #", "Required Response", "Participant Response", "Correct?"])
        for c in catch_enc:
            writer.writerow([f"Catch {c['catch_num']}", c["correct_label"],
                             c["response"], "Yes" if c["accuracy"] == 1 else "No"])
        writer.writerow([])
        writer.writerow(["--- CATCH TRIALS: RECOGNITION DETAIL ---"])
        writer.writerow(["Catch #", "Required Response", "Participant Response", "Correct?"])
        for c in catch_rec:
            writer.writerow([f"Catch {c['catch_num']}", c["correct_label"],
                             c["response"], "Yes" if c["accuracy"] == 1 else "No"])
        writer.writerow([])
        writer.writerow([])

# ─── PAM summary ─────────────────────────────────────────────────────────────
pam_summary_filename = os.path.join(
    "data", "PAM_memory",
    f"sub-{exp_info['Participant ID']}_ses-{exp_info['Session']}_summary_{exp_info['date']}.csv"
)

with open(pam_summary_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    pam_experiments = []
    if EXPERIMENT_MODE in ("pam_objects",   "pam_all", "all"):
        pam_experiments.append(("pam_objects",   "PAM OBJECT PAIRS"))
    if EXPERIMENT_MODE in ("pam_scenes",    "pam_all", "all"):
        pam_experiments.append(("pam_scenes",    "PAM SCENE PAIRS"))
    if EXPERIMENT_MODE in ("pam_itemscene", "pam_all", "all"):
        pam_experiments.append(("pam_itemscene", "PAM ITEM-SCENE PAIRS"))

    for exp_key, exp_label in pam_experiments:
        enc_pairs  = results_store[exp_key]["encoding_pairs"]
        rec_trials = results_store[exp_key]["recognition_trials"]
        catch_rec  = results_store[exp_key]["catch_recognition"]
        s = compute_pam_summary(enc_pairs, rec_trials, catch_rec)

        writer.writerow([f"===== {exp_label} ====="])
        writer.writerow([])
        writer.writerow(["--- ENCODING: PAIRS PRESENTED ---"])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total pairs shown", s["enc_pairs_total"]])
        writer.writerow([])
        writer.writerow(["--- RECOGNITION TASK: OVERALL SUMMARY ---"])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total trials",                  s["rec_total"]])
        writer.writerow(["Hits (correct)",                 s["rec_hits"]])
        writer.writerow(["Misses (wrong)",                 s["rec_misses"]])
        writer.writerow(["Overall score (Hits - Misses)",  s["rec_score"]])
        writer.writerow([])
        writer.writerow(["--- CATCH TRIALS: RECOGNITION SUMMARY ---"])
        writer.writerow(["Correct", "Total", "Accuracy (%)"])
        rec_pct = (round(100 * s["catch_rec_correct"] / s["catch_rec_total"], 1)
                   if s["catch_rec_total"] else "N/A")
        writer.writerow([s["catch_rec_correct"], s["catch_rec_total"], rec_pct])
        writer.writerow([])
        writer.writerow(["--- ENCODING: PAIRS DETAIL ---"])
        writer.writerow(["Pair #", "Image A", "Image B"])
        for p in enc_pairs:
            writer.writerow([p["pair_num"], p["image_a"], p["image_b"]])
        writer.writerow([])
        writer.writerow(["--- RECOGNITION TASK: PER-PAIR RESULTS ---"])
        writer.writerow(["Image A", "Image B", "Status", "Response", "Correct?"])
        for t in rec_trials:
            writer.writerow([
                t.get("image_a", t.get("image", "")),
                t.get("image_b", ""),
                t["status"], t["response"],
                "Yes" if t["accuracy"] == 1 else "No",
            ])
        writer.writerow([])
        writer.writerow(["--- CATCH TRIALS: RECOGNITION DETAIL ---"])
        writer.writerow(["Catch #", "Required Response", "Participant Response", "Correct?"])
        for c in catch_rec:
            writer.writerow([f"Catch {c['catch_num']}", c["correct_label"],
                             c["response"], "Yes" if c["accuracy"] == 1 else "No"])
        writer.writerow([])
        writer.writerow([])

# ─── END ──────────────────────────────────────────────────

final_end = visual.TextStim(
    win,
    text=(
        "Well done!\n\n"
        "You have completed the experiment.\n\n"
        "Thank you for your participation!\n\n"
        "Press SPACE or ESCAPE to exit."
    ),
    height=30, color=TEXT_COLOUR, wrapWidth=900, alignText="center",
)
final_end.draw()
win.flip()
event.waitKeys(keyList=["space", "escape"])

exp_handler.close()
pam_exp_handler.close()
win.close()
core.quit()
