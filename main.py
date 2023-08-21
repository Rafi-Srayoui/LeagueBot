import os.path
import time
import PIL.Image as Image
import PIL.ImageDraw
import matplotlib.pyplot as plt
import tensorflow_hub as hub
import tensorflow as tf
import pyautogui
import pydirectinput
import numpy as np
from PIL import ImageDraw, ImageOps
import pytesseract
import math
from operator import itemgetter
from PIL import ImageFont, ImageColor

start_time = time.time()
pyautogui.FAILSAFE = False

def right_mouse_click():
    pyautogui.mouseDown(button='right')
    time.sleep(0.1)
    pyautogui.mouseUp(button='right')


def LeagueOfLegendsRunning():
    import psutil
    if "League of Legends.exe" in (p.name() for p in psutil.process_iter()):
        return True


#while not LeagueOfLegendsRunning():
#    time.sleep(3)
#
#time.sleep(90)  #give 1.5 minutes for loading


img = pyautogui.screenshot()
im_w, im_h = img.size
units_multiplier = im_w / im_h
player_x = im_w / 2
player_y = im_h / 2


# we can get the coordinates of all the towers
# we need using the coordinates of the points on one resolution
# and porting them to the 'current' one
def newCoords(original_x, original_y):
    TowerCount_x = round((original_x / 2560) * im_w)
    TowerCount_y = round((original_y / 1080) * im_h)

    return TowerCount_x, TowerCount_y


minimap_x, minimap_y = newCoords(2240, 760)
minimap_x, minimap_y = round(minimap_x), round(minimap_y)

minimap_region = [minimap_x, minimap_y, im_w - minimap_x, im_h - minimap_y]

mid_coordinates_minimap_X = minimap_x + ((im_w - minimap_x) / 2)
mid_coordinates_minimap_Y = minimap_y + ((im_h - minimap_y) / 2)  # mid coordinates

# turret coordinates on 2560x1080 resolution
# t1  2430 901
# t2  2451 872
# t3  2475 851
# t4  2507 830
t1_x, t1_y = newCoords(2430, 901)
t2_x, t2_y = newCoords(2451, 872)
t3_x, t3_y = newCoords(2475, 851)
nexus_t_x, nexus_t_y = newCoords(2507, 830)


# movement based and using the minimap
# generally static, all logic in-method
# used to move to mid, or closer to turrets when far off
# gets called only when turrets_number changes
def periodic_movement(t_d):
    if t_d == 0:
        pyautogui.moveTo(mid_coordinates_minimap_X, mid_coordinates_minimap_Y)
        right_mouse_click()
        print('preiodic')
    elif t_d == 1:  # since we're only going to be playing on the middle lane, and since
        pyautogui.moveTo((t1_x, t1_y))
        right_mouse_click()
    elif t_d == 2:
        pyautogui.moveTo((t2_x, t2_y))
        right_mouse_click()
    elif t_d == 3:
        pyautogui.moveTo((t3_x, t3_y))
        right_mouse_click()
    elif t_d == 4:
        pyautogui.moveTo((nexus_t_x, nexus_t_y))
        right_mouse_click()


pyautogui.moveTo(mid_coordinates_minimap_X,
                 mid_coordinates_minimap_Y)  # move cursor to the middle of the minimap and move character there
right_mouse_click()

enemy_hp = Image.open('pictures/enemyHealthBar.png')
victory_screen = Image.open('pictures/victoryScreen.png')
model_dir = os.path.dirname('venv/object_detection_model/my_model/saved_model/')

detector = hub.load(model_dir)


def display_image(image):
    fig = plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(image)
    plt.show()


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=2,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)

    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)

    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
               (left, top)],
              width=thickness,
              fill=color)
    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                       fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                  display_str,
                  fill="black",
                  font=font)
        text_bottom -= text_height - 2 * margin


# noinspection PyTypeChecker
def draw_boxes(image, boxes, class_names, scores, max_boxes=35, min_score=0.35):
    class_names_s = [None] * 100
    for j in range(len(class_names[0])):
        if class_names[0][j] == 1:
            class_names_s[j] = 'Acaster'
        elif class_names[0][j] == 2:
            class_names_s[j] = 'Amelee'
        elif class_names[0][j] == 3:
            class_names_s[j] = 'Acanon'
        elif class_names[0][j] == 4:
            class_names_s[j] = 'Ecaster'
        elif class_names[0][j] == 5:
            class_names_s[j] = 'emelee'
        elif class_names[0][j] == 6:
            class_names_s[j] = 'Ecanon'
        elif class_names[0][j] == 7:
            class_names_s[j] = 'AllyTurret'
        elif class_names[0][j] == 8:
            class_names_s[j] = 'EnemyTurret'
        elif class_names[0][j] == 9:
            class_names_s[j] = 'EnemyInhibitor'
        elif class_names[0][j] == 10:
            class_names_s[j] = 'Asuperminion'
    class_names = class_names_s
    scores = np.array(scores)
    image = np.array(image)
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())
    font = ImageFont.load_default()

    for i in range(len(boxes[0])):
        if scores[0][i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[0][i])
            display_str = "{}: {}%".format(class_names[i],
                                           int(100 * scores[0][i]))
            # color = colors[hash(class_names[i]) % len(colors)]
            color = 'peru'
            image_pil = Image.fromarray(np.uint8(image))  # .convert("RGB")
            draw_bounding_box_on_image(
                image_pil,
                ymin,
                xmin,
                ymax,
                xmax,
                color,
                font,
                display_str_list=[display_str])
            np.copyto(image, np.array(image_pil))
    return image

