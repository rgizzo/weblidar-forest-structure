import streamlit as st
import laspy
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from streamlit_extras.card_selector import *

st.set_page_config(layout="wide")
st.markdown("<h1 style='font-size: 35px;'>Seeing the Trees for the Forest: Visualizing Forest Structure with LiDAR</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    h1, h2, h3, p, label {
        -webkit-text-stroke: 0.5px #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)
left, center, right = st.columns([0.85, 3.5, 1.5], gap="medium")

# Map forest types to LAZ files
forest_files = {
    "Old Growth Deciduous": "data/BART_cropped.laz",
    "Mixed Pine Forest": "data/TALL_cropped.laz",
    "Longleaf Pine Savanna": "data/OSBS_cropped.laz"
}

forest_names = list(forest_files.keys())

with left:
    
    st.markdown("<label style='font-size: 15px;'>Select Forest Type:</h1>", unsafe_allow_html=True)
    
    forest = card_selector(
    [
        dict(
            icon='↟˖˚𖤣𖥧↟˖˚𓋼𖤣𖥧˖˚𓋼𓍊',
            title="Old Growth Deciduous",
            description="This site is part of Bartlett Experimental Forest in Carroll County, New Hampshire. The area is dominated by old growth deciduous hardwoods consisting of beech (Fagus sp.) and sugar maple (Acer saccarum)."
        ),
        dict(
            icon='↟𖠰˚☀︎˖˚ᨒ↟˖˚𖠰',
            title="Mixed Pine Forest",
            description="Located in Alabama's Talladega National forest, this site is dominated by longleaf pine (Pinus palustris) and loblolly pine (Pinus taeda) with mixed species of oak in the understory."
        ),
        dict(
            icon='˖˚ʚ ⸙₊ ෴⋆.𖥧',
            title="Longleaf Pine Savanna",
            description="Dominated by pine and turkey oak (Quercus laevis), this site is located at Ordway Swisher Biological station in Putnam County, Florida. Pines are primarily Longleaf (Pinus palustris) and Loblolly (P.taeda), with a grass and forb groundcover."
        )
    ],
    key = list("forest_selector")
    )

    def load_point_cloud(filepath):
        return laspy.read(filepath)
    if forest is None:
        forest = 0  # Default to first forest

    forest = forest_names[forest]
    las = load_point_cloud(forest_files[forest])

    # Extract coordinates
    x = np.asarray(las.x)
    y = np.asarray(las.y)
    z = np.asarray(las.z)

    classification = np.asarray(las.classification)

    # RGB 
    red = np.asarray(las.red)
    green = np.asarray(las.green)
    blue = np.asarray(las.blue)

    idx = np.arange(len(x))
        
    x = x[idx]
    y = y[idx]
    z = z[idx]

    classification = classification[idx]
    red = red[idx]
    green = green[idx]
    blue = blue[idx]

    color_mode = st.radio(
        "Select Point Cloud Color:",
        ["RGB", "Classification", "Height"],
        horizontal=False
    )

with center:

# Determine point colors
    if color_mode == "RGB":

        rgb = np.column_stack((red, green, blue))

        # Convert 16-bit RGB to 8-bit
        if rgb.max() > 255:
            rgb = (rgb / 257).astype(np.uint8)
        else:
            rgb = rgb.astype(np.uint8)

        colors = [
            f"rgb({r},{g},{b})"
            for r, g, b in rgb
        ]

        marker = dict(
            size=1.5,
            color=colors,
            opacity=0.8
        )

    elif color_mode == "Classification":

        class_colors = {
            2: "#8B4513",  # Ground
            3: "#646464",  # Unclassified
            5: "#006400"   # High vegetation
        }

        colors = [
            class_colors.get(int(c), "#808080")
            for c in classification
        ]

        marker = dict(
            size=1.5,
            color=colors,
            opacity=0.8
        )

    else:  # Height

        marker = dict(
            size=1.5,
            color=z,
            colorscale="Viridis",
            opacity=0.8,
            colorbar=dict(title="Height (m)")
        )
        
        # Height range slider
    height_range = st.slider(
        "Height Range (m)",
        min_value=float(np.floor(z.min())),
        max_value=float(np.ceil(z.max())),
        value=(float(np.floor(z.min())), float(np.ceil(z.max()))),
        step=1.0
    )
    # Filter points by height
    height_mask = (z >= height_range[0]) & (z <= height_range[1])

    # Create figure
    fig = go.Figure()

    # Filter marker colors to match the selected points
    marker["color"] = np.asarray(marker["color"])[height_mask]

    fig.add_trace(
        go.Scatter3d(
            x=x[height_mask],
            y=y[height_mask],
            z=z[height_mask],
            mode="markers",
            marker=marker,
            showlegend=False
        )
    )

    # Figure layout
    fig.update_layout(
        title=f"{forest} LiDAR Point Cloud",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data"
        ),
        height=650,
        margin=dict(l=0, r=130, t=40, b=0),
        showlegend=False
    )

    # Static classification legend
    if color_mode == "Classification":

        class_names = {
            2: "Ground",
            3: "Unclassified",
            5: "High Vegetation"
        }

        for i, (class_id, name) in enumerate(class_names.items()):
            fig.add_annotation(
                x=0.85,
                y=0.95 - i * 0.06,
                xref="paper",
                yref="paper",
                text=(
                    f"<span style='color:{class_colors[class_id]}'>"
                    f"●</span> {name}"
                ),
                showarrow=False,
                xanchor="left",
                font=dict(size=13)
            )
        # Display figure
    st.plotly_chart(fig, use_container_width=True)
    
