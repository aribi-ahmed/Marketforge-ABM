from src.simulation import MarketSimulation
from src.visualization import plot_market_activity, plot_agent_performance, visualize_network

def main():
    print("Initializing MarketForge Simulation...")
    
    # 1. Create the simulation environment with 100 agents
    sim = MarketSimulation(num_agents=100)
    
    # 2. Run the simulation
    steps = 100
    print(f"Running market simulation for {steps} steps. Please wait...")
    sim.run_simulation(steps)
    
    # 3. Generate and display the interactive charts
    print("Generating visualizations...")
    
    print("--> Showing Market Activity (Price & Volume)...")
    fig_activity = plot_market_activity(sim)
    fig_activity.show()
    
    print("--> Showing Agent Performance by Personality...")
    fig_performance = plot_agent_performance(sim)
    fig_performance.show()
    
    print("--> Showing Trading Network Topography...")
    fig_network = visualize_network(sim)
    fig_network.show()
    
    print("Simulation complete!")

if __name__ == "__main__":
    main()
