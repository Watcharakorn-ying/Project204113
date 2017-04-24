#!/usr/bin/env python3

import time
import pygame
import pyaudio
import audioop
import wave
import random
import threading
import speech_recognition as sr
from gtts import gTTS
import mp3
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
        return str(self.data.ai)

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
    """ 
    ############################################################
    ################            Setup           ################
    ############################################################
    """
    def __init__(self, width=640, height=400, fps=30):
        threading.Thread.__init__(self)
        pygame.init()
        pygame.display.set_caption("Guess")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.blue = (0,0,255)
        self.use = ""
        self.no = 0
        self.yes = 0
        self.i = 0
        self.list_box = []
        self.running = True
        self.back = False
        self.Provider = False
        self.References = False
        self.listen_command, self.listen_num = False,False
        self.number_input = ""
        self.background = read_folder("Image", ".jpg")
        self.icon_bottom = read_folder("Image", ".png")
        self.voice_simon = read_folder("sound_simon", ".wav") #['understand.wav','Siri1.wav','Siri2.wav','talk_num.wav']
        self.image_simon = read_folder("simon", ".jpeg")
        self.witch_sound = pygame.mixer.Sound("Song\witch.wav")
        self.button_a = pygame.mixer.Sound("Song\\01_button_sound.wav")
    """ 
    ############################################################
    ################            Start           ################
    ############################################################
    """
    def run(self):
        pygame.mixer.music.load("Song\Darkest_Child_A.mp3")
        pygame.mixer.music.set_volume(0.5)
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
##        elif self.Provider is False and self.References is False:
##            self.how_to()
        else:
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
        global simon_done
        self.font = pygame.font.SysFont("CHILLER", 90, bold=True)
        pygame.mixer.music.load("Song\Colorless_Aura.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        while self.running:
            try:
                if recognize == 'หวัดดีไซมอน' or recognize.find('ไซมอน') >= 0 or recognize.find('ไซม่อน') >= 0:
                    simon_done = False
                    self.start_anime = True
                    self.simon_anime()
                    self.listen_command = False
                else:Error
            except:
                pass
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
        global simon_done
        guess = random_number(int(self.number_input)) # input
        self.random_box = [i for i in range(guess.box)]
        random.shuffle(self.random_box)
        self.list_box = [0] * guess.box
        while self.running:
            try:
                if recognize == 'หวัดดีไซมอน' or recognize.find('ไซมอน') >= 0 or recognize.find('ไซม่อน') >= 0:
                    simon_done = False
                    self.start_anime = True
                    self.simon_anime()
                    self.listen_command = False
                else:Error
            except:
                pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
            self.screen.blit(pygame.image.load(self.background[2]),(0,0))
            if self.i < guess.box:
                self.height = 2500
                a = list(map(str, guess.show(self.random_box[self.i])))
                num = 0
                if self.listen_command:
                    self.t2 = threading.Thread(target=self.simon_yes_no)
                    self.t2.start()
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
                pygame.display.update()
            else:
                self.running = False
            pygame.display.update()
        self.running = True
        pygame.mixer.music.pause()
        self.last_seen(str(guess.sent_AI(self.list_box)))

    # หน้าจบ
    def last_seen(self, text):
        self.t1 = threading.Thread(target=simon)
        self.t1.start()
        pygame.mixer.Sound.play(self.witch_sound)
        pygame.mixer.music.load("Song\Guess_Who.mp3")
        pygame.mixer.music.set_volume(1)
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
                    self.References = False
                    clock = pygame.time.wait(300)
                elif action == "No":
                    self.no += 1
                    self.i += 1
                    clock = pygame.time.wait(300)
                elif action == "Yes":
                    self.list_box[self.random_box[self.i]] = 1
                    self.yes += 1
                    self.i += 1
                    clock = pygame.time.wait(300)
                elif action == "NewGame":
                    self.use = ""
                    self.no = 0
                    self.yes = 0
                    self.i = 0
                    self.list_box = []
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

    """ 
    ############################################################
    ################    AI Simon assistant      ################
    ############################################################
    """
    def simon_wave(self):
##        print('wave')
        self.CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        p = pyaudio.PyAudio()
        self.stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=self.CHUNK)
        clock=pygame.time.Clock()
        self.margin = 20
        self.samples_per_section = self.width//3 - 2*self.margin
        self.sound_tracks = [[0]*self.samples_per_section]*3
        self.max_value = [0]*3
        self.current_section = 0
        while self.wave_done:
            
            total = 0
            for i in range(0,2):
                data=self.stream.read(self.CHUNK)
                if True:
                    reading=audioop.max(data, 2)
                    total=total+reading
                time.sleep(.0001)
            total=total/100
