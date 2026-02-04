"""
Vegetation Health Analysis using Satellite NDVI
FastAPI Backend for Computing NDVI from Sentinel-2 Imagery

This module provides an API endpoint to compute the Normalized Difference 
Vegetation Index (NDVI) from Sentinel-2 Red (B04) and Near-Infrared (B08) bands.

NDVI Formula: (NIR - RED) / (NIR + RED)
Range: -1 to +1
- Values > 0.5: Healthy vegetation
- Values 0.2-0.5: Stressed vegetation  
- Values < 0.2: Non-vegetation (soil, water, urban)
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import io
from typing import Dict, Tuple
import tempfile
import os

# Initialize FastAPI application
app = FastAPI(
    title="Vegetation Health Analysis API",
    description="Compute NDVI from Sentinel-2 satellite imagery",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_band(file_bytes: bytes, filename: str) -> np.ndarray:
    """
    Read a satellite image band from uploaded file bytes.
    
    Args:
        file_bytes: Raw bytes of the uploaded file
        filename: Original filename (used to determine format)
    
    Returns:
        2D numpy array containing the band data
    
    Raises:
        ValueError: If the file cannot be read or has invalid format
    """
    # Create temporary file to store uploaded data
    # Rasterio requires file-like objects or paths
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    
    try:
        # Open the raster file using Rasterio
        with rasterio.open(tmp_path) as src:
            # Read the first band (Sentinel-2 bands are single-channel)
            band_data = src.read(1)
            
            # Convert to float for numerical computation
            # Sentinel-2 data is typically uint16
            band_data = band_data.astype(np.float32)
            
        return band_data
    
    except Exception as e:
        raise ValueError(f"Error reading band file {filename}: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def compute_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    """
    Compute NDVI from Red and Near-Infrared bands.
    
    NDVI = (NIR - RED) / (NIR + RED)
    
    Physics: Healthy vegetation strongly reflects NIR and absorbs Red light
    for photosynthesis, resulting in high NDVI values.
    
    Args:
        red_band: 2D array of Red band reflectance (B04)
        nir_band: 2D array of NIR band reflectance (B08)
    
    Returns:
        2D array of NDVI values ranging from -1 to +1
    
    Raises:
        ValueError: If band dimensions don't match
    """
    # Validate that both bands have the same dimensions
    if red_band.shape != nir_band.shape:
        raise ValueError(
            f"Band dimension mismatch: RED {red_band.shape} vs NIR {nir_band.shape}"
        )
    
    # Compute numerator and denominator
    numerator = nir_band - red_band
    denominator = nir_band + red_band
    
    # Handle division by zero: set NDVI to 0 where denominator is 0
    # This occurs in completely dark pixels (both bands = 0)
    ndvi = np.zeros_like(numerator, dtype=np.float32)
    
    # Only compute NDVI where denominator is non-zero
    # Use a small epsilon to avoid numerical instability
    valid_mask = np.abs(denominator) > 1e-6
    ndvi[valid_mask] = numerator[valid_mask] / denominator[valid_mask]
    
    # Clip NDVI to theoretical range [-1, 1]
    # This handles any potential numerical overflow
    ndvi = np.clip(ndvi, -1.0, 1.0)
    
    return ndvi


def calculate_statistics(ndvi: np.ndarray) -> Dict[str, float]:
    """
    Calculate vegetation health statistics from NDVI values
    using only physically valid pixels.
    """

    # Remove NaN and Inf values (true invalid pixels)
    valid_ndvi = ndvi[np.isfinite(ndvi)]

    if valid_ndvi.size == 0:
        raise ValueError("No valid NDVI pixels found after masking")

    total_pixels = valid_ndvi.size

    # Standard NDVI classification (remote sensing)
    healthy = np.sum(valid_ndvi > 0.6)
    moderate = np.sum((valid_ndvi > 0.4) & (valid_ndvi <= 0.6))
    stressed = np.sum((valid_ndvi > 0.2) & (valid_ndvi <= 0.4))
    bare = np.sum(valid_ndvi <= 0.2)

    stats = {
        "healthy_vegetation_percent": round((healthy / total_pixels) * 100, 2),
        "moderate_vegetation_percent": round((moderate / total_pixels) * 100, 2),
        "stressed_vegetation_percent": round((stressed / total_pixels) * 100, 2),
        "bare_land_percent": round((bare / total_pixels) * 100, 2),
        "mean_ndvi": round(float(np.mean(valid_ndvi)), 3),
        "std_ndvi": round(float(np.std(valid_ndvi)), 3),
        "min_ndvi": round(float(np.min(valid_ndvi)), 3),
        "max_ndvi": round(float(np.max(valid_ndvi)), 3),
        "total_valid_pixels": int(total_pixels)
    }

    return stats




def generate_ndvi_image(ndvi: np.ndarray) -> io.BytesIO:
    """
    Generate a color-mapped NDVI visualization.
    
    Color scheme:
    - Red: Low NDVI (non-vegetated areas)
    - Yellow: Medium NDVI (stressed vegetation)
    - Green: High NDVI (healthy vegetation)
    
    Args:
        ndvi: 2D array of NDVI values
    
    Returns:
        BytesIO buffer containing PNG image
    """
    # Create figure with appropriate size
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define custom colormap for vegetation visualization
    # Red (low) -> Yellow (medium) -> Green (high)
    cmap = colors.LinearSegmentedColormap.from_list(
        "ndvi",
        ["#8B0000", "#FF4500", "#FFD700", "#ADFF2F", "#228B22"],
        N=256
    )
    
    # Display NDVI with colormap
    im = ax.imshow(ndvi, cmap=cmap, vmin=-1, vmax=1)
    
    # Add colorbar with label
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label('NDVI Value', rotation=270, labelpad=20, fontsize=12)
    
    # Set title and remove axes for cleaner appearance
    ax.set_title('NDVI - Vegetation Health Map', fontsize=14, fontweight='bold')
    ax.axis('off')
    
    # Save to buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    # Reset buffer position to beginning
    buf.seek(0)
    
    return buf


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Vegetation Health Analysis API",
        "version": "1.0.0",
        "description": "Compute NDVI from Sentinel-2 satellite imagery",
        "endpoints": {
            "/compute-ndvi": "POST - Upload Red and NIR bands to compute NDVI"
        }
    }


@app.post("/compute-ndvi")
async def compute_ndvi_endpoint(
    red_band: UploadFile = File(..., description="Red band image (B04) - .jp2 or .tif"),
    nir_band: UploadFile = File(..., description="NIR band image (B08) - .jp2 or .tif")
):
    """
    Compute NDVI from Sentinel-2 Red (B04) and NIR (B08) bands.
    
    This endpoint accepts two satellite image files, computes the NDVI,
    generates a visualization, and returns statistics.
    
    Args:
        red_band: Uploaded Red band file (Sentinel-2 B04)
        nir_band: Uploaded NIR band file (Sentinel-2 B08)
    
    Returns:
        JSON response with NDVI statistics and image download information
    
    Raises:
        HTTPException: If file reading or processing fails
    """
    try:
        # Read uploaded files
        red_bytes = await red_band.read()
        nir_bytes = await nir_band.read()
        
        # Parse bands using Rasterio
        red_array = read_band(red_bytes, red_band.filename)
        nir_array = read_band(nir_bytes, nir_band.filename)
        
        # Compute NDVI
        ndvi = compute_ndvi(red_array, nir_array)
        
        # Calculate statistics
        stats = calculate_statistics(ndvi)
        
        # Generate visualization
        image_buffer = generate_ndvi_image(ndvi)
        
        # Return image as streaming response
        # Statistics are included in response headers for easy access
        return StreamingResponse(
            image_buffer,
            media_type="image/png",
           headers={
    "X-Healthy-Vegetation": str(stats["healthy_vegetation_percent"]),
    "X-Moderate-Vegetation": str(stats["moderate_vegetation_percent"]),
    "X-Stressed-Vegetation": str(stats["stressed_vegetation_percent"]),
    "X-Bare-Land": str(stats["bare_land_percent"]),
    "X-Mean-NDVI": str(stats["mean_ndvi"])
}

        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during NDVI computation: {str(e)}"
        )


@app.post("/compute-ndvi-json")
async def compute_ndvi_json_endpoint(
    red_band: UploadFile = File(..., description="Red band image (B04) - .jp2 or .tif"),
    nir_band: UploadFile = File(..., description="NIR band image (B08) - .jp2 or .tif")
):
    """
    Compute NDVI and return statistics only (no image).
    
    This endpoint is useful for batch processing or when only
    statistical analysis is needed without visualization.
    
    Args:
        red_band: Uploaded Red band file (Sentinel-2 B04)
        nir_band: Uploaded NIR band file (Sentinel-2 B08)
    
    Returns:
        JSON response with NDVI statistics
    """
    try:
        # Read uploaded files
        red_bytes = await red_band.read()
        nir_bytes = await nir_band.read()
        
        # Parse bands using Rasterio
        red_array = read_band(red_bytes, red_band.filename)
        nir_array = read_band(nir_bytes, nir_band.filename)
        
        # Compute NDVI
        ndvi = compute_ndvi(red_array, nir_array)
        
        # Calculate statistics
        stats = calculate_statistics(ndvi)
        
        return {
            "status": "success",
            "message": "NDVI computed successfully",
            "statistics": stats
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during NDVI computation: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    # Run the FastAPI application
    # Host 0.0.0.0 allows external connections (important for Docker)
    # Port 8000 is the standard FastAPI port
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )