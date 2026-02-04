import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, Satellite, Sprout } from "lucide-react";

const InfoSection = () => {
  return (
    <div className="grid md:grid-cols-3 gap-6">
      {/* What is NDVI */}
      <Card className="scientific-card">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            <CardTitle className="text-base">What is NDVI?</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground leading-relaxed">
            The <strong className="text-foreground">Normalized Difference Vegetation Index (NDVI)</strong> is 
            a quantitative measure of vegetation health derived from satellite imagery. 
            It ranges from −1 to +1, where higher values indicate denser, healthier vegetation. 
            NDVI is widely used in agriculture, forestry, and environmental monitoring.
          </p>
        </CardContent>
      </Card>

      {/* Why Red and NIR */}
      <Card className="scientific-card">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Satellite className="h-5 w-5 text-primary" />
            <CardTitle className="text-base">Why Red & NIR Bands?</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Healthy vegetation <strong className="text-foreground">absorbs red light</strong> for 
            photosynthesis and <strong className="text-foreground">reflects near-infrared (NIR) light</strong> due 
            to cell structure. By comparing these two bands, NDVI distinguishes vegetated areas 
            from non-vegetated surfaces. Sentinel-2's B04 (red) and B08 (NIR) bands are ideal for this analysis.
          </p>
        </CardContent>
      </Card>

      {/* Real-world Applications */}
      <Card className="scientific-card">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Sprout className="h-5 w-5 text-primary" />
            <CardTitle className="text-base">Agricultural Applications</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground leading-relaxed">
            NDVI enables <strong className="text-foreground">precision agriculture</strong> by identifying 
            crop stress before visible symptoms appear. It supports irrigation planning, yield estimation, 
            drought monitoring, and land-use classification. Government agencies use NDVI for 
            crop insurance assessment and food security monitoring.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default InfoSection;
