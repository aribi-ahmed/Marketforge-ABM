class MarketSimulation:
    """Simulates a market with networked agents"""
    def __init__(self, num_agents=100):
        # Create agents with different personalities
        self.agents = []
        personalities = ['cautious', 'aggressive', 'random', 'contrarian']
        for i in range(num_agents):
            personality = personalities[i % len(personalities)]
            self.agents.append(MarketAgent(i, personality))

        # Create influence network
        self.network = nx.barabasi_albert_graph(num_agents, 3)
        for i in range(num_agents):
            self.agents[i].neighbors = list(self.network.neighbors(i))

        # Initialize market state
        self.price = 100
        self.price_history = [self.price]
        self.volume_history = [0]
        self.step_number = 0

    def step(self):
        """Execute one simulation step"""
        actions = []
        volume = 0

        # Collect agent decisions
        for agent in self.agents:
            neighbor_actions = [actions[n] for n in agent.neighbors if n < len(actions)]
            action = agent.decide_action(self.price, neighbor_actions)
            actions.append(action)

            if action != 'hold':
                volume += 1
            agent.take_action(action, self.price)

        # Update price based on supply/demand
        buy_count = actions.count('buy')
        sell_count = actions.count('sell')
        price_change = (buy_count - sell_count) / len(self.agents)
        self.price *= (1 + price_change * 0.1)

        # Record history
        self.price_history.append(self.price)
        self.volume_history.append(volume)
        self.step_number += 1
