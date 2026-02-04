import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Leaf, AlertTriangle, Mountain } from "lucide-react";

interface NDVIStats {
  healthy_vegetation_percent: number;
  moderate_vegetation_percent: number;
  stressed_vegetation_percent: number;
  bare_land_percent: number;
  mean_ndvi: number;
}

interface InsightsPanelProps {
  stats: NDVIStats | null;
}

const InsightsPanel = ({ stats }: InsightsPanelProps) => {
  if (!stats) {
    return (
      <Card className="scientific-card">
        <CardHeader>
          <CardTitle>Analysis Insights</CardTitle>
        </CardHeader>
        <CardContent className="text-center text-muted-foreground">
          Generate NDVI to see vegetation insights
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="scientific-card">
      <CardHeader>
        <CardTitle>Analysis Insights</CardTitle>
      </CardHeader>

      <CardContent className="grid grid-cols-3 gap-4">
        <Stat
          icon={Leaf}
          label="Healthy"
          value={stats.healthy_vegetation_percent}
        />
        <Stat
          icon={AlertTriangle}
          label="Stressed"
          value={stats.stressed_vegetation_percent}
        />
        <Stat icon={Mountain} label="Bare" value={stats.bare_land_percent} />

        <div className="col-span-3 text-center mt-4 text-sm">
          Mean NDVI: <b>{stats.mean_ndvi}</b>
        </div>
      </CardContent>
    </Card>
  );
};

const Stat = ({
  icon: Icon,
  label,
  value,
}: {
  icon: any;
  label: string;
  value: number;
}) => (
  <div className="text-center p-4 bg-muted/30 rounded">
    <Icon className="mx-auto mb-2 h-5 w-5" />
    <p className="text-xl font-bold">{value}%</p>
    <p className="text-xs">{label}</p>
  </div>
);

export default InsightsPanel;
