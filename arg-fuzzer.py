#!/usr/bin/python3

import subprocess
import sys
import re


class bcolors:

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'



logo = """
⠄⠄⠄⠄⠄⠄⠄⠄⠄⡀⠄⡀⠄⡀⠄⡀⢀⠄⡀⢀⠄⡀⠄⡀⠄⠄⠄⠄⢀⠄⠄⡀⢀⠄⠄⡀⠄⠄⠄⠄
⠄⠄⠄⠈⠄⠁⠈⠄⠂⠄⡀⠄⠄⡀⢀⠄⢀⠄⢀⠄⡀⠠⠄⠄⠂⠁⠈⡀⠄⠄⠁⠄⠄⠄⠂⠄⡀⠁⠄⠄
⠄⠄⠄⠁⠄⠁⠄⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⠄⡀⡀⠄⠄⠁⢀⢁⠄⡀⠠⠄⠁⡈⢀⠈⢀⠠⠄⢀⠄⠄
⠄⠄⠄⠄⠁⠄⠁⠄⠂⠄⡠⣲⢧⣳⡳⡯⣟⣼⢽⣺⣜⡵⣝⢜⢔⠔⡅⢂⠄⠄⠁⠄⢀⠄⡀⠄⡀⠄⠄⠄
⠄⠄⠄⠄⠈⠄⠈⠄⢀⡇⡯⡺⢵⣳⢿⣻⣟⣿⣿⣽⢾⣝⢮⡳⣣⢣⠣⡃⢅⠂⠐⠈⠄⠄⢀⠄⡀⠄⠄⠄
⠄⠄⠄⠄⠈⠄⠐⢀⠇⡪⡸⡸⣝⣾⣻⣯⣿⣿⡿⣟⣿⡽⣗⡯⣞⢜⢌⠢⡡⢈⠈⠄⠁⠈⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠐⠄⠈⠆⠕⢔⠡⣓⣕⢷⣻⣽⣝⢷⣻⣻⣝⢯⢿⠹⠸⡑⡅⠕⠠⠠⠄⠅⠄⠂⠄⠂⠈⠄⠄⠄
⠄⠄⠄⠄⠄⠂⠡⡑⢍⠌⡊⢢⢢⢱⠼⣺⢿⢝⠮⢪⣪⡺⣘⡜⣑⢤⢐⠅⠡⢂⠡⠐⡀⢀⠠⠐⠄⠐⠄⠄
⠄⠄⠄⠄⢈⢀⠡⠨⡢⡑⡌⡔⡮⡷⣭⢧⣳⠭⣪⣲⣼⣾⣟⣻⣽⣺⣸⣜⢌⢆⢌⠐⠄⡀⠄⡀⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠠⠄⠌⡢⡵⠺⠞⠟⠛⠯⠟⠟⠝⡫⢗⠟⠝⠙⠉⠊⠑⠉⠉⠉⠑⢒⠠⠁⠄⡀⠠⠄⠄⠄⠄
⠄⠄⠄⠐⡀⠄⠄⠅⡪⠄⠂⠄⠄⠄⠄⠄⠄⠄⢀⢕⢔⠄⠄⠄⠄⡀⠠⠐⠈⢀⠄⠠⠄⡁⠄⡀⠂⠠⠄⠄
⠄⠄⠄⠠⠄⠄⠂⡑⠄⠄⠠⠐⠄⠁⠄⠁⠄⠄⢸⣿⣿⡂⠄⠄⢀⠄⡀⠄⠂⠠⠐⠄⡐⡀⠂⢀⠐⠄⠄⠄
⠄⠄⠄⠄⢐⠄⠂⢕⢅⢄⠄⣀⡀⢄⠄⠁⣀⣔⡵⣿⣯⠧⡣⣢⡠⢀⢀⡠⠐⢀⢐⠠⢀⠐⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠐⡔⢀⠘⢽⣻⣶⣥⣉⠥⡣⣱⣷⠻⣪⣻⣷⡣⡣⢫⣞⣗⡦⡵⢻⠺⡸⠐⡀⠐⠄⠂⡀⠄⠄⠄
⠄⠄⠄⠄⠂⠘⡀⠔⢀⠑⠍⠍⡽⣽⣿⣻⠂⡷⣯⡿⣟⡿⠌⡆⠘⣾⣻⢵⢕⠔⢀⠁⠠⠈⡀⠁⠄⡀⠄⠄
⠄⠄⠄⠄⠠⠄⠄⡐⢰⢈⢄⠱⢽⣺⢳⠁⣈⠄⠄⠈⠊⠈⠄⠄⢡⣐⢫⢯⡢⢊⢄⢪⠨⠠⠄⡀⠁⠄⠄⠄
⠄⠄⠄⠄⠂⠄⠂⠠⠱⣕⡣⡇⡏⢮⢕⣸⣾⠠⠄⠄⠄⠂⠄⠄⠌⢟⣜⡵⣯⢷⡴⡅⠅⡂⠠⠄⢈⠄⠄⠄
⠄⠄⠄⠄⠂⠁⢀⠈⠌⡪⢝⢾⣝⣎⠒⠏⠙⠠⠑⠁⠆⠒⠐⠐⠉⢀⠑⣍⡿⣽⡽⡂⠕⠄⠄⠂⢀⠠⠄⠄
⠄⠄⠄⠐⠄⡈⠄⢀⠄⠊⠍⢯⣷⣏⢊⢀⣈⣠⣤⣤⣤⣴⣶⢶⣴⢤⢬⣌⢻⡺⡻⠈⠄⠂⠄⠂⡀⠄⠄⠄
⠄⠄⠄⠄⠂⢀⠐⠄⠄⠂⠡⠑⠕⠅⡕⡽⡑⡁⠉⠉⠉⠉⠁⠁⠁⠠⢊⠊⠢⠈⠄⠨⠄⠄⠁⠐⢀⠈⠄⠄
⠄⠄⠄⠈⢀⠄⠄⠈⡀⢂⠐⠄⠂⠁⠠⠁⡢⡪⣢⣲⣦⣖⡔⡤⡨⡐⢄⠌⠠⠈⠐⠄⠂⠠⠁⢈⠠⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⢂⠄⠢⠂⠈⡀⠈⡀⠈⠰⠹⡨⠑⡑⠕⠕⠊⠌⠌⠄⠐⠄⠂⠁⢈⠄⡁⠐⠄⡐⢀⠂⠄
⠄⠄⠄⠄⡐⢄⠑⠄⠄⡇⡁⠄⠄⠄⠄⡈⠄⠄⠄⠄⢀⠠⠄⠂⢀⠐⠄⡈⠠⠈⠄⠄⠠⠐⠄⠁⠠⠄⠄⠄
⠄⠄⡀⢊⠨⢀⢊⠄⠨⡂⡂⠄⠂⠄⢀⠄⠠⠄⠂⠄⠄⡀⠠⠄⠄⠄⠐⠄⠄⡀⠁⡀⠂⠄⠂⠁⠨⠄⠅⠄
⠄⠄⠐⠄⢂⠢⡀⠄⠬⠄⠂⠅⡀⠈⠄⠄⠄⠄⠄⠄⠄⠄⠄⡀⠂⠄⠂⠄⢀⠄⠄⠄⠄⠂⠄⠂⢈⠐⠄⠄
⠄⠄⠈⡀⠄⠄⠄⠄⠅⠅⠐⠄⠄⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠁⠄⠄⠄⠂⢐⠄⠐⠄
⠄⠄⠄⠄⠄⠂⠄⠄⠕⠈⡂⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠄⠄⠂⠄
"""

