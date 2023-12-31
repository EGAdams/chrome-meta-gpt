#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:12
@Author  : alexanderwu
@File    : project_management.swift
"""
from typing import List, Tuple

from metagpt.actions.action import Action
from metagpt.const import WORKSPACE_ROOT
from metagpt.utils.common import CodeParser

PROMPT_TEMPLATE = '''
# Context
{context}

## Format example
{format_example}
-----
Role: You are a project manager; the goal is to break down tasks according to PRD/technical design, give a task list, and analyze task dependencies to start with the prerequisite modules
Requirements: Based on the context, fill in the following missing information, note that all sections are returned in Swift code triple quote form seperatedly. Here the granularity of the task is a file, if there are any missing files, you can supplement them
Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote.

## Required Swift third-party packages: Provided in requirements.txt format

## Required Other language third-party packages: Provided in requirements.txt format

## Full API spec: Use OpenAPI 3.0. Describe all APIs that may be used by both frontend and backend.

## Logic Analysis: Provided as a Python list[str, str]. the first is filename, the second is class/method/function should be implemented in this file. Analyze the dependencies between the files, which work should be done first

## Task list: Provided as Python list[str]. Each str is a filename, the more at the beginning, the more it is a prerequisite dependency, should be done first

## Shared Knowledge: Anything that should be public like utils' functions, config's variables details that should make clear first. 

## Anything Unclear Provide as Plain text. Make clear here. For example, don't forget a main entry. don't forget to init 3rd party libs.

'''

FORMAT_EXAMPLE = '''
---
## Required Swift third-party packages
```swift
"""
flask==1.1.2
bcrypt==3.2.0
"""
```

## Required Other language third-party packages
```swift
"""
No third-party ...
"""
```

## Full API spec
```swift
"""
openapi: 3.0.0
...
description: A JSON object ...
"""
```

## Logic Analysis
```swift
[
    ("game.swift", "Contains ..."),
]
```

## Task list
```swift
[
    "game.swift",
]
```

## Shared Knowledge
```swift
"""
'game.swift' contains ...
"""
```

## Anything Unclear
We need ... how to start.
---
'''

OUTPUT_MAPPING = {
    "Required Swift third-party packages": (str, ...),
    "Required Other language third-party packages": (str, ...),
    "Full API spec": (str, ...),
    "Logic Analysis": (List[Tuple[str, str]], ...),
    "Task list": (List[str], ...),
    "Shared Knowledge": (str, ...),
    "Anything Unclear": (str, ...),
}


class WriteTasks(Action):

    def __init__(self, name="CreateTasks", context=None, llm=None):
        super().__init__(name, context, llm)
    
    def _save(self, context, rsp):
        ws_name = CodeParser.parse_str(
            block="Swift Package Name", text=context[-1].content)
        file_path = WORKSPACE_ROOT / ws_name / 'docs/api_spec_and_tasks.md'
        file_path.write_text(rsp.content)

        # Write requirements.txt
        requirements_path = WORKSPACE_ROOT / ws_name / 'requirements.txt'
        requirements_path.write_text(rsp.instruct_content.dict().get(
            "Required Swift third-party packages").strip('"\n'))

    async def run(self, context):
        prompt = PROMPT_TEMPLATE.format( context=context, format_example=FORMAT_EXAMPLE )
        # write prompt to temp file so we can read it first
        file = open("write_tasks_prompt.md", "w")
        file.write(prompt)
        file.close()
        # enter to continue...
        input( "Press Enter to continue..." )
        # read prompt from file and assign it to prompt
        file = open("write_tasks_prompt.md", "r")
        prompt = file.read()
        file.close() 
        print(f"Prompt: {prompt}")
        print(f"Task: 'task'")
        print(f"Output Mapping: {OUTPUT_MAPPING}")

        try:
            rsp = await self._aask_v1(prompt, "task", OUTPUT_MAPPING)
        except Exception as e:
            print( e )
            print( '*** ERROR: retry with 16k model... ***' )
            rsp = await self._aask_v1(prompt, "task", OUTPUT_MAPPING)
            
        self._save(context, rsp)
        return rsp

class AssignTasks(Action):
    async def run(self, *args, **kwargs):
        # Here you should implement the actual action
        pass

# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/EGAdams/swift-metagpt.git
# git push -u origin main