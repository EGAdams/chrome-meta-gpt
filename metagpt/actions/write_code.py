#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:45
@Author  : alexanderwu
@File    : write_code.py
"""
from metagpt.actions import WriteDesign
from metagpt.actions.action import Action
from metagpt.const import WORKSPACE_ROOT
from metagpt.logs import logger
from metagpt.schema import Message
from metagpt.utils.common import CodeParser
from tenacity import retry, stop_after_attempt, wait_fixed

from os import sys

PROMPT_TEMPLATE = """
# Context
Provide any necessary background or contextual information here to guide the respondent:
{context}

## Instructions:

### Role:
- Assume the role of a professional engineer.
- Your primary objective is to write Swift code that adheres to PEP8 standards, ensuring the code is elegant, modular, easily readable, and maintainable.

### Code Implementation:
- Implement the code in just one file. Reference the filename using {filename}.
- Rely on existing APIs. If a necessary API doesn't exist, you should implement it.
- Ensure the code you provide is complete, reliable, and reusable, as it will be integrated into a larger project.
- Any settings or configurations in the code should have default values.
- Always use strong typing and explicit variable declarations.
- Follow the provided "Data Structures and Interface Definitions" without making changes to the design.
- Refrain from using public member functions that aren't part of your design.

### Formatting:
- Separate sections using '##' for headers.
- Reference the example format provided to structure your responses.

## Sections to Complete:

## Code Implementation:
Provide the code for the filename {filename}. Ensure it's enclosed within triple quotes and follows the Swift syntax.

```swift
## {filename}
...
```

## Format Example:
Provide an example format to guide the respondent:
...
"""


class WriteCode(Action):
    def __init__(self, name="WriteCode", context: list[Message] = None, llm=None):
        super().__init__(name, context, llm)

    def _is_invalid(self, filename):
        return any(i in filename for i in ["mp3", "wav"])

    def _save(self, context, filename, code):
        # logger.info(filename)
        # logger.info(code_rsp)
        if self._is_invalid(filename):
            return

        design = [i for i in context if i.cause_by == WriteDesign][0]

        ws_name = CodeParser.parse_str(
            block="Swift Package Name", text=design.content)
        ws_path = WORKSPACE_ROOT / ws_name
        if f"{ws_name}/" not in filename and all(i not in filename for i in ["requirements.txt", ".md"]):
            ws_path = ws_path / ws_name
        code_path = ws_path / filename
        code_path.parent.mkdir(parents=True, exist_ok=True)
        code_path.write_text(code)
        logger.info(f"Saving Code to {code_path}")

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    async def write_code(self, prompt):
        code_rsp = await self._aask(prompt)  # call g4 here?
        code = CodeParser.parse_code(block="", text=code_rsp)
        return code

    async def run(self, context, filename):
        prompt = PROMPT_TEMPLATE.format(context=context, filename=filename)
        logger.info(f'Writing {filename}..')
        
        # write this prompt to a markdown file so that we can read it first
        # then we can use the markdown file as the prompt
        file = open("write_code_prompt.md", "w")
        file.write(prompt)
        file.close()
        
        # use a try-except block to catch the exception and retry with 16k model
        try:
            code = await self.write_code(prompt) 
        except Exception as e:
            print( e )
            # check exception details for maximum length exceeded error
            if "maximum length exceeded" in str( e ):
                # switch to 16k model here!
                self.llm.model = "gpt-3.5-turbo-16k"
                code = await self.write_code(prompt)
                self.llm.model = "gpt-3.5-turbo" # switch back to cheaper model

        # code_rsp = await self._aask_v1(prompt, "code_rsp", OUTPUT_MAPPING)
        # self._save(context, filename, code)
        return code
