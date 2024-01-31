import os
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np


device = torch.device("mps" if torch.cuda.is_available() else "cpu") # Set up the device (CPU or GPU)

# Load the images and preprocess them
images = []
for filename in os.listdir("font-data"):
    if filename.endswith(".png"): # Target all images
        img = Image.open(os.path.join("font-data", filename)).convert("RGB") # Set the mode to RGB
        img = transforms.Resize((512, 512))(img)  # resize to 512x512
        img = transforms.ToTensor()(img)  # convert to tensor
        img = transforms.Normalize(mean=[0.485, 0.456, 0.406],  # normalize
                                   std=[0.229, 0.224, 0.225])(img)
        images.append(img.to(device))

# Load a pre-trained CNN model
resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
resnet50(weights="IMAGENET1K_V1")

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)


# Extract features from the images using the pre-trained model
features = []
with torch.no_grad():
    for img in images:
        feat = model(img.unsqueeze(0)).squeeze().cpu().numpy()
        features.append(feat)

# Perform clustering using K-means
kmeans = KMeans(n_clusters=5, random_state=0).fit(features)

# Save the preprocessed images to a file
torch.save(images, "images.pt")

# Save the cluster labels to a file
np.save("cluster_labels.npy", kmeans.labels_)

# Save the feature vectors to a file
np.save("features.npy", features)
