import pygame as pg
from pathlib import Path
import json
import platform

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
tick = 0
cycle = 0
offset_x = 0
offset_y = 0
window_moving = False
busy = False
mode = "work"
is_working = True
appslot1 = ""
appslot2 = ""
appslot3 = ""
appslot4 = ""
apps = [appslot1, appslot2, appslot3, appslot4]
current_appslot = 1
current_object = -1
win_size = (600, 300)
VERSION = "Public Beta 1"
VERSION_NAMED = "FinalStep "+VERSION


class Window:
    def __init__(self, screen, window_size_y=300, title="", x=50, y=50, objects=[("label", "", 0, 0, 100, 40, "action")], size_x=300, size_y=150, hidable=False, closable=True, functions=[()]):
        self.title = title
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.hidable = hidable
        self.closable = closable
        self.win = screen
        self.objects = objects
        self.hidden = False
        self.hidden_x = 0
        self.hidden_y = int(window_size_y) - 40
        self.functions = functions

    def redraw(self):
        win = self.win
        if platform.system() != "Windows":
            path_gui_window = path_folder + "/gui/window.png"
            path_gui_titlebar = path_folder + "/gui/titlebar.png"
            path_gui_button_close = path_folder + "/gui/close_button.png"
            path_gui_button_hide = path_folder + "/gui/hide_button.png"
            path_gui_font = path_folder + "/gui/pixel_font.ttf"
            path_gui_button = path_folder + "/gui/button.png"
            path_gui_textbox = path_folder + "/gui/textbox.png"
            path_gui_hidden_window = path_folder + "/gui/window_icon.png"
        else:
            path_gui_window = path_folder + "\\gui\\window.png"
            path_gui_titlebar = path_folder + "\\gui\\titlebar.png"
            path_gui_button_close = path_folder + "\\gui\\close_button.png"
            path_gui_button_hide = path_folder + "\\gui\\hide_button.png"
            path_gui_font = path_folder + "\\gui\\pixel_font.ttf"
            path_gui_button = path_folder + "\\gui\\button.png"
            path_gui_textbox = path_folder + "\\gui\\textbox.png"
            path_gui_hidden_window = path_folder + "\\gui\\window_icon.png"

        gui_window = pg.image.load(path_gui_window)
        gui_titlebar = pg.image.load(path_gui_titlebar)
        gui_button_close = pg.image.load(path_gui_button_close)
        gui_button_hide = pg.image.load(path_gui_button_hide)
        gui_button = pg.image.load(path_gui_button)
        gui_textbox = pg.image.load(path_gui_textbox)
        font = pg.font.Font(path_gui_font, 16)
        small_font = pg.font.Font(path_gui_font, 16)
        gui_hidden_window = pg.image.load(path_gui_hidden_window)
        if not self.hidden:
            win.blit(pg.transform.scale(gui_window, (self.size_x, self.size_y)), (self.x, self.y))
            for obj in self.objects:
                if obj[0] == "button":
                    win.blit(pg.transform.scale(gui_button, (obj[4], obj[5])), (obj[2] + self.x, obj[3] + self.y))
                if obj[0] == "textbox":
                    win.blit(pg.transform.scale(gui_textbox, (obj[4], obj[5])), (obj[2] + self.x, obj[3] + self.y))
                object_text = font.render(str(obj[1]), 1, BLACK)
                win.blit(object_text, [obj[2] + 10 + self.x, obj[3] + 5 + self.y])
            win.blit(pg.transform.scale(gui_titlebar, (self.size_x, 35)), (self.x, self.y))
            if self.closable:
                win.blit(pg.transform.scale(gui_button_close, (30, 30)), (self.size_x + self.x - 32, self.y + 2))
            if self.hidable:
                win.blit(pg.transform.scale(gui_button_hide, (30, 30)), (self.x + 2, self.y + 2))
            window_title = font.render(str(self.title), 1, WHITE)
            win.blit(window_title, [self.x + 36, self.y + 10])
        else:
            win.blit(pg.transform.scale(gui_hidden_window, (90, 90)), (self.hidden_x, self.hidden_y))
            window_title = small_font.render(str(self.title[:9] + "."), 1, WHITE)
            win.blit(window_title, [self.hidden_x + 6, self.hidden_y + 8])


def fill_background(path_image, window_x, window_y, window_object):
    iter1 = int(window_x / 60) + 1
    iter2 = int(window_y / 60) + 1
    image_gui_background = pg.image.load(path_image)
    for i in range(0, iter1):
        for i1 in range(0, iter2):
            window_object.blit(pg.transform.scale(image_gui_background, (60, 60)), (60 * i, 60 * i1))

def fetchapp(filename):
    path_app = path_folder + filename
    with open(path_app, mode="r") as app_file:
        window_arguments = json.loads(app_file.read())
    args_fixed = []
    for i in range(0, 11):
        try:
            args_fixed.append(window_arguments[i])
        except:
            args_fixed.append(None)
    return window, win_size[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10]

