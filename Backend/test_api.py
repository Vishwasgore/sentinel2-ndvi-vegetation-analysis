"""
Test script for NDVI computation API
This script demonstrates how to use the API endpoints programmatically.
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

# Example file paths (update these to your actual Sentinel-2 band files)
RED_BAND_PATH = "data/T43QCC_20240203T053031_B04_10m.jp2"  # Replace with actual path
NIR_BAND_PATH = "data/T43QCC_20240203T053031_B08_10m.jp2"  # Replace with actual path


def test_root_endpoint():
    """Test the root endpoint to verify API is running."""
    print("=" * 60)
    print("Testing Root Endpoint")
    print("=" * 60)
    
    response = requests.get(f"{API_BASE_URL}/")
    
    if response.status_code == 200:
        print("✓ API is running")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Error: {response.status_code}")
    
    print()


def test_compute_ndvi_json():
    """Test NDVI computation with JSON response."""
    print("=" * 60)
    print("Testing NDVI Computation (JSON)")
    print("=" * 60)
    
    try:
        with open(RED_BAND_PATH, 'rb') as red_file, \
             open(NIR_BAND_PATH, 'rb') as nir_file:
            
            files = {
                'red_band': red_file,
                'nir_band': nir_file
            }
            
            response = requests.post(
                f"{API_BASE_URL}/compute-ndvi-json",
                files=files
            )
            
            if response.status_code == 200:
                print("✓ NDVI computed successfully")
                result = response.json()
                print(json.dumps(result, indent=2))
                
                # Display key statistics
                stats = result['statistics']
                print("\nKey Statistics:")
                print(f"  - Healthy Vegetation: {stats['healthy_vegetation_percent']}%")
                print(f"  - Stressed Vegetation: {stats['stressed_vegetation_percent']}%")
                print(f"  - Non-Vegetation: {stats['non_vegetation_percent']}%")
                print(f"  - Mean NDVI: {stats['mean_ndvi']}")
                
            else:
                print(f"✗ Error: {response.status_code}")
                print(response.text)
    
    except FileNotFoundError:
        print("✗ Error: Band files not found")
        print("Please update RED_BAND_PATH and NIR_BAND_PATH in this script")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print()


def test_compute_ndvi_image():
    """Test NDVI computation with image response."""
    print("=" * 60)
    print("Testing NDVI Computation (Image)")
    print("=" * 60)
    
    try:
        with open(RED_BAND_PATH, 'rb') as red_file, \
             open(NIR_BAND_PATH, 'rb') as nir_file:
            
            files = {
                'red_band': red_file,
                'nir_band': nir_file
            }
            
            response = requests.post(
                f"{API_BASE_URL}/compute-ndvi",
                files=files
            )
            
            if response.status_code == 200:
                print("✓ NDVI image generated successfully")
                
                # Save the image
                output_path = "ndvi_output.png"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Image saved to: {output_path}")
                
                # Display statistics from headers
                print("\nStatistics from response headers:")
                print(f"  - Healthy Vegetation: {response.headers.get('X-Healthy-Vegetation')}%")
                print(f"  - Stressed Vegetation: {response.headers.get('X-Stressed-Vegetation')}%")
                print(f"  - Non-Vegetation: {response.headers.get('X-Non-Vegetation')}%")
                print(f"  - Mean NDVI: {response.headers.get('X-Mean-NDVI')}")
                
            else:
                print(f"✗ Error: {response.status_code}")
                print(response.text)
    
    except FileNotFoundError:
        print("✗ Error: Band files not found")
        print("Please update RED_BAND_PATH and NIR_BAND_PATH in this script")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("NDVI API Test Suite")
    print("=" * 60 + "\n")
    
    # Test 1: Check if API is running
    test_root_endpoint()
    
    # Test 2: Compute NDVI with JSON response
    print("Note: Update RED_BAND_PATH and NIR_BAND_PATH to run tests 2 and 3\n")
    # Uncomment these lines when you have actual band files:
    # test_compute_ndvi_json()
    # test_compute_ndvi_image()
    
    print("=" * 60)
    print("Test suite completed")
    print("=" * 60)