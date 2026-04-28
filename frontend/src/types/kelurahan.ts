export interface GeoJSONGeometry {
  type: string;
  coordinates: number[] | number[][] | number[][][] | number[][][][];
}

export interface KelurahanFeature {
  type: 'Feature';
  properties: {
    id: string;
    nama: string;
    kecamatan: string;
    kota: string;
    populasi: number | null;
    luas_km2: number | null;
    centroid?: [number, number] | null;
    uss: number | null;
    uss_level: string | null;
    climate_score: number | null;
    infrastructure_score: number | null;
    socioeconomic_score: number | null;
    computed_at: string | null;
  };
  geometry: GeoJSONGeometry;
}

export interface KelurahanGeoJSON {
  type: 'FeatureCollection';
  features: KelurahanFeature[];
}