# turret range is 750 in-game units
# x * 650.66811816778 = 750 was the pixel distance between the turret and edge on 1650x1050 res
# x * 611.8570094393  = 750 this one was the pixel distance between the turret and edge on 2550x1080 res
# we solve the system and get
range_multiplier = 1.148589540412044  # multiply this by the current distance between player and turret to check if in range of 750 on any resolution


def check_in_turret_range(distance):
    r = distance * range_multiplier
    if r <= 750:
        return True
    else:
        return False


def get_distance_between_points(p1_x, p1_y, p2_x, p2_y):
    distance = math.sqrt(((p2_x - p1_x) * (p2_x - p1_x)) + ((p2_y - p1_y) * (p2_y - p1_y)))
    return distance


# Since the screen is a rectangle and
# mid, the lane we're playing, has a slope of -1
# we only need to multiply the number of units we
# want to move on the y axis with the units_mutiplier
# to move proportionally
def move_on_screen(units, forward):
    if forward:
        pyautogui.moveTo(x + (units * units_multiplier), y - units)
    else:
        pyautogui.moveTo(x - (units * units_multiplier), y + units)
    right_mouse_click()


def get_mid_point_box(box):
    ymin, xmin, ymax, xmax = tuple(box)
    (left, right, top, bottom) = (xmin * im_w, xmax * im_w,
                                  ymin * im_h, ymax * im_h)
    x = (right + left) / 2
    y = (top + bottom) / 2
    return x, y


def update_turrets():
    if time.time() - start_time < 800:  # by 13 minutes the first turret should be destroyed
        return 0
    elif time.time() - start_time < 1100:
        return 1
    elif time.time() - start_time < 1400:
        return 2
    elif time.time() - start_time < 1600:
        return 3


# Since our player is always in
# the middle of the screen
# then we always know where our player is
def get_objects_distance_to_player(object):
    x_center, y_center = get_mid_point_box(object)
    d = math.sqrt(((x_center - player_x) * (x_center - player_x)) + ((y_center - player_y) * (y_center - player_y)))
    r = d * range_multiplier
    return r, x_center, y_center


def enemy_champion_in_range():
    on_screen = pyautogui.locateCenterOnScreen(enemy_hp, confidence=0.8,
                                               region=[int(im_w / 3), int(im_h / 3), int(im_w / 2), int(im_h / 2)])
    if on_screen != None:
        return on_screen
    else:
        return (-1, -1)


def ally_minions_in_turret_range(minions, turrets):
    minions_in_turret_range = 0
    for i, turret in enumerate(turrets):
        for m, minion in enumerate(minions):
            distance = get_distance_between_points(minions[m][1], minions[m][2], turrets[i][1], turrets[i][2])
            if check_in_turret_range(distance + 75):  #we add bias to be safe
                minions_in_turret_range += 1
    return minions_in_turret_range


def use_ability(a):
    pydirectinput.press(a)


def attack_point(x, y):
    pyautogui.moveTo(x, y)
    pydirectinput.press('space')


def move_champ_to(x, y):
    pyautogui.moveTo(x, y)
    right_mouse_click()
    move_on_screen(20, True)  # to offset the bot being slow we move 20 units ahead to catch up


def reset_cursor():
    pyautogui.moveTo(im_w / 2, im_h / 2)


game_over = False
player_is_up_front = True
enemy_champion_near = False
champion_in_turret_range = False
no_allies_near_champ = True
champion_is_attacking = False

