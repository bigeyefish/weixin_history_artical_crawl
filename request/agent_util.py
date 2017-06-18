# -*- coding: UTF-8 -*-
import os
import random


class AgentUtil:

    def __init__(self):
        self.agentList = []
        self.agent_static_file = os.path.dirname(os.path.abspath('__file__')) + '/resource/temp_agent.txt'

    def get_random_agent(self):
        if len(self.agentList) == 0:

            for line in open(os.path.abspath(self.agent_static_file)):
                self.agentList.append(line.replace('\n', ''))

        return random.choice(self.agentList)

agentUtil = AgentUtil()
