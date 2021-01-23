import pygame as pg
from pathlib import Path
from pprint import pprint
import json
import platform
import os
import shutil

WHITE = (255, 255, 255)
DARKGRAY = (112, 112, 112)
LIGHTGRAY = (163, 163, 163)
BLACK = (0, 0, 0)
tick = 0
cycle = 0
clicked = False
offset_x = 0
offset_y = 0
window_moving = False
busy = False
mode = "work"
is_working = True
dock_hidden = False
appslot1 = ""
appslot2 = ""
appslot3 = ""
appslot4 = ""
splitter = "\n"
apps = [appslot1, appslot2, appslot3, appslot4]
current_appslot = 1
current_object = ""
win_size = (620, 300)
VERSION = "Beta 2.4"
VERSION_NAMED = "FinalStep " + VERSION
path_folder = str(Path().absolute())
disk_root = os.getcwd()
if platform.system() != "Windows":
    path_background = path_folder + "/gui/bgs/bg1.png"
    path_gui_button_close = path_folder + "/gui/close_button.png"
    path_gui_button_hide = path_folder + "/gui/hide_button.png"
    path_gui_font = path_folder + "/gui/pixel_font.ttf"
else:
    path_background = path_folder + "\\gui\\bgs\\bg1.png"
    path_gui_button_close = path_folder + "\\gui\\close_button.png"
    path_gui_button_hide = path_folder + "\\gui\\hide_button.png"
    path_gui_font = path_folder + "\\gui\\pixel_font.ttf"

