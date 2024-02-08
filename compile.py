#!/usr/bin/env python
"""Builds the OSU MISC system using either testing defaults or user generated inputs"""
import os

def main():
    """Main function, the entry point"""

    # Default AP build inputs
    design = os.getcwd()
    ap_output_name = "ap"
    attest_pin = "123456"
    component_count = 2
    component_ids = ["0x11111124", "0x11111125"]
    boot_message = "System booted"
    replacement_token = "0123456789abcdef"
    ap_output_directory = "build"

    # Default Component build inputs; Some arguments are not set here because they might be different for different Components
    comp_output_names = ["comp1", "comp2"]
    comp_output_directory = "build"
    component_boot_messages = ["\"Component 1 booted\"", "\"Component 2 booted\""]
    attest_locations = ["\"Component 1 location\"", "\"Component 2 location\""]
    attest_dates = ["\"Component 1 date\"", "\"Component 2 date\""]
    attest_customers = ["\"Component 1 customer\"", "\"Component 2 customer\""]

    # Here's where the fun begins...
    os.system("clear")
    print("Welcome to the OSU 2024 Mitre eCTF build tool!\n")
    print()

    # Getting arguments from user, or using defaults if they want
    getting_user_input = True
    while (getting_user_input):
        # Most the time we will probably just want to see if it will even compile, so default of yes is smart here
        user_in = input("Procede with defaults? Y/n (Press ENTER to use defaults): ")

        if user_in in('n', 'N'):
            print("Please enter new values, or press ENTER to use defaults in parentheses:")
            user_in = input("Design directory (Default: " + design + "): ")
            if user_in != "":
                design = user_in
            
            user_in = input("AP output file name (Default: " + ap_output_name + "): ")
            if user_in != "":
                ap_output_name = user_in

            user_in = input("AP output directory (Default: " + ap_output_directory + "): ")
            if user_in != "":
                ap_output_directory = user_in

            user_in = input("Attestation pin (Default: " + attest_pin + "): ")
            if user_in != "":
                attest_pin = user_in

            user_in = input("Number of components (Default: " + str(component_count) + "): ")
            if user_in != "":
                component_count = int(user_in)

            component_ids = []
            for i in range(0, component_count):
                user_in = input("Component " + str(i+1) + " id (Default: \"" + hex((0x11111124)+i) + "\"): ")
                if user_in != "":
                    component_ids.append(user_in)
                else:
                    component_ids.append(hex((0x11111124)+i))
        
            user_in = input("AP boot message (Default: " + boot_message + "): ")
            if user_in != "":
                attest_pin = "\"" + user_in + "\""

            user_in = input("Replacement token (Default: " + replacement_token + "): ")
            if user_in != "":
                replacement_token = user_in

            user_in = input("Components output directory (Default: " + comp_output_directory + "): ")
            if user_in != "":
                comp_output_directory = user_in

            comp_output_names = []
            for i in range(0, component_count):
                user_in = input("Component " + str(i+1) + " output file name (Default: comp" + str(i+1) + "): ")
                if user_in != "":
                    comp_output_names.append(user_in)
                else:
                    comp_output_names.append("comp" + str(i+1))

            component_boot_messages = []
            for i in range(0, component_count):
                user_in = input("Component " + str(i+1) + " boot message (Default: \"Component " + str(i+1) + " booted\"): ")
                if user_in != "":
                    component_boot_messages.append("\"" + user_in + "\"")
                else:
                    component_boot_messages.append("\"Component " + str(i+1) + " booted\"")
            
            attest_locations = []
            for i in range(0, component_count):
                user_in = input("Component " + str(i+1) + " location (Default: \"Component " + str(i+1) + " location\"): ")
                if user_in != "":
                    attest_locations.append("\"" + user_in + "\"")
                else:
                    attest_locations.append("\"Component " + str(i+1) + " location\"")

            attest_dates = []
            for i in range(0, component_count):
                user_in = input("Component " + str(i+1) + " date (Default: \"Component " + str(i+1) + " date\"): ")
                if user_in != "":
                    attest_dates.append("\"" + user_in + "\"")
                else:
                    attest_dates.append("\"Component " + str(i+1) + " date\"")

            attest_customers = []
            for i in range(0, component_count):
                user_in = input("Component " + str(i+1) + " customer (Default: \"Component " + str(i+1) + " customer\"): ")
                if user_in != "":
                    attest_customers.append("\"" + user_in + "\"")
                else:
                    attest_customers.append("\"Component " + str(i+1) + " customer\"")

            getting_user_input = False

        elif user_in in('', 'Y', 'y'):
            getting_user_input = False
        else:
            print("Invalid input, please type Y/y/N/n or press ENTER")

        print()
        print("Commands:")
        print()


        print("Build deployment command:")
        # Deployment build command
        build_depl_cmd = "ectf_build_depl -d " + design
        print(build_depl_cmd)
        print()

        print("AP build command:")
        # Putting together AP build command
        ap_command = "ectf_build_ap -d " + design + " -on " + ap_output_name + " --p " + attest_pin + " -c " + str(component_count) + " -ids \""
        for i in range(0, component_count):
            if i != 0:
                ap_command += ", "
            ap_command += component_ids[i]
        ap_command += "\" -b \"" + boot_message + "\" -t " + replacement_token + " -od " + ap_output_directory
        print(ap_command)
        print()

        print("Component build commands:")
        component_build_commands = []
        for i in range(0, component_count):
            temp_cmd = "ectf_build_comp -d " + design + " -on " + comp_output_names[i] + " -od " + comp_output_directory + " -id " + component_ids[i] + " -b " + component_boot_messages[i] + " -al " + attest_locations[i] + " -ad " + attest_dates[i] + " -ac " + attest_customers[i]
            component_build_commands.append(temp_cmd)
            print("Component " + str(i+1))
            print(temp_cmd)
            print()

        print(build_depl_cmd)
        os.system(build_depl_cmd)

        print(ap_command)
        os.system(ap_command)

        for i in component_build_commands:
            print(i)
            os.system(i)


if __name__ == "__main__":
    main()
