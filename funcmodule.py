import time
import sys
import curses
import random
from curses import textpad
from cfonts import render, say
from blessed import Terminal
file_id =0
code_file = []



################################################ MENU ###############################################
def simulate_menu(stdscr):
    menu =  ["Play","Scores","Credits","Exit"]
    #navigating the print_menu
    current_row = 0

    print_menu(stdscr,menu,current_row)

    while 1:
        key = stdscr.getch()

        # clear existing texts
        stdscr.clear()

        if key == curses.KEY_UP:
            current_row = max(0,current_row-1)
        elif key == curses.KEY_DOWN:
            current_row = min(len(menu)-1,current_row+1)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if(menu[current_row] == "Exit"):
                exit()
            stdscr.clear()
            if(menu[current_row] == "Play"):
                play(stdscr)
            elif (menu[current_row] == 'Credits'):
                credit(stdscr)
            else:
                stdscr.addstr(0,0,"opened {}".format(menu[current_row]))
                stdscr.refresh()
                stdscr.getch()
            stdscr.clear()

        print_menu(stdscr,menu,current_row)

        # update screen
        stdscr.refresh()

def print_menu(stdscr,menu,selected_row):

    (h,w) = stdscr.getmaxyx()

    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_YELLOW) # pair of foreground and background color


    for i in range(len(menu)):
        if(i == selected_row):
            stdscr.attron(curses.color_pair(1))
        text = menu[i]
        x = w//2-len(text)//2
        y = h//2 - (len(menu)//2) + i
        stdscr.addstr(y,x,text)
        stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()

#####################################################################################################

############################################# PLAY ##################################################

def play(stdscr):

    #deciding the texts
    file_id = random.randint(0,349)
    file = open("./codes/" + str(file_id) + ".txt","r")
    code_file = []
    for line in file.readlines():
        code_file.append(line)
    file.close()


    stdscr.clear()

    curses.use_default_colors()
    stdscr.clear()
    curses.curs_set(1)

    time_start = -1
    time_end = -1



    (h,w) = stdscr.getmaxyx()

    box = [[3,3],[h-3,w-3]]

    textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
    stdscr.refresh()

    stdscr.addstr(h-5,w-40,"Press F8 to report bad sample")
    stdscr.addstr(h-6,w-40,"Press F9 to Exit")


    w_left = 20
    w_right = int(w*.9)
    h_top = 5
    texts = code_file

    totalCharacters = 0

    for (idx,line) in enumerate(texts):
        stripped_line = line.rstrip()
        try:
            stdscr.addstr(h_top+idx,w_left,stripped_line) # remove trailing zeros
        except:
            print("Error at " ,stripped_line)

        stdscr.refresh()


    curses.init_pair(1, curses.COLOR_GREEN, -1) # pair of foreground and background color
    curses.init_pair(2,curses.COLOR_RED,-1) # for wrong answer;

    for (id,line) in enumerate(texts):
        # the position of the cursor initially is h_top
        stripped_line = line.rstrip()
        stripped_line += "\n"
        stdscr.move(h_top+id, w_left) # go to the start of the line
        (y,x) = (h_top+id, w_left)
        stdscr.refresh()
        idx = 0

        while(stripped_line[idx] == ' '):
            idx+=1
            x+=1;
        stdscr.move(y,x)
        totalCharacters += len(stripped_line)-idx
        while(idx!=len(stripped_line)):


                key = stdscr.getch()
                if(key == curses.KEY_F9):
                    exit()
                elif(key == curses.KEY_F8):
                    exit()
                if(key == ord(stripped_line[idx])): # do they match ?
                    stdscr.attron(curses.color_pair(1))

                    if(time_start == -1):
                        time_start = time.time() # initialize start time
                    stdscr.addstr(y,x,str(chr(key)))
                    x+=1
                    idx+=1
                    stdscr.move(y, x)
                    stdscr.refresh()
                    stdscr.attroff(curses.color_pair(1))

                else:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(y,x,stripped_line[idx])
                    #remvoe the curson to the prev posiotn
                    stdscr.move(y,x)
                    stdscr.attroff(curses.color_pair(2))
    time_end = time.time()
    stdscr.clear()
    verdict = "Hurray! Your time of completion was {} seconds, I last longer than that he he".format(int(time_end - time_start))
    cpm = "CPM -- {}".format(int(60*totalCharacters)/(time_end-time_start))
    (y,x) = (h//2,w//2 - len(verdict)//2)
    stdscr.addstr(y,x,verdict)
    stdscr.refresh()
    stdscr.addstr(y+1,x,cpm)
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    curses.napms(2000)



#############################################################################################
###################################### CREDITS ##############################################
def credit(stdscr):
    stdscr.clear()
    (h,w) = stdscr.getmaxyx()
    stdscr.addstr(h//2,w//2,"Created by Divyansh Tyagi")
    stdscr.refresh()
    curses.napms(2000)
#############################################################################################
###################################### INIT ##################################################
def curse(stdscr):
    curses.curs_set(0)
    simulate_menu(stdscr)


def interact():
    curses.wrapper(curse)
######################################################################################################
