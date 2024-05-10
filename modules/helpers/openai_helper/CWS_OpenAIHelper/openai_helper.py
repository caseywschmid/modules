import os
from importlib.metadata import version

# ------ CONFIGURE LOGGING ------
import logging

try:
    # if running the code from the package itself
    if os.getenv("OPENAI_HELPER_PACKAGE_TEST", "False").lower() in ("true", "1", "t"):
        from modules.logs.logger.CWS_Logger import logger
    else:
        # if running the code as an imported package in another project
        from CWS_Logger import logger  # type: ignore
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "The necessary 'Logger' module is not installed. Please install it by running \n'pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger'"
    )

logger.configure_logging(__name__)
log = logging.getLogger(__name__)

if os.getenv("OPENAI_HELPER_PACKAGE_TEST", "False").lower() in ("true", "1", "t"):
    log.info("Running in test mode.")

import json
from openai import OpenAI
from typing import List, Optional, Annotated, Dict, Any, Union, Iterable
import base64
from openai.types.chat_model import ChatModel
from openai.types.chat.completion_create_params import ResponseFormat
from openai.types.chat.chat_completion_tool_choice_option_param import (
    ChatCompletionToolChoiceOptionParam,
)
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_content_part_param import (
    ChatCompletionContentPartParam,
)
from openai.types.chat.chat_completion_content_part_text_param import (
    ChatCompletionContentPartTextParam,
)
from openai.types.chat.chat_completion_content_part_image_param import (
    ChatCompletionContentPartImageParam,
    ImageURL,
)
from openai._types import NotGiven, NOT_GIVEN

OPENAI_VERSION = "1.25.1"

