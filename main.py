#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from clint.textui import prompt, puts, colored, validators, columns

import src.sd.setup
import src.fw.download
import src.utility.launcher
import src.cheat.manager
import src.misc

### FUNCTIONS ###
def display_banner():
    # Clears the terminal screen, and displays a title bar.
    os.system('cls||clear')

    puts(columns(
        [(colored.red('')), 17],
        [(colored.green('**************************************')), 50],
        [(colored.magenta('')), 25]
    ))
    puts(columns(
        [(colored.red('')), 17],
        [(colored.green('***  NSW - CWF & Homebrew Utilities  ***')), 50],
        [(colored.magenta('')), 25]
    ))
    puts(columns(
        [(colored.red('')), 17],
        [(colored.green('**************************************')), 50],
        [(colored.magenta('')), 25]
    ))

def display_quit_message():
    # Clears the terminal screen, and displays a title bar.
    os.system('cls||clear')

    puts(columns(
        ["", 17],
        [(colored.green('******************************************************')), 60],
        ["", 25]
    ))
    puts(columns(
        ["", 17],
        [(colored.green('***  https://github.com/codeotamlong/atm-nx-toolkit  ***')), 60],
        ["", 25]
    ))
    puts(columns(
        ["", 17],
        [(colored.green('** *** **** Give me STAR★ if you like this **** *** **')), 60],
        ["", 25]
    ))
    puts(columns(
        ["", 17],
        [(colored.green('***********************˗ˏˋ ★ ˎˊ˗**********************')), 60],
        ["", 25]
    ))


def main_menu():
    return src.misc.get_single_selection(
        question="What would you like to do?",
        options=[
            {'selector': '1', 'desc': 'SD Setup', 'return': 'sd-setup'},
            {'selector': '2', 'desc': 'Firmware Download', 'return': 'fw-dload'},
            {'selector': '3', 'desc': 'Atmosphere-NX Utilities', 'return': 'atm-utility'},
            {'selector': '4', 'desc': 'Cheat Management','return': 'cheat-mng'},
            {'selector': 'q', 'desc': 'Quit', 'return': 'quit'}
        ],
        two_column=True
    )


def get_nand_choice():
    return src.misc.get_single_selection(
        question="Select your NAND?",
        options=[
            {'selector': '1', 'desc': 'EmuNAND', 'return': 'emunand'},
            {'selector': '2', 'desc': 'SysNAND', 'return': 'sysnand'}
        ],
        default="1"
    )

def get_sd_config(nand):
    path = Path("/".join(["cfg", "sd", nand +".json"]))
    with open(path, 'r') as config_file:
        cfg = json.load(config_file)
    return cfg


def get_fw_site_choice(sites):
    inst_options = []

    for (i, s) in enumerate(sites):
        inst_options.append({'selector': i, 'desc': s["url"], 'return': i})

    choice = src.misc.get_single_selection(
        question="What would you like to do?",
        options=inst_options
    )
    return sites[int(choice)]


def get_fw_table_choice(site):
    # Let users know what they can do.
    inst_options = []

    for (i, t) in enumerate(site["table"]):
        inst_options.append({'selector': i, 'desc': t['name'], 'return': i})
        # puts(s="["+str(i)+"] "+ t['name'])

    choice = src.misc.get_single_selection(
        question="What would you like to do?",
        options=inst_options,
        answer="Select region:"
    )
    return site["table"][int(choice)]


def get_fw_version_choice(table):
    # Let users know what they can do.
    inst_options = []

    for (i, fw) in enumerate(table):
        inst_options.append(
            {'selector': i, 'desc': '%-*s %s' % (40, fw.version, fw.md5), 'return': i})
        # puts(s="["+str(i)+"] "+ t['name'])

    choice = src.misc.get_single_selection(
        question="What would you like to do?",
        options=inst_options,
        default="0",
        answer="Select version [0: lastest]:"
    )
    return table[int(choice)]


def get_fw_dload_option(fw):
    puts("%s - %s - %s" % (fw.version, fw.filesize, fw.md5))

    inst_options = [{'selector': '1', 'desc': "mega.nz - Open web-browser (FASTER but MANUALLY)", 'return': fw.mega_nz},
                    {'selector': '2', 'desc': "archive.org - Download here (SLOWER but AUTOMATICALLY)", 'return': fw.archive_org}]

    choice = src.misc.get_single_selection(
        question="What would you like to do?",
        options=inst_options,
        default="1",
        answer="Select download method [Rcmd: 1 - faster]:"
    )
    return choice


### MAIN PROGRAM ###
with open(Path("./cfg/config.json"), 'r') as config_file:
    CONFIG = json.load(config_file)
# Set up a loop where users can choose what they'd like to do.
choice = ''
display_banner()
while choice != 'quit':
    # Respond to the user's choice.
    display_banner()
    choice = main_menu()
    if choice == 'sd-setup':
        nand = get_nand_choice()
        if (nand is None):
            print("Bad choice")
            continue
        src.sd.setup.run(CONFIG, get_sd_config(nand))
    if choice == 'fw-dload':
        site = get_fw_site_choice(CONFIG["fw-dload"])
        table = get_fw_table_choice(site)
        data = src.fw.download.run(site["url"], table["class"])
        version = get_fw_version_choice(data.firmware)
        dl_link = get_fw_dload_option(version)
        src.fw.download.open_(dl_link)
    elif choice == 'atm-utility':
        src.utility.launcher.launch(CONFIG)
    elif choice == 'cheat-mng':
        src.cheat.manager.main(CONFIG)
    elif choice == 'quit':
        display_quit_message()
    input("Press Enter to continue...")
