class MarketAgent:
    """Trading agent with personality and network influences"""
    def __init__(self, agent_id, personality='random', initial_money=1000):
        self.id = agent_id
        self.personality = personality
        self.money = initial_money
        self.stocks = 0
        self.history = []
        self.neighbors = []

        # Personality thresholds for trading
        self.thresholds = {
            'cautious': 0.7,
            'aggressive': 0.3,
            'random': 0.5,
            'contrarian': 0.4
        }

    def decide_action(self, current_price, neighbor_actions):
        """Decide whether to buy, sell, or hold"""
        if not neighbor_actions:
            return 'hold'

        buy_count = neighbor_actions.count('buy')
        sell_count = neighbor_actions.count('sell')
        total = len(neighbor_actions)

        buy_pressure = buy_count / total
        threshold = self.thresholds[self.personality]

        if self.personality == 'contrarian':
            if buy_pressure > threshold and self.stocks > 0:
                return 'sell'
            elif buy_pressure < (1 - threshold) and self.money >= current_price:
                return 'buy'
        else:
            if buy_pressure > threshold and self.money >= current_price:
                return 'buy'
            elif buy_pressure < (1 - threshold) and self.stocks > 0:
                return 'sell'

        return 'hold'

    def take_action(self, action, current_price):
        """Execute trading action"""
        if action == 'buy' and self.money >= current_price:
            self.stocks += 1
            self.money -= current_price
        elif action == 'sell' and self.stocks > 0:
            self.stocks -= 1
            self.money += current_price

        self.history.append({
            'action': action,
            'price': current_price,
            'money': self.money,
            'stocks': self.stocks,
            'total_value': self.money + (self.stocks * current_price)
        })
