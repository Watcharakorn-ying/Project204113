#!/usr/bin/env python3

import pygame
import random
import threading
from read_folder import *

class group:

    def __init__(self, at, num, n=None):
        self.position = at
        self.number = num
        self.next = n
        

    def get_next(self):
        return self.next

    def set_next(self, n):
        self.next = n

    def get_number(self):
        return self.number

class random_number(object):
    
    def __init__(self,num):
        self.root = []
        self.length = 0
        
        for i in self.add(num):
            if self.root[i.position] == None:
                self.root[i.position] = i
                if self.length == 0:
                    self.length = 1
                    
                continue
            else: curr = self.root[i.position]
            mlength = 1
            while curr.get_next():
                mlength += 1
                curr = curr.get_next()
            mlength += 1
            curr.set_next(i)
            if self.length < mlength:
                self.length = mlength
        self.check_length(num)

    def add(self,num):
        generater = (((((num * 80) + 1) * 250) - 250) // 2) // (10**4)
        binary = bin(num)[2:]
        self.box = len(binary)
        for create in range(self.box):
            self.root.append(None)
        for i in range(1,generater+1):
            count = 0
            change = bin(i)[2:][::-1]
            for b in change:
                if b == '1':
                    yield group(count,i)
                count += 1
    def show(self, at):
        curr = self.root[at]
        while curr:
            yield curr.get_number()
            curr = curr.get_next()
    def check_length(self,num):
        count_box = 0
        for box in self.root:
            length_box = 1
            while box.get_next():
                length_box += 1
                box = box.get_next()
            if length_box != self.length:
                distance = self.length - length_box
                self.add_random(num,count_box,distance)
            count_box += 1
    def add_random(self,num,box,distance):
        curr_box = self.root[box]
        for r in range(distance,0,-1):
            while curr_box.get_next():
                curr_box = curr_box.get_next()
            while True:
                num += 1
                change = bin(num)[2:][::-1]
                if change[box] == '1':
                    ran_num = group(box,num)
                    curr_box.set_next(ran_num)
                    break
    def sent_AI(self, ls):
        self.data = AI(ls)
        return self.data.ai

class AI:

    def __init__(self, ls):
        self.ai = 0
        self.kd = 1
        self.match = []
        count = 0
        for x in ls:
            if (x != 0) and (count not in self.match):
                self.match.append(count)
            count += 1
        for cal in self.match:
            self.ai += (self.kd << cal)
            
class Screen(threading.Thread):

    def __init__(self, width=640, height=400, fps=30):
        threading.Thread.__init__(self)
        pygame.init()
        pygame.display.set_caption("Guess")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.white = (255,255,255)
        self.background = read_folder("Image", ".jpg")
        self.icon_bottom = read_folder("Image", ".png")
        self.witch_sound = pygame.mixer.Sound("Song\witch.wav")
        self.button_a = pygame.mixer.Sound("Song\\01_button_sound.wav")
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.b_red = (255, 0, 51)
        self.green = (0,200,0)
        self.b_green = (51, 255, 0)
        self.red = (255,0,0)      
        self.use = ""
        self.no = 0
        self.yes = 0
        self.i = 0
        self.list = []
        self.running = True
        self.back = False
        self.Provider = False
        self.References = False
        self.number_input = ""
    # หน้าเริ่มโปรแกรม
    def run(self):
        pygame.mixer.music.load("Song\Darkest_Child_A.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
            self.screen.blit(pygame.image.load(self.background[5]),(0,0))
            self.button(100, 487, 246, 42, "References", pygame.image.load(self.icon_bottom[17]), pygame.image.load(self.icon_bottom[16]))
            self.button(470, 240, 246, 42, "Next", pygame.image.load(self.icon_bottom[3]), pygame.image.load(self.icon_bottom[2]))
            self.button(470, 340, 246, 42, "Provider", pygame.image.load(self.icon_bottom[15]), pygame.image.load(self.icon_bottom[14]))
            self.button(470, 440, 246, 42, "Quit", pygame.image.load(self.icon_bottom[7]), pygame.image.load(self.icon_bottom[6]))
            pygame.display.update()
        self.running = True
        if self.Provider:
            self.Provider_screen()
        elif self.References:
            self.References_screen()
        elif self.Provider is False and self.References is False:
            self.how_to()
    # หน้ารายชื่อคนทำ
    def Provider_screen(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
            self.screen.blit(pygame.image.load(self.background[7]),(0,0))
            self.button(273, 485, 246, 42, "Back", pygame.image.load(self.icon_bottom[1]),  pygame.image.load(self.icon_bottom[0]))
            pygame.display.update()
        self.running = True
        self.run()
    # หน้าอ้างอิง 1
    def References_screen(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
            self.screen.blit(pygame.image.load(self.background[8]),(0,0))
            self.button(447, 485, 246, 42, "Next", pygame.image.load(self.icon_bottom[3]), pygame.image.load(self.icon_bottom[2]))
            self.button(100, 485, 246, 42, "Back", pygame.image.load(self.icon_bottom[1]),  pygame.image.load(self.icon_bottom[0]))
            pygame.display.update()         
        self.running = True
        if self.back:
            self.run()
        else:
            self.References_screen_2()
    # หน้าอ้างอิง 2
    def References_screen_2(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
            self.screen.blit(pygame.image.load(self.background[9]),(0,0))
            self.button(100, 485, 246, 42, "Back", pygame.image.load(self.icon_bottom[1]),  pygame.image.load(self.icon_bottom[0]))
            self.button(447, 485, 246, 42, "MainManu", pygame.image.load(self.icon_bottom[13]), pygame.image.load(self.icon_bottom[12]))
            pygame.display.update()
        self.running = True
        self.References_screen()        
    # หน้า How to play
    def how_to(self):
        pygame.mixer.music.load("Song\Day_Of_Recon.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()                    
            self.screen.blit(pygame.image.load(self.background[0]),(0,0))#x = 246 y = 42 
            self.button(100, 485, 246, 42, "Next", pygame.image.load(self.icon_bottom[3]), pygame.image.load(self.icon_bottom[2]))
            self.button(447, 485, 246, 42, "Back", pygame.image.load(self.icon_bottom[1]),  pygame.image.load(self.icon_bottom[0]))
            pygame.display.update()
        self.running = True
        if self.back:
            self.run()
        else:
            self.put_number_screen()
    # หน้าใส่ตัวเลข
    def put_number_screen(self):
        self.font = pygame.font.SysFont("CHILLER", 90, bold=True)
        pygame.mixer.music.load("Song\Colorless_Aura.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.number_input = self.number_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            self.number_input = self.number_input + event.unicode
                            if self.number_input != "":
                                if int(self.number_input) == 0:
                                    self.number_input = ""
                                elif int(self.number_input) > 127:
                                    if len(self.number_input) > 3:
                                        self.number_input = self.number_input[:3]
                                    else:
                                        self.number_input = self.number_input[:2]
            self.screen.blit(pygame.image.load(self.background[1]),(0,0))
            font_center = (478 - self.font.size(self.number_input)[0]) // 2
            self.text_screen(str(self.number_input), font_center + 164, 260, self.black)
            self.button(100, 450, 246, 42, "Next", pygame.image.load(self.icon_bottom[9]), pygame.image.load(self.icon_bottom[8]))
            self.button(447, 450, 246, 42, "Back", pygame.image.load(self.icon_bottom[1]),  pygame.image.load(self.icon_bottom[0]))
            if self.back is False:
                if self.running is False and self.number_input == "":
                    self.running = True
            pygame.display.update()
        self.running = True
        if self.back:
            self.how_to()
        else:
            self.number()
    # หน้าแสดวงตัวเลขแล้วกด Y/N
    def number(self):
        guess = random_number(int(self.number_input)) # input
        self.random_box = [i for i in range(guess.box)]
        random.shuffle(self.random_box)
        self.list = [0] * guess.box
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()   
            self.screen.blit(pygame.image.load(self.background[2]),(0,0))
            if self.i < guess.box:
                self.height = 2500
                a = list(map(str, guess.show(self.random_box[self.i])))
                num = 0
                for j in range(guess.length):
                    if num < 10:
                        self.use += str(a[j])
                        self.use += "  "
                        num += 1
                    else:
                        self.draw_text(self.use, self.black)
                        self.use = ""
                        self.use += str(a[j])
                        self.use += "  "
                        num = 1
                        self.height += 700
                self.draw_text(self.use, self.black)
                self.use = ""
                self.button(100, 450, 246, 42, "Yes", pygame.image.load(self.icon_bottom[11]), pygame.image.load(self.icon_bottom[10]))
                self.button(447, 450, 246, 42, "No", pygame.image.load(self.icon_bottom[5]), pygame.image.load(self.icon_bottom[4]))
            else:
                self.running = False
            pygame.display.update()
        self.running = True
        pygame.mixer.music.pause()
        self.last_seen(str(guess.sent_AI(self.list)))
    # หน้าจบ
    def last_seen(self, text):
        pygame.mixer.Sound.play(self.witch_sound)
        pygame.mixer.music.load("Song\Guess_Who.mp3")
        pygame.mixer.music.play(-1)
        witch = pygame.image.load(self.background[3]).convert()
        pic = witch.get_rect()
        i = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
            witch.set_alpha(i)
            self.screen.blit(witch, pic)
            if i != 350 :
                i += 5
            else:
                break
            pygame.display.update()
            pygame.time.delay(50)
        if text != '0':
            self.font = pygame.font.Font("CHILLER.TTF", 90)
            i = 0
            label = self.font.render(text,1,(255,255,255))
            fade = pygame.Surface(self.font.size(text))
            fade.set_colorkey((0,0,0))
            fade.blit(label,(0,0))
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_function()
                fade.set_alpha(i)
                self.screen.blit(pygame.image.load(self.background[4]),(0,0))
                out_put = (220 - self.font.size(text)[0]) // 2
                self.screen.blit(fade, (out_put + 290,236))
                clock = pygame.time.wait(30)
                self.button(100, 490, 246, 42, "NewGame", pygame.image.load(self.icon_bottom[19]), pygame.image.load(self.icon_bottom[18]))
                self.button(447, 490, 246, 42, "Quit", pygame.image.load(self.icon_bottom[7]), pygame.image.load(self.icon_bottom[6]))
                if i != 380:
                    i += 10 # ความเร็วตอนเฟด
                pygame.display.update()
                pygame.time.delay(1) # ความสมูท
        else:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_function()
                self.screen.blit(pygame.image.load(self.background[6]),(0,0))
                self.button(100, 490, 246, 42, "NewGame", pygame.image.load(self.icon_bottom[19]), pygame.image.load(self.icon_bottom[18]))
                self.button(447, 490, 246, 42, "Quit", pygame.image.load(self.icon_bottom[7]), pygame.image.load(self.icon_bottom[6]))
                pygame.display.update()
    # ฟังก์ชันหยุด
    def quit_function(self):
        pygame.mixer.music.pause()
        pygame.quit()
        quit()            
    # ตัวหนังสือ
    def text_screen(self, text, width, height, color):
        self.font = pygame.font.Font("CHILLER.TTF", 90)
        surface_text = self.font.render(text, True, color)
        self.screen.blit(surface_text, (width, height))
    # ตัวเลขตัวเลขที่ซุ่ม
    def draw_text(self, text, color):
        self.font = pygame.font.Font("CHILLER.TTF", 30)
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 20))
    # ปุ่ม
    def button(self, width, height, width_p, height_p, action, b_new_button, a_new_button): 
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if width <= mouse[0] <= width + width_p and height + 38 <= mouse[1] <= height + height_p + 38:
            self.screen.blit(a_new_button, (width,height))
            if click[0] == 1:
                pygame.mixer.Sound.play(self.button_a)
                if action == "Next":
                    self.running = False
                    self.back = False
                    clock = pygame.time.wait(300)
                elif action == "References":
                    self.running = False
                    self.References = True
                    clock = pygame.time.wait(300)
                elif action == "Back":
                    self.running = False
                    self.back = True
                    self.Provider = False
                    self.Provider = False
                    self.References = False
                    clock = pygame.time.wait(300)
                elif action == "No":
                    self.no += 1
                    self.i += 1
                    clock = pygame.time.wait(300)
                elif action == "Yes":
                    self.list[self.random_box[self.i]] = 1
                    self.yes += 1
                    self.i += 1
                    clock = pygame.time.wait(300)
                elif action == "NewGame":
                    self.use = ""
                    self.no = 0
                    self.yes = 0
                    self.i = 0
                    self.list = []
                    self.running = True
                    self.back = False
                    self.Provider = False
                    self.References = False
                    self.number_input = ""
                    self.put_number_screen()
                elif action == "Provider":
                    self.running = False
                    self.Provider = True
                    clock = pygame.time.wait(300)
                elif action == "MainManu":
                    self.running = True
                    self.back = False
                    self.Provider = False
                    self.References = False
                    self.run()
                    clock = pygame.time.wait(300)
                elif action == "Quit":
                    self.quit_function()
        else:
            self.screen.blit(b_new_button, (width,height))

def main():
    t1 = Screen(800, 600)
    t1.start()
    print('start')
    

if __name__ == '__main__':
    main()
