# -*- coding: utf-8 -*-
"""
Created on: 13-Jul-2018

@author: Ai
"""

import os
import shutil
from time import sleep
import subprocess
import plac
from pyfiglet import figlet_format


def run_for_asin(command):
    """
    Run a Shell command
    Arguments:
        command (str)
    Returns:
        p_status (int)
    """
    print("\n======\n{0}\n======\n".format(command))
    cwd = os.getcwd()+'\\amazon_asin_fetcher'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False, cwd=cwd)
    (output, err) = p.communicate()
    p_status = p.wait()
    return p_status


def copy_file():
    print("\nCopying ASIN_Data...")
    src = os.getcwd() + "\\amazon_asin_fetcher\\Data\\ASIN_Data.xlsx"
    dest = os.getcwd() + "\\amazon_reviews_scrapper\\Data"
    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)
    shutil.copy(src, dest)


def run_for_reviews(command):
    """
    Run a Shell command
    Arguments:
        command (str)
    Returns:
        p_status (int)
    """
    print("\n======\n{0}\n======\n".format(command))
    cwd = os.getcwd()+'\\amazon_reviews_scrapper'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False, cwd=cwd)
    (output, err) = p.communicate()
    p_status = p.wait()
    return p_status


@plac.annotations(
    country=("Amazon Website Country", "option", "c", str),
    key=("Search Key Phrase (use +)", "option", "k", str))
def main(country=None, key=None):
    print(figlet_format("Amazon Reviews Web Scrapper"))
    commands_for_asin = ['python run_asin_fetcher.py -c {0} -k {1}'.format(country, key),
                         'python fix_json.py',
                         'python json2excel.py']
    commands_for_reviews = ['python run_reviews_scrapper.py',
                            'python fix_json.py',
                            'python reviews_json2excel.py']
    if key is None:
        raise Exception(("Key Phrase required!"))

    if country is None:
        raise Exception("Country required!")
    else:
        for c in commands_for_asin:
            p_status = run_for_asin(c)
            print("Current Task Complete...")
            sleep(1)
        copy_file()
        for c in commands_for_reviews:
            p_status = run_for_reviews(c)
            print("Current Task Complete...")
            sleep(1)


if __name__ == '__main__':
    plac.call(main)
