# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 00:02:03 2022

@author: Nader Safa
"""

from pandas import read_excel, DatetimeIndex
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import os
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageFilter

set_names = ['01-First Set','02-Second Set','03-Third Set','04-Fourth Set','05-Fifth Set']
bg_color = '#171717'
accent_color = '#2ed573'
active_color = "#7bed9f"
fg_color = '#f4f4f4'

def reset_data():
    global match_data
    match_data = {
        'date': '',
        'player_1': '',
        'player_2': '',
        'location': '',
        'championship': '',
        'age_group': '',
        'stage': '',
        'event': '',
        'gender': '',
        'club_1': '',
        'club_2': '',
        'sets_1': 0,
        'sets_2': 0,
        'points_1': 0,
        'points_2': 0,
        'lead': 'draw',
        'sets': 0
        }

# Create image function
def create_image (match_data):
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    font_basic = ImageFont.truetype('scrc/fonts/Montserrat-Bold.ttf',32)
    font_sets = ImageFont.truetype('scrc/fonts/Montserrat-Bold.ttf',38)
    # Define display names
    if match_data['event'] == "Singles":
        display_name_1 = '{} | {}'.format(match_data['player_1'], match_data['club_1'].split('-')[1].strip())
        display_name_2 = '{} | {}'.format(match_data['player_2'], match_data['club_2'].split('-')[1].strip())
    elif match_data['event'] == "Doubles":
        display_name_1 = '{} & {}'.format(match_data['player_1'].split(' ')[0],match_data['player_1'].split(' ')[3])
        display_name_2 = '{} & {}'.format(match_data['player_2'].split(' ')[0],match_data['player_2'].split(' ')[3])

    draw.text(xy=(95,31),text=display_name_1,fill=(fg_color),font=font_basic)
    draw.text(xy=(85,81),text=display_name_2,fill=(fg_color),font=font_basic)
    draw.text(xy=(464,27),text=str(match_data['sets_1']),fill=(bg_color),font=font_sets)
    draw.text(xy=(464,77),text=str(match_data['sets_2']),fill=(bg_color),font=font_sets)
    draw.text(xy=(529,31),text=str(match_data['points_1']),fill=(fg_color),font=font_basic)
    draw.text(xy=(529,81),text=str(match_data['points_2']),fill=(fg_color),font=font_basic)
    
    if not os.path.exists('{}/{}'.format(output_folder,set_names[match_data['sets']])):
        os.makedirs('{}/{}'.format(output_folder,set_names[match_data['sets']]))
    
    image.save('{}/{}/{}-{}.png'.format(output_folder,set_names[match_data['sets']],match_data['sets']+1,match_data['points_2'] + match_data['points_1']))

# create_thumbnail function definition:
def create_thumbnail(match_data):
    # open screenshot, resize to FHD & add blur
    ss = Image.open(screenshot)
    ss = ss.resize((1920,1080))
    ss = ss.filter(ImageFilter.GaussianBlur(5))

    # add logo and darken background
    base = Image.open("src/singles_thumbnail.png")
    ss.paste(base, (0,0), base)

    # add text
    draw = ImageDraw.Draw(ss)
    font_title = ImageFont.truetype('scrc/fonts/Montserrat-ExtraBold.ttf',60)
    font_subtitle = ImageFont.truetype('scrc/fonts/Montserrat-Bold.ttf',50)
    font_footer = ImageFont.truetype('scrc/fonts/Montserrat-Regular.ttf',35)
    font_player = ImageFont.truetype('scrc/fonts/Montserrat-SemiBold.ttf',60)
    font_club = ImageFont.truetype('scrc/fonts/Montserrat-ExtraBold.ttf',40)
    # Define display names
    # if match_data['event'] == "Singles":
    #     display_name_1 = '{} | {}'.format(match_data['player_1'], match_data['club_1'].split('-')[1].strip())
    #     display_name_2 = '{} | {}'.format(match_data['player_2'], match_data['club_2'].split('-')[1].strip())
    # elif match_data['event'] == "Doubles":
    #     display_name_1 = '{} & {}'.format(match_data['player_1'].split(' ')[0],match_data['player_1'].split(' ')[3])
    #     display_name_2 = '{} & {}'.format(match_data['player_2'].split(' ')[0],match_data['player_2'].split(' ')[3])

    draw.text((960,108), match_data['age_group'] + " " + match_data['championship'] + " " + "Championship", fill=(fg_color), anchor="mt", font=font_title)
    draw.text((960,180), match_data['gender'] + " " + match_data['event'] + " " + match_data['stage'], fill=(fg_color), anchor="mt", font=font_subtitle)
    draw.text((960,972), str(match_data['date']).split('-')[0].strip() + " | " + match_data['location'], fill=(fg_color), anchor="mb", font=font_footer)
    draw.text((192,860), match_data['club_1'].split('-')[0], fill=(accent_color), anchor="lb", font=font_club)

    if match_data['event'] == "Singles":
        draw.text((192,810), match_data['player_1'], fill=(fg_color), anchor="lb", font=font_player)
        draw.text((1200,325), match_data['player_2'], fill=(fg_color), anchor="lt", font=font_player)
        draw.text((1200,375), match_data['club_2'].split('-')[0], fill=(accent_color), anchor="lt", font=font_club)
    elif match_data['event'] == "Doubles":
        draw.text((192,810),match_data['player_1'].split("&")[1].strip(), fill=(fg_color), anchor="lb", font=font_player)
        draw.text((192,740),match_data['player_1'].split("&")[0].strip(), fill=(fg_color), anchor="lb", font=font_player)
        draw.text((1200,325), match_data['player_2'].split("&")[0].strip(), fill=(fg_color), anchor="lt", font=font_player)
        draw.text((1200,395), match_data['player_2'].split("&")[1].strip(), fill=(fg_color), anchor="lt", font=font_player)
        draw.text((1200,460), match_data['club_2'].split('-')[0], fill=(accent_color), anchor="lt", font=font_club)
        
    ss.save('{}/thumbnail.png'.format(output_folder))

# import_excel function definition
def import_excel_data():
    excel_file_path = askopenfilename()
    global df
    df = read_excel(excel_file_path)
    df = df.reset_index()
    
# import_image function definition
def import_image():
    img_path = askopenfilename()
    global img
    img = img_path

# import_screenshot function definition
def import_screenshot():
    screenshot_path = askopenfilename()
    global screenshot
    screenshot = screenshot_path
    
# set_output function definition
def set_output_folder():
    global output_folder
    output_folder = askdirectory()

# create_txt function definition
def create_txt(match_data):

    if match_data['lead'] == 'first':
        winner = match_data['player_1']
        winner_club = match_data['club_1'].split('-')[0]
        loser = match_data['player_2']
        loser_club = match_data['club_2'].split('-')[0]
    else:
        winner = match_data['player_2']
        winner_club = match_data['club_2'].split('-')[0]
        loser = match_data['player_1']
        loser_club = match_data['club_1'].split('-')[0]


    if match_data['event'] == 'Singles':

        txt = """
        Title:
        Speedball | {} vs {} | Full Match | {} {} {} {}

        Description:
        {} [{}] takes on {} [{}] in the {} of the {} {} at the {} {} Championship {}.

        Date: {}
        Location: {}

        Facebook: https://www.facebook.com/RowadSpeedballTeam
        Instagram: https://www.instagram.com/rsc_speedball
        Tiktok: https://www.tiktok.com/@rsc_speedball

        Tags:
        speedball,speed ball,speed-ball,player,{},{}
        """.format(
            match_data['player_1'], 
            match_data['player_2'], 
            str(match_data['date']).split('-')[0].strip(),
            match_data['championship'], 
            match_data['age_group'],
            match_data['stage'],
            winner,
            winner_club,
            loser,
            loser_club,
            match_data['stage'],
            match_data['gender'],
            match_data['event'],
            match_data['age_group'],
            match_data['championship'],
            str(match_data['date']).split('-')[0].strip(),
            str(match_data['date']).split(' ')[0],
            match_data['location'],
            match_data['player_1'], 
            match_data['player_2'], 
            )
    elif match_data['event'] == 'Doubles':
        txt = """
        Title:
        Speedball | {} vs {} | Full Match | {} {} {} {}

        Description:
        {} [{}] take on {} [{}] in the {} of the {} {} at the {} {} Championship {}.

        Date: {}
        Location: {}

        Facebook: https://www.facebook.com/RowadSpeedballTeam
        Instagram: https://www.instagram.com/rsc_speedball
        Tiktok: https://www.tiktok.com/@rsc_speedball

        Tags:
        speedball,speed ball,speed-ball,player,{},{}
        """.format(
            match_data['player_1'].split(' ')[0] + " & " + match_data['player_1'].split(' ')[3], 
            match_data['player_2'].split(' ')[0] + " & " + match_data['player_2'].split(' ')[3], 
            str(match_data['date']).split('-')[0].strip(),
            match_data['championship'], 
            match_data['age_group'],
            match_data['stage'],
            winner,
            winner_club,
            loser,
            loser_club,
            match_data['stage'],
            match_data['gender'],
            match_data['event'],
            match_data['age_group'],
            match_data['championship'],
            str(match_data['date']).split('-')[0].strip(),
            str(match_data['date']).split(' ')[0],
            match_data['location'],
            match_data['player_1'], 
            match_data['player_2'], 
            )

    f = open("{}/text.txt".format(output_folder), "w")
    f.write(txt)
    f.close()

# start_generating function definition
def start_generating():
    reset_data()    
    line_count = 0
    for index, row in df.iterrows():
        # Edit player names
        if line_count == 0:
            match_data['player_1'] = row['player_1'].strip().title()
            match_data['player_2'] = row['player_2'].strip().title()
            match_data['date'] = row['date']
            match_data['location'] = row['location'].strip().title()
            match_data['championship'] = row['championship'].strip().title()
            match_data['age_group'] = row['age_group'].strip().title()
            match_data['stage'] = row['stage'].strip()
            match_data['event'] = row['event'].strip().title()
            match_data['gender'] = row['gender'].strip().title()
            match_data['club_1'] = row['club_1'].strip()
            match_data['club_2'] = row['club_2'].strip()
            line_count += 1

        else:
            # Edit the points
            match_data['points_1'] = int(row['player_1'])
            match_data['points_2'] = int(row['player_2'])
            
            # Edit sets    
            if row['player_1'] == 0 and row['player_2'] == 0:
                if match_data['lead'] == 'first':
                    match_data['sets_1'] += 1
                    match_data['sets'] += 1
                elif match_data['lead'] == 'second':
                    match_data['sets_2'] += 1
                    match_data['sets'] += 1
                    
            # Edit the lead
            if int(row['player_1']) > int(row['player_2']):
                match_data['lead'] = 'first'
            elif int(row['player_1']) < int(row['player_2']):
                match_data['lead'] = 'second'
            else:
                match_data['lead'] = 'draw'
                
        create_image(match_data)   
    create_txt(match_data) 
    create_thumbnail(match_data)

# Define the window
window = tk.Tk()
window.title('Scoreboard Generator')
window.eval("tk::PlaceWindow . center")

# GUI elements

frame1 = tk.Frame(window, width=960, height=540, bg=bg_color) 
frame1.grid(row=0, column=0)
# preventchild from modifying parent
frame1.pack_propagate(False)

# frame1 widgets
logo_img = ImageTk.PhotoImage(file="src/logo.png")
logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
logo_widget.image = logo_img
logo_widget.pack()

tk.Label(
    frame1,
    text="Scoreboard Generator",
    bg=bg_color,
    fg=fg_color,
    font=("TkMenuFont",14)
    ).pack()

tk.Button(
    frame1,
    text='BROWSE CSV',
    font=("TkHeadingFont", 16),
    bg=accent_color,
    fg=fg_color,
    cursor="hand2",
    activebackground=active_color,
    activeforeground=bg_color,
    command=import_excel_data
    ).pack(pady=5)

tk.Button(
    frame1,
    text='BROWSE SCOREBOARD',
    font=("TkHeadingFont", 16),
    bg=accent_color,
    fg=fg_color,
    cursor="hand2",
    activebackground=active_color,
    activeforeground=bg_color,
    command=import_image
    ).pack(pady=5)

tk.Button(
    frame1,
    text='BROWSE SCREENSHOT',
    font=("TkHeadingFont", 16),
    bg=accent_color,
    fg=fg_color,
    cursor="hand2",
    activebackground=active_color,
    activeforeground=bg_color,
    command=import_screenshot
    ).pack(pady=5)

tk.Button(
    frame1,
    text='OUTPUT FOLDER',
    font=("TkHeadingFont", 16),
    bg=accent_color,
    fg=fg_color,
    cursor="hand2",
    activebackground=active_color,
    activeforeground=bg_color,
    command=set_output_folder
    ).pack(pady=5)

tk.Button(
    frame1,
    text='START GENERATING',
    font=("TkHeadingFont", 16),
    bg=fg_color,
    fg=bg_color,
    cursor="hand2",
    activebackground=accent_color,
    activeforeground=fg_color,
    command=start_generating
    ).pack(pady=5)

window.mainloop()


    
