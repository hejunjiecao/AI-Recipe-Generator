import re

import setting
import gpt

def recognize_food_ingredients(upload_folder, save_path):
    myGPT = gpt.MyGPT(setting.configs)
    msgs = []
    insctruct_prompt = "Your task is to recognize the annotated food ingrediants in the picture. \
        If there is no annotation, recongize all the food ingrediants. \
        As reply only list the recoginzed food ingredients quoted in square brackets and each of them is quoted with double quotes and seperated with a comma. If there are only non-food items recognized, reply me only []"
    user_msg= gpt.GPTMsg('user', insctruct_prompt)
    example_prompt = 'I will give you two examples. \
        Q1: Recognize the annotated food ingrediants in first picture. \
        If there is no annotation, recongize all the food ingrediants. \
        A1: ["aubergine","chicken wings"] \
        Q2: Recognize the annotated food ingrediants in second picture. \
        If there is no annotation, recongize all the food ingrediants. \
        A2: ["aubergine","romaine lettuce","chicken wings","red bell pepper"]'
    example_msg = gpt.GPTMsg('user', example_prompt, [setting.Path(setting.root_dir) / upload_folder / 'origin' / 'test1.jpg', setting.Path(setting.root_dir) / upload_folder / 'origin' / 'test2.jpg'])
    task_prompt = 'Q3: Recognize the annotated food ingrediants in second picture. \
        If there is no annotation, recongize all the food ingrediants. \
        A3:'
    task_msg = gpt.GPTMsg('user', task_prompt, [setting.Path(setting.root_dir) / save_path])
    msgs.append(user_msg)
    msgs.append(example_msg)
    msgs.append(task_msg)

    result, reply = gpt.process_response(myGPT.query(msgs), myGPT.model)
    if not result:
        print("Error! See the details below.")
    print(reply)
    match = re.search(r'\[.*\]', reply)
    if match:
        cleaned_reply = match.group(0)
    else:
        cleaned_reply = "[]"
    return (cleaned_reply)
