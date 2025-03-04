import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx

# Streamlit App
st.title("HRHP Fundraising Strategy")

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
    st.subheader("Funding Diversification")

    labels = ["Endowment & Investments", "Mid-sized Grants & HNWIs", "Short-term Grants & Corporate"]
    values = [10, 30, 60]  # Proportions of funding sources

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

# 2. Data Monetization Strategy Flowchart
elif option == "Data Monetization Strategy":
    st.subheader("Data Monetization Strategy")

    nodes = ["HRHP Data Assets", "Corporate Users", "Conservation Reinvestment"]
    edges = [("HRHP Data Assets", "Corporate Users"), ("Corporate Users", "Conservation Reinvestment")]

    G = nx.DiGraph()
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x, node_y, text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color="#888"),
                            hoverinfo="none", mode="lines")

    node_trace = go.Scatter(x=node_x, y=node_y, mode="markers+text",
                            text=text, marker=dict(size=20, color=["#09188d", "#ff7f0e", "#2ca02c"]),
                            textposition="bottom center", hoverinfo="text")

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Data Monetization Flowchart", showlegend=False, height=500, width=700)

    st.plotly_chart(fig)

    st.write("""
    - **HRHP collects valuable data** on marine ecosystems and biodiversity.  
    - **Corporate users leverage this data** for risk assessment, insurance, and sustainability analysis.  
    - **Reinvest profits** into conservation efforts, creating a sustainable revenue cycle.  
    """)

# 3. Implementation Timeline (Gantt Chart)
elif option == "Implementation Timeline":
    st.subheader("Implementation Timeline (March - September 2025)")

    df = pd.DataFrame([
        {"Task": "Grant Acquisition", "Start": "2025-03-01", "End": "2025-06-30"},
        {"Task": "Corporate Partnerships", "Start": "2025-03-15", "End": "2025-07-31"},
        {"Task": "In-Kind Expansion", "Start": "2025-04-01", "End": "2025-09-01"},
        {"Task": "Endowment Structuring", "Start": "2025-05-01", "End": "2025-09-30"},
    ])

    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])
    df["Duration"] = df["End"] - df["Start"]

    fig = px.timeline(df, x_start="Start", x_end="End", y="Task", title="HRHP Implementation Timeline",
                      color="Task", labels={"Task": "Task", "Start": "Start Date", "End": "End Date"},
                      template="plotly_white")

    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig)

    st.write("""
    - **Grant Acquisition:** Secure new funding streams.  
    - **Corporate Partnerships:** Strengthen relationships with businesses.  
    - **In-Kind Expansion:** Reduce costs through resource sharing.  
    - **Endowment Structuring:** Lay the foundation for long-term financial stability.  
    """)

# 4. HRHP Partnership Ecosystem Map
elif option == "HRHP Partnership Ecosystem":
    st.subheader("HRHP Partnership Ecosystem")

    G = nx.Graph()

    # Define node categories
    main_node = "HRHP"
    funders = ["Government Grants", "Private Foundations", "Corporate Sponsors", "HNWIs"]
    partners = ["MARFund", "Research Universities", "NGOs", "Local Governments"]

    # Add nodes and edges
    G.add_node(main_node)
    for f in funders:
        G.add_edge(main_node, f)
    for p in partners:
        G.add_edge(main_node, p)

    pos = nx.spring_layout(G, seed=42)

    # Extract edge positions
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Extract node positions and assign colors/sizes
    node_x, node_y, text, colors, sizes = [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

        # Assign colors and sizes
        if node == main_node:
            colors.append("#09188d")  # Dark Blue for HRHP
            sizes.append(30)  # Larger size for HRHP
        elif node in funders:
            colors.append("#2ca02c")  # Green for Funders
            sizes.append(20)
        elif node in partners:
            colors.append("#ff7f0e")  # Orange for Partners
            sizes.append(20)

    # Create edge trace (lighter and transparent edges)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color="rgba(150,150,150,0.5)"),  # Lighter, semi-transparent
        hoverinfo="none",
        mode="lines"
    )

    # Create node trace (larger, color-coded nodes)
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=text,
        marker=dict(size=sizes, color=colors, line=dict(width=2, color="white")),
        textposition="top center",  # Moves text slightly above nodes
        hoverinfo="text"
    )

    # Create figure with hidden axes
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="HRHP Partnership Ecosystem",
        showlegend=False,
        height=600,
        width=800,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),  # Hide X-axis
        yaxis=dict(showgrid=False, zeroline=False, visible=False)   # Hide Y-axis
    )

    st.plotly_chart(fig)

    st.write("""
    - **HRHP sits at the center of a vast network** of funders, research partners, and conservation institutions.  
    - **Funders (Green):** Government grants, private foundations, corporate sponsors, and high-net-worth individuals (HNWIs).  
    - **Partners (Orange):** NGOs, research universities, MARFund, and local governments.  
    - **Strengthening these relationships** will enhance funding reliability and resource-sharing opportunities.  
    """)





# End of Streamlit App
st.sidebar.info("Select a visualization from the dropdown to view strategy insights.")
