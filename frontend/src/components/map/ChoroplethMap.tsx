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

  useEffect(() => {
    // Only initialize map if container is ready and atlas SDK is loaded
    if (!mapRef.current || !window.atlas || mapInstance.current) return;

    // Initialize Azure Map
    const map = new window.atlas.Map(mapRef.current, {
      center: [107.6191, -6.9175], // Bandung center
      zoom: 11,
      style: 'grayscale_light', // Clean style to make choropleth stand out
      authOptions: {
        authType: 'subscriptionKey',
        subscriptionKey: import.meta.env.VITE_AZURE_MAPS_KEY || '',
      },
    });

    mapInstance.current = map;

    map.events.add('ready', () => {
      // Add data source
      const source = new window.atlas.source.DataSource();
      map.sources.add(source);
      sourceRef.current = source;

      // Add polygon layer for choropleth/heatmap
      const polygonLayer = new window.atlas.layer.PolygonLayer(source, null, {
        fillColor: [
          'step',
          ['get', 'uss'],
          '#EFEDE8', // default/null
          0, '#75A58A', // zone-green (0-39)
          40, '#D4A373', // zone-yellow (40-69)
          70, '#B93A3A'  // zone-red (70-100)
        ],
        fillOpacity: [
          'case',
          ['==', ['get', 'id'], selectedId || ''],
          0.85,
          0.65
        ]
      });

      // Add line layer for boundaries
      const lineLayer = new window.atlas.layer.LineLayer(source, null, {
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

      map.layers.add([polygonLayer, lineLayer]);

      // Add click event to polygons
      map.events.add('click', polygonLayer, (e: any) => {
        if (e.shapes && e.shapes.length > 0) {
          const prop = e.shapes[0].getProperties();
          const item: USSLatestItem = {
            kelurahan_id: prop.id,
            nama: prop.nama,
            uss: prop.uss,
            uss_level: prop.uss_level,
            climate_score: prop.climate_score,
            infrastructure_score: prop.infrastructure_score,
            socioeconomic_score: prop.socioeconomic_score,
            computed_at: prop.computed_at
          };
          onSelect(item);
        }
      });
      
      // Load data if already available
      if (geojson) {
        source.add(geojson);
        // Automatically adjust map view to bounds of data
        map.setCamera({
          bounds: window.atlas.data.BoundingBox.fromData(geojson),
          padding: 30
        });
      }
    });

    return () => {
      map.dispose();
      mapInstance.current = null;
      sourceRef.current = null;
    };
  }, []); // Run once on mount

  // Update data when geojson changes
  useEffect(() => {
    if (sourceRef.current && geojson && mapInstance.current) {
      sourceRef.current.clear();
      sourceRef.current.add(geojson);
      mapInstance.current.setCamera({
        bounds: window.atlas.data.BoundingBox.fromData(geojson),
        padding: 30
      });
    }
  }, [geojson]);

  // Update styling when selectedId changes
  useEffect(() => {
    if (mapInstance.current && mapInstance.current.layers.getLayers().length > 0) {
      const layers = mapInstance.current.layers.getLayers();
      const polygonLayer = layers.find((l: any) => l instanceof window.atlas.layer.PolygonLayer);
      const lineLayer = layers.find((l: any) => l instanceof window.atlas.layer.LineLayer);
      
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
      if (lineLayer) {
        lineLayer.setOptions({
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
      <div ref={mapRef} className="w-full h-full" />

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
