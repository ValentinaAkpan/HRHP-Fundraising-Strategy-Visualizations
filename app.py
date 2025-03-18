import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import base64

# Function to render SVG logos
def render_svg(svg_file, width="150"):
    with open(svg_file, "r") as f:
        svg = f.read()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" width="{width}"/>'
    return html

# Display logos and title
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown(render_svg("66b16833c7877e9078babfd7_Healthy-Reefs.svg", width="600"), unsafe_allow_html=True)

with col2:
    st.title("Healthy Reefs for Healthy People (HRHP) Fundraising Strategy")

with col3:
    st.write("")  # Add another logo here if available

# Sidebar for Visualization Selection
st.sidebar.header("Select Visualization")
option = st.sidebar.selectbox(
    "Choose a visualization",
    [
        "Funding Diversification",
        "Data Monetization Strategy",
        "Implementation Timeline",
        "HRHP Partnership Ecosystem"
    ]
)

# 1. Funding Diversification Pyramid
if option == "Funding Diversification":
    labels = ["Endowment & Investments", "Mid-sized Grants & HNWIs", "Short-term Grants & Corporate"]
    values = [10, 30, 60]

    fig = px.funnel(
        x=values,
        y=labels,
        title="Funding Sources Distribution",
        labels={"x": "Funding Percentage", "y": "Funding Category"},
        color_discrete_sequence=["#09188d", "#58508d", "#bc5090"]
    )

    st.plotly_chart(fig)

    st.write("""
    - **Base (Short-term stability):** Short-term grants, corporate sponsorships, and existing donors.  
    - **Middle (Growth & expansion):** Mid-sized grants, new partnerships, HNWIs.  
    - **Top (Long-term sustainability):** Endowment fund, unrestricted foundation funding, investment returns.  
    """)

# 2. Data Monetization Strategy
elif option == "Data Monetization Strategy":
    nodes = ["HRHP Data Assets", "Corporate Users", "Conservation Reinvestment"]
    edges = [("HRHP Data Assets", "Corporate Users"), ("Corporate Users", "Conservation Reinvestment")]

    G = nx.DiGraph()
    G.add_edges_from(edges)

    pos = {"HRHP Data Assets": (0, 1), "Corporate Users": (1, 0.5), "Conservation Reinvestment": (2, 1)}

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x, node_y, text = [], [], []
    colors = ["#09188d", "#ff7f0e", "#2ca02c"]
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color="#888"), hoverinfo="none", mode="lines")
    node_trace = go.Scatter(x=node_x, y=node_y, mode="markers+text", text=text,
                            marker=dict(size=40, color=colors, line=dict(width=2, color='white')),
                            textposition="bottom center", hoverinfo="text")

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Data Monetization Strategy Flow", showlegend=False, height=400, width=700,
                      xaxis=dict(showgrid=False, zeroline=False, visible=False),
                      yaxis=dict(showgrid=False, zeroline=False, visible=False), plot_bgcolor='white')

    st.plotly_chart(fig)

# 3. Implementation Timeline
elif option == "Implementation Timeline":
    df = pd.DataFrame([
        {"Task": "Grant Acquisition", "Start": "2025-03-01", "End": "2025-06-30"},
        {"Task": "Corporate Partnerships", "Start": "2025-03-15", "End": "2025-07-31"},
        {"Task": "In-Kind Expansion", "Start": "2025-04-01", "End": "2025-09-01"},
        {"Task": "Endowment Structuring", "Start": "2025-05-01", "End": "2025-09-30"},
    ])
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])

    fig = px.timeline(df, x_start="Start", x_end="End", y="Task", title="Implementation Timeline",
                      color="Task", template="plotly_white")

    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig)

# 4. HRHP Partnership Ecosystem
elif option == "HRHP Partnership Ecosystem":
    G = nx.Graph()
    main_node = "HRHP"
    funders = ["Government Grants", "Private Foundations", "Corporate Sponsors", "HNWIs"]
    partners = ["MARFund", "Research Universities", "NGOs", "Local Governments"]

    G.add_node(main_node)
    for f in funders + partners:
        G.add_edge(main_node, f)

    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x, node_y, text, colors, sizes = [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

        if node == main_node:
            colors.append("#09188d")
            sizes.append(30)
        elif node in funders:
            colors.append("#2ca02c")
            sizes.append(20)
        else:
            colors.append("#ff7f0e")
            sizes.append(20)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color="#888"), hoverinfo="none", mode="lines")
    node_trace = go.Scatter(x=node_x, y=node_y, mode="markers+text", text=text,
                            marker=dict(size=sizes, color=colors, line=dict(width=2, color="white")),
                            textposition="top center", hoverinfo="text")

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="HRHP Partnership Ecosystem", showlegend=False,
                      xaxis=dict(visible=False), yaxis=dict(visible=False))

    st.plotly_chart(fig)


    st.write("""
    - **HRHP sits at the center of a vast network** of funders, research partners, and conservation institutions.  
    - **Funders:** Government grants, private foundations, corporate sponsors, and high-net-worth individuals (HNWIs).  
    - **Partners:** NGOs, research universities, MARFund, and local governments.  
    - **Strengthening these relationships** will enhance funding reliability and resource-sharing opportunities.  
    """)

st.sidebar.info("Select a visualization from the dropdown to view strategy insights.")