# Full point cloud heights
heights = np.asarray(las.z)
heights = heights[
    np.isfinite(heights) &
    (heights >= height_range[0]) &
    (heights <= height_range[1])
]

# Calculate vertical return density (0.5 m bins)
counts, edges = np.histogram(
    heights,
    bins=np.arange(
        np.floor(heights.min()),
        np.ceil(heights.max()) + 0.5,
        0.5
    )
)

bin_centers = (edges[:-1] + edges[1:]) / 2
density = counts / counts.sum()

# Calculate RH metrics
rh_values = {
    "RH25": np.percentile(heights, 25),
    "RH50": np.percentile(heights, 50),
    "RH98": np.percentile(heights, 98)
}

# Calculate RH metrics for all three forests
rh_results = []

for forest_name, filepath in forest_files.items():

    site_las = laspy.read(filepath)
    heights = np.asarray(site_las.z)

    # Filter by selected height range
    heights = heights[
        np.isfinite(heights) &
        (heights >= height_range[0]) &
        (heights <= height_range[1])
    ]

    if len(heights) == 0:
        rh25 = rh50 = rh98 = np.nan
    else:
        rh25, rh50, rh98 = np.percentile(
            heights, [25, 50, 98]
        )

    rh_results.append({
        "Forest": forest_name,
        "RH25 (m)": rh25,
        "RH50 (m)": rh50,
        "RH98 (m)": rh98
    })

rh_df = pd.DataFrame(rh_results)

# Create three pseudo-waveform plots
transect_figures = []

for metric, rh in rh_values.items():

    fig_rh = go.Figure()

    fig_rh.add_trace(
        go.Scatter(
            x=density,
            y=bin_centers,
            mode="lines",
            line=dict(color="black", width=1.5),
            showlegend=False
        )
    )

    fig_rh.add_hline(
        y=rh,
        line_color="red",
        line_dash="dash",
        annotation_text=f"{metric}: {rh:.1f} m",
        annotation_position="top right"
    )

    fig_rh.update_layout(
        title=metric,
        xaxis_title="Return Density",
        yaxis_title="Height (m)",
        height=300,
        margin=dict(l=45, r=15, t=35, b=35),
        showlegend=False
    )

    transect_figures.append(fig_rh)
    
with right:
    for i, fig_rh in enumerate(transect_figures):
        st.plotly_chart(
            fig_rh,
            use_container_width=True,
            key=f"rh_profile_{i}"
        )
        
with center: 
    st.markdown("<label style='font-size: 15px;'>Forest Structure Comparison</h1>", unsafe_allow_html=True)

    st.dataframe(
        rh_df.style.format({
            "RH25 (m)": "{:.2f}",
            "RH50 (m)": "{:.2f}",
            "RH98 (m)": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

  