class OpenAIHelper:

    def __init__(
        self,
        api_key: Annotated[str, "The OpenAI API Key you wish to use"],
        organization: str,
    ):
        self.client = OpenAI(api_key=api_key, organization=organization)
        self.check_dependency_versions()

    def check_dependency_versions(self):
        current_openai_version = version("openai")
        # Check if the warning should be muted
        mute_warning = os.getenv("MUTE_OPENAI_HELPER_WARNING", "False").lower() in (
            "true",
            "1",
            "t",
        )

        if not mute_warning and current_openai_version != OPENAI_VERSION:
            log.warning(
                f"The 'OpenAIHelper' tool was created using openai version {OPENAI_VERSION}. The version you have installed in this project ({current_openai_version}) may not be compatible with this tool. If you encounter any issues, either downgrade your BeautifulSoup version to 4.12.3 or email the creator at caseywschmid@gmail.com to have the package updated."
            )
            log.info(
                "This warning can be muted by setting the MUTE_OPENAI_HELPER_WARNING environment variable to 'True'."
            )

    def create_chat_completion(
        self,
        prompt: str,
        images: Optional[
            Annotated[List[str], "The list of image paths you want to pass in"]
        ] = None,
        system_message: Optional[
            Annotated[
                str,
                "The system message you want to pass in.",
            ]
        ] = None,
        model: Union[str, ChatModel] = "gpt-4-turbo",
        stream: bool = False,
        json_mode: bool = False,
        max_tokens: Optional[int] | None = 4000,
        temperature: Optional[float] | None = 0,
        n: Optional[int] | None = 1,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
    ) -> Union[Dict[str, Any], str]:
        """
        Creates a chat completion using the specified parameters and returns the
        response from the OpenAI API.

        This method prepares a chat completion request by encoding any provided
        images to base64 and appending them to the prompt. It then sends this
        data to the OpenAI API and returns the response, optionally in JSON
        format.

        Parameters
        ----------
         - prompt: The text prompt to send to the chat completion API.

         - images : A list of local image paths. These images will be encoded to
           base64 and included in the chat completion request.

         - system_message: An optional system message to include in the chat
           completion request. Defaults to None.

         - json_mode : bool, optional If True, the response from the OpenAI API
           will be returned as a JSON object. Defaults to False. If you set this
            to True, you must also tell the LLM to output JSON as its response
            in the prompt or system message.

         - model: ID of the model to use. Defaults to "gpt-4-turbo".

         - stream: If set, partial message deltas will be sent, like in ChatGPT.
           Tokens will be sent as data-only [server-sent
           events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
           as they become available, with the stream terminated by a `data:
           [DONE]` message. [Example Python
           code](https://cookbook.openai.com/examples/how_to_stream_completions).

         - frequency_penalty: Number between -2.0 and 2.0. Positive values
           penalize new tokens based on their existing frequency in the text so
           far, decreasing the model's likelihood to repeat the same line
           verbatim. [See more information about frequency and presence
           penalties.](https://platform.openai.com/docs/guides/text-generation/parameter-details)

         - logit_bias: Modify the likelihood of specified tokens appearing in
           the completion. Accepts a JSON object that maps tokens (specified by
           their token ID in the tokenizer) to an associated bias value from
           -100 to 100. Mathematically, the bias is added to the logits
           generated by the model prior to sampling. The exact effect will vary
           per model, but values between -1 and 1 should decrease or increase
           likelihood of selection; values like -100 or 100 should result in a
           ban or exclusive selection of the relevant token.

         - logprobs: Whether to return log probabilities of the output tokens or
           not. If true, returns the log probabilities of each output token
           returned in the `content` of `message`.

         - max_tokens: The maximum number of [tokens](/tokenizer) that can be
           generated in the chat completion. The total length of input tokens
           and generated tokens is limited by the model's context length.
           [Example Python
           code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
           for counting tokens.

         - n: How many chat completion choices to generate for each input
           message. Note that you will be charged based on the number of
           generated tokens across all of the choices. Keep `n` as `1` to
           minimize costs.

         - presence_penalty: Number between -2.0 and 2.0. Positive values
           penalize new tokens based on whether they appear in the text so far,
           increasing the model's likelihood to talk about new topics. [See more
           information about frequency and presence
           penalties.](https://platform.openai.com/docs/guides/text-generation/parameter-details)

         - response_format: An object specifying the format that the model must
           output. Compatible with [GPT-4 Turbo]
           (https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) and
           all GPT-3.5 Turbo models newer than `gpt-3.5-turbo-1106`. Setting to
           `{ "type": "json_object" }` enables JSON mode, which guarantees the
           message the model generates is valid JSON. **Important:** when using
           JSON mode, you **must** also instruct the model to produce JSON
           yourself via a system or user message. Without this, the model may
           generate an unending stream of whitespace until the generation
           reaches the token limit, resulting in a long-running and seemingly
           "stuck" request. Also note that the message content may be partially
           cut off if `finish_reason="length"`, which indicates the generation
           exceeded `max_tokens` or the conversation exceeded the max context
           length.

         - seed: This feature is in Beta. If specified, our system will make a
           best effort to sample deterministically, such that repeated requests
           with the same `seed` and parameters should return the same result.
           Determinism is not guaranteed, and you should refer to the
           `system_fingerprint` response parameter to monitor changes in the
           backend.

         - stop: Up to 4 sequences where the API will stop generating further
           tokens.

         - temperature: What sampling temperature to use, between 0 and 2.
           Higher values like 0.8 will make the output more random, while lower
           values like 0.2 will make it more focused and deterministic. We
           generally recommend altering this or `top_p` but not both.

         - tool_choice: Controls which (if any) function is called by the model.
           `none` means the model will not call a function and instead generates
           a message. `auto` means the model can pick between generating a
           message or calling a function. Specifying a particular function via
           `{"type": "function", "function": {"name": "my_function"}}` forces
           the model to call that function. `none` is the default when no
           functions are present. `auto` is the default if functions are
           present.

         - tools: A list of tools the model may call. Currently, only functions
           are supported as a tool. Use this to provide a list of functions the
           model may generate JSON inputs for. A max of 128 functions are
           supported.

         - top_logprobs: An integer between 0 and 20 specifying the number of
           most likely tokens to return at each token position, each with an
           associated log probability. `logprobs` must be set to `true` if this
           parameter is used.

         - top_p: An alternative to sampling with temperature, called nucleus
           sampling, where the model considers the results of the tokens with
           top_p probability mass. So 0.1 means only the tokens comprising the
           top 10% probability mass are considered. We generally recommend
           altering this or `temperature` but not both.

         - user: A unique identifier representing your end-user, which can help
           OpenAI to monitor and detect abuse. [Learn
           more](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

         - timeout: Override the client-level default timeout for this request,
           in seconds

        Returns
        -------
        dict or str
            The response from the OpenAI API. Returns a dictionary if json_mode
            is True, otherwise returns a string.
        """
        log.fine("OpenAIHelper.create_chat_completion")
        completion_params = {
            "messages": None,
            "model": model,
            "stream": stream,
            "frequency_penalty": frequency_penalty,
            "logit_bias": logit_bias,
            "logprobs": logprobs,
            "max_tokens": max_tokens,
            "n": n,
            "presence_penalty": presence_penalty,
            "response_format": response_format,
            "seed": seed,
            "stop": stop,
            "temperature": temperature,
            "tool_choice": tool_choice,
            "tools": tools,
            "top_logprobs": top_logprobs,
            "top_p": top_p,
            "user": user,
        }
        # Create the messages
        messages: List[ChatCompletionMessageParam] = []
        if system_message:
            system_message_param = ChatCompletionSystemMessageParam(
                role="system", content=system_message
            )
            messages.append(system_message_param)

        user_message_content: List[ChatCompletionContentPartParam] = []

        text_param: ChatCompletionContentPartTextParam = {
            "type": "text",
            "text": prompt,
        }

        user_message_content.append(text_param)

        if images:
            for image in images:
                image_base64 = self.encode_image(image)
                image_url: ImageURL = {
                    "url": f"data:image/jpeg;base64,{image_base64}",
                    # Optionally specify "detail" if needed, e.g., "detail": "high"
                }
                image_param: ChatCompletionContentPartImageParam = {
                    "type": "image_url",
                    "image_url": image_url,
                }
                user_message_content.append(image_param)

        # Create the user message
        user_message_param: ChatCompletionUserMessageParam = {
            "role": "user",
            "content": user_message_content,
        }

        messages.append(user_message_param)

        completion_params["messages"] = messages

        # If json_mode is enabled, adjust the response_format accordingly
        if json_mode:
            completion_params["response_format"] = {"type": "json_object"}

        # Filter out None values
        completion_params = {
            k: v for k, v in completion_params.items() if v is not None
        }

        # Filter out NotGiven values and potentially problematic parameters for debugging
        completion_params = {
            k: v for k, v in completion_params.items() if v is not NOT_GIVEN
        }

        response: Any = self.client.chat.completions.create(**completion_params)

        content = response.choices[0].message.content
        if json_mode:
            content = json.loads(content)

        return content

    @staticmethod
    def encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
