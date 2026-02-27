import { useState } from "react";
import LogoForm from "./LogoForm";
import LogoPreview from "./LogoPreview";

/**
 * Root application component.
 *
 * Holds the generated logo blob URL in state and passes callbacks / data down
 * to the form and preview components.
 */
export default function App() {
  const [logoUrl, setLogoUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [logoMeta, setLogoMeta] = useState(null);

  /**
   * Request a logo from the backend API.
   *
   * Converts the response blob into an object URL that can be rendered in an
   * <img> tag or used as a download href.
   *
   * @param {object} params - { name, color, format, size }
   */
  async function handleGenerate(params) {
    setLoading(true);
    setError(null);

    // Release the previous object URL to avoid memory leaks
    if (logoUrl) {
      URL.revokeObjectURL(logoUrl);
      setLogoUrl(null);
    }

    try {
      // The API base URL is injected at build time; falls back to current
      // origin so it works behind a reverse proxy as well.
      const base = import.meta.env.VITE_API_URL || "";
      const res = await fetch(`${base}/api/logos/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail || `Server error ${res.status}`);
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setLogoUrl(url);
      setLogoMeta({ ...params, mimeType: blob.type });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.wrapper}>
      <header style={styles.header}>
        <h1 style={styles.title}>Logo Generator</h1>
        <p style={styles.subtitle}>
          Enter a brand name and pick a colour to generate a unique logo
        </p>
      </header>

      <main style={styles.main}>
        <LogoForm onGenerate={handleGenerate} loading={loading} />
        <LogoPreview url={logoUrl} error={error} loading={loading} meta={logoMeta} />
      </main>
    </div>
  );
}

const styles = {
  wrapper: {
    maxWidth: 960,
    margin: "0 auto",
    padding: "2rem 1.5rem",
    flex: 1,
  },
  header: {
    textAlign: "center",
    marginBottom: "2.5rem",
  },
  title: {
    fontSize: "2rem",
    fontWeight: 700,
    color: "#f8fafc",
  },
  subtitle: {
    marginTop: "0.5rem",
    color: "#94a3b8",
    fontSize: "1rem",
  },
  main: {
    display: "flex",
    gap: "2rem",
    flexWrap: "wrap",
    justifyContent: "center",
  },
};
