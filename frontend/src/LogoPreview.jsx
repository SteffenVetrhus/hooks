/**
 * Preview panel that displays the generated logo.
 *
 * Shows loading state, error messages, or the resulting image with a download
 * link.
 *
 * @param {object}      props
 * @param {string|null} props.url     - Object URL of the generated logo blob.
 * @param {string|null} props.error   - Error message, if any.
 * @param {boolean}     props.loading - Whether a request is in flight.
 * @param {object|null} props.meta    - Logo metadata { name, format, mimeType }.
 */
export default function LogoPreview({ url, error, loading, meta }) {
  /**
   * Derive a filesystem-safe filename from the brand name and format.
   *
   * @returns {string} The download filename.
   */
  function downloadName() {
    if (!meta) return "logo";
    const safe = meta.name.replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 50);
    return `logo-${safe}.${meta.format}`;
  }

  return (
    <div style={styles.panel}>
      {loading && <p style={styles.info}>Generating…</p>}
      {error && <p style={styles.error}>{error}</p>}

      {!loading && !error && !url && (
        <p style={styles.placeholder}>Your logo will appear here</p>
      )}

      {url && !loading && (
        <div style={styles.result}>
          <img src={url} alt="Generated logo" style={styles.img} />
          <a href={url} download={downloadName()} style={styles.download}>
            Download {meta?.format?.toUpperCase()}
          </a>
        </div>
      )}
    </div>
  );
}

const styles = {
  panel: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#1e293b",
    borderRadius: 12,
    padding: "2rem",
    minWidth: 300,
    minHeight: 340,
    flex: "1 1 340px",
    maxWidth: 480,
  },
  placeholder: {
    color: "#475569",
    fontSize: "1rem",
  },
  info: {
    color: "#94a3b8",
  },
  error: {
    color: "#f87171",
    wordBreak: "break-word",
  },
  result: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "1.25rem",
  },
  img: {
    maxWidth: "100%",
    maxHeight: 400,
    borderRadius: 8,
  },
  download: {
    padding: "0.5rem 1.25rem",
    borderRadius: 8,
    background: "#334155",
    color: "#e2e8f0",
    textDecoration: "none",
    fontWeight: 500,
    fontSize: "0.9rem",
  },
};
