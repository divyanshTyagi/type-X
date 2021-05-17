import time
import sys
import curses
import random
sampe_texts = []

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

    curses.use_default_colors()
    stdscr.clear()
    curses.curs_set(0)

    time_start = -1
    time_end = -1

    (h,w) = stdscr.getmaxyx()

    w_left = int(w*.1)
    w_right = int(w*.8)
    h_top = h//2
    texts = random.choice(sampe_texts)
    words = texts.split()
    x,y = w_left,h_top

    for text in words:
        # can we add ?
        if((x + len(text))> w_right):
            x = w_left
            y+=1
        stdscr.addstr(y,x,text)
        x+=len(text)+1


    stdscr.move(h_top, w_left) # go to the start of the word
    stdscr.refresh()
    x,y = w_left,h_top

    curses.init_pair(1, curses.COLOR_GREEN, -1) # pair of foreground and background color
    curses.init_pair(2,curses.COLOR_RED,-1) # for wrong answer;
    stdscr.attron(curses.color_pair(1)) # correct writing with green COLOR_RED


    for (kthWord,text) in enumerate(words):
        stdscr.addstr(0,0,str(kthWord))
        # can we add ?
        if((x + len(text))> w_right):
            x = w_left
            y+=1
            stdscr.move(y, x)
            stdscr.refresh()
        idx = 0
        while(idx != len(text)):
            (y_cursor,x_cursor) = stdscr.getyx()
            stdscr.addstr(0,0,str(x_cursor))
            key = stdscr.getch()
            if(key == ord('0')):
                exit()
            if(key == ord(text[idx])): # do they match ?
                if(time_start == -1):
                    time_start = time.time() # initialize start time
                stdscr.addstr(y,x,str(chr(key)))
                stdscr.refresh()
                x+=1
                idx+=1
                stdscr.move(y, x)
                stdscr.refresh()
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y,x,text[idx])
                #remvoe the curson to the prev posiotn
                stdscr.move(y,x)
                stdscr.attroff(curses.color_pair(2))
                stdscr.attron(curses.color_pair(1))

        if(kthWord == len(words)-1):
            break

        key = stdscr.getch()
        while(key != ord(' ')):
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y,x,"_")
            #remvoe the curson to the prev posiotn
            stdscr.move(y,x)
            stdscr.attroff(curses.color_pair(2))
            stdscr.attron(curses.color_pair(1))
            key = stdscr.getch()

        if((x + 1 + len(words[kthWord+1]))  > w_right):
            x = w_left
            y+=1
            stdscr.move(y, x)
        else:
            stdscr.addstr(y,x,"_")
            stdscr.refresh()
            x+=1

        stdscr.move(y,x)
        stdscr.refresh()


    time_end = time.time()
    stdscr.clear()

    stdscr.attroff(curses.color_pair(1))


    verdict = "Hurray! Your time of completion was {} seconds, I last longer than that he he".format(int(time_end - time_start))
    wpm = "WPM -- {}".format(int(60*len(words)/(time_end-time_start)))
    (y,x) = (h//2,w//2 - len(verdict)//2)
    stdscr.addstr(y,x,verdict)
    stdscr.refresh()
    stdscr.addstr(y+1,x,wpm)
    stdscr.refresh()
    curses.napms(2000)
    stdscr.attroff(curses.color_pair(1))

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
    file = open("text_sample.txt","r")
    for line in file.readlines():
        sampe_texts.append(line)
    simulate_menu(stdscr)


def interact():
    curses.wrapper(curse)
######################################################################################################