mode = "startup"
clock = pg.time.Clock()
pg.init()
path_folder = str(Path().absolute())
pg.display.set_caption('FinalStep Shell '+VERSION)
window = pg.display.set_mode((600, 300))
starting_up = True
if platform.system() != "Windows":
    path_background = path_folder + "/gui/bgs/bg1.png"
    path_gui_button_shutdown = path_folder + "/gui/button_shutdown.png"
    path_gui_button_reboot = path_folder + "/gui/button_reboot.png"
else:
    path_background = path_folder + "\\gui\\bgs\\bg1.png"
    path_gui_button_shutdown = path_folder + "\\gui\\button_shutdown.png"
    path_gui_button_reboot = path_folder + "\\gui\\button_reboot.png"

while is_working:
    pos = pg.mouse.get_pos()
    pg.mouse.set_visible(False)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_working = False
        elif event.type == pg.KEYDOWN:
            if current_object != -1 and event.key == pg.K_BACKSPACE or current_object != -1 and event.key == pg.K_DELETE:
                current_window.objects[current_object][1] = current_window.objects[current_object][1][:-1]
            elif current_object != -1 and event.key == pg.K_ESCAPE:
                current_object = -1
            elif current_object != -1:
                current_window.objects[current_object][1] += event.unicode
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                cannot_reselect = False
                if mouse_x >= win_size[0]-40 and mouse_x <= win_size[0] and mouse_y >= win_size[1]-40 and mouse_y <= win_size[1] and mode == "work":
                    cycle = 0
                    tick =0 
                    mode = "shutdown"
                elif mouse_x >= win_size[0]-80 and mouse_x <= win_size[0]-40 and mouse_y >= win_size[1]-40 and mouse_y <= win_size[1] and mode == "work":
                    cycle = 0
                    tick =0 
                    mode = "reboot"    
                if not current_window.hidden:
                    for obj_id in range(len(current_window.objects)):
                        obj = current_window.objects[obj_id]
                        x = obj[2] + current_window.x
                        y = obj[3] + current_window.y
                        size_x = obj[4]
                        size_y = obj[5]
                        if mouse_x >= x and mouse_x <= x + size_x and mouse_y >= y and mouse_y <= y + size_y and not current_window.hidden:
                            if obj[0] == "button":
                                for funct in current_window.functions[obj_id]:
                                    if "fetch" in funct:
                                        if platform.system() != "Windows":
                                            args_fixed = fetchapp("/" + funct[6:])
                                        else:
                                            args_fixed = fetchapp("\\" + funct[6:])
                                        if appslot2 == "":
                                            appslot2 = Window(args_fixed[0], args_fixed[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10])
                                            appslot2.hidden_x = 90
                                            current_appslot = 2
                                            current_window = appslot2
                                        elif appslot3 == "":
                                            appslot3 = Window(args_fixed[0], args_fixed[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10])
                                            appslot3.hidden_x = 180
                                            current_appslot = 3
                                            current_window = appslot3
                                        elif appslot4 == "":
                                            appslot4 = Window(args_fixed[0], args_fixed[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10])
                                            appslot4.hidden_x = 270
                                            current_appslot = 4
                                            current_window = appslot4
                                    else:
                                        exec(funct)
                                    cannot_reselect = True
                                break
                            elif mouse_x >= x and mouse_x <= x + size_x and mouse_y >= y and mouse_y <= y + size_y and not current_window.hidden and obj[0] == "textbox":
                                current_object = obj_id
                                cannot_reselect = True
                                break
                if window_moving:
                    window_moving = False
                    current_window.x = mouse_x
                    current_window.y = mouse_y
                elif mouse_x >= current_window.x + 2 and mouse_x <= current_window.x + 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32 and not busy and not current_window.hidden and current_window.hidable:
                    current_window.hidden = True
                elif mouse_x <= current_window.x + current_window.size_x - 2 and mouse_x >= current_window.x + current_window.size_x - 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32 and current_window.closable and not busy and not current_window.hidden:
                    if current_appslot == 2:
                        appslot2 = ""
                        current_object = -1
                    elif current_appslot == 3:
                        appslot3 = ""
                        current_object = -1
                    elif current_appslot == 4:
                        appslot4 = ""
                        current_object = -1
                    current_appslot = 1
                    current_window = appslot1
                elif mouse_x >= current_window.hidden_x and mouse_x <= current_window.hidden_x + 90 and mouse_y >= current_window.hidden_y and mouse_y <= current_window.hidden_y + 90 and not busy and current_window.hidden and current_window.hidable:
                    current_window.hidden = False
                elif mouse_x >= current_window.x and mouse_x <= current_window.x + current_window.size_x and mouse_y >= current_window.y and mouse_y <= current_window.y + 40 and not busy and not(mouse_x >= current_window.x + 2 and mouse_x <= current_window.x + 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32):
                    if not window_moving:
                        window_moving = True
                apps = [appslot1, appslot2, appslot3, appslot4]
                if not cannot_reselect:
                    for search_window_id in range(len(apps)):
                        search_window = apps[search_window_id]
                        do_break = False
                        if search_window != "":
                            if mouse_x >= search_window.x and mouse_x <= search_window.x + search_window.size_x and mouse_y >= search_window.y and mouse_y <= search_window.y + search_window.size_y and search_window_id + 1 != current_appslot and not search_window.hidden:
                                current_window = search_window
                                current_appslot = search_window_id + 1
                                current_object = -1
                                do_break = True
                            elif mouse_x >= search_window.hidden_x and mouse_x <= search_window.hidden_x + 90 and mouse_y >= search_window.hidden_y and mouse_y <= search_window.hidden_y + 90 and not busy and search_window.hidden and search_window.hidable and search_window_id + 1 != current_appslot:
                                search_window.hidden = False
                                current_object = -1
                                current_appslot = search_window_id + 1
                                current_window = search_window
                                do_break = True
                        if do_break:
                            break
                cannot_reselect = False
    clock.tick(30)
    tick += 1
    if tick == 31:
        tick = 0
        cycle += 1
    if cycle == 0 and tick == 1 and mode == "startup":
        appslot1 = Window(window, win_size[1], VERSION_NAMED, 150, 50, [["label", "Booting up...", 50, 80, 100, 50]], 300, 170, False, False)
        appslot1.hidden = False
        current_window = appslot1
        busy = True
    elif cycle == 3 and tick == 1:
        busy = False
        if mode == "shutdown":
            is_working = False
            cycle = 0
            tick = 0
        elif mode == "startup":
            mode = "work"
            appslot1 = Window(window, win_size[1], "FinalWorkspace "+VERSION, 10, 40, [("button", "Calc.exec", 10, 40, 100, 20)], 300, 170, True, False, [("fetch calc.exec", "")])
            appslot1.hidden = False
            current_window = appslot1
        elif mode == "reboot":
            mode = "blackscreen"
            cycle = 0
            tick = 0
            appslot1 = ""
            current_window = appslot1
    if cycle == 0 and tick == 1 and mode == "shutdown":
        appslot1 = Window(window, win_size[1], VERSION_NAMED, 150, 50, [["label", "Shutting down...", 50, 80, 100, 50]], 300, 170, False, False)
        appslot1.hidden = False
        current_window = appslot1
        busy = True
    elif cycle == 0 and tick == 1 and mode == "reboot":
        appslot1 = Window(window, win_size[1], VERSION_NAMED, 150, 50, [["label", "Rebooting...", 50, 80, 100, 50]], 300, 170, False, False)
        appslot1.hidden = False
        current_window = appslot1
        busy = True
    elif cycle == 1 and mode == "blackscreen":
        mode = "startup"
        cycle = 0
        tick = 0
    window.fill(BLACK)
    if mode != "blackscreen":
        fill_background(path_background, win_size[0], win_size[1], window)
    apps = [appslot1,appslot2,appslot3,appslot4]
    for selected_window in apps:
        try:
            selected_window.redraw()
        except:
            pass
    if mode == "work":
        gui_button_shutdown = pg.image.load(path_gui_button_shutdown)
        window.blit(pg.transform.scale(gui_button_shutdown,(40,40)),(win_size[0]-40,win_size[1]-40))
        gui_button_reboot = pg.image.load(path_gui_button_reboot)
        window.blit(pg.transform.scale(gui_button_reboot,(40,40)),(win_size[0]-80,win_size[1]-40))
    try:current_window.redraw()
    except:pass
    if pg.mouse.get_focused():
        pos = pg.mouse.get_pos()
        if window_moving:
            if platform.system() != "Windows":
                path_cursor = path_folder + "/gui/cursor_move.png"
            else:
                path_cursor = path_folder + "\\gui\\cursor_move.png"
            gui_cursor = pg.image.load(path_cursor)
            window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
        elif busy:
            if tick <= 30 and tick >= 21:
                if platform.system() != "Windows":
                    path_cursor = path_folder + "/gui/cursor_busy2.png"
                else:
                    path_cursor = path_folder + "/gui/cursor_busy2.png"
                gui_cursor = pg.image.load(path_cursor)
                window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
            elif tick <= 20 and tick >= 11:
                if platform.system() != "Windows":
                    path_cursor = path_folder + "/gui/cursor_busy1.png"
                else:
                    path_cursor = path_folder + "/gui/cursor_busy1.png"
                gui_cursor = pg.image.load(path_cursor)
                window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
            else:
                if platform.system() != "Windows":
                    path_cursor = path_folder + "/gui/cursor_busy0.png"
                else:
                    path_cursor = path_folder + "/gui/cursor_busy0.png"
                gui_cursor = pg.image.load(path_cursor)
                window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
        else:
            if platform.system() != "Windows":
                path_cursor = path_folder + "/gui/cursor.png"
            else:
                path_cursor = path_folder + "/gui/cursor.png"
            gui_cursor = pg.image.load(path_cursor)
            window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
    pg.display.update()