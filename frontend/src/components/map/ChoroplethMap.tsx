import { useEffect, useRef } from 'react';
import type { KelurahanGeoJSON } from '../../types/kelurahan';
import type { USSLatestItem } from '../../types/uss';

// Declare atlas namespace for Azure Maps SDK loaded via CDN
declare global {
  interface Window {
    atlas: any;
  }
}

interface ChoroplethMapProps {
  geojson: KelurahanGeoJSON | null;
  loading: boolean;
  selectedId: string | null;
  onSelect: (item: USSLatestItem) => void;
}

export function ChoroplethMap({ geojson, loading, selectedId, onSelect }: ChoroplethMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<any>(null);
  const sourceRef = useRef<any>(null);
  const pointSourceRef = useRef<any>(null);
  const lineLayerRef = useRef<any>(null);

  useEffect(() => {
    let timeoutId: number;
    let retries = 0;

    const initMap = () => {
      if (!mapRef.current || mapInstance.current) return;
      
      if (!window.atlas) {
        if (retries < 50) { // Try for up to 5 seconds
          retries++;
          timeoutId = window.setTimeout(initMap, 100);
        } else {
          console.error("Azure Maps SDK failed to load");
        }
        return;
      }

      // Initialize Azure Map
      const map = new window.atlas.Map(mapRef.current, {
        center: [107.6191, -6.9175], // Bandung center
        zoom: 12, // Start closer to Bandung
        style: 'grayscale_light',
        authOptions: {
          authType: 'subscriptionKey',
          subscriptionKey: import.meta.env.VITE_AZURE_MAPS_KEY || '',
        },
      });

      mapInstance.current = map;

    map.events.add('ready', () => {
      const source = new window.atlas.source.DataSource();
      map.sources.add(source);
      sourceRef.current = source;

      const pointSource = new window.atlas.source.DataSource();
      map.sources.add(pointSource);
      pointSourceRef.current = pointSource;

      // 1. Polygon Layer (Choropleth) - Distinct Colors
      const polygonLayer = new window.atlas.layer.PolygonLayer(source, null, {
        fillColor: [
          'step',
          ['get', 'uss'],
          '#EFEDE8',
          0, '#22C55E',  // Vibrant Green
          40, '#FACC15', // Vibrant Yellow
          70, '#EF4444'  // Vibrant Red
        ],
        fillOpacity: 0.5
      });

      // 2. Heatmap Layer - Exponential Weight for better variance
      const heatmapLayer = new window.atlas.layer.HeatMapLayer(pointSource, null, {
        weight: ['pow', ['get', 'uss'], 1.5], // Exponential scaling to show big difference between scores
        radius: 40,
        opacity: 0.8,
        color: [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0, 'rgba(0,0,0,0)',
          0.2, 'rgba(34, 197, 94, 0.2)',  // Greenish glow for low
          0.5, 'rgba(250, 204, 21, 0.5)', // Yellow glow for mid
          0.8, 'rgba(239, 68, 68, 0.8)',  // Red glow for high
          1, 'rgba(153, 27, 27, 1.0)'     // Dark red core for extreme
        ]
      });

      // 3. Line Layer
      const lineLayer = new window.atlas.layer.LineLayer(source, null, {
        strokeColor: '#ffffff',
        strokeWidth: 2
      });

      lineLayerRef.current = lineLayer;

      map.layers.add([polygonLayer, heatmapLayer, lineLayer]);

      // Add click event to polygons
      map.events.add('click', polygonLayer, (e: any) => {
        if (e.shapes && e.shapes.length > 0) {
          const prop = e.shapes[0].getProperties();
          const item = {
            kelurahan_id: prop.id,
            nama: prop.nama,
            uss: prop.uss,
            uss_level: prop.uss_level,
            climate_score: prop.climate_score,
            infrastructure_score: prop.infrastructure_score,
            socioeconomic_score: prop.socioeconomic_score,
            computed_at: prop.computed_at
          };
          onSelect(item as any);
          
          // Also zoom to it locally
          if (prop.centroid) {
            map.setCamera({
              center: prop.centroid,
              zoom: 15,
              type: 'fly',
              duration: 1000
            });
          }
        }
      });

      if (geojson) {
        source.add(geojson);
        const pointFeatures = geojson.features.map((f: any) => ({
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: f.properties.centroid || f.geometry.coordinates[0][0][0]
          },
          properties: f.properties
        }));
        pointSource.add(pointFeatures);

        map.setCamera({
          bounds: window.atlas.data.BoundingBox.fromData(geojson),
          padding: 80,
          type: 'jump'
        });
      }
    });
    };

    initMap();
    
    return () => {
      if (timeoutId) clearTimeout(timeoutId);
      if (mapInstance.current) {
        mapInstance.current.dispose();
        mapInstance.current = null;
      }
      sourceRef.current = null;
      pointSourceRef.current = null;
      lineLayerRef.current = null;
    };
  }, [loading]); // Re-run when loading state changes to detect mapRef container

  // Listen for selection from Card list to Zoom
  useEffect(() => {
    if (mapInstance.current && selectedId && geojson) {
      const selectedFeature = geojson.features.find((f: any) => f.properties.id === selectedId);
      if (selectedFeature && selectedFeature.properties.centroid) {
        mapInstance.current.setCamera({
          center: selectedFeature.properties.centroid,
          zoom: 15,
          type: 'fly',
          duration: 1000
        });
      }
    }
  }, [selectedId, geojson]);

  // Update data when geojson changes
  useEffect(() => {
    if (sourceRef.current && pointSourceRef.current && geojson && mapInstance.current) {
      sourceRef.current.clear();
      sourceRef.current.add(geojson);

      pointSourceRef.current.clear();
      const pointFeatures = geojson.features.map((f: any) => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: f.properties.centroid || f.geometry.coordinates[0][0][0]
        },
        properties: f.properties
      }));
      pointSourceRef.current.add(pointFeatures);

      mapInstance.current.setCamera({
        bounds: window.atlas.data.BoundingBox.fromData(geojson),
        padding: 60
      });
    }
  }, [geojson]);

  // Update styling when selectedId changes
  useEffect(() => {
    if (mapInstance.current && mapInstance.current.layers.getLayers().length > 0) {
      const layers = mapInstance.current.layers.getLayers();
      const polygonLayer = layers.find((l: any) => l instanceof window.atlas.layer.PolygonLayer);
      
      if (polygonLayer) {
        polygonLayer.setOptions({
          fillOpacity: [
            'case',
            ['==', ['get', 'id'], selectedId || ''],
            0.85,
            0.65
          ]
        });
      }
      if (lineLayerRef.current) {
        lineLayerRef.current.setOptions({
          strokeColor: [
            'case',
            ['==', ['get', 'id'], selectedId || ''],
            ['step', ['get', 'uss'], '#E8E4DC', 0, '#75A58A', 40, '#D4A373', 70, '#B93A3A'],
            '#E8E4DC'
          ],
          strokeWidth: [
            'case',
            ['==', ['get', 'id'], selectedId || ''],
            3,
            1
          ]
        });
      }
    }
  }, [selectedId]);

  if (loading) {
    return (
      <div className="skeleton h-[400px] rounded-lg" />
    );
  }

  return (
    <div className="relative bg-surface rounded-lg border border-border overflow-hidden h-[400px] shadow-sm">
      {/* Map Header */}
      <div className="absolute top-3 left-3 z-10 bg-surface/90 backdrop-blur-md rounded-md px-3 py-2 shadow-sm border border-border pointer-events-none">
        <p className="font-display text-xs font-semibold text-text-primary uppercase tracking-wider">
          Peta Kerentanan Urban
        </p>
        <p className="text-xs text-text-tertiary">Kota Bandung</p>
      </div>

      {/* Azure Map Container */}
      <div id="azure-map-container" ref={mapRef} className="absolute inset-0 w-full h-full" />

      {/* Legend */}
      <div className="absolute bottom-3 right-3 bg-surface/90 backdrop-blur-md rounded-md px-3 py-2 shadow-sm border border-border z-10 pointer-events-none">
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-zone-green opacity-60" />
            <span className="text-text-secondary">0–39</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-zone-yellow opacity-60" />
            <span className="text-text-secondary">40–69</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-zone-red opacity-70" />
            <span className="text-text-secondary">70–100</span>
          </span>
        </div>
      </div>
    </div>
  );
}
