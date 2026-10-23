# Seeing the Trees for the Forest: A Streamlit-based Application for Visualizing Forest Structure with LiDAR

An interactive Streamlit application for exploring three-dimensional forest structure using airborne light detection and ranging (LiDAR) data. 

This application allows users to visualize LiDAR point clouds and compare relative height metrics across three distinct forest types.

Access the web version here: https://forestlidar.streamlit.app/

# Overview 
## Background
Forest structure is a fundamental characteristic of plant communities and plays an essential role in ecosystem functions (Ehbrecht et al., 2021). Forest structure primarily refers to the three-dimensional (3-D) arrangement of vegetation in a forest, extending from the forest floor to the top of the canopy (Oliver and Larson, 1996). Light detection and ranging (LiDAR) technologies provide a powerful tool for retrieving forest structure measurements across multiple dimensions (Coops et al., 2021). However, processing and visualizing these data can require specialized software and substantial computational resources.

_Seeing the Trees for the Forest_ provides an accessible interface for exploring forest structure without requiring users to directly manipulate raw LiDAR datasets. This allows users to investigate the question: How do LiDAR-derived measurements of vertical forest structure vary across ecosystems with different vegetation types and climatic conditions?

## Methods
There are many different approaches for estimating forest structure from LiDAR, but for this app we focus on relative height (RHn), as it is applicable to both spaceborne and airborne platforms and has demonstrated relation to biomass and canopy volume (Lefsky 2002). RHn are defined as the distance between the elevations of detected ground return and the n% accumulated waveform energy, where n ranges from 1 to 100 (Duncanson et al., 2020).

For this application, three analogous RH metrics are calculated directly from the distribution of height-normalized discrete LiDAR returns:

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
├── app.py   # main app script
├── assets/ 
├── requirements.txt  # dependencies
├── data/              # data used    
├── notebooks/            
│   ├── analysis.ipynb  # figure generation script
│   └── preprocessing.R  # preprocessing script
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
pip install -r requirements.txt
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

# Limitations 
As of now, this app is an exploratory visualization tool for examining forest structure, and derived metrics, across three distinct NEON sites. Users are unable to upload their own data for inference or export the derived metrics for use in analysis. 

RH is a metric typically derived from full waveform data. The calculation of RH metrics using discretized data can potentially induce error depending on the LiDAR sensors specification; differences in scan angle, point density, and return classification can influence the vertical distribution of LiDAR returns. Users should use caution when interpreting the results of this data. 

# Acknowledgements 
This material is based in part upon work supported by the National Ecological Observatory Network (NEON), a program sponsored by the U.S. National Science Foundation (NSF) and operated under cooperative agreement by Battelle.

# AI-use disclosure 
The author used ChatGPT (OpenAI, GPT-6, accessed October 2026) to assist with debugging code for the streamlit interface.
The author tested all generated code, and made modifications. ChatGPT was not used for project conceptualization, data processing decisions, interpreting findings, or writing. The author takes sole responsibility for the final code and content.

# References 
Coops, N.C., Tompalski, P., Goodbody, T.R.H., Queinnec, M., Luther, J.E., Bolton, D.K., White, J.C., Wulder, M.A., Lier, O.R. van, Hermosilla, T., 2021. Modelling lidar-derived estimates of forest attributes over space and time: A review of approaches and future trends. Remote Sensing of Environment 260, 112477. https://doi.org/10.1016/j.rse.2021.112477

Duncanson, L., Neuenschwander, A., Hancock, S., Thomas, N., Fatoyinbo, T., Simard, M., Silva, C.A., Armston, J., Luthcke, S.B., Hofton, M., Kellner, J.R., Dubayah, R., 2020. Biomass estimation from simulated GEDI, ICESat-2 and NISAR across environmental gradients in Sonoma County, California. Remote Sensing of Environment 242, 111779. https://doi.org/10.1016/j.rse.2020.111779

Ehbrecht, M., Seidel, D., Annighöfer, P., Kreft, H., Köhler, M., Zemp, D.C., Puettmann, K., Nilus, R., Babweteera, F., Willim, K., Stiers, M., Soto, D., Boehmer, H.J., Fisichelli, N., Burnett, M., Juday, G., Stephens, S.L., Ammer, C., 2021. Global patterns and climatic controls of forest structural complexity. Nat Commun 12, 519. https://doi.org/10.1038/s41467-020-20767-z

Lefsky, M.A., Cohen, W.B., Parker, G.G., Harding, D.J., 2002. Lidar Remote Sensing for Ecosystem Studies: Lidar, an emerging remote sensing technology that directly measures the three-dimensional distribution of plant canopies, can accurately estimate vegetation structural attributes and should be of particular interest to forest, landscape, and global ecologists. BioScience 52, 19–30. https://doi.org/10.1641/0006-3568(2002)052%255B0019:LRSFES%255D2.0.CO;2
Oliver, C.D., Larson, B., 1996. Forest stand dynamics. New York.

