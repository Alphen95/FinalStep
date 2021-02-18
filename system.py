import pygame as pg
import pathlib
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
window_indent = -1
splitter = "\n"
crt_tick = -31
display_prefs = [False,"/BGs/default.png",False]
apps = [""]
current_appslot = 0
current_object = ""
win_size = (800, 600)
VERSION = "Beta 4"
VERSION_NAMED = "FinalStep " + VERSION
path_folder = str(pathlib.Path(__file__).parent.absolute())
disk_root = str(pathlib.Path(__file__).parent.absolute())
os.chdir(disk_root)
path_folder = path_folder.replace("\\","/")
path_gui_button_close = path_folder + "/gui/close_button.png"
path_gui_button_hide = path_folder + "/gui/hide_button.png"
path_gui_font = path_folder + "/gui/pixel_font.ttf"
path_icon = path_folder + "/gui/logo.png"
path_overlay2 = path_folder + "/gui/overlay_crt_scanlines.png"
path_overlay1 = path_folder + "/gui/overlay_crt_line.png"

class Window:
    def __init__(self, screen, window_size_y=300, title="Window", x=50, y=50, objects=[("label", "", 0, 0, 100, 40, "")], size_x=300, size_y=150, hidable=False, has_titlebar=True, closable=True, functions=[("", "")], on_refresh=(),color = (255,255,255), border = True):
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
        self.color = color
        self.border = border

    def redraw(self):
        win = self.win
        gui_button_close = pg.image.load(path_gui_button_close)
        gui_button_hide = pg.image.load(path_gui_button_hide)
        font = pg.font.Font(path_gui_font, 16)
        small_font = pg.font.Font(path_gui_font, 16)
        if not self.hidden:
            pg.draw.rect(win, self.color, (self.x, self.y, self.size_x, self.size_y))
            if self.border:
                pg.draw.line(win, BLACK, [self.x, self.y + 2], [self.x + self.size_x - 1, self.y + 2], 5)
                pg.draw.line(win, BLACK, [self.x + self.size_x - 2, self.y], [self.x + self.size_x - 2, self.y + self.size_y], 5)
                pg.draw.line(win, BLACK, [self.x + self.size_x - 2, self.y + self.size_y - 2], [self.x + 2, self.y + self.size_y - 2], 5)
                pg.draw.line(win, BLACK, [self.x + 2, self.y + 2], [self.x + 2, self.y + self.size_y], 5)                
            if self.on_refresh != ():
                for action in self.on_refresh:exec(action)
            for obj in self.objects:
                if obj[0] == "button":
                    pg.draw.rect(win, DARKGRAY, (obj[2] + self.x, obj[3] + self.y, obj[4], obj[5]))
                    pg.draw.line(win, BLACK, [obj[2] + self.x, obj[3] + self.y - 1], [obj[2] + self.x + obj[4] - 1, obj[3] + self.y - 1], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + obj[4] - 2, obj[3] + self.y], [obj[2] + self.x + obj[4] - 2, obj[3] + self.y + obj[5] - 1], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x + obj[4] - 2, obj[3] + self.y + obj[5] - 2], [obj[2] + self.x + 2, obj[3] + self.y + obj[5] - 2], 3)
                    pg.draw.line(win, BLACK, [obj[2] + self.x, obj[3] + self.y - 2], [obj[2] + self.x, obj[3] + self.y + obj[5] - 1], 3)
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
                elif obj[0] == "line":pg.draw.line(win, BLACK, [obj[2] + self.x, obj[3] + self.y], [obj[4]+ self.x, obj[5]+ self.y], 3)
                elif obj[0] == "image":
                    image_gui = pg.image.load(path_folder+obj[1])
                    win.blit(pg.transform.scale(image_gui, (obj[4], obj[5])), (self.x+obj[2], self.y+obj[3]))
                if not(obj[0] == "progressbar" or obj[0] == "textfield" or obj[0] == "checkbox" or obj[0] == "image"):
                    object_text = font.render(str(obj[1]), 1, BLACK)
                    win.blit(object_text, [obj[2] + 2 + self.x, obj[3] + 2 + self.y])
                elif obj[0] == "textfield":
                    line = obj[6]
                    textfield_lines = obj[1]
                    lines_amount = int((obj[5] - 5) / 10)
                    try:
                        line_num = 0
                        if int(line) - 1 == -1:add = 1
                        else:add = 0
                        for line_id in range(int(line) - 1 + add, int(line) + lines_amount - 1 + add):
                            line_text = textfield_lines[line_id]
                            if line_id == line:object_text = font.render("\u2192" + str(line_text), 1, BLACK)
                            else:object_text = font.render(" " + str(line_text), 1, BLACK)
                            win.blit(object_text, [obj[2] + 10 + self.x, obj[3] + 4 + self.y + (10 * line_num)])
                            line_num += 1
                    except:pass
            if self.has_titlebar:
                pg.draw.rect(win, LIGHTGRAY, (self.x, self.y, self.size_x + 1, 35))
                if self.closable:win.blit(pg.transform.scale(gui_button_close, (30, 30)), (self.size_x + self.x - 32, self.y + 2))
                if self.hidable:win.blit(pg.transform.scale(gui_button_hide, (30, 30)), (self.x + 2, self.y + 2))                
                window_title = font.render(str(self.title), 1, WHITE)
                win.blit(window_title, [self.x + 36, self.y + 10])


