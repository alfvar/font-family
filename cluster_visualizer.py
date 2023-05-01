import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Load the feature vectors
features = np.load("features.npy")

# Perform PCA to reduce the dimensionality to 2D
pca = PCA(n_components=2)
features_2d = pca.fit_transform(features)

# Load the cluster labels
labels = np.load("cluster_labels.npy")

# Get the filenames for the images in the same order they were processed
filenames = sorted([f for f in os.listdir("font-data") if f.endswith(".png")])

# Create a new matplotlib figure and axes with a larger size and higher DPI
fig, ax = plt.subplots(1, figsize=(24, 18), dpi=150)

# Set the axes limits
ax.set_xlim(features_2d[:, 0].min() - 10, features_2d[:, 0].max() + 10)
ax.set_ylim(features_2d[:, 1].min() - 10, features_2d[:, 1].max() + 10)

# Go through font-data directory
for filename, (x, y), label in zip(filenames, features_2d, labels):
    img = Image.open(os.path.join("font-data", filename))
    width, height = img.size
    glyph = img.crop((3*width//10, 3*height//10, 4*width//10, 4*height//10))  # Extract a part of the image
    glyph.thumbnail((20, 20), Image.ANTIALIAS)  # Resize the glyph to a smaller size

    # Convert the PIL Image to a numpy array
    img_array = np.array(glyph)

    # If the image has a transparency layer, get the RGB channels and ignore the alpha channel
    if img_array.ndim == 3 and img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    # If the image is not entirely white
    if np.sum(img_array) < img_array.size * 255 - 1000:  # Adjust the threshold if necessary
        # Print some debug information

        # Create an image glyph at the given coordinates with the given label as color
        im = OffsetImage(img_array, zoom=0.3)  # Reduce zoom level to avoid overlapping
        ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False)
        ax.add_artist(ab)

        # Add a marker at the position where the image is added
        ax.plot(x, y, marker='o', markersize=5, color='red')
    else:
        print(f"Image {filename} is entirely white")

plt.savefig("cluster_visualization.png")
