import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { AppRouterCacheProvider } from "@mui/material-nextjs/v15-appRouter";

import ThemeRegistry from "./components/ThemeRegistry";
import App from "./App.tsx";

import "./styles/globals.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppRouterCacheProvider>
      <ThemeRegistry>
        <App />
      </ThemeRegistry>
    </AppRouterCacheProvider>
  </StrictMode>,
);
