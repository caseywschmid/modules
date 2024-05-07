# OpenAIHelper Documentation

The `OpenAIHelper` class is a helper module for interacting with the OpenAI API.
I made this to simplify the process of creating chat completions. I kept all the
functionality currently in the OpenAI module. 

## Requirements

This package depends on a custom Logger. To install the Logger package, run the
following command:

```terminal
pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger
```

Note: You will receive an error if you try to run the OpenAIHelper without first
installing the Logger package.

## Installation

Install the package directly from GitHub:

```terminal
pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/helpers/openai_helper
```


## Methods

Methods
### `__init__()`
This is the constructor method for the OpenAIHelper class.

- **Parameters:**
  - `api_key` (str): The OpenAI API Key you wish to use.
  - `organization` (str): The organization ID for the OpenAI API.

### `create_chat_completion()`
This method creates a chat completion using the specified parameters and returns the response from the OpenAI API.

- **Parameters:**
  - `prompt` (str): The text prompt to send to the chat completion API.
  - `images` (list): A list of local image paths. These images will be encoded to base64 and included in the chat completion request.
  - `system_message` (str): An optional system message to include in the chat completion request.
  - `model` (str): ID of the model to use. Defaults to "gpt-4-turbo".
  - `stream` (bool): If set, partial message deltas will be sent, like in ChatGPT.
  - `json_mode` (bool): If True, the response from the OpenAI API will be returned as a JSON object.
  - `max_tokens` (int): The maximum number of tokens that can be generated in the chat completion.
  - `temperature` (float): What sampling temperature to use, between 0 and 2.
  - `n` (int): How many chat completion choices to generate for each input message.
  - `frequency_penalty` (float): Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far.
  - `logit_bias` (dict): Modify the likelihood of specified tokens appearing in the completion.
  - `logprobs` (int): Whether to return log probabilities of the output tokens or not.
  - `presence_penalty` (float): Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far.
  - `response_format` (dict): An object specifying the format that the model must output.
  - `seed` (int): If specified, our system will make a best effort to sample deterministically.
  - `stop` (list): Up to 4 sequences where the API will stop generating further tokens.
  - `tool_choice` (str): Controls which (if any) function is called by the model.
  - `tools` (list): A list of tools the model may call.
  - `top_logprobs` (int): An integer between 0 and 20 specifying the number of most likely tokens to return at each token position.
  - `top_p` (float): An alternative to sampling with temperature, called nucleus sampling.
  - `user` (str): A unique identifier representing your end-user.
- **Returns:**
  - The response from the OpenAI API. Returns a dictionary if json_mode is True, otherwise returns a string.

### `encode_image()`
This static method encodes an image to base64.

- **Parameters:**
  - `image_path` (str): The path to the image file.
- **Returns:**
  - The base64 encoded string of the image.

## Usage

```python
from CWS_OpenAIHelper.openai_helper import OpenAIHelper

oaih = OpenAIHelper()
result = oaih.create_chat_completion(
    system_message="system message goes here",
    prompt="prompt goes here",
    images = ["path/to/image1", "path/to/image2"],
    json_mode=True
)
```
