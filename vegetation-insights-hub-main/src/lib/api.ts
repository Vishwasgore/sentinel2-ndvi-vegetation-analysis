const API_BASE_URL = "http://localhost:8000";

export interface NDVIStats {
  healthy: number;
  stressed: number;
  nonVegetation: number;
  meanNDVI: number;
}

export async function computeNDVI(
  redBand: File,
  nirBand: File
): Promise<{ imageUrl: string; stats: NDVIStats }> {
  const formData = new FormData();
  formData.append("red_band", redBand);
  formData.append("nir_band", nirBand);

  const response = await fetch(`${API_BASE_URL}/compute-ndvi`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  const imageBlob = await response.blob();

  return {
    imageUrl: URL.createObjectURL(imageBlob),
    stats: {
      healthy: Number(response.headers.get("X-Healthy-Vegetation")),
      stressed: Number(response.headers.get("X-Stressed-Vegetation")),
      nonVegetation: Number(response.headers.get("X-Non-Vegetation")),
      meanNDVI: Number(response.headers.get("X-Mean-NDVI")),
    },
  };
}
