'''
Env actions:
    - look up cards +
    - upload decklist from string +
    - save uploaded decklist
    - load collection
    - price deck with respec to collection
    - change configs
    - working decklist +
    - change working decklist +
    - show working decklist +
'''


from cards import *


class EnvLogger:
    def show_decklists(self, env, *args, **kwargs):
        for key in env.decklists:
            print(key)
        
        if env.current_decklist is not None:
            decklist, name = env.current_decklist
            print(f'current decklist: {name}')
        
    def confirm_current_decklist_change(self, env, *args, **kwargs):
        print(f'new working decklist: {kwargs["name"]}')
        
    def show_current_decklist(self, env, *args, **kwargs):
        if env.current_decklist is None:
            print('no current decklist')
            return
            
        cd, name = env.current_decklist
        for key in cd:
            print(f'{key} {cd[key]}')
        
    def custom_msg(self, env, *args, **kwargs):
        print(kwargs[msg])


class Env:
    db: CardDatabase
    card_pool: list[CardCollection]
    decklists: dict
    current_decklist: tuple
    
    
    def look_up(self, **kwargs):
        return self.db[kwargs['key']]
        
    def upload_decklist(self, **kwargs):
        name, src = kwargs['name'], kwargs['src']
        self.decklists[name] = Decklist.universal_init(src)
        if self.current_decklist is None:
            self.current_decklist = (self.decklists[name], name)
        
    def show_decklists(self, **kwargs):
        EnvLogger().show_decklists(self)
        
    def change_current_decklist(self, **kwargs):
        name = kwargs['name']
        try:
            self.current_decklist = (self.decklists[name], name)
            EnvLogger().confirm_current_decklist_change(self, name=name)
        except KeyError:
            EnvLogger().custom_msg(self, msg='no such decklist')
    
    def show_current_decklist(self, **kwargs):
        EnvLogger().show_current_decklist(self)
    
    def __init__(self):
        self.decklists = {}
        self.current_decklist = None
        self.actions = {'lu': self.look_up,
                        'upload': self.upload_decklist,
                        'show': self.show_current_decklist,
                        'inspect': self.show_decklists,}
    
    @staticmethod
    def parse(string):
        tokens = string.split(' -')
        cmd = tokens[0]
        kwargs = {}
        for token in tokens[1:]:
            subtokens = token.split(' ')
            kwargs[subtokens[0]] = subtokens[1]
            
        return {'cmd': cmd, 'kwargs': kwargs}
    
    
if __name__ == '__main__':
    env = Env()
    while True: 
        x = input('env ')
        if x == 'q':
            break
        
        try:
            action = env.parse(x)
            env.actions[action['cmd']](**action['kwargs'])
        except Exception as e:
            print(e)
        