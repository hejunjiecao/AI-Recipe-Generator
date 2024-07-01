import json

import setting
import gpt

def generate_recipe_from_ingredients(ingredients, style):
	three_res = []
	msgs = []
	rcp_prompt_sys = 'You are a excellent chef and familiar with different food style. You are not only good at existing food recites, but also developing new dishes.'

	rcp_prompt_usr = ""
	if ingredients == "[]":
		rcp_prompt_usr = f"You will create a recipe for a dish in {style} sytle using random food ingredients"
	else:
		rcp_prompt_usr = f"You will be given a list of food ingredients with fields for their names and quantity.\nYou will create a recipe for a dish in {style} sytle using the following given ingredients:\n{ingredients}\n"
	rcp_prompt_usr += "Your reply will be in JSON format. The reply will only be a JSON object, starting with '''json and and with ''', with fields for 'dishName', 'timeToPrepare', 'ingredients' and 'Steps'.\n\t'dishName' field represents the name of the generated dish. \n\t'timeToPrepare' indicates the total time required to prepare and cook the dish.\n\t\'ingredients' is dictionary object of food ingredients needed for this dish, with name of the food ingredients as keys and their required amount as values.\n\t'Steps' is a list of steps that describe the cooking process.\nEach step is a string detailing a specific action to be taken without enumeration markers."

	sys_msg = gpt.GPTMsg('system', rcp_prompt_sys)
	usr_msg = gpt.GPTMsg('user', rcp_prompt_usr)
	msgs.append(sys_msg)
	msgs.append(usr_msg)

	# Generate three recipes using different temperature 
	for i in range(3):
		setting.configs["temperature"]  = str(1 + (0.5 * i))
		myGPT = gpt.MyGPT(setting.configs)
		result, reply = gpt.process_response(myGPT.query(msgs), myGPT.model)
		if not result:
			print("Error when generating recipe %i! See the deatils below.", (i+1))
			reply = ""
		three_res.append(reply)
	return three_res
