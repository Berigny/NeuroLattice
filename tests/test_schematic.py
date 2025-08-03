import plotly.graph_objects as go

# Vertices of the first tetrahedron
tetra1_vertices = [(0.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0)]
tetra1_weights = [2, 3, 5, 7]

# Vertices of the second tetrahedron
tetra2_vertices = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 1.0)]
tetra2_weights = [19, 17, 13, 11] # Updated weights

# Edges for connecting vertices (pairs of vertex indices)
tetra1_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
tetra2_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

# Create traces for the first tetrahedron
tetra1_lines = []
for edge in tetra1_edges:
    x = [tetra1_vertices[edge[0]][0], tetra1_vertices[edge[1]][0]]
    y = [tetra1_vertices[edge[0]][1], tetra1_vertices[edge[1]][1]]
    z = [tetra1_vertices[edge[0]][2], tetra1_vertices[edge[1]][2]]
    tetra1_lines.append(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='blue', width=2)))

tetra1_scatter = go.Scatter3d(
    x=[v[0] for v in tetra1_vertices],
    y=[v[1] for v in tetra1_vertices],
    z=[v[2] for v in tetra1_vertices],
    mode='markers+text', # Add text mode
    marker=dict(color='blue', size=5),
    name='Tetrahedron 1',
    text=[str(w) for w in tetra1_weights], # Add prime weights as text
    textposition="bottom center" # Adjust text position
)

# Create traces for the second tetrahedron
tetra2_lines = []
for edge in tetra2_edges:
    x = [tetra2_vertices[edge[0]][0], tetra2_vertices[edge[1]][0]]
    y = [tetra2_vertices[edge[0]][1], tetra2_vertices[edge[1]][1]]
    z = [tetra2_vertices[edge[0]][2], tetra2_vertices[edge[1]][2]]
    tetra2_lines.append(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='red', width=2)))

tetra2_scatter = go.Scatter3d(
    x=[v[0] for v in tetra2_vertices],
    y=[v[1] for v in tetra2_vertices],
    z=[v[2] for v in tetra2_vertices],
    mode='markers+text', # Add text mode
    marker=dict(color='red', size=5),
    name='Tetrahedron 2',
    text=[str(w) for w in tetra2_weights], # Add prime weights as text
    textposition="bottom center" # Adjust text position
)

# Combine traces and create the figure
fig = go.Figure(data=tetra1_lines + [tetra1_scatter] + tetra2_lines + [tetra2_scatter])

# Update layout for clarity
fig.update_layout(
    title='Two Tetrahedrons in 3D Space (Plotly) with Prime Weights',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Display the plot
fig.show()