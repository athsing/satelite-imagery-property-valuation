# Satellite Imagery Based Property Valuation

This repository contains a **multimodal regression pipeline** for predicting property prices by combining  
**tabular housing attributes** with **satellite imagery–based features** extracted using a pretrained CNN.

## Project Overview

The model estimates house prices using:
- **Tabular data** (structural, location-based, and engineered features)
- **Satellite images** of properties
- **Image embeddings** extracted using a pretrained **ResNet-50**
- **Gradient boosting models** for final price prediction

The pipeline follows this high-level flow:

1. Raw tabular data preprocessing and feature engineering  
2. Satellite image download (API-based)  
3. Image embedding extraction using a pretrained CNN  
4. Dimensionality reduction of image features  
5. Multimodal regression using tabular + image features  

## Repository Structure

```text
satelite-imagery-property-valuation/
├── data/
│   ├── raw/              # Original CSV datasets
│   ├── images/           # Train/Test satellite images (Git LFS)
│   └── processed/        # Processed features and embeddings (Git LFS)
│
├── notebooks/
│   ├── preprocessing.ipynb       # Data Cleaning and Feature Engineering
│   └── model_training.ipynb      # Training Loop for the Model
│
├── src/
│   └── datafetcher.py    # Script for satellite image download
│
├── 24113027_final.csv    # Final price predictions
├── .gitattributes        # Git LFS configuration
├── .gitignore
└── README.md
```

## Satellite Image Download (Mapbox API)

Satellite images are fetched using the **Mapbox Static Images API**.

### Note on Mapbox Token

- **The Mapbox access token is intentionally NOT included in this original source code**
    MAPBOX_TOKEN="pk.eyJ1IjoiYXRoc2luZyIsImEiOiJjbWppNWo4azkweXdjM2RxdnRoZWlsejl3In0.--SlKohb554GbcuUFRnBSQ"
- Users must provide their **own Mapbox token**

## Image Embedding Extraction

- Satellite images are resized to **224 × 224** and normalized using ImageNet statistics
- A pretrained **ResNet-50** (ImageNet weights) is used as a fixed feature extractor 
- The final classification layer is removed
- Each image is converted into a **2048-dimensional embedding vector**
- Embeddings are saved as CSV files in `data/processed/`  

The embeddings serve as high-level visual representations of the surrounding built environment.

## Modelling Approach

### Tabular Features
- Structural attributes (bedrooms, bathrooms, area, floors, condition, grade)
- Renovation-based features (house age, years since renovation)
- Location-aware engineered features (zipcode-level price statistics)

### Image Features
- ResNet-50 image embeddings
- Standard scaling followed by PCA-based dimensionality reduction
- Reduced image features are weighted and fused with tabular data

### Models Used
- **HistGradientBoostingRegressor** for tabular-only baselines
- **XGBoost Regressor** for multimodal regression

Target values are log-transformed during training and inverse-transformed at inference.

## Reproducibility & Git LFS

This repository uses **Git Large File Storage (Git LFS)** to manage:
- Satellite image datasets
- Large processed CSV files (image embeddings, feature matrices)

After cloning the repository, run:
```bash
git lfs pull
```
## Requirements

Primary libraries used in this project:

- Python 3.10+
- NumPy
- Pandas
- PyTorch
- Torchvision
- Scikit-learn
- XGBoost
- TQDM
- Pillow (PIL)

Exact versions can be inferred from the Jupyter notebooks.
  
## Final Outputs

- `24113027_final.csv` — final predicted property prices  
- Processed feature files and embeddings stored in `data/processed/`  
- End-to-end reproducible pipeline from raw data to final predictions

## Notes

- End-to-end CNN training was explored, but did not outperform pretrained embeddings  
- Grad-CAM-based visual analysis was performed for interpretability  
- Emphasis was placed on reproducibility, clarity, and real-world ML practices  
- All large data files are intentionally tracked using Git LFS



