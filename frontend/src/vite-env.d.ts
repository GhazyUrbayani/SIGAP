/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_AZURE_MAPS_KEY: string;
  readonly VITE_API_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
