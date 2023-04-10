import os
import json
import cv2
import numpy as np
from sklearn.cluster import KMeans
from math import ceil
from skimage import io
from PIL import Image


folder_path = "output/"

all_files = os.listdir(folder_path)
image_files = [f for f in all_files if f.endswith(".png")]
metadata_files = [f for f in all_files if f.endswith(".json")]

image_paths = [os.path.join(folder_path, f) for f in image_files]
metadata_paths = [os.path.join(folder_path, f) for f in metadata_files]

image_paths.sort()
metadata_paths.sort()

# Feature extraction
sift = cv2.SIFT_create()

descriptors_list = []

for image_path in image_paths:
    img = io.imread(image_path, as_gray=True)
    if img is None or img.dtype != 'uint8':
        print(f"Error: Image '{image_path}' is empty or has incorrect depth.")
        continue

    keypoints, descriptors = sift.detectAndCompute(img, None)
    descriptors_list.append(descriptors)

# Stack all the descriptors vertically in a numpy array
all_descriptors = np.vstack(descriptors_list)

# Perform k-means clustering
k = 5  # Number of clusters
kmeans = KMeans(n_clusters=k)
kmeans.fit(all_descriptors)

# Create a histogram of clustered descriptors for each image
image_histograms = []

for descriptors in descriptors_list:
    histogram = np.zeros(k)
    clusters = kmeans.predict(descriptors)
    for cluster in clusters:
        histogram[cluster] += 1
    image_histograms.append(histogram)

# Perform k-means clustering on image histograms
k = 5  # Number of font clusters
kmeans = KMeans(n_clusters=k)
font_clusters = kmeans.fit_predict(image_histograms)

# Print font clusters
for i, font_cluster in enumerate(font_clusters):
    metadata_path = metadata_paths[i]
    with open(metadata_path) as f:
        metadata = json.load(f)
    print(f"Font: {metadata['name']} {metadata['style-head']} | Cluster: {font_cluster}")

k = 5  # Number of font clusters
kmeans = KMeans(n_clusters=k)
font_clusters = kmeans.fit_predict(image_histograms)

# Save font clusters in a dictionary
clustered_fonts = {i: [] for i in range(k)}

for i, font_cluster in enumerate(font_clusters):
    metadata_path = metadata_paths[i]
    with open(metadata_path) as f:
        metadata = json.load(f)
    print(f"Font: {metadata['name']} {metadata['style-head']} | Cluster: {font_cluster}")

    font_file = os.path.split(image_paths[i])[-1]
    clustered_fonts[font_cluster].append(font_file)

    output_dir = 'output'
collage_dir = 'collage'
os.makedirs(collage_dir, exist_ok=True)

max_fonts_per_row = 5
thumbnail_size = (224, 224)

# Iterate through clusters and create a collage image
for cluster, font_files in clustered_fonts.items():
    num_rows = ceil(len(font_files) / max_fonts_per_row)
    num_columns = min(max_fonts_per_row, len(font_files))
    collage_width = num_columns * thumbnail_size[0]
    collage_height = num_rows * thumbnail_size[1]

    collage_img = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))

    for idx, font_file in enumerate(font_files):
        img_path = os.path.join(output_dir, font_file)
        img = Image.open(img_path).convert('RGB')
        img.thumbnail(thumbnail_size)

        x = (idx % max_fonts_per_row) * thumbnail_size[0]
        y = (idx // max_fonts_per_row) * thumbnail_size[1]
        collage_img.paste(img, (x, y))

    collage_img.save(os.path.join(collage_dir, f'cluster_{cluster}.png'))
