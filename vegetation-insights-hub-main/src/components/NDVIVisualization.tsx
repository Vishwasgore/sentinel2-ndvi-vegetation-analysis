import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface NDVIVisualizationProps {
  imageUrl: string | null;
}

const NDVIVisualization = ({ imageUrl }: NDVIVisualizationProps) => {
  return (
    <Card className="scientific-card h-full">
      <CardHeader>
        <CardTitle>NDVI Output Map</CardTitle>
        <p className="text-sm text-muted-foreground">
          Computed vegetation index
        </p>
      </CardHeader>

      <CardContent>
        {imageUrl ? (
          <img
            src={imageUrl}
            alt="NDVI Map"
            className="rounded border w-full"
          />
        ) : (
          <div className="h-64 flex items-center justify-center text-muted-foreground">
            Upload bands to generate NDVI
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default NDVIVisualization;
