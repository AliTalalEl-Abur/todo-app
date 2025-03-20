
// Importa el módulo 'path' para resolver rutas
const path = require('path');
 
const nextConfig = {
  reactStrictMode: true,
 
  // Extiende la configuración de Webpack
  webpack: (config) => {
    // Configura un alias '@' que apunta a la raíz del directorio del proyecto
    config.resolve.alias['@'] = path.resolve(__dirname);
    return config;
  },
}






