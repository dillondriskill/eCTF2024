#!/usr/bin/env python
"""Updates a connected MISC device"""
import os

def main():
    """Main function, the entry point"""

    # Default values
    ap_img = "build/ap.img"

    component_count = 2
    comp_imgs = ["build/comp1.img", "build/comp2.img"]
    

    os.system("clear")
    print("Welcome to the OSU 2024 Mitre eCTF update tool!")
    print()

    # Getting arguments from user, or using defaults if they want
    getting_user_input = True
    while (getting_user_input):
        # Most the time we will probably just want to see if it will even compile, so default of yes is smart here
        user_in = input("Procede with defaults? Y/n (Press ENTER to use defaults): ")

        if user_in in('n', 'N'):
            print("Please enter new values, or press ENTER to use defaults in parentheses:")

            user_in = input("AP image (Default: build/ap.img): ")
            if user_in != "":
                ap_img = user_in
            
            user_in = input("Component count (Default: 2): ")
            if user_in != "":
                component_count = int(user_in)

            comp_imgs = []
            for i in range(0, component_count):
                user_in = input("Component " + str(i+1) + " image (Default build/comp" + str(i) + ".img): ")
                if user_in != "":
                    comp_imgs.append(user_in)
                else:
                    comp_imgs.append("component/build/comp" + str(i) + ".img")

            getting_user_input = False

        elif user_in in('', 'Y', 'y'):
            getting_user_input = False
        else:
            print("Invalid input, please type Y/y/N/n or press ENTER")

        os.system("clear")
        print("Available devices: ")
        os.system("ls /dev/tty*")
        print()

        # Set to none just for clarity
        ap_path = "DEFAULT_AP_PATH"
        user_in = input("AP device path (NO DEFAULT): ")
        if user_in != "":
            component_count = int(user_in)

        comp_paths =[]
        for i in range(0, component_count):
            user_in = input("Component " + str(i+1) + " device path (NO DEFAULTS): ")
            if user_in != "":
                comp_paths.append(user_in)
            else:
                comp_paths.append("DEFAULT_COMPONENT_PATH")

        ap_update_command = "ectf_update --infile " + ap_img + " --port " + ap_path
        comp_update_commands = []
        for i in range(0, component_count):
            comp_update_commands.append("ectf_update --infile " + comp_imgs[i] + " --port " + comp_paths[i])
        print()

        print(ap_update_command)
        os.system(ap_update_command)
        print()

        for command in comp_update_commands:
            print(command)
            os.system(command)

if __name__ == "__main__":
    main()
