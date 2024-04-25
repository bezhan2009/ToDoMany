import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@components": "/src/components",
      "@assets": "/src/assets",
      "@pages": "/src/pages",
      "@redux": "/src/redux",
      "@styles": "/src/styles",
      "@UI": "/src/components/UI",
    }
  },
})