print(bcolors.RED,logo,bcolors.ENDC)

title = """
    **          ****          ****                        ****
   */*         */// *        /**/                        */// *
  * /*  ******/*   /*       ****** **   ** ****** ******/    /* ******
 ******//**//*/ ****       ///**/ /**  /**////** ////**    *** //**//*
/////*  /** /  ///*          /**  /**  /**   **     **    /// * /** /
    /*  /**      *           /**  /**  /**  **     **    *   /* /**
    /* /***     *            /**  //****** ****** ******/ **** /***
    /  ///     /             //    ////// ////// //////  ////  ///

[+]Fuzzer for BufferOverFlow
[+]payload to arguments
"""

print(bcolors.BLUE,title,bcolors.ENDC)

if len(sys.argv) != 3:
    
    print(bcolors.YELLOW)

    print(f"[!]Usage   : {sys.argv[0]} <binary> <value_range>")
    print(f"[+]Example : {sys.argv[0]} vuln 10-30 <default = 20-50>")
    
    print(bcolors.ENDC)

    sys.exit()


target = sys.argv[1]
value_range = sys.argv[2]

reg = re.search(r"^\d.+-\d.+$",value_range)

if reg:

    value_range = value_range.split("-")

else:

    print(bcolors.YELLOW)

    print(f"[!]Wrong forms.... {value_range}")
    print("[*]Fix to 20-50")
    value_range = "20-50"    
    value_range = value_range.split("-")
    print(bcolors.ENDC)




print(bcolors.RED,"[*]NowTrying........",bcolors.ENDC)

for i in range(int(value_range[0]),int(value_range[1])+1):

    count = int(i)
    res = subprocess.getoutput(f"./{target} `python -c'print(\"A\"*{count})'`")

    if "Segmentation fault (core dumped)" in res:

        print(bcolors.BLUE)
        print(f"[!]Found OverFlows value: {count}")
        print(bcolors.ENDC)
        sys.exit()
