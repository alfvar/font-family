import torch
import numpy as np
import matplotlib.pyplot as plt

# Load the preprocessed images
images = torch.load("images.pt")

# Load the cluster labels
cluster_labels = np.load("cluster_labels.npy")

# Load the feature vectors
features = np.load("features.npy")

# Compute the pairwise distances between feature vectors
distances = np.linalg.norm(features[:, np.newaxis] - features, axis=2)

# Sort the images by cluster label and distance
sorted_indices = np.lexsort((distances, cluster_labels))
sorted_images = [images[i].cpu().numpy() for i in sorted_indices]

# Create a grid of subplots and display the images
nrows, ncols = 2, 5
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 6))
for i, ax in enumerate(axes.flat):
    if i < len(sorted_images):
        img = sorted_images[i]
        img = np.transpose(img, (1, 2, 0))  # convert from (C, H, W) to (H, W, C)
        ax.imshow(img)
        ax.set_title(f"Cluster {cluster_labels[sorted_indices[i]]}")
        ax.axis("off")
    else:
        ax.axis("off")

plt.tight_layout()
plt.show()
