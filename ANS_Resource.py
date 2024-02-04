from IPython.display import display, Image, clear_output, HTML
import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import ipywidgets as widgets
from jupyter_ui_poll import ui_events

event_info = {
    'type': '',
    'description': '',
    'time': -1
    }

# Wait for event function
def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):    
    """
    Waits for button press
    
    Args:
        timeout
        interval
        max_rate
        allow_interupt
    
    Returns:
        event_info
    """
    start_wait = time.time()
    # Defining buttons/widgets & dictionaries to hold results
    # set event info to be empty
    # as this is dict we can change entries
    # directly without using
    # the global keyword
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            # add pause before looping
            # to check events again
            time.sleep(interval)
    
    # return event description after wait ends
    # will be set to empty string '' if no event occured
    return event_info
    
# this function lets buttons 
# register events when clicked
def register_btn_event(btn):
    """
    Defines the Button Event
    
    Args:
        btn
    
    Returns:
    NAN
    """

    # Defining buttons/widgets & dictionaries to hold results    
    event_info['type'] = "button click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

# Function to send user data to a google form
def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form 
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

def single_ans_test():
    """
    Runs the entire ANS Test
    
    Arg:
    NAN
    
    Returns:
    User's final score
    """
    
    # Defining variables and buttons
    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdZ8_rvGoTnt4F5J_2jYSXv1cyikRP6IUdHkIX1ziUH2pVAig/viewform?usp=sf_link'
    random.seed(1)

    # Defining the image variables for the ANS test
    # 4:3 images
    test12_9 = Image("9_12.png", width = 600)
    test16_12 = Image("16_12.png", width = 600)
    test20_15 = Image("20_15.png", width = 600)
    # 7:6 images
    test14_12 = Image("14_12.png", width = 600)
    test21_18 = Image("18_21.png", width = 600)
    test6_7 = Image("6_7.png", width = 600)
    # 9:8 images
    test18_16 = Image("18_16.png", width = 600)
    # 10:9 images
    test10_9 = Image("10_9.png", width = 600)
    test20_18 = Image("18_20.png", width = 600)
    blank_placeholder = Image("blank_placeholder.png", width = 600)
    # New
    # 5:4 images
    test4_5 = Image("4_5.png", width = 600)
    test8_10 = Image("8_10.png", width = 600)
    test16_20 = Image("16_20.png", width = 600)
    # 6:5 images
    test6_5 = Image("6_5.png", width = 600)
    test12_10 = Image("12_10.png", width = 600)
    test12_15 = Image("12_15.png", width = 600)
    test18_15 = Image("18_15.png", width = 600)

    # Extra images
    test6_8 = Image("6_8.png", width = 600)
    test9_8 = Image("9_8.png", width = 600)
    test18_24 = Image("18_24.png", width = 600)
    test8_7 = Image("8_7.png", width = 600)
    test3_1 = Image("3_1.png", width = 600)


    # List of all ANS images used for reshuffling later
    ans_images_global = []
    ans_images_global.append(test12_9)
    ans_images_global.append(test16_12)
    ans_images_global.append(test20_15)
    ans_images_global.append(test14_12)
    ans_images_global.append(test21_18)
    ans_images_global.append(test18_16)
    ans_images_global.append(test10_9)
    ans_images_global.append(test20_18)
    ans_images_global.append(test4_5)
    ans_images_global.append(test8_10)
    ans_images_global.append(test16_20)
    ans_images_global.append(test6_5)
    ans_images_global.append(test12_10)
    ans_images_global.append(test12_15)
    ans_images_global.append(test18_15)
    ans_images_global.append(test6_7)
    ans_images_global.append(test6_8)
    ans_images_global.append(test9_8)
    ans_images_global.append(test18_24)
    ans_images_global.append(test8_7)

    # Correct answers dictionary
    ans_answers_global = {test12_9:'r', test16_12:'l', test20_15:'l', test14_12:'l', test21_18:'r', test18_16:'l',
                         test10_9:'l', test20_18:'r', test4_5:'r', test8_10:'r', test16_20:'r', test6_5:'l', test12_10:'l',
                         test12_15:'r', test18_15:'l', test6_7:'r', test6_8:'r', test9_8:'l', test18_24:'r', test8_7:'l'}
    # For converting the cycled test to a str for easy identification of question
    ans_conversions_global = {test12_9:'9_12', test16_12:'16_12', test20_15:'20_15', test14_12:'14_12', 
                              test21_18:'18_21', test18_16:'18_16', test10_9:'10_9', test20_18:'18_20', test4_5:'4_5', 
                              test8_10:'8_10', test16_20:'16_20', test6_5:'6_5', test12_10:'12_10', test12_15:'12_15', 
                              test18_15:'18_15', test6_7:'6_7', test6_8:'6_8', test9_8:'9_8', test18_24:'18_24', test8_7:'8_7'}
    # For converting the test question id to a str for easy identification of which question's time recording
    ans_timeconversions_global = {test12_9:'time9_12', test16_12:'time16_12', test20_15:'time20_15', test14_12:'time14_12', 
                              test21_18:'time18_21', test18_16:'time18_16', test10_9:'time10_9', test20_18:'time18_20', test4_5:'time4_5', 
                              test8_10:'time8_10', test16_20:'time16_20', test6_5:'time6_5', test12_10:'time12_10', test12_15:'time12_15', 
                              test18_15:'time18_15', test6_7:'time6_7', test6_8:'time6_8', test9_8:'time9_8', test18_24:'time18_24', test8_7:'time8_7'}

    # Temp holds users answers for upload to google form
    #user_id_dict = {'user_id': ''}
    user_answers_dict = {
        'user_id': '',
        'age': '',
        'education':'',
        'ms':'',
        'total_time': '',
        '9_12': '',
        'time9_12': '',
        '16_12': '',
        'time16_12': '',
        '20_15': '',
        'time20_15': '',
        '14_12': '',
        'time14_12': '',
        '18_21': '',
        'time18_21': '',
        '18_16': '',
        'time18_16': '',
        '10_9': '',
        'time10_9': '',
        '18_20': '',
        'time18_20': '',
        '4_5': '',
        'time4_5': '',
        '8_10': '',
        'time8_10': '',
        '16_20': '',
        'time16_20': '',
        '6_5': '',
        'time6_5': '',
        '12_10': '',
        'time12_10': '',
        '12_15': '',
        'time12_15': '',
        '18_15': '',
        'time18_15': '',
        '6_7': '',
        'time6_7': '',
        '6_8': '',
        'time6_8': '',
        '9_8': '',
        'time9_8': '',
        '18_24': '',
        'time18_24': '',
        '8_7': '',
        'time8_7': ''
    }
    
    
    images_list = ans_images_global.copy()
    random.shuffle(images_list)
    score = 0
    total_time = 0
    btn1 = widgets.Button(description="Left")
    btn2 = widgets.Button(description="Right")
    btn1.on_click(register_btn_event)
    btn2.on_click(register_btn_event)
    panel = widgets.HBox([btn1, btn2])
    
    # Asking for User Agreement
    data_consent_info = """DATA CONSENT INFORMATION:
    
    Please read:
    
    We wish to record your response data
    
    to an anonymised public data repository.
    
    Your data will be used for educational teaching purposes
    
    practising data analysis and visualisation.
    
    Please type yes in the box below if you consent to the upload."""

    print(data_consent_info)
    result = input("> ")
    clear_output(wait=True)
    if result == "yes":
        print("Thanks for your participation.")
        print("Please contact philip.lewis@ucl.ac.uk")
        print("If you have any questions or concerns")
        print("regarding the stored results.")
    else:
        # end code execution by raising an exception
        raise(Exception("User did not consent to continue test."))
    time.sleep(5)
    clear_output(wait=True)
    
    # Creating a Unique User ID
    id_instructions = """

    Enter your anonymised ID
    
    To generate an anonymous 4-letter unique user identifier please enter:
    
    - two letters based on the initials (first and last name) of a childhood friend
    
    - two letters based on the initials (first and last name) of a favourite actor / actress
    
    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
    
    then your unique identifer would be CBTC

    """

    print(id_instructions)
    
    user_answers_dict['user_id'] = input("> ")
    clear_output(wait=True)
    print("User entered id:", user_answers_dict['user_id'])
    
    time.sleep(4)
    clear_output(wait=True)
    
    print("Enter your age:")
    user_answers_dict['age'] = input("> ")
    clear_output(wait=True)
    
    print("What is the highest educational level you have undertaken or are currently undergoing?")
    print("E.g. high school, undergraduate, postgraduate, doctorate, or prefer not to answer")
    user_answers_dict['education'] = input("> ")
    clear_output(wait=True)
    
    print("What is your level of experience with math or sciences?")
    print("""E.g. None, high school, undergraduate introductory, undergraduate advanced, postgraduate,
    professional/research, or prefer not to answer""")
    user_answers_dict['ms'] = input("> ")
    clear_output(wait=True)
    
    print("""Welcome to the ANS test\n
    Two dot arrays with different numbers of dots will be flashed on screen quickly.\n
    Please judge as quickly and accurately which of the arrays contains a greater number of dots.\n
    Please press the button left or right to select your answer.
    """)
    time.sleep(6)
    clear_output(wait=False)
    
    # User Practice Questions
    print("A practice questions will now be shown to help you better understand the test")
    time.sleep(2)
    print("Practice Test starting in:")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    clear_output(wait=False)
    
    # Showing ANS Test Picture
    # Show buttons
    display(panel)
    display(test3_1)
    time.sleep(0.75)
    clear_output(wait=True)
    # Show buttons
    display(panel)
    display(blank_placeholder)
    result = wait_for_event(timeout = 3)
    
    # Checking if test answer is correct
    if result['description'] == 'Left':
        clear_output(wait=False)
        print('Correct!')
    elif result['description'] == 'Right':
        clear_output(wait=False)
        print("Incorrect, please choose the array with more dots")
    elif result['description'] == '':
        clear_output(wait=False)
        print("No button was pressed! Answer more quickly")
    time.sleep(2.5)
    clear_output(wait=False)
    
    print("The real test will now start in:")
    time.sleep(2.5)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    clear_output(wait=False)
    
    for i in images_list:
        # Variable recording which question/picture is being shown
        question_id = ans_conversions_global[i]
        time_id = ans_timeconversions_global[i]
        
        # Showing ANS pictures
        clear_output(wait=True)
        # Show buttons
        display(panel)
        
        display(i)
        time.sleep(0.75)
        clear_output(wait=True)
        # Show buttons
        display(panel)
        display(blank_placeholder)      
        
        # Implementing buttons and waiting for input
        #display(panel)
        start_time = time.time()
        result = wait_for_event(timeout = 3)
        end_time = time.time()
        time_taken = end_time - start_time
        total_time += time_taken
        clear_output(wait=True)
        display(blank_placeholder)
        # Recording time taken for each question
        user_answers_dict[time_id] = time_taken
        
        # Recording user decision and confirming whether correct
        if result['description'] == 'Left':
            answer = 'l'
            if answer == ans_answers_global[i]:
                score += 1
                user_answers_dict[question_id] = True
            elif answer != ans_answers_global[i]:
                user_answers_dict[question_id] = False
                
        elif result['description'] == 'Right':
            answer = 'r'
            if answer == ans_answers_global[i]:
                score += 1
                user_answers_dict[question_id] = True
            elif answer != ans_answers_global[i]:
                user_answers_dict[question_id] = False
        elif result['description'] == '':
            print("No button was pressed! Answer more quickly")
            user_answers_dict[question_id] = 'NA'

        time.sleep(1.5)

    # Sending dictionary of user answers to google form
    user_answers_dict['total_time'] = total_time
    send_to_google_form(user_answers_dict, form_url)
    clear_output(wait=False)
    print(f"Your approximation for {score} of the {len(images_list)} image arrays were correct.")
    print("Thank you so much for participating in my test! Have a good day!")
    return
