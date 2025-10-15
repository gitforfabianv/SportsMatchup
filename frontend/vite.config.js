// vite.config.js

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// ⚠️ IMPORTANT: Replace 'YOUR_REPO_NAME' with the actual name of your GitHub repository.
// For example, if your repo URL is github.com/username/SportsMatchup, use '/SportsMatchup/'
const BASE_PATH = "/SportsMatchup/"; 

export default defineConfig({
    // 👇 ADD THE 'base' OPTION HERE FOR GITHUB PAGES DEPLOYMENT
    base: BASE_PATH, 

    plugins: [tailwindcss(), react()],
    server: {
        port: 3000, 
        host: true, 
        proxy: {
            "/api": {
                target: "http://localhost:5000",
                changeOrigin: true,
                secure: false,
            },
        },
    },
});