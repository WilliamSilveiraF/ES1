import math

class Player:
    INIT_SALARY = 2000
    INIT_BANK = 10000
    MAX_CHILDREN = 4
    CHILD_COST = -500

    def __init__(self, player_id, turn, cor):
        self.player_id = player_id
        self.turn = int(turn)
        self.cor = cor
        self.posicao = 0
        self.salary = self.INIT_SALARY
        self.child_amount = 0
        self.dinheiro = self.INIT_BANK
        self.is_retired = False
        self.is_playing = True
        self.is_life_insured = False
        self.is_vehicle_insured = False

    def increase_salary_10_percent(self):
        self.salary = math.ceil(1.1 * self.salary)
    
    def increase_salary_20_percent(self):
        self.salary = math.ceil(1.2 * self.salary)
    
    def add_child(self):
        if self.child_amount == self.MAX_CHILDREN:
            raise ValueError('A player can only have up to 4 children. So no events will be reflected back to you this turn.')
        self.child_amount += 1

    def handle_default_turn_income(self):
        transaction = self.salary

        if self.is_retired:
            transaction += 5000

        transaction += self.child_amount * self.CHILD_COST

        self.dinheiro += transaction

    def apply_income_tax(self):
        BASE = 0.7
        self.dinheiro = math.ceil(BASE * self.dinheiro)
    
    def handle_internship(self):
        self.dinheiro -= math.ceil(0.5 * self.salary)
    
    def handle_volunter_work(self):
        self.dinheiro -= self.salary

    def buy_life_insurance(self):
        if self.is_life_insured:
            raise ValueError("Player already has life insurance. So no events will be reflected back to you this turn.")

        self.dinheiro -= 10000
        self.is_life_insured = True

    def buy_car_insurance(self):
        if self.is_vehicle_insured:
            raise ValueError("Player already has vehicle insurance. So no events will be reflected back to you this turn.")
        
        self.dinheiro -= 8000
        self.is_vehicle_insured = True

    def set_retirement(self):
        if self.is_retired:
            raise ValueError('You already is retired. So no events will be reflected back to you this turn.')
        self.is_retired = True
    
    def get_card_content(self):
        return [
            { 'field': 'Bank', 'value': f'U$$ {self.dinheiro}' },
            { 'field': 'Salary', 'value': f'U$$ {self.salary}' },
            { 'field': 'Childs', 'value': f'{self.child_amount}' },
            { 'field': 'Retirement', 'value': 'U$$ 5000' if self.is_retired else 'U$$ 0' },
            { 'field': 'Life insurance', 'value': 'Yes' if self.is_life_insured else 'No' },
            { 'field': 'Vehicle insurance', 'value': 'Yes' if self.is_vehicle_insured else 'No' }
        ]
    
    def set_out_of_match(self):
        self.is_playing = False

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'turn': self.turn,
            'cor': self.cor,
            'posicao': self.posicao,
            'salary': self.salary,
            'child_amount': self.child_amount,
            'dinheiro': self.dinheiro,
            'is_retired': self.is_retired,
            'is_playing': self.is_playing,
            'is_life_insured': self.is_life_insured,
            'is_vehicle_insured': self.is_vehicle_insured
        }

    def update(self, data: dict):
        self.posicao = data['posicao']
        self.salary = data['salary']
        self.child_amount = data['child_amount']
        self.dinheiro = data['dinheiro']
        self.is_retired = data['is_retired']
        self.is_playing = data['is_playing']
        self.is_life_insured = data['is_life_insured']
        self.is_vehicle_insured = data['is_vehicle_insured']

    @property
    def is_broke(self):
        return self.dinheiro < 0