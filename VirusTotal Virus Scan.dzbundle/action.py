#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Dropzone Action Info
# Name: VirusTotal Virus Scan
# Description: This action sends your sample to VirusTotal.com and returns results as browser page
# Handles: Files
# Creator: Tarik Taha Uygun
# URL: http://bilginesayar.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.5
# OptionsNIB: APIKey
# LoginTitle: API Key

import time
import requests
import webbrowser
import os

def dragged():
    api_key = None
    # Each meta option at the top of this file is described in detail in the Dropzone API docs at https://github.com/aptonic/dropzone3-actions/blob/master/README.md#dropzone-3-api
    # You can edit these meta options as required to fit your action.
    # You can force a reload of the meta data by clicking the Dropzone status item and pressing Cmd+R

    # This is a Python method that gets called when a user drags items onto your action.
    # You can access the received items using the items global variable e.g.
    print(items)
    # The above line will list the dropped items in the debug console. You can access this console from the Dropzone settings menu
    # or by pressing Command+Shift+D after clicking the Dropzone status item
    # Printing things to the debug console with print is a good way to debug your script. 
    # Printed output will be shown in red in the console
    try:
        api_key = os.environ['api_key']
    except ValueError:
        dz.fail("You must enter your VirusTotal Private API Key")
    
    if api_key is not None and len(api_key) != 64:
        dz.fail("Error", "You API key credentials are wrong!")

    # You mostly issue commands to Dropzone to do things like update the status - for example the line below tells Dropzone to show
    # the text "Starting some task" and show a progress bar in the grid. If you drag a file onto this action now you'll see what I mean
    # All the possible dz methods are described fully in the API docs (linked up above)
    dz.begin("Your sample uploading VirusTotal.com...")

    params = {'apikey': api_key}
    files = {'file': (items[0], open(items[0], 'rb'))}
    response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
    json_response = response.json()
    link = json_response['permalink']
    print(link)

    # Below line switches the progress display to determinate mode so we can show progress
    dz.determinate(True)

    # Below lines tell Dropzone to update the progress bar display
    dz.percent(10)
    time.sleep(1)
    dz.percent(50)
    time.sleep(1)
    dz.percent(100)

    # The below line tells Dropzone to end with a notification center notification with the text "Task Complete"
    dz.finish("Task Complete")

    # You should always call dz.url or dz.text last in your script. The below dz.text line places text on the clipboard.
    # If you don't want to place anything on the clipboard you should still call dz.url(false)
    dz.url(link)
    webbrowser.open_new(link)
 
def clicked():
    # This method gets called when a user clicks on your action
    dz.fail("Drag a file to analyze")
    dz.url(False)