class Window:
    def __init__(self, screen, window_size_y=300, title="Window", x=50, y=50, objects=[("label", "", 0, 0, 100, 40, "")], size_x=300, size_y=150, hidable=False, has_titlebar=True, closable=True, functions=[("", "")], on_refresh=()):
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
        self.on_refresh = on_refresh
        self.has_titlebar = has_titlebar

    def redraw(self):
        win = self.win
        gui_button_close = pg.image.load(path_gui_button_close)
        gui_button_hide = pg.image.load(path_gui_button_hide)
        font = pg.font.Font(path_gui_font, 16)
        small_font = pg.font.Font(path_gui_font, 16)
        if not self.hidden:
            pg.draw.rect(win, WHITE, (self.x, self.y, self.size_x, self.size_y))
            pg.draw.line(win, BLACK, [self.x, self.y + 2], [self.x + self.size_x - 1, self.y + 2], 5)
            pg.draw.line(win, BLACK, [self.x + self.size_x - 2, self.y], [self.x + self.size_x - 2, self.y + self.size_y], 5)
            pg.draw.line(win, BLACK, [self.x + self.size_x - 2, self.y + self.size_y - 2], [self.x + 2, self.y + self.size_y - 2], 5)
            pg.draw.line(win, BLACK, [self.x + 2, self.y + 2], [self.x + 2, self.y + self.size_y], 5)
            if self.on_refresh != ():
                for action in self.on_refresh:
                    exec(action)
            for obj in self.objects:
                if obj[0] == "button":
                    pg.draw.rect(win, DARKGRAY, (obj[2] + self.x, obj[3] + self.y, obj[4], obj[5]))
                    pg.draw.line(win, LIGHTGRAY, [obj[2] + self.x, obj[3] + self.y - 1], [obj[2] + self.x + obj[4] - 1, obj[3] + self.y - 1], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + obj[4] - 2, obj[3] + self.y], [obj[2] + self.x + obj[4] - 2, obj[3] + self.y + obj[5] - 1], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + obj[4] - 2, obj[3] + self.y + obj[5] - 2], [obj[2] + self.x + 2, obj[3] + self.y + obj[5] - 2], 3)
                    pg.draw.line(win, LIGHTGRAY, [obj[2] + self.x, obj[3] + self.y - 2], [obj[2] + self.x, obj[3] + self.y + obj[5] - 1], 3)
                elif obj[0] == "textbox" or obj[0] == "textfield":
                    pg.draw.rect(win, WHITE, (obj[2] + self.x, obj[3] + self.y, obj[4], obj[5]))
                    pg.draw.line(win, BLACK, [obj[2] + self.x, obj[3] + self.y - 1], [obj[2] + self.x + obj[4] - 1, obj[3] + self.y - 1], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + obj[4] - 2, obj[3] + self.y], [obj[2] + self.x + obj[4] - 2, obj[3] + self.y + obj[5] - 1], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + obj[4] - 1, obj[3] + self.y + obj[5] - 2], [obj[2] + self.x + 1, obj[3] + self.y + obj[5] - 2], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + 1, obj[3] + self.y - 2], [obj[2] + self.x + 1, obj[3] + self.y + obj[5] - 1], 3)
                elif obj[0] == "checkbox":
                    obj[4] = 15
                    obj[5] = 15
                    pg.draw.rect(win, WHITE, (obj[2] + self.x, obj[3] + self.y, obj[4], obj[5]))
                    pg.draw.line(win, BLACK, [obj[2] + self.x, obj[3] + self.y - 1], [obj[2] + self.x + 15,obj[3] + self.y - 1], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + 15,obj[3] + self.y - 2], [obj[2] + self.x + 15,obj[3] + self.y +15], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + 15,obj[3] + self.y +14], [obj[2] + self.x + 1, obj[3] + self.y +14], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x, obj[3] + self.y-2 ],[obj[2] + self.x , obj[3] + self.y +15], 3)
                    if obj[1]:
                        pg.draw.line(win, BLACK, [obj[2] + self.x +4, obj[3] + self.y +7], [obj[2] + self.x + 8,obj[3] + self.y + 10], 3)
                        pg.draw.line(win, BLACK, [obj[2] + self.x + 8,obj[3] + self.y + 10], [obj[2] + self.x + 11,obj[3] + self.y + 2], 3)
                elif obj[0] == "line":
                    pg.draw.line(win, BLACK, [obj[2] + self.x, obj[3] + self.y], [obj[4]+ self.x, obj[5]+ self.y], 3)
                if not(obj[0] == "progressbar" or obj[0] == "textfield" or obj[0] == "checkbox"):
                    object_text = font.render(str(obj[1]), 1, BLACK)
                    win.blit(object_text, [obj[2] + 10 + self.x, obj[3] + 5 + self.y])
                elif obj[0] == "textfield":
                    line = obj[6]
                    textfield_lines = obj[1]
                    lines_amount = int((obj[5] - 5) / 10)
                    try:
                        line_num = 0
                        if int(line) - 1 == -1:
                            add = 1
                        else:
                            add = 0
                        for line_id in range(int(line) - 1 + add, int(line) + lines_amount - 1 + add):
                            line_text = textfield_lines[line_id]
                            if line_id == line:
                                object_text = font.render("\u2192" + str(line_text), 1, BLACK)
                            else:
                                object_text = font.render(" " + str(line_text), 1, BLACK)
                            win.blit(object_text, [obj[2] + 10 + self.x, obj[3] + 4 + self.y + (10 * line_num)])
                            line_num += 1
                    except:
                        pass
            if self.has_titlebar:
                pg.draw.rect(win, LIGHTGRAY, (self.x, self.y, self.size_x + 1, 35))
                if self.closable:
                    win.blit(pg.transform.scale(gui_button_close, (30, 30)), (self.size_x + self.x - 32, self.y + 2))
                if self.hidable:
                    win.blit(pg.transform.scale(gui_button_hide, (30, 30)), (self.x + 2, self.y + 2))                
                window_title = font.render(str(self.title), 1, WHITE)
                win.blit(window_title, [self.x + 36, self.y + 10])


def fill_background(path_image, window_x, window_y, window_object):
    iter1 = int(window_x / 60) + 1
    iter2 = int(window_y / 60) + 1
    image_gui_background = pg.image.load(path_image)
    for i in range(0, iter1):
        for i1 in range(0, iter2):
            window_object.blit(pg.transform.scale(image_gui_background, (60, 60)), (60 * i, 60 * i1))


def fetchapp(filename):
    path_app = os.getcwd() + filename
    with open(path_app, mode="r") as app_file:
        window_arguments = json.loads(app_file.read())
    args_fixed = []
    for i in range(0, 13):
        try:
            args_fixed.append(window_arguments[i])
        except:
            args_fixed.append(None)
    return window, win_size[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10], args_fixed[11],args_fixed[12]


