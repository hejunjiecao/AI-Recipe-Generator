import setting
import gpt

def generate_recipe_from_ingredients(ingredients, style):
	three_res = []
	msgs = []
	rcp_prompt_sys = 'You are a excellent chef and familiar with different food style. You are not only good at developing new dishes.'
	rcp_prompt_usr = f"You will be given a JSON object for food ingredients with fields for their names and quantity.\nYou will create a recipe for a dish in {style} sytle using the following given ingredients:\n```{ingredients}```\nYour reply will be a JSON object with fields for 'dishName', 'timeToPrepare' and 'Steps'.\n\t'dishName' field represents the name of the generated dish. \n\t'timeToPrepare' indicates the total time required to prepare and cook the dish.\n\t'Steps' is a list of steps that describe the cooking process.\nEach step is a string detailing a specific action to be taken."
	# TEST user_prompt
	print(rcp_prompt_usr)
	# END OF TEST user_prompt
	sys_msg = gpt.GPTMsg('system', rcp_prompt_sys)
	usr_msg = gpt.GPTMsg('user', rcp_prompt_usr)
	msgs.append(sys_msg)
	msgs.append(usr_msg)
	myGPT = gpt.MyGPT(setting.configs)
	for i in range(3):
		result, reply = gpt.process_response(myGPT.query(msgs), myGPT.model)
		if not result:
			print("Error when generating recipe! See the deatils below.")
			return ["Error from recipe generator"]
		three_res.append(reply)
	return three_res
