import setting

class GPTMsg:

  def __init__(self, role, prompt, imgs=None):
    assert role in ['user', 'system', 'assistant']
    self.role = role
    self.prompt = prompt
    self.imgs = imgs


class MyGPT:

    def __init__(self, configs=None):
        if configs is not None:
            for key, value in configs.items():
                setattr(self, key, value)

    @staticmethod
    def encode_image(img_path):
      # open the image in correct mode, encode into base64 binary format and return it.
      img = open(img_path, 'rb')
      encoded_img = setting.base64.b64encode(img.read()).decode('utf-8')
      return encoded_img

    def compose_content(self, prompt, img_paths):
      content = [
          {
              "type": "text",
              "text": prompt
          }
      ]
      print(img_paths)
      if img_paths == None:
         return content
      for img_path in img_paths:
        # encode the image
        b64_img = self.encode_image(img_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64_img}"
            }
        })

      return content

    def query(self, msgs):
      print(self.model)
      encoded_msgs = []
      for msg in msgs:
        # if (msg.imgs) != None:
        content = self.compose_content(msg.prompt, msg.imgs)
        encoded_msgs.append({
            "role": msg.role,
            "content": content
        })

      headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {self.api_key}"
      }

      payload = {
        "model": self.model,
        "messages": encoded_msgs,
        "max_tokens": self.max_tokens,
      }

      response = setting.requests.post(self.api_base, headers=headers, json=payload).json()
      return response

def process_response(response, GPTModel):
  # Intended behaviour of this function:
  # returns True, "textual reply from GPT", and prints the cost at the same time
  # OR returns False, "reason why the error occurs"
  print("response: ")
  print(response)
  if "error" not in response:
    usage = response["usage"]
    prompt_tokens = usage["prompt_tokens"]
    completion_tokens = usage["completion_tokens"]

    if GPTModel == 'gpt-3.5-turbo':
      prompt_cost = prompt_tokens / 1000000 * 0.5
      response_cost = completion_tokens / 1000000 * 1.5
      print(f"This round costs ${'{0:.5f}'.format(prompt_cost + response_cost)}")

    elif GPTModel == 'gpt-4-turbo':
      prompt_cost = prompt_tokens / 1000000 * 10
      response_cost = completion_tokens / 1000000 * 30
      print(f"This round costs ${'{0:.5f}'.format(prompt_cost + response_cost)}")

    elif GPTModel == 'gpt-4o':
      prompt_cost = prompt_tokens / 1000000 * 5
      response_cost = completion_tokens / 1000000 * 15
      print(f"This round costs ${'{0:.5f}'.format(prompt_cost + response_cost)}")
    else:
      return False, response["error"]["message"]

    return True, response['choices'][0]['message']['content']
  else:
    return False, response["error"]["message"]

if __name__ == '__main__':
    print(setting.config_path)
    for key, value in setting.configs.items():
        print(key, ':', value)
    myGPT = MyGPT(setting.configs)
    user_msg = GPTMsg('user', 'Generate a recipe based on the ingredients on the image', [setting.Path(setting.root_dir) / 'uploads' /'test_image.jpg'])
    msgs = []
    msgs.append(user_msg)

    result, reply = process_response(myGPT.query(msgs), myGPT.model)
    if not result:
      print("Error! See the deatils below.")
    print(reply)
    # reply = myGPT.query(msgs)
    # print(reply)