mode = "startup"
clock = pg.time.Clock()
pg.init()
pg.display.set_caption('FinalStep Shell ' + VERSION)
window = pg.display.set_mode(win_size)
starting_up = True

while is_working:
    pos = pg.mouse.get_pos()
    if platform.system() != "Windows":
        path = str(os.getcwd()) + "/"
    else:
        path = str(os.getcwd()) + "\\"
    pg.mouse.set_visible(False)
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused(): clicked = True
        elif event.type == pg.MOUSEBUTTONUP: clicked = False
        if event.type == pg.QUIT:
            is_working = False
        elif event.type == pg.KEYDOWN:
            if current_object != "":
                if current_window.objects[current_object][0] == "textbox":
                    if current_object != -1 and event.key == pg.K_BACKSPACE or current_object != -1 and event.key == pg.K_DELETE:
                        current_window.objects[current_object][1] = current_window.objects[current_object][1][:-1]
                    elif current_object != -1 and event.key == pg.K_ESCAPE:
                        current_object = -1
                    elif current_object != -1:
                        current_window.objects[current_object][1] += event.unicode
                elif current_window.objects[current_object][0] == "textfield":
                    line = current_window.objects[current_object][-1]
                    if current_object != "" and event.key == pg.K_BACKSPACE or current_object != "" and event.key == pg.K_DELETE:
                        try:
                            if current_window.objects[current_object][1][int(line)] != "":
                                current_window.objects[current_object][1][int(line)] = current_window.objects[current_object][1][int(line)][:-1]
                            else:
                                if line != 0:
                                    current_window.objects[current_object][1].pop(int(line))
                                    line -= 1
                                    current_window.objects[current_object][6] = line

                        except:
                            pass
                    elif current_object != "" and event.key == pg.K_DOWN:
                        try:
                            if current_window.objects[current_object][1][int(line)] != current_window.objects[current_object][1][-1]:
                                line += 1
                                current_window.objects[current_object][6] = line
                        except:
                            pass
                    elif current_object != "" and event.key == pg.K_UP:
                        if line != 0:
                            line -= 1
                            current_window.objects[current_object][6] = line
                    elif current_object != "" and event.key == pg.K_ESCAPE:
                        current_object = ""
                    elif current_object != "" and event.key == pg.K_RETURN:
                        line += 1
                        current_window.objects[current_object][1].insert(line, "")

                        current_window.objects[current_object][6] = line
                    elif current_object != "":
                        current_window.objects[current_object][1][int(line)] += event.unicode
        elif clicked:
            mouse_x = pos[0]
            mouse_y = pos[1]
            cannot_reselect = False
            if mouse_x >= win_size[0] - 90 and mouse_x <= win_size[0] and mouse_y >= win_size[1]-50 and mouse_y <= win_size[1]-25 and mode == "work":
                cycle = 0
                tick = 0
                mode = "reboot"
                appslot2 = ""
                appslot3 = ""
                appslot4 = ""
            if mouse_x >= win_size[0] - 90 and mouse_x <= win_size[0] and mouse_y >= win_size[1]-25 and mouse_y <= win_size[1] and mode == "work":
                cycle = 0
                tick = 0
                mode = "shutdown"
                appslot2 = ""
                appslot3 = ""
                appslot4 = ""
            if mouse_x >= 90 and mouse_x <= 199 and mouse_y >= win_size[1]-50 and mouse_y <= win_size[1]-25 and mode == "work":
                current_appslot = 1
                current_window = appslot1
                current_object = ""
                appslot1.hidden = False
            if mouse_x >= 200 and mouse_x <= 309 and mouse_y >= win_size[1]-50 and mouse_y <= win_size[1]-25 and mode == "work" and appslot2 != "":
                current_appslot = 2
                current_window = appslot2
                current_object = ""
                appslot2.hidden = False
            if mouse_x >= 310 and mouse_x <= 419 and mouse_y >= win_size[1]-50 and mouse_y <= win_size[1]-25 and mode == "work" and appslot3 != "":
                current_appslot = 3
                current_window = appslot3
                current_object = ""
                appslot3.hidden = False
            if mouse_x >= 420 and mouse_x <= 529 and mouse_y >= win_size[1]-50 and mouse_y <= win_size[1]-25 and mode == "work" and appslot4 != "":
                current_appslot = 4
                current_window = appslot4
                current_object = ""
                appslot4.hidden = False
            if not current_window.hidden:
                for obj_id in range(len(current_window.objects)):
                    obj = current_window.objects[obj_id]
                    obj_type = obj[0]
                    x = obj[2] + current_window.x
                    y = obj[3] + current_window.y
                    size_x = obj[4]
                    size_y = obj[5]
                    if mouse_x >= x and mouse_x <= x + size_x and mouse_y >= y and mouse_y <= y + size_y and not current_window.hidden:
                        if obj[0] == "button" or obj[0] == "label":
                            for funct in current_window.functions[obj_id]:
                                if "fetch" in funct:
                                    if platform.system() != "Windows":
                                        args_fixed = fetchapp("/" + funct[6:])
                                    else:
                                        args_fixed = fetchapp("\\" + funct[6:])
                                    if appslot2 == "":
                                        appslot2 = Window(args_fixed[0], args_fixed[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10], args_fixed[11],args_fixed[12])
                                        appslot2.hidden_x = 90 + 40
                                        current_appslot = 2
                                        current_window = appslot2
                                    elif appslot3 == "":
                                        appslot3 = Window(args_fixed[0], args_fixed[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10], args_fixed[11],args_fixed[12])
                                        appslot3.hidden_x = 180 + 40
                                        current_appslot = 3
                                        current_window = appslot3
                                    elif appslot4 == "":
                                        appslot4 = Window(args_fixed[0], args_fixed[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10], args_fixed[11],args_fixed[12])
                                        appslot4.hidden_x = 270 + 40
                                        current_appslot = 4
                                        current_window = appslot4
                                else:
                                    exec(funct)
                                cannot_reselect = True
                            break
                        elif obj[0] == "textbox" or obj[0] == "textfield":
                            current_object = obj_id
                            cannot_reselect = True
                            break
                        elif obj[0] == "checkbox":
                            obj[1] = not obj[1]
                            cannot_reselect = True
                            break                            
            if mouse_x >= current_window.x + 2 and mouse_x <= current_window.x + 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32 and not busy and not current_window.hidden and current_window.hidable:
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
            elif mouse_x >= current_window.x and mouse_x <= current_window.x + current_window.size_x and mouse_y >= current_window.y and mouse_y <= current_window.y + 40 and not busy and not(mouse_x >= current_window.x + 2 and mouse_x <= current_window.x + 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32):
                current_window.x = mouse_x - (current_window.size_x / 2)
                current_window.y = mouse_y - 17
                window_moving = True
            apps = [appslot1, appslot2, appslot3, appslot4]
            if not cannot_reselect:
                for search_window_id in range(len(apps)):
                    search_window = apps[search_window_id]
                    do_break = False
                    if search_window != "":
                        if mouse_x >= search_window.x and mouse_x <= search_window.x + search_window.size_x and mouse_y >= search_window.y and mouse_y <= search_window.y + search_window.size_y and search_window_id + 1 != current_appslot and not search_window.hidden and not(mouse_x >= current_window.x and mouse_x <= current_window.x +current_window.size_x and mouse_y >= current_window.y and mouse_y <= current_window.y + current_window.size_y):
                            current_window = search_window
                            current_appslot = search_window_id + 1
                            current_object = -1
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
        appslot1 = Window(window, win_size[1], VERSION_NAMED, 150, 50, [["label", "Booting up...", 50, 80, 100, 50]], 300, 170, False, True, False)
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
            appslot1 = Window(window, win_size[1], "fFiles " + VERSION, 10, 10, [["checkbox",False,190,204,15,15]], 300, 225, True, True, False, [["", ""]], ("""indent_x = 0\nindent_y = 0\nfiles = os.listdir()\nself.objects = [self.objects[0],["label","Delete:",120,200,0,0]]\nself.functions = [['',''],["",""]]\nfor file_id in range(len(files)):\n    if file_id % 10 == 0 and file_id != 0:\n        indent_x +=1\n        indent_y = 0\n    file = files[file_id]\n    if len(file) >= 14:\n        file = file[:3]+'~'+file[-5:]\n    if os.path.isdir(files[file_id]):\n        self.objects.append(('label','['+str(file)+']',10+(100*indent_x),40+(15*indent_y),len('['+str(file)+']')*10,20))\n    else:\n        self.objects.append(('label',file,10+(100*indent_x),40+(15*indent_y),len(str(file))*10,20))\n    if self.objects[0][1] and os.path.isdir(files[file_id]):\n      self.functions.append(("shutil.rmtree('"+files[file_id]+"')",""))\n    if self.objects[0][1]:\n      self.functions.append(("os.remove('"+files[file_id]+"')",""))\n    elif file[-5:] == '.exec':\n        self.functions.append(('fetch '+str(files[file_id]),''))\n    elif os.path.isdir(files[file_id]):\n        self.functions.append(('os.chdir("'+path+str(files[file_id])+'")',''))\n    else:\n        self.functions.append(('',''))\n    indent_y +=1\nself.objects.append(('label','Go to:',10,200,60,20))\nself.functions.append(('',''))\nself.objects.append(('label','/',75,200,10,10))\nself.functions.append(('os.chdir(disk_root)',''))\nif os.getcwd() != disk_root:\n    self.objects.append(('label','..',90,200,20,20))\n    self.functions.append(('os.chdir("..")',''))""", ""))
            appslot1.hidden = False
            appslot1.hidden_x = 40
            current_window = appslot1
        elif mode == "reboot":
            mode = "blackscreen"
            cycle = 0
            tick = 0
            appslot1 = ""
            current_window = appslot1
    if cycle == 0 and tick == 1 and mode == "shutdown":
        appslot1 = Window(window, win_size[1], VERSION_NAMED, 150, 50, [["label", "Shutting down...", 50, 80, 100, 50]], 300, 170, False, True, False)
        appslot1.hidden = False
        current_window = appslot1
        busy = True
    elif cycle == 0 and tick == 1 and mode == "reboot":
        appslot1 = Window(window, win_size[1], VERSION_NAMED, 150, 50, [["label", "Rebooting...", 50, 80, 100, 50]], 300, 170, False, True, False)
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
    apps = [appslot1, appslot2, appslot3, appslot4]
    for selected_window in apps:
        try:
            if dock_hidden and selected_window.hidden:
                pass
            else:
                selected_window.redraw()
        except:
            pass
    if mode == "work":
        if not dock_hidden:
            appbuttons = []
            length = (win_size[0] - 130) /4
            appbuttons.append(["button", "1 FinalWork.", 90, 2, 110, 25])
            if appslot2 != "":
                appbuttons.append(["button", "2 "+appslot2.title[:9], 200, 2, 110, 25])
            if appslot3 != "":
                appbuttons.append(["button", "3 "+appslot3.title[:9], 310, 2, 110, 25])
            if appslot4 != "":
                appbuttons.append(["button", "4 "+appslot4.title[:9], 420, 2, 110, 25])
            appbuttons = [["label", "FinalStep", 5, 5, 100, 50],["label", VERSION, 3, 20, 100, 50],["button", "Reboot", win_size[0]-90, 2, 90, 25],["button", "Shutdown", win_size[0]-90, 27, 90, 25]]+appbuttons
            appfunctions = [[],[],["""cycle = 0\ntick = 0\nmode = "reboot"\nappslot2 = ""\nappslot3 = ""\nappslot4 = "" """,""],["""cycle = 0\ntick = 0\nmode = "shutdown"\nappslot2 = ""\nappslot3 = ""\nappslot4 = "" """,""]]
            dock_window = Window(window, win_size[1], "", 0, 250, appbuttons, win_size[0], 50, False, False, False,appfunctions)
            dock_window.redraw()            
    try:
        if dock_hidden and current_window.hidden:
            pass
        else:
            current_window.redraw()
    except:
        pass
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
