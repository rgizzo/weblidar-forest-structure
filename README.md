# Seeing the Trees for the Forest: A Streamlit-based Application for Visualizing Forest Structure with LiDAR

An interactive Streamlit application for exploring three-dimensional forest structure using airborne light detection and ranging (LiDAR) data. 

This application allows users to visualize LiDAR point clouds and compare relative height metrics across three distinct forest types.

Access the web version here: https://forestlidar.streamlit.app/

# Overview 
## Background
Forest structure is a fundamental characteristic of plant communities and plays an essential role in ecosystem functions (Ehbrecht et al., 2021; Gamfeldt et al., 2012). Forest structure primarily refers to the three-dimensional (3-D) arrangement of vegetation in a forest, extending from the forest floor to the top of the canopy (Oliver and Larson, 1996). Light detection and ranging (LiDAR) technologies provide a powerful tool for retrieving forest structure measurements across multiple dimensions (Coops et al., 2021). However, processing and visualizing these data can require specialized software and substantial computational resources.

_Seeing the Trees for the Forest_ provides an accessible interface for exploring forest structure without requiring users to directly manipulate raw LiDAR datasets. This allows users to investigate the question: How do LiDAR-derived measurements of vertical forest structure vary across ecosystems with different vegetation types and climatic conditions?

## Methods
There are many different approaches for estimating forest structure from LiDAR, but for this app we focus on relative height (RHn), as it is applicable to both spaceborne and airborne platforms and has demonstrated relation to biomass and canopy volume (Lefsky 2002; Lim et al., 2003). RHn are defined as the distance between the elevations of detected ground return and the n% accumulated waveform energy, where n ranges from 1 to 100 (Duncanson et al., 2020).

For this application, analogous three RH metrics are calculated directly from the distribution of height-normalized discrete LiDAR returns:

- **RH25**: Height below which 25% of returns occur.

- **RH50**: Height below which 50% of returns occur.

- **RH98**: Height below which 98% of returns occur.

Users can explore how these measurements change when restricting the vertical range of the point cloud.

### Example plot of RH 25, 50, & 98
![RH fig](./figures/BART.png)

## Features

- **Interactive 3D visualization:** Explore LiDAR point clouds through rotation, zooming, and panning.
- **Forest selection:** Compare three distinct forest ecosystems: old growth deciduous, mixed pine, and longleaf pine savanna.
- **Point cloud visualization:** Color LiDAR returns by RGB, classification, or height.
- **Height filtering:** Interactively restrict the vertical range of displayed returns.
- **Vertical return-density profiles:** Examine the vertical distribution of LiDAR returns and associated RH metrics.
- **Site comparison:** Compare RH25, RH50, and RH98 across the three forest types.

# Repository Structure
```
weblidar-forest-structure/
├── README.md
├── app.py
├── assets/
│    └── app-demo.gif
├── requirements.txt      
├── data/                 
├── notebooks/            
│   ├── analysis.ipynb
│   └── preprocessing.R
└── figures/              
```
# Getting Started
clone the repository:
```
git clone https://github.com/rgizzo/weblidar-forest-structure.git
cd weblidar-forest-structure
```

Create a virtual environment:
```
python -m venv .venv
```

Activate the environment and install the required libraries:
```
pip install -r requirments.txt
```

Launch the application 
```
streamlit run app.py
```

![App Demo](./assets/app-demo.gif)

# Data Access

Airborne discrete-return LiDAR data were obtained from the National Ecological Observatory Network (NEON). The application uses approximately 50 × 50 m subsets from three NEON sites:

| Site | Location | Forest type | Year of Acquisition |
|---|---|---|---|
| BART | Bartlett Experimental Forest, New Hampshire | Old growth deciduous forest | 2025 |
| TALL | Talladega National Forest, Alabama | Mixed pine forest | 2025 |
| OSBS | Ordway-Swisher Biological Station, Florida | Longleaf pine savanna | 2025 |

The processed, height-normalized LAZ files used by the application are included in the `data/` directory.

The original NEON LiDAR datasets can be accessed through the [NEON Data Portal](https://data.neonscience.org/).

A representative preprocessing workflow is provided in `notebooks/preprocessing.R`. This script demonstrates cropping, noise filtering, height normalization, and percentile-based filtering using a classified LiDAR tile from TALL.

The original source tile must be downloaded separately to reproduce the preprocessing example.

# Acknowledgements 
All data was accessed 

# AI-use disclosure 

# References 
