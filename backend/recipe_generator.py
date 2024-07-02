import re

import setting
import gpt

def modify_usr_prompt_based_on_creativity(msgs, rcp_prompt_usr, idx):
	if idx == 0:
		rcp_prompt_usr_creativity = rcp_prompt_usr
	if idx == 1:
		rcp_prompt_usr_creativity = re.sub('<creativeExtent>', 'creative', rcp_prompt_usr)
	if idx == 2:
		rcp_prompt_usr_creativity = re.sub('<creativeExtent>', 'very creative', rcp_prompt_usr)
	usr_msg = gpt.GPTMsg('user', rcp_prompt_usr_creativity)
	msgs.append(usr_msg)
	return (msgs)

def generate_recipe_from_ingredients(ingredients, style):
	three_res = []
	msgs = []
	rcp_prompt_sys = 'You are a excellent chef and familiar with different food style. You are not only good at existing food recipes, but also developing new dishes.'

	rcp_prompt_usr = ""
	if ingredients == "[]":
		rcp_prompt_usr = f"You will create a recipe for a dish in {style} sytle using random food ingredients"
	else:
		rcp_prompt_usr = f"You will be given a list of food ingredients with fields for their names and quantity.\nYou will generate a <creativeExtent> recipe for a dish in {style} sytle using the following given ingredients:\n{ingredients}\nIf there are non-food ingredients in the list {ingredients}, ignore them."
	rcp_prompt_usr += "Your reply will be in JSON format. The reply will only be a JSON object, starting with '''json and end with ''', with fields for 'dishName', 'timeToPrepare', 'ingredients' and 'Steps'.\n\t'dishName' field represents the name of the generated dish. \n\t'timeToPrepare' indicates the total time required to prepare and cook the dish.\n\t\'ingredients' is dictionary object of food ingredients needed for this dish, with name of the food ingredients as keys and their required amount as values.\n\t'Steps' is a list of steps that describe the cooking process.Each step is a string detailing a specific action to be taken without enumeration markers."
	sys_msg = gpt.GPTMsg('system', rcp_prompt_sys)
	msgs.append(sys_msg)

	for i in range(3):
		msg_based_on_creativity = modify_usr_prompt_based_on_creativity(msgs, rcp_prompt_usr, i)
		setting.configs["temperature"]  = 1 + (0.5 * i)
		myGPT = gpt.MyGPT(setting.configs)
		result, reply = gpt.process_response(myGPT.query(msg_based_on_creativity), myGPT.model)
		if not result:
			print("Error when generating recipe %i! See the deatils below." % (i+1))
			# TEST reply
			print(reply)
			# END OF TEST
			reply = ""
		# TEST reply
		print(reply)
		# END OF TEST
		three_res.append(reply)
	return three_res

if __name__ == '__main__':
	three_res = generate_recipe_from_ingredients(ingredients = '["grapes","tofu","cheese spread"]', style="any")