def fill_background(path_image, window_x, window_y, window_object):
    iter1 = int(window_x / 60) + 1
    iter2 = int(window_y / 60) + 1
    try:
        image_gui_background = pg.image.load(path_image)
        for i in range(0, iter1):
            for i1 in range(0, iter2):window_object.blit(pg.transform.scale(image_gui_background, (60, 60)), (60 * i, 60 * i1))
    except: pass


def fetchapp(filename):
    path_app = os.getcwd() + filename
    with open(path_app, mode="r") as app_file:window_arguments = json.loads(app_file.read())
    args_fixed = []
    for i in range(0, 13):
        try:args_fixed.append(window_arguments[i])
        except:args_fixed.append(None)
    return window, win_size[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10], args_fixed[11],args_fixed[12]


mode = "startup"
clock = pg.time.Clock()
pg.init()
pg.display.set_caption('FinalStep ' + VERSION)
icon = pg.image.load(path_icon)
pg.display.set_icon(icon)
window = pg.display.set_mode(win_size)
starting_up = True
crt_overlay1= pg.image.load(path_overlay1)
crt_overlay2= pg.image.load(path_overlay2)
try:
    with open("preferences.json",mode="r") as file:display_prefs = json.loads(file.read())
except:
    with open("preferences.json",mode="w+") as file:file.write(json.dumps(display_prefs))

