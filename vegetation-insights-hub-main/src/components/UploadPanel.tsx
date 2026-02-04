import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useState } from "react";

interface UploadPanelProps {
  onGenerate: (red: File, nir: File) => void;
  isProcessing: boolean;
}

const UploadPanel = ({ onGenerate, isProcessing }: UploadPanelProps) => {
  const [redBand, setRedBand] = useState<File | null>(null);
  const [nirBand, setNirBand] = useState<File | null>(null);

  const canGenerate = !!(redBand && nirBand && !isProcessing);

  return (
    <Card className="scientific-card">
      <CardHeader>
        <CardTitle>Input Data</CardTitle>
        <p className="text-sm text-muted-foreground">
          Upload Sentinel-2 Red (B04) and NIR (B08) bands
        </p>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* RED BAND */}
        <div>
          <label className="text-xs font-medium">Red Band (B04)</label>
          <input
            type="file"
            accept=".jp2,.tif,.tiff"
            onChange={(e) => setRedBand(e.target.files?.[0] || null)}
            className="w-full text-sm"
          />
        </div>

        {/* NIR BAND */}
        <div>
          <label className="text-xs font-medium">NIR Band (B08)</label>
          <input
            type="file"
            accept=".jp2,.tif,.tiff"
            onChange={(e) => setNirBand(e.target.files?.[0] || null)}
            className="w-full text-sm"
          />
        </div>

        <Button
          disabled={!canGenerate}
          onClick={() => redBand && nirBand && onGenerate(redBand, nirBand)}
          className="w-full"
        >
          {isProcessing ? "Processing NDVI…" : "Generate NDVI"}
        </Button>

        <p className="text-xs text-center font-mono text-muted-foreground">
          NDVI = (NIR − Red) / (NIR + Red)
        </p>
      </CardContent>
    </Card>
  );
};

export default UploadPanel;
