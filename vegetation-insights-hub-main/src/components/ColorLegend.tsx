import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const ColorLegend = () => {
  const legendItems = [
    {
      range: "0.6 to 1.0",
      color: "hsl(142, 71%, 45%)",
      label: "Dense/Healthy Vegetation",
      description: "Forests, well-irrigated crops",
    },
    {
      range: "0.4 to 0.6",
      color: "hsl(84, 80%, 45%)",
      label: "Moderate Vegetation",
      description: "Grasslands, shrubs",
    },
    {
      range: "0.2 to 0.4",
      color: "hsl(45, 93%, 47%)",
      label: "Sparse/Stressed Vegetation",
      description: "Dry crops, stressed plants",
    },
    {
      range: "0.0 to 0.2",
      color: "hsl(30, 90%, 50%)",
      label: "Very Sparse Vegetation",
      description: "Bare soil with some cover",
    },
    {
      range: "-1.0 to 0.0",
      color: "hsl(0, 84%, 60%)",
      label: "No Vegetation",
      description: "Water, bare soil, urban",
    },
  ];

  return (
    <Card className="scientific-card">
      <CardHeader className="pb-4">
        <CardTitle className="section-title mb-0 border-0 pb-0">
          NDVI Classification Legend
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {legendItems.map((item, index) => (
            <div key={index} className="flex items-center gap-3">
              <div
                className="w-6 h-6 rounded flex-shrink-0"
                style={{ backgroundColor: item.color }}
              />
              <div className="flex-1 min-w-0">
                <div className="flex items-baseline gap-2">
                  <span className="font-medium text-sm">{item.label}</span>
                  <span className="text-xs text-muted-foreground font-mono">
                    [{item.range}]
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default ColorLegend;
