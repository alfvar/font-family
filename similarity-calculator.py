import os
import torch
import torchvision.transforms as transforms
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

# Set up the device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the images and preprocess them
images = []
for filename in os.listdir("font-data"):
    if filename.endswith(".png"):
        img = Image.open(os.path.join("font-data", filename)).convert("RGB")
        img = transforms.Resize((224, 224))(img)  # resize to 224x224
        img = transforms.ToTensor()(img)  # convert to tensor
        img = transforms.Normalize(mean=[0.485, 0.456, 0.406],  # normalize
                                   std=[0.229, 0.224, 0.225])(img)
        images.append(img.to(device))

# Load a pre-trained CNN model
model = torch.hub.load('pytorch/vision', 'resnet18', pretrained=True)
model.eval()
model.to(device)

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
