import time, pyautogui, threading, os
from pynput.keyboard import Key, Listener

class DummyArcher:
    def __init__(self):

        self.arrow_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] #Set the keys under which are arrow stacks mapped (i.e. ALT+1, CTRL+2, SHIFT+3)
        self.bow_dura = 50 #Set durability of ALL your current and spare bows
        self.spare_bow_key = ['ALT+1', 'ALT+2'] #Set keys under which are your spare bows mappes
        self.draw_bow_key = 'x' # Set key which is used to draw a weapon
        self.sequence_downtime = 5 # Set a time to wait between each attack sequence and equiping arrows sequence


        # !!!! DO NOT EDIT ANYTHING UNDER THIS LINE IF YOU DO NOT PERFECTLY KNOW HOW EVERYTHING WORKS, ONLY CHANGE THE VARIABLES ABOVE TO ALTER THE BEHAVIOR !!! #

        self.__dura_loss = 0.1
        self.__draw_time = 0.2
        self.__equip_arrows_downtime = 1
        self.__attack_downtime = 0.7
        self.__current_dura = 0
        self.__current_arrow_count = 1
        self.__current_arrow_stack = 0
        # self.__current_arrow_stack_use = 1
        self.__bow_swapped = 0

        pb = threading.Thread(target=self.__panicButton)
        pb.start()

        print('!--- You have 10 seconds to activate Mortal Online 2 window and have your weapon out ---!')
        time.sleep(10);
        self.startShooting();

    def __panicButton(self):
        def on_press(key):
            if(key == Key.f5):
                print('--Stopping the script based on user input--')
                os._exit(0)

        # Collect events until released
        with Listener(on_press=on_press,) as listener:
            listener.join()

    def startShooting(self):
        print('--Starting the attack sequence--')
        self.__current_dura = self.bow_dura
        while self.__current_arrow_count <= 25:
            print('--Shooting the dummy--')
            self.__doShoot()
            time.sleep(self.__attack_downtime)
        else:
            print(f'--Sequence is done, preparing to equip another arrow stacks. Wait time is {self.sequence_downtime}. It is safe to close the script now with CTRL+C--')
            time.sleep(self.sequence_downtime)
            if self.__current_arrow_stack + 1 <= len(self.arrow_keys):
                print('--No arrows on the character, equiping another stack--')
                split_arrow_key = self.arrow_keys[self.__current_arrow_stack].split('+')
                if len(split_arrow_key) == 2:
                    with pyautogui.hold(split_arrow_key[0]):
                        pyautogui.press(split_arrow_key[1])
                else:
                    pyautogui.press(split_arrow_key[0])
                time.sleep(self.__equip_arrows_downtime)
                # self.__current_arrow_stack_use += 1
                # if self.__current_arrow_stack_use > 4:
                self.__current_arrow_stack += 1
                self.__current_arrow_count = 0
                self.startShooting()
            else:
                print('--No arrows left, closing the script--')
                os._exit(0)

    def __doShoot(self):
        print(f'--Shooting an arrow number {self.__current_arrow_count}--')
        if self.__current_dura > 0 and self.__bow_swapped < len(self.spare_bow_key):
            pyautogui.mouseDown()
            time.sleep(self.__draw_time)
            pyautogui.mouseUp()
            self.__current_arrow_count += 1
            self.__current_dura -= self.__dura_loss
        else:
            if self.__bow_swapped < len(self.spare_bow_key):
                print('--Not enough durability, swaping the bow')
                spare_bow_keys = self.spare_bow_key[self.__bow_swapped].split('+')
                if len(spare_bow_keys) == 2:
                    with pyautogui.hold(spare_bow_keys[0]):
                        pyautogui.press(spare_bow_keys[1])
                else:
                    pyautogui.press(spare_bow_keys[0])
                self.__bow_swapped += 1
                time.sleep(0.5)
                pyautogui.press(self.draw_bow_key)
                time.sleep(1)
                self.__doShoot()
            else:
                print('--All spare bows have already been used, stopping the script--')
                os._exit(0)
DummyArcher()
