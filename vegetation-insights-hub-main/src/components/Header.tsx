import { Leaf } from "lucide-react";

const Header = () => {
  return (
    <header className="bg-card border-b border-border">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary rounded-md">
            <Leaf className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-xl md:text-2xl font-semibold text-foreground">
              Vegetation Health Analysis
            </h1>
            <p className="text-sm text-muted-foreground">
              Using Satellite NDVI from Sentinel-2 Imagery
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
