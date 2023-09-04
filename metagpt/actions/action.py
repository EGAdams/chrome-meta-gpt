#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : action.py
"""
from abc import ABC
from typing import Optional

from tenacity import retry, stop_after_attempt, wait_fixed

from metagpt.actions.action_output import ActionOutput
from metagpt.llm import LLM
from metagpt.utils.common import OutputParser
from metagpt.logs import logger

import pprint

class Action(ABC):
    def __init__(self, name: str = '', context=None, llm: LLM = None):
        self.name: str = name
        if llm is None:
            llm = LLM()
        self.llm = llm
        self.context = context
        self.prefix = ""
        self.profile = ""
        self.desc = ""
        self.content = ""
        self.instruct_content = None
    
    def transform_requirement_pool(requirement_pool: list) -> list:
        """
        Transforms the 'Requirement Pool' list from a list of strings to a list of tuples.
        """
        transformed_pool = []
        
        for item in requirement_pool:
                # Split the string at the last occurrence of a space followed by a parenthesis.
                # This will give us the requirement description and its priority.
                description, priority = item.rsplit(' ', 1)
                
                # Remove the parenthesis from the priority.
                priority = priority.strip("()")
                
                transformed_pool.append((description, priority))
        
        return transformed_pool
    
    def needs_transformation(requirement_pool: list) -> bool:
        """
        Check if the 'Requirement Pool' needs transformation.
        """
        # Check if the first item is not a tuple (assuming non-empty list)
        return bool(requirement_pool) and not isinstance(requirement_pool[0], tuple)


    def set_prefix(self, prefix, profile):
        """Set prefix for later usage"""
        self.prefix = prefix
        self.profile = profile

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    async def _aask(self, prompt: str, system_msgs: Optional[list[str]] = None) -> str:
        """Append default prefix"""
        if not system_msgs:
            system_msgs = []
        system_msgs.append(self.prefix)
        return await self.llm.aask(prompt, system_msgs)

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    async def _aask_v1(self, prompt: str, output_class_name: str,
                       output_data_mapping: dict,
                       system_msgs: Optional[list[str]] = None) -> ActionOutput:
        """Append default prefix"""
        if not system_msgs:
            system_msgs = []
        system_msgs.append(self.prefix)
        # write prompt to temp_action.md
        with open("temp_action.md", "w") as f:
            f.write(prompt)
        try:
            content = await self.llm.aask(prompt, system_msgs)
        except Exception as e:
            print( e )
            
        logger.debug(content)
        output_class = ActionOutput.create_model_class(output_class_name, output_data_mapping)
        parsed_data = OutputParser.parse_data_with_mapping(content, output_data_mapping)
        # pprint( parsed_data[ "Requirement Pool" ]) why is this causing so much trouble?
        logger.debug(parsed_data)
        print(parsed_data)
        # if self.needs_transformation( parsed_data[ "Requirement Pool" ]):
        #     parsed_data["Requirement Pool"] = self.transform_requirement_pool(parsed_data["Requirement Pool"])
        instruct_content = output_class(**parsed_data)
        return ActionOutput(content, instruct_content)

    async def run(self, *args, **kwargs):
        """Run action"""
        raise NotImplementedError("The run method should be implemented in a subclass.")
