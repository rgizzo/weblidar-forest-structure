# Title: preprocessing.R 
# Author: TRG
# Date: 10/21/2026 
#
# This script demonstrates the preprocessing workflow used to prepare
# airborne LiDAR point clouds for the Seeing the Trees for the Forest
# Streamlit application.
#
# Using a classified NEON airborne LiDAR tile from Talladega National
# Forest (TALL), the script extracts a 50 x 50 m subset, removes
# classified noise returns, normalizes point heights using a
# 1 m resolution digital terrain model (DTM), and filters extreme
# Z values.
#
# The resulting height-normalized point cloud is exported as a
# compressed LAZ file for interactive visualization and analysis.

# The data used here can be downloaded from the NEON open data repository
# discrete point cloud LiDAR:
# https://data.neonscience.org/data-products/DP1.30003.001

# The site used in this example is Talladega National Forest (TALL) and the 
# year the data was downloaded for it 2025. The tile number exact tile file:
# NEON_D08_TALL_DP1_461000_3645000_classified_point_cloud_colorized.laz


# lets load some packages
library(lidR)

#-------------------------
# set paths for ya directories
#-------------------------
# laz input directory
input.dir <- file.path("data/raw")

# specify output directory for the laz file 
output.dir <- file.path("data/processed")

# create directory if it does not exist
if(!dir.exists(output.dir)){
  dir.create(output.dir)
}

#------------------
# load point clouds 
#-----------------
# load a nice looking point cloud 
las <- readLAS(file.path(input.dir, 
                         "NEON_D08_TALL_DP1_461000_3645000_classified_point_cloud_colorized.laz"))

# plot so we can really see what's up
plot(las, color = "RGB", bg = "white")

# lets double check that there are valid RGB values 
names(las@data)
summary(las@data[, c("R","G","B")])

#---------
# crop 
#---------

# now lets crop to a 50 x 50 m subset of the tile 
las_crop <- clip_rectangle(
  las,
  xleft   = 461950,
  ybottom = 3645500,
  xright  = 462000,
  ytop    = 3645550
)

# now plot 
plot(las_crop, color = "RGB", bg = "white", size = 3)

#---------
# remove noise classified points
#-----------
las_crop <- filter_poi(las_crop, Classification != 7L & Classification != 18L)

#-----------
# normalize 
#-----------

# since the tile isn't cleaned lets normalize and remove some outliers 
dtm <- rasterize_terrain(las_crop, res = 1, algorithm = tin())
las_norm <- normalize_height(las_crop, dtm)

#-----------
# remove extreme z outliers
#-----------
zmin <- quantile(las_norm$Z, 0.01, na.rm = TRUE)
zmax <- quantile(las_norm$Z, 0.995, na.rm = TRUE)

# filter 
las_plot<- filter_poi(las_norm, Z >= zmin & Z <= zmax)

# now check again! 
plot(las_plot, color = "RGB", bg = "white", size = 3)

# export cropped, cleaned point cloud 
writeLAS(las_plot, file.path(output.dir, "TALL_cropped.laz"))
