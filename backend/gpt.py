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
        if msg.role == 'user':
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

if __name__ == '__main__':
    print(setting.config_path)
    for key, value in setting.configs.items():
        print(key, ':', value)
    myGPT = MyGPT(setting.configs)
    user_msg = GPTMsg('user', 'Tell me how good is restaurant shown in the image', [setting.Path(setting.root_dir) / 'uploads' /'test_image.jpg'])
    msgs = []
    msgs.append(user_msg)

    response = myGPT.query(msgs)
    # print(response['choices'][0]['message']['content'])
    print(response)
    # result, reply = process_response(...)
    # if not result:
    #   print("Error! See the deatils below.")
    # print(reply)