##            print(total)
            self.screen.blit(pygame.image.load(self.image_simon[self.start_img_simon]), (0,0))
            
            self.sound_tracks[self.current_section] = self.sound_tracks[self.current_section][1:] + [total]
            self.max_value[self.current_section] = max(self.max_value[self.current_section], total)
            for t in range(1):
                sectionx = t*self.width/3 + self.margin
                for j in range(0,self.width//3 - 2*self.margin):
                    x = j + sectionx
                    y = self.height - self.sound_tracks[t][j]
##                    print(self.sound_tracks[t][j])
                    pygame.draw.rect(self.screen,self.blue,(x, y, 1, self.sound_tracks[t][j]))
            pygame.display.flip()

    def simon_anime(self):
        global T_wave
        pygame.time.wait(1000)
        pygame.mixer.music.pause()
        self.sound(8)
        self.start_img_simon = 0
        self.previous = False
        alpha = 30
        while self.start_anime:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_function()
            image = pygame.image.load(self.image_simon[self.start_img_simon]).convert()
            rect = image.get_rect()
            image.set_alpha(alpha)
            self.screen.blit(image, rect)
            if alpha != 50:
                alpha += 1
            if self.start_img_simon == 260:
                if self.command_ == 'ใส่ตัวเลขหน่อย':
                    self.sound(3)
                elif self.command_ == 'ช่วยกด yes no':
                    self.sound(5)
                    self.start_anime = False
                    self.wave_done = False
                    pygame.time.wait(8000)
                    self.t2 = threading.Thread(target=self.simon_yes_no)
                    self.t2.start()
                    break
                self.start_img_simon += 1
                pygame.time.wait(5000)
                self.t1 = threading.Thread(target=simon)
                self.t1.start()
                self.sound(1)
            # ใส่ตัวเลข
            if self.start_img_simon <= 120 or 122 <= self.start_img_simon < 260:
                if 122 <= self.start_img_simon <= 260 and self.previous:
                    self.start_img_simon -= 1
                    continue
                else:
                    self.start_img_simon += 1
##            print(self.start_img_simon)
            # อนิเมชั่นหยุด
            if self.start_img_simon == 120:
##                print('sound')
                self.sound(1)
                self.start_img_simon += 1
                self.t1 = threading.Thread(target=simon)
                self.t1.start()
##                print(recognize)
##                print(self.start_img_simon, 'enter')
                self.wave_done = True
                T_speech = threading.Thread(target=self.speech_input)
                T_wave = threading.Thread(target=self.simon_wave)
                T_wave.start()
                T_speech.start()
##                T_speech.join()
            # พูดตัวเลขกับพูดออก
            if (self.start_img_simon == 121 and self.previous) or recognize.find('ออก') >= 0:
                if recognize.find('ออก') >= 0:
                    pass
                else:
                    voice = mp3.talktalk(self.string_talk, 'sound_simon/number.mp3')
                    self.string_talk = ''
                    pygame.time.wait(4000)
                    self.t1 = threading.Thread(target=simon)
                    self.t1.start()
                self.start_anime = False
                self.wave_done = False
            pygame.display.flip()
        pygame.mixer.music.unpause()

    def speech_input(self):
        global simon_done, recognize
        self.speech_ = True
        while self.speech_ and recognize.find('ออก') < 0:
##            print('s')
            self.listen_command, self.listen_num = False,False
            while not self.listen_num and recognize.find('ออก') < 0:                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_function()
                while not self.listen_command and recognize.find('ออก') < 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    if recognize.find('ใส่ตัวเลขหน่อย') >= 0:
                        simon_done = False
                        self.command_ = 'ใส่ตัวเลขหน่อย'
                        self.start_img_simon += 1
                        self.sound(2)
##                        print(simon_done)
                        self.listen_command = True
                    elif recognize.find('ช่วยกด') >= 0 and recognize.find('yes') >= 0 and recognize.find('no'):
                        simon_done = False
                        self.command_ = 'ช่วยกด yes no'
                        self.start_img_simon += 1
                        self.sound(2)
                        self.listen_command = True
                        self.listen_num = True
                        self.speech_ = False
                        pass
                    elif recognize != '' and recognize.find('ออก') < 0 and recognize.find('พูดอีกครั้ง') < 0:
##                        print(recognize)
                        simon_done = False
##                        print(simon_done)
                        self.sound(2)
                        self.sound(0)
                        pygame.time.wait(7000)
                        self.sound(1)
                        self.t1 = threading.Thread(target=simon)
                        self.t1.start()
##                    elif recognize.find('พูดอีกครั้ง') >= 0:
##                        self.sound(1)
##                        pygame.time.wait(1000)  
##                if recognize.find('ต้องการใส่หมายเลข') >= 0:
##                    self.sound(1)
##                    pygame.time.wait(1000)  
                if recognize.isdigit():
                    simon_done = False
                    if int(recognize) > 127:
                        self.sound(2)
                        self.sound(4)
                        pygame.time.wait(6000)
                        self.sound(1)
                        self.t1 = threading.Thread(target=simon)
                        self.t1.start()
                    else:
                        self.number_input = recognize
                        recognize = ''
##                        print(self.start_img_simon)
                        self.start_img_simon -= 2
                        self.previous = True
                        self.sound(2)
                        self.string_talk = 'นำตัวเลข %s ใส่เข้าไปแล้วค่ะ' %self.number_input
##                        print(self.string_talk)
##                        print('a')
                        self.listen_num = True
                        self.speech_ = False
                elif recognize.find('ศูนย์') >= 0:
                    simon_done = False
                    self.sound(4)
                    pygame.time.wait(6000)
                    self.sound(1)
                    self.t1 = threading.Thread(target=simon)
                    self.t1.start()
    # พูด yes no
    def simon_yes_no(self):
        global simon_done, recognize
        self.listen_command = False
        self.sound(6)
        pygame.time.wait(5000)
        self.sound(1)
        self.t1 = threading.Thread(target=simon)
        self.t1.start()
        while not self.listen_command and recognize.find('ออก') < 0:
            if recognize.find('ไม่มี') >= 0:
                simon_done = False
                self.sound(2)
                self.no += 1
                self.i += 1
                pygame.time.wait(1000)
                self.listen_command = True
            elif recognize.find('มี') >= 0 and recognize.find('ไม่มี') < 0:
                simon_done = False
                self.sound(2)
                self.list_box[self.random_box[self.i]] = 1
                self.yes += 1
                self.i += 1
                pygame.time.wait(1000)
                self.listen_command = True
            elif recognize != '' and recognize.find('มี') < 0:
                simon_done = False
                self.sound(2)
                self.sound(7)
                recognize = ''
                pygame.time.wait(5000)
                self.listen_command = True
                    

    def sound(self, at):
        pygame.mixer.music.pause()
        sound = pygame.mixer.Sound(self.voice_simon[at]).play()
        pass

def simon():
    global recognize,simon_done
##    t1 = threading.Thread(target=simon)
    r = sr.Recognizer()
    m = sr.Microphone()
    recognize = ''
    simon_done = True
    while simon_done:
        print('talk')
        with m as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                recognize = r.recognize_google(audio,language = "th-TH")
                print('you said :' + recognize)
            except:
                recognize = ''
            if recognize.find('หยุด') != -1:
                return
    recognize = ''
    print("Simon Finish")
##    t1.start()

def main():
    t1 = threading.Thread(target=simon)
    t1.start()
    t2 = Screen(800, 600)
    t2.start()
    print('start')


if __name__ == '__main__':
    main()
##    Screen(800, 600).run()
##    simon()
##    Screen(800, 600).simon_anime()
##    while True:
##    t2 = threading.Thread(target= Sceen(800, 600).run())  
##    t2.start()
##    t1.join()
##    guess = random_number(51)
##    for  i in range(guess.box):
##        a = list(map(str, guess.show(i)))
##        print(a)
##        print('-------------------------------------')
##        print('-------------------------------------')
##    print(guess.list_length)
