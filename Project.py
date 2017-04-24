#!/usr/bin/env python3

import pygame
import random
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
        if self.ai == 0:
            self.ai = 'The number you have in mind are not in the input range.'
            
class Sceen(object):

    def __init__(self, width=640, height=400, fps=30):
        pygame.init()
        pygame.display.set_caption("Guess")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
##        self.font = pygame.font.SysFont("CHILLER", 90, bold=True)
        self.white = (255,255,255)
        self.background = read_folder("Image", ".jpg")
        self.icon_bottom = read_folder("Image", ".png")
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
        self.put_number = False
        self.number_run = False
        self.last = True
        self.number_input = ""
        self.back = True
    # หน้า How to play
    def run(self):
        pygame.mixer.music.load("Song\Darkest_Child_A.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()                     
            self.screen.blit(pygame.image.load(self.background[0]),(0,0))#x = 246 y = 42 
            self.screen.blit(pygame.image.load(self.icon_bottom[3]),(100,485))
            self.screen.blit(pygame.image.load(self.icon_bottom[7]),(447,485))
            self.button(100, 485, 246, 42, "Next", pygame.image.load(self.icon_bottom[2]))
            self.button(447, 485, 246, 42, "Quit", pygame.image.load(self.icon_bottom[6]))
            pygame.display.update()
        if self.put_number:
            self.put_number_screen()
    # หน้าใส่ตัวเลข
    def put_number_screen(self):
        self.font = pygame.font.SysFont("CHILLER", 90, bold=True)
        pygame.mixer.music.load("Song\Day_Of_Recon.mp3")
        pygame.mixer.music.play(-1)
        while self.put_number:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.number_input = self.number_input[:-1]
                    else:
                        if event.unicode.isdigit():
                            self.number_input = self.number_input + event.unicode
            self.screen.blit(pygame.image.load(self.background[1]),(0,0))
            self.screen.blit(pygame.image.load(self.icon_bottom[9]),(100,450))
            self.screen.blit(pygame.image.load(self.icon_bottom[1]),(447,450))
            font_center = (478 - self.font.size(self.number_input)[0]) // 2
            self.text_screen(str(self.number_input), font_center + 164, 260, self.black)
            self.button(100, 450, 246, 42, "Start", pygame.image.load(self.icon_bottom[8]))
            self.button(447, 450, 246, 42, "Back", pygame.image.load(self.icon_bottom[0]))
            if self.back is False:
                if self.put_number == False and self.number_input == "":
                    self.put_number = True
            pygame.display.update()
        if self.running:
            self.run()
        else:
            self.number()
    # หน้าแสดวงตัวเลขแล้วกด Y/N
    def number(self):
        pygame.mixer.music.load("Song\Colorless_Aura.mp3")
        pygame.mixer.music.play(-1)
        guess = random_number(int(self.number_input)) # input
        self.random_box = [i for i in range(guess.box)]
        random.shuffle(self.random_box)
        self.list = [0] * guess.box
        while self.number_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()   
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
                self.screen.blit(pygame.image.load(self.icon_bottom[11]),(100,450))
                self.screen.blit(pygame.image.load(self.icon_bottom[5]),(447,450))
                self.button(100, 450, 246, 42, "Yes", pygame.image.load(self.icon_bottom[10]))
                self.button(447, 450, 246, 42, "No", pygame.image.load(self.icon_bottom[4]))
            else:
                self.number_run = False
            pygame.display.update()
        self.last_seen(str(guess.sent_AI(self.list)))
    # หน้าจบ
    def last_seen(self, text):
        self.font = pygame.font.Font("CHILLER.TTF", 90)
        while self.last:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.blit(pygame.image.load(self.background[4]),(0,0))
            out_put = (220 - self.font.size(text)[0]) // 2
            self.text_screen(text, out_put + 290, 286, self.black) # ตำแหน่ง out put
            clock = pygame.time.wait(30)
            self.screen.blit(pygame.image.load(self.icon_bottom[13]),(100,490))
            self.screen.blit(pygame.image.load(self.icon_bottom[7]),(447,490))
            self.button(100, 490, 246, 42, "MainMenu", pygame.image.load(self.icon_bottom[12]))
            self.button(447, 490, 246, 42, "Quit", pygame.image.load(self.icon_bottom[6]))
            pygame.display.update()
        self.put_number_screen()
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
    def button(self, width, height, width_p, height_p, action, new_button): 
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if width <= mouse[0] <= width + width_p and height + 38 <= mouse[1] <= height + height_p + 38:
            self.screen.blit(new_button, (width,height))            
            if click[0] == 1:
                if action == "Next":
                    self.running = False
                    self.put_number = True
                    self.back = False
                    clock = pygame.time.wait(150)
                elif action == "Back":
                    self.running = True
                    self.put_number = False
                    self.back = True
                    clock = pygame.time.wait(150)
                elif action == "Start":
                    self.last = True
                    self.put_number = False
                    self.number_run = True
                    clock = pygame.time.wait(150)
                elif action == "No":
                    self.no += 1
                    self.i += 1
                    clock = pygame.time.wait(150)
                elif action == "Yes":
                    self.list[self.random_box[self.i]] = 1
                    self.yes += 1
                    self.i += 1
                    clock = pygame.time.wait(150)
                elif action == "MainMenu":
                    self.last = False
                    self.put_number = True
                    self.number_run = False
                    self.number_input = ""
                    self.no = 0
                    self.yes = 0
                    self.i = 0
                    self.list = []
                    clock = pygame.time.wait(150)
                elif action == "Quit":
                    pygame.quit()
                    quit()
##        else:
##            self.screen.blit(pygame.image.load(self.icon_bottom[1]),(width,height))
    

if __name__ == '__main__':
    Sceen(800, 600).run()
