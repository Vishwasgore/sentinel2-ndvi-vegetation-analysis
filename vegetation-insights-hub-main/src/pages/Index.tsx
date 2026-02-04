import { useState } from "react";
import Header from "@/components/Header";
import UploadPanel from "@/components/UploadPanel";
import NDVIVisualization from "@/components/NDVIVisualization";
import InsightsPanel from "@/components/InsightsPanel";
import ColorLegend from "@/components/ColorLegend";
import InfoSection from "@/components/InfoSection";
import Footer from "@/components/Footer";
const API_BASE = import.meta.env.VITE_API_URL;

const Index = () => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleGenerate = async (redBand: File, nirBand: File) => {
    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append("red_band", redBand);
      formData.append("nir_band", nirBand);

      /* ===============================
         1️⃣ FETCH NDVI IMAGE
      =============================== */
      const imageResponse = await fetch(`${API_BASE}/compute-ndvi`, {
        method: "POST",
        body: formData,
      });

      if (!imageResponse.ok) {
        throw new Error("Failed to generate NDVI image");
      }

      const imageBlob = await imageResponse.blob();
      const imageObjectUrl = URL.createObjectURL(imageBlob);
      setImageUrl(imageObjectUrl);

      /* ===============================
         2️⃣ FETCH NDVI STATISTICS (JSON)
      =============================== */
      const statsResponse = await fetch(`${API_BASE}/compute-ndvi-json`, {
        method: "POST",
        body: formData,
      });

      if (!statsResponse.ok) {
        throw new Error("Failed to compute NDVI statistics");
      }

      const statsJson = await statsResponse.json();

      console.log("NDVI statistics from backend:", statsJson.statistics);

      // 🔥 THIS IS THE KEY FIX
      setStats(statsJson.statistics);
    } catch (error: any) {
      console.error(error);
      alert(error.message || "NDVI computation failed");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />

      <main className="flex-1 container mx-auto px-4 py-8">
        {/* Main Analysis Section */}
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          {/* Upload Panel */}
          <div className="lg:col-span-1">
            <UploadPanel
              onGenerate={handleGenerate}
              isProcessing={isProcessing}
            />
          </div>

          {/* NDVI Visualization */}
          <div className="lg:col-span-2">
            <NDVIVisualization imageUrl={imageUrl} />
          </div>
        </div>

        {/* Insights and Legend */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <InsightsPanel stats={stats} />
          <ColorLegend />
        </div>

        {/* Educational Information */}
        <section className="mb-8">
          <h2 className="section-title">Understanding NDVI</h2>
          <InfoSection />
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default Index;