# minimum detection score
min_score = 0.5
while not game_over:

    ori_img = pyautogui.screenshot()

    input_t = np.array(ori_img)
    image = tf.convert_to_tensor(input_t)
    image = image[tf.newaxis, ...]

    result = detector(image)
    #uncomment if you want to see the images and the detected objects
    # image_with_boxes = draw_boxes(
    #    ori_img, result["detection_boxes"],
    #    result["detection_classes"], result["detection_scores"])
    # display_image(image_with_boxes)
    # print(result)

    boxes = result['detection_boxes'][0]
    scores = result['detection_scores'][0]
    classes = result['detection_classes'][0]
    ally_m = 0
    enemy_m = 0
    ally_canon_or_super_minion = 0
    enemy_turrets = 0
    ally_turrets = 0
    enemy_inhib = 0
    detected_objects = []

    ally_minion_distances = [[9999, 9999, 9999]]
    enemy_minion_distances = [[9999, 9999, 9999]]
    enemy_turrets_distance = [[9999, 9999, 9999]]
    enemy_caster_minions = [[9999, 9999, 9999]]
    enemy_c_m = 0
    ally_m_index = 0
    enemy_m_index = 0
    enemy_turrets_index = 0
    enemy_caster_index = 0

    for i, box in enumerate(boxes):
        if scores[i] >= min_score:
            if classes[i] in (1, 2, 3, 10):
                ally_m += 1
                distance, x, y = get_objects_distance_to_player(boxes[i])
                temp = [distance, x, y]
                ally_minion_distances = np.vstack([ally_minion_distances, temp])
                ally_m_index += 1
            elif classes[i] in (4, 5, 6):
                enemy_m += 1
                distance, x, y = get_objects_distance_to_player(boxes[i])
                temp = [distance, x, y]
                enemy_minion_distances = np.vstack([enemy_minion_distances, temp])

                if classes[i] == 4:
                    enemy_c_m += 1
                    temp = [distance, x, y]
                    enemy_caster_minions = np.vstack([enemy_caster_minions, temp])
                    enemy_caster_index += 1

                enemy_m_index += 1
            elif classes[i] == 7:
                ally_turrets += 1
            elif classes[i] == 8:
                enemy_turrets += 1
                distance, x, y = get_objects_distance_to_player(boxes[i])
                temp = [distance, x, y]
                enemy_turrets_distance = np.vstack([enemy_turrets_distance, temp])
                enemy_turrets_index += 1
            elif classes[i] == 9:
                enemy_inhib += 1
        detected_objects.append(boxes[i])

    # get the closest objects to player
    # by sorting the distance arrays
    ally_minion_distances = sorted(ally_minion_distances, key=itemgetter(0))
    enemy_minion_distances = sorted(enemy_minion_distances, key=itemgetter(0))
    enemy_caster_minions = sorted(enemy_caster_minions, key=itemgetter(0))
    enemy_turrets_distance = sorted(enemy_turrets_distance, key=itemgetter(0))
    champion_alone = False

    if enemy_m == 0 and ally_m == 0:
        champion_alone = True

    if ally_m > 0:
        closest_ally_minion = ally_minion_distances[0]
        no_allies_near_champ = False
    else:
        no_allies_near_champ = True

    # check if minions are on the same side of the player
    # this is to avoid being the target of enemy minions
    if enemy_m > 0:
        closest_enemy_minion = enemy_minion_distances[0]
        if not no_allies_near_champ:
            if (closest_ally_minion[1] > player_x and closest_enemy_minion[1] > player_x) or (
                    closest_ally_minion[1] < player_x and closest_enemy_minion[1] < player_x):
                player_is_up_front = False
            else:
                player_is_up_front = True
        else:
            player_is_up_front = True

    if enemy_turrets > 0:
        closest_enemy_turret = enemy_turrets_distance[0]

    (enemy_champion_x, enemy_champion_y) = enemy_champion_in_range()

    if enemy_champion_x == -1:
        enemy_champion_near = False
    else:
        enemy_champion_near = True
        champion_alone = False

    ally_minions_TR = 0
    if enemy_turrets > 0:
        ally_minions_TR = ally_minions_in_turret_range(ally_minion_distances, enemy_turrets_distance)
        if check_in_turret_range(enemy_turrets_distance[0][0] + 100):
            champion_in_turret_range = True
        else:
            champion_in_turret_range = False
    else:
        champion_in_turret_range = False

    turrets_destroyed = update_turrets()

    try:
        if no_allies_near_champ or (champion_in_turret_range and (ally_minions_TR < 2)) or (champion_in_turret_range and enemy_champion_near and ally_minions_TR <= 2):
            periodic_movement(turrets_destroyed)
        elif ally_m > 0 and enemy_m > 0:
            if enemy_minion_distances[0][0] > ally_minion_distances[0][0] * 1.5:
                attack_point(ally_minion_distances[0][1], ally_minion_distances[0][2])
        elif ally_m > 0 and enemy_m == 0 and enemy_turrets == 0:
            move_champ_to(ally_minion_distances[0][1], ally_minion_distances[0][2])
            print('move to chosen ')
        elif enemy_champion_near and not champion_in_turret_range and ally_m > enemy_m + 2:
            attack_point(enemy_champion_x, enemy_champion_y)
            use_ability('q')
        elif enemy_turrets > 0 and ally_minions_TR > 2:
            attack_point(enemy_turrets_distance[0][1], enemy_turrets_distance[0][2])
            use_ability('q')
            print('attack turret chosen')
        elif player_is_up_front:
            move_on_screen(20, False)
    except Exception as e:
        print('there was an exception', e)
        periodic_movement(turrets_destroyed)

    if pyautogui.locateCenterOnScreen(victory_screen, confidence=0.8):
        game_over = True

    time.sleep(0.5)
