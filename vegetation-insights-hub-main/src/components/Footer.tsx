const Footer = () => {
  return (
    <footer className="bg-card border-t border-border mt-12">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="text-center md:text-left">
            <p className="font-medium text-foreground">
              Vegetation Health Analysis using Satellite NDVI
            </p>
            <p className="text-xs mt-1">
              Research & Educational Tool • Sentinel-2 Data Processing
            </p>
          </div>
          <div className="text-center md:text-right text-xs">
            <p>Data Source: Copernicus Sentinel-2 Mission (ESA)</p>
            <p className="mt-1">
              For research and educational purposes only
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