while is_working:
    pos = pg.mouse.get_pos()
    path = str(os.getcwd()) + "/"
    path = path.replace("\\","/")
    pg.mouse.set_visible(False)
    current_window = apps[current_appslot]
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused(): clicked = True
        elif event.type == pg.MOUSEBUTTONUP: clicked = False
        if event.type == pg.QUIT:is_working = False
        elif event.type == pg.KEYDOWN:
            if current_object != "":
                if current_window.objects[current_object][0] == "textbox":
                    if current_object != -1 and event.key == pg.K_BACKSPACE or current_object != -1 and event.key == pg.K_DELETE:current_window.objects[current_object][1] = current_window.objects[current_object][1][:-1]
                    elif current_object != -1 and event.key == pg.K_ESCAPE:current_object = -1
                    elif current_object != -1:current_window.objects[current_object][1] += event.unicode
                elif current_window.objects[current_object][0] == "textfield":
                    line = current_window.objects[current_object][-1]
                    if current_object != "" and event.key == pg.K_BACKSPACE or current_object != "" and event.key == pg.K_DELETE:
                        try:
                            if current_window.objects[current_object][1][int(line)] != "": current_window.objects[current_object][1][int(line)] = current_window.objects[current_object][1][int(line)][:-1]
                            else:
                                if line != 0:
                                    current_window.objects[current_object][1].pop(int(line))
                                    line -= 1
                                    current_window.objects[current_object][6] = line

                        except:pass
                    elif current_object != "" and event.key == pg.K_DOWN:
                        try:
                            if current_window.objects[current_object][1][int(line)] != current_window.objects[current_object][1][-1]:
                                line += 1
                                current_window.objects[current_object][6] = line
                        except:pass
                    elif current_object != "" and event.key == pg.K_UP:
                        if line != 0:
                            line -= 1
                            current_window.objects[current_object][6] = line
                    elif current_object != "" and event.key == pg.K_ESCAPE:current_object = ""
                    elif current_object != "" and event.key == pg.K_RETURN:
                        line += 1
                        current_window.objects[current_object][1].insert(line, "")
                        current_window.objects[current_object][6] = line
                    elif current_object != "":current_window.objects[current_object][1][int(line)] += event.unicode
        elif clicked:
            mouse_x = pos[0]
            mouse_y = pos[1]
            cannot_reselect = False
            if len(apps) >= 5:
                button_size_x = (win_size[0] - 190) /len(apps)
            else:
                button_size_x = (win_size[0] - 190) /4
            if mouse_x >= win_size[0] - 90 and mouse_x <= win_size[0] and mouse_y >= win_size[1]-50 and mouse_y <= win_size[1]-25 and mode == "work":
                cycle = 0
                tick = 0
                mode = "reboot"
                apps = [apps[0]]
            elif mouse_x >= win_size[0] - 90 and mouse_x <= win_size[0] and mouse_y >= win_size[1]-25 and mouse_y <= win_size[1] and mode == "work":
                cycle = 0
                tick = 0
                mode = "shutdown"
                apps = [apps[0]]
            else:
                for program_id in range(len(apps)+1):
                    if mouse_x >= 90+(button_size_x*(program_id-1)) and mouse_x <= int(90 +(button_size_x*program_id)) and mouse_y >= win_size[1]-50 and mouse_y <= win_size[1]-25 and mode == "work":
                        current_appslot = program_id-1
                        current_window = apps[program_id-1]
                        current_object = ""
                        apps[program_id-1].hidden = False                
            if not current_window.hidden:
                for obj_id in range(len(current_window.objects)):
                    obj = current_window.objects[obj_id]
                    obj_type = obj[0]
                    x = obj[2] + current_window.x
                    y = obj[3] + current_window.y
                    size_x = obj[4]
                    size_y = obj[5]
                    if mouse_x >= x and mouse_x <= x + size_x and mouse_y >= y and mouse_y <= y + size_y and not current_window.hidden and not window_moving:
                        if obj[0] == "button" or obj[0] == "label":
                            for funct in current_window.functions[obj_id]:
                                if "fetch" in funct:
                                    if platform.system() != "Windows":
                                        args_fixed = fetchapp("/" + funct[6:])
                                    else:
                                        args_fixed = fetchapp("\\" + funct[6:])
                                    if len(apps) != -1:
                                        apps.append(Window(args_fixed[0], args_fixed[1], args_fixed[2], args_fixed[3], args_fixed[4], args_fixed[5], args_fixed[6], args_fixed[7], args_fixed[8], args_fixed[9], args_fixed[10], args_fixed[11],args_fixed[12]))
                                        current_appslot = len(apps)-1
                                        current_window = apps[-1]
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
            if mouse_x >= current_window.x + 2 and mouse_x <= current_window.x + 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32 and not busy and not current_window.hidden and current_window.hidable and not window_moving:
                current_window.hidden = True
                cannot_reselect = True
            elif mouse_x <= current_window.x + current_window.size_x - 2 and mouse_x >= current_window.x + current_window.size_x - 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32 and current_window.closable and not busy and not current_window.hidden:
                apps.pop(current_appslot)
                current_appslot = 0
                current_window = apps[0]
            elif mouse_x >= current_window.x and mouse_x <= current_window.x + current_window.size_x and mouse_y >= current_window.y and mouse_y <= current_window.y + 40 and not busy and not(mouse_x >= current_window.x + 2 and mouse_x <= current_window.x + 32 and mouse_y >= current_window.y + 2 and mouse_y <= current_window.y + 32) and not current_window.hidden:
                window_moving = True
            if not cannot_reselect:
                for search_window_id in range(len(apps)):
                    search_window = apps[search_window_id]
                    do_break = False
                    if mouse_x >= search_window.x and mouse_x <= search_window.x + search_window.size_x and mouse_y >= search_window.y and mouse_y <= search_window.y + search_window.size_y and search_window_id != current_appslot and not search_window.hidden and not(mouse_x >= current_window.x and mouse_x <= current_window.x +current_window.size_x and mouse_y >= current_window.y and mouse_y <= current_window.y + current_window.size_y and window_moving):
                        current_window = search_window
                        current_appslot = search_window_id
                        current_object = ""
                        do_break = True
                    if do_break:
                        break
            cannot_reselect = False
    clock.tick(30)
    tick += 1
    crt_tick += 3
    apps[current_appslot] = current_window
    if not window_moving:
        window_indent = -1
    if crt_tick >= win_size[1] +30:
        crt_tick = -31
    if tick == 31:
        tick = 0
        cycle += 1
    if window_moving:
        current_window.x = int(mouse_x - current_window.size_x/2)
        current_window.y = mouse_y - 17        
    if cycle == 0 and tick == 1 and mode == "startup":
        apps[0] = Window(window, win_size[1], VERSION_NAMED, int((win_size[0]-300)/2), int((win_size[1]-170)/2), [["label", "Booting up...", 50, 80, 100, 50]], 300, 170, False, True, False)
        current_window = apps[0]
        current_appslot = 0
        busy = True
    elif cycle == 3 and tick == 1:
        busy = False
        if mode == "shutdown":
            is_working = False
            cycle = 0
            tick = 0
        elif mode == "startup":
            mode = "work"
            apps[0] = Window(window, win_size[1], "fFiles " + VERSION, 10, 10, [["checkbox",False,190,204,15,15]], 300, 235, True, True, False, [["", ""]], ("""indent_x = 0\nindent_y = 0\nfiles = os.listdir()\nself.objects = [self.objects[0],["label","Delete:",120,200,0,0]]\nself.functions = [['',''],["",""]]\nfor file_id in range(len(files)):\n    if file_id % 10 == 0 and file_id != 0:\n        indent_x +=1\n        indent_y = 0\n    file = files[file_id]\n    if len(file) >= 14:\n        file = file[:3]+'~'+file[-5:]\n    if os.path.isdir(files[file_id]):\n        self.objects.append(('label','['+str(file)+']',10+(140*indent_x),40+(15*indent_y),len('['+str(file)+']')*10,20))\n    else:\n        self.objects.append(('label',file,10+(140*indent_x),40+(15*indent_y),len(str(file))*10,20))\n    if self.objects[0][1] and os.path.isdir(files[file_id]):\n      self.functions.append(("shutil.rmtree('"+files[file_id]+"')",""))\n    if self.objects[0][1]:\n      self.functions.append(("os.remove('"+files[file_id]+"')",""))\n    elif file[-5:] == '.exec':\n        self.functions.append(('fetch '+str(files[file_id]),''))\n    elif os.path.isdir(files[file_id]):\n        self.functions.append(('os.chdir("'+path+str(files[file_id])+'")',''))\n    else:\n        self.functions.append(('',''))\n    indent_y +=1\nself.objects.append(('label','Go to:',10,200,60,20))\nself.functions.append(('',' '))\nself.objects.append(('label','/',75,200,20,20))\nself.functions.append(('os.chdir(disk_root)',''))\nif os.getcwd() != disk_root:\n    self.objects.append(('label','..',90,200,20,20))\n    self.functions.append(( 'os.chdir("..")',''))\nself.objects.append(('label','Root:'+str(path[len(disk_root):]),10,213,20,20))\nself.functions.append(('',''))""", ""))
            current_window = apps[0]
            current_appslot = 0
        elif mode == "reboot":
            mode = "blackscreen"
            cycle = 0
            tick = 0
            apps[0] =  ""
            current_window = apps[0]
    if cycle == 0 and tick == 1 and mode == "shutdown":
        apps[0] = Window(window, win_size[1], VERSION_NAMED, int((win_size[0]-300)/2), int((win_size[1]-170)/2),[["label", "Shutting down...", 50, 80, 100, 50]], 300, 170, False, True, False)
        current_window = apps[0]
        busy = True
        current_appslot = 0
    elif cycle == 0 and tick == 1 and mode == "reboot":
        apps[0] =  Window(window, win_size[1], VERSION_NAMED, int((win_size[0]-300)/2), int((win_size[1]-170)/2), [["label", "Rebooting...", 50, 80, 100, 50]], 300, 170, False, True, False)
        current_window = apps[0]
        busy = True
        current_appslot = 0
    elif cycle == 1 and mode == "blackscreen":
        mode = "startup"
        cycle = 0
        tick = 0
        current_appslot = 0
    if mode != "blackscreen":
        window.fill((1,130,129))
        if display_prefs[2]:fill_background(str(path_folder+display_prefs[1]), win_size[0], win_size[1], window)
        else:
            try:
                image_gui_background = pg.image.load(path_folder+display_prefs[1])
                window.blit(pg.transform.scale(image_gui_background, win_size), (0,0))
            except:pass
    else:
        window.fill((0,0,0))
    for selected_window in apps:
        try:
            if selected_window.hidden:
                pass
            else:
                selected_window.redraw()
        except:
            pass
    if mode == "work":
        appbuttons = []
        if len(apps) >= 5:
            button_size_x = (win_size[0] - 190) /len(apps)
        else:
            button_size_x = (win_size[0] - 190) /4
        for app_id in range(len(apps)):
            try:
                appslot = apps[app_id]
                named_app_id = str(app_id +1)
                indent_x = 100+(button_size_x *app_id)
                title = appslot.title
                button = ["button", named_app_id+" "+title[:int(button_size_x/10)], indent_x, 2, button_size_x , 25]
                appbuttons.append(button)
            except:pass
        appbuttons = [["label", "FinalStep", 5, 5, 100, 50],["label", VERSION, 3, 20, 100, 50],["button", "Reboot", win_size[0]-90, 2, 90, 25],["button", "Shutdown", win_size[0]-90, 27, 90, 25]]+appbuttons
        dock_window = Window(window, win_size[1], "", 0, win_size[1]-50, appbuttons, win_size[0], 50, False, False, False,[],("",""),LIGHTGRAY,False)
        dock_window.redraw()            
    try:
        if current_window.hidden:
            pass
        else:
            current_window.redraw()
    except:
        pass
    if pg.mouse.get_focused():
        pos = pg.mouse.get_pos()
        if window_moving:
            path_cursor = path_folder + "/gui/cursor_move.png"
            gui_cursor = pg.image.load(path_cursor)
            window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
            if not clicked:
                window_moving = False  
        elif busy:
            if tick <= 30 and tick >= 21:
                path_cursor = path_folder + "/gui/cursor_busy2.png"
                gui_cursor = pg.image.load(path_cursor)
                window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
            elif tick <= 20 and tick >= 11:
                path_cursor = path_folder + "/gui/cursor_busy1.png"
                gui_cursor = pg.image.load(path_cursor)
                window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
            else:
                path_cursor = path_folder + "/gui/cursor_busy0.png"
                gui_cursor = pg.image.load(path_cursor)
                window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
        else:
            path_cursor = path_folder + "/gui/cursor.png"
            gui_cursor = pg.image.load(path_cursor)
            window.blit(gui_cursor, (pos[0] - 10, pos[1] - 10))
    if display_prefs[0]:
        window.blit(pg.transform.scale(crt_overlay2, win_size), (0, 0))
        window.blit(pg.transform.scale(crt_overlay1, (win_size[0],30)), (0, crt_tick))        
    pg.display.update()
