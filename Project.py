# -*- coding: utf-8 -*-
# @Author: Nonp.znn
# @Date:   2017-04-06 15:09:08
# @Last Modified by:   Nonp.znn
# @Last Modified time: 2017-04-07 17:39:22

import pygame
import random

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
            
class Sceen(object):

    def __init__(self, width=640, height=400, fps=30):
        pygame.init()
        pygame.display.set_caption("Guess")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.font = pygame.font.SysFont('mono', 20, bold=True)
        self.white = (255,255,255)
        self.howto = pygame.image.load("Image\howto.jpg")
        self.answer = pygame.image.load("Image\0.jpg")
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
        pygame.mixer.music.load("Darkest_Child_A.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()                     
            self.screen.blit(self.howto,(0,0))
            self.text_screen("", 150, 50, self.black)
            self.button(self.b_green, self.green, 250, 530, 100, 50, "Next", "Next")
            self.button(self.b_red, self.red, 450, 530, 100, 50, "Quit", "Quit")
            pygame.display.update()
        if self.put_number:
            self.put_number_screen()
    # หน้าใส่ตัวเลข
    def put_number_screen(self):
        pygame.mixer.music.load("Day_Of_Recon.mp3")
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
            self.screen.fill(self.white)
##            self.screen.blit(self.howto,(0,0))
            self.text_screen(str(self.number_input), 100, 50, self.black)
            self.button(self.b_green, self.green, 250, 500, 100, 50, "Start", "Start")
            self.button(self.b_red, self.red, 450, 500, 100, 50, "Back", "Back")
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
            self.screen.fill(self.white)
##            self.screen.blit(self.howto,(0,0))
            if self.i < guess.box:
                self.height = 400
                a = list(map(str, guess.show(self.random_box[self.i])))
                num = 0
                for j in range(guess.length):
                    if num < 10:
                        self.use += str(a[j])
                        self.use += " "
                        num += 1
                    else:
                        self.draw_text(self.use, self.black)
                        self.use = ""
                        self.use += str(a[j])
                        self.use += " "
                        num = 1
                        self.height += 400
                self.draw_text(self.use, self.black)
                self.use = ""                    
                self.button(self.b_green, self.green, 650, 100, 100, 50, "Yes", "Yes")
                self.button(self.b_red, self.red, 650, 300, 100, 50, "No", "No")
            else:
                self.last("Your number is %s" %str(guess.sent_AI(self.list)))  # output
                self.number_run = False
            pygame.display.update()
        self.last_seen(str(guess.sent_AI(self.list)))
    # หน้าจบ
    def last_seen(self, text):
        x = 0
        while self.last:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.blit(self.answer,(0,0))
            clock = pygame.time.wait(30)
            self.draw_text(text, self.white)
            self.button(self.b_green, self.green, 250, 500, 100, 50, "MainMenu", "MainMenu")
            self.button(self.b_red, self.red, 450, 500, 100, 50, "Quit", "Quit")
            pygame.display.update()
        self.put_number_screen()
    # ตัวหนังสือ
    def text_screen(self, text, width, height, color):
        surface_text = self.font.render(text, True, color)
        self.screen.blit(surface_text, (width, height))
    # ตัวเลขตัวเลขที่ซุ่ม
    def draw_text(self, text, color):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 20))
    # ปุ่ม
    def button(self, color_button_1, color_button_2, width, height, width_p, height_p, action, text_1): 
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if width <= mouse[0] <= width + width_p and height <= mouse[1] <= height + height_p:
            pygame.draw.rect(self.screen, color_button_1, (width, height, width_p, height_p))            
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
        else:
            pygame.draw.rect(self.screen, color_button_2, (width, height, width_p, height_p))
        self.text_screen(text_1, (width+(width_p//4)), (height+(height_p//3)), self.black)

if __name__ == '__main__':
    Sceen(800, 600).run()
