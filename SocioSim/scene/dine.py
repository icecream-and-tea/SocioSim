from typing import List
from .base import Scene
from ..agent import Player
from ..utils import NAME2PORT, PORT2NAME, log_table, \
                    get_data_from_database, send_data_to_database

import numpy as np
 
processes = [
    {"name": "order", "from_db": False, "to_db": False},
    {"name": "comment", "from_db": False, "to_db": False},
    {"name": "feeling", "from_db": False, "to_db": False},
]


class Dine(Scene):
    
    type_name = "dine"
    
    def __init__(self, players: List[Player], id: int, log_path: str, **kwargs):
        super().__init__(players=players, id=id, log_path=log_path,  
                                type_name=self.type_name, **kwargs)
        self.processes = processes
        
        self.day = 1
        self.dishes = None
        self.terminal_flag = False
    
    @classmethod
    def action_for_next_scene(cls, data):  
        restaurant_list = []
        daybooks = {}
        comments = {}
        num_of_customer = {}
        infos = {}
        rival_info = {}
        customer_choice = {}

        for value in PORT2NAME.values():
            restaurant_list.append(value)
            comments[value] = []
            daybooks[value] = {}
            num_of_customer[value] = 0
            infos[value] = ''
            rival_info[value] = ''
            
        for d in data:
            agent_name = next(iter(d))
            d = d[agent_name]
            day = d["day"]
            r_name = d["restaurant"]
            
            # record customer choice
            customer_choice[agent_name] = r_name
            
            if "comment" in d:
                # construct comment
                comment = {"day": day, "name": agent_name, "score": d["score"], "content":  d["comment"]}
                comments[r_name].append({"type": "add", "data": comment})
            
            # construct daybook
            dishes = d["dishes"]
            num_of_customer[r_name] += 1
            for dish in dishes:
                if not dish in daybooks[r_name]:
                    daybooks[r_name][dish] = 0
                daybooks[r_name][dish] += 1
                
        # 1. log customer choice
        from ..simul import LOG_PATH
        log_path = f'{LOG_PATH}/{cls.type_name}'
        log_table(log_path, customer_choice, f"day{day}")
        
        # 2. send comments to database
        for key in comments:
            send_data_to_database(comments[key], "comment", port=NAME2PORT[key])
    
        # construct whole daybook  
        for r_name in restaurant_list:
            show = get_data_from_database("show", port=NAME2PORT[r_name])
            info = f"Restaurant: {r_name} \nNumber of customers: {num_of_customer[r_name]} \nCustomer Comments: {show['comment']} \nMenu: {show['menu']}\n "
            infos[r_name] = info
        
        for key in daybooks:
            for r_name in restaurant_list:
                if r_name != key:
                    rival_info[key] += infos[r_name]
            daybook = {"dishes": daybooks[key], "num_of_customer": num_of_customer[key], "rival_info": rival_info[key]}
            
            print(f'debugging-daybook: {daybook}')
            
            daybooks[key] = {"type": "add", "data": daybook}

        # 3. send daybooks to database
        for key in daybooks:
            send_data_to_database(daybooks[key], "daybook", port=NAME2PORT[key])
        
        return
        
        
    def is_terminal(self):
        return self.terminal_flag

    def terminal_action(self):
        self.day += 1
        self._curr_process_idx = 0
        self.terminal_flag = False
        
    def move_to_next_player(self):
        self._curr_player_idx = 0  # In restaurant design, only one player
    
    def move_to_next_process(self):
        # 30% order->comment, 70% order->feeling
        if self._curr_process_idx == 0:
            self._curr_process_idx += np.random.choice([1, 2], p=[0.3, 0.7])
        else:
            self.terminal_flag = True

    def prepare_for_next_step(self):
        self.move_to_next_player()
        self.move_to_next_process()
        self._curr_turn += 1
    
    # interactive step design
    def step(self, input=None):
        curr_player = self.get_curr_player()
        curr_process = self.get_curr_process()
        result = None
        
        # pre-process
        if curr_process['name'] == 'order':
            for k in input.keys():
                print(input[k]['today_offering'])
                # add all today offerings to message pool
                self.add_new_prompt(player_name=curr_player.name, 
                                data=input[k]['today_offering'])
            # add order prompt
            self.add_new_prompt(player_name=curr_player.name, 
                                scene_name=self.type_name, 
                                step_name=curr_process['name'], 
                                from_db=curr_process['from_db'])
        elif curr_process['name'] in ('comment', 'feeling'):
            # add dish score and comment prompt
            self.add_new_prompt(player_name=curr_player.name,
                                scene_name=self.type_name,
                                step_name=curr_process['name'],
                                data=input)

        observation = self.message_pool.get_visible_messages(agent_name=curr_player.name, turn=self._curr_turn)
        
        for i in range(self.invalid_step_retry):
            try:
                output = curr_player(observation)
                parsed_ouput = self.parse_output(output, curr_player.name, curr_process['name'], curr_process['to_db'])
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed with error: {e}")
        else:
            raise Exception("Invalid step retry arrived at maximum.")
        
        # post-process
        if curr_process['name'] == 'order':
            restaurant = parsed_ouput['restaurant']
            self.dishes = parsed_ouput['dishes']
            dish_score = input[restaurant]['dish_score']
            
            prompt = ''
            for dish in self.dishes:
                # check if the dish is in the restaurant
                if dish in dish_score.keys():
                    score = dish_score[dish]
                    prompt += f"\n{dish}: {score}"
                result = prompt
        
        if curr_process['name'] in ('comment', 'feeling'):
            dine_info = parsed_ouput
            dine_info['dishes'] = self.dishes
            dine_info['day'] = self.day
            customer_name = self.players[0].name
            dine_info = {customer_name: dine_info}
            result = dine_info
                
        self.prepare_for_next_step()
        
        return result
        
        
        