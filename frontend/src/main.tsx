import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import ThemeRegistry from "./components/ThemeRegistry";
import App from "./App.tsx";

import "./styles/globals.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeRegistry>
      <App />
    </ThemeRegistry>
  </StrictMode>,
);
