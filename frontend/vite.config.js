import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig (({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "VITE_");

  const HOST = env.VITE_HOST || "127.0.0.1";
  const PORT = Number(env.VITE_PORT || 5173);

  return {
    plugins: [react()],
    server: {
      host: HOST,
      port: PORT,
    },
  };
})
