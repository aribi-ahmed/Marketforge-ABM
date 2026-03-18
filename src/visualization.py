import pandas as pd
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_market_activity(simulation):
    """Plot price and volume over time"""
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Price', 'Volume')
    )

    # Price plot
    fig.add_trace(
        go.Scatter(y=simulation.price_history, name="Price",
                  line=dict(color='blue')),
        row=1, col=1
    )

    # Volume plot
    fig.add_trace(
        go.Bar(y=simulation.volume_history, name="Volume",
               marker_color='lightblue'),
        row=2, col=1
    )

    fig.update_layout(height=600, title_text="Market Activity",
                      showlegend=True)
    return fig

def plot_agent_performance(simulation):
    """Plot performance by personality type"""
    performance_data = []

    for agent in simulation.agents:
        if agent.history:
            initial_value = 1000
            final_value = agent.history[-1]['total_value']
            returns = (final_value - initial_value) / initial_value * 100

            performance_data.append({
                'Personality': agent.personality,
                'Returns (%)': returns
            })

    df = pd.DataFrame(performance_data)
    fig = px.box(df, x='Personality', y='Returns (%)',
                 color='Personality',
                 title='Trading Performance by Personality Type')
    return fig

def visualize_network(simulation):
    """Create network visualization"""
    G = simulation.network
    pos = nx.spring_layout(G)

    edge_trace = go.Scatter(
        x=[], y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_trace = go.Scatter(
        x=[], y=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlOrRd',
            size=10,
        ))

    # Add edges
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    # Add nodes
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        agent = simulation.agents[node]
        wealth = agent.money + (agent.stocks * simulation.price)
        node_color.append(wealth)
        node_text.append(f'Agent {node}<br>Type: {agent.personality}<br>Wealth: ${wealth:.2f}')

    node_trace.x = node_x
    node_trace.y = node_y
    node_trace.text = node_text
    node_trace.marker.color = node_color

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Trading Network',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40)
                    ))
    return fig
