import { useState } from "react";

/**
 * Form component for collecting logo generation parameters.
 *
 * Renders input fields for brand name, colour, output format, and canvas size,
 * then calls the parent `onGenerate` callback with the collected values.
 *
 * @param {object}   props
 * @param {function} props.onGenerate - Callback invoked with { name, color, format, size }.
 * @param {boolean}  props.loading    - Whether a request is currently in flight.
 */
export default function LogoForm({ onGenerate, loading }) {
  const [name, setName] = useState("");
  const [color, setColor] = useState("#3B82F6");
  const [format, setFormat] = useState("svg");
  const [size, setSize] = useState(400);

  /**
   * Handle form submission.
   *
   * Prevents the default browser submit, validates that a name is provided,
   * and delegates to the parent callback.
   *
   * @param {Event} e - The submit event.
   */
  function handleSubmit(e) {
    e.preventDefault();
    if (!name.trim()) return;
    onGenerate({ name: name.trim(), color, format, size });
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      {/* Brand name */}
      <label style={styles.label}>
        Brand name
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Acme Corp"
          maxLength={50}
          required
          style={styles.input}
        />
      </label>

      {/* Colour picker */}
      <label style={styles.label}>
        Primary colour
        <div style={styles.colorRow}>
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            style={styles.colorPicker}
          />
          <input
            type="text"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            pattern="#[0-9a-fA-F]{6}"
            style={{ ...styles.input, flex: 1 }}
          />
        </div>
      </label>

      {/* Format */}
      <label style={styles.label}>
        Format
        <select
          value={format}
          onChange={(e) => setFormat(e.target.value)}
          style={styles.input}
        >
          <option value="svg">SVG</option>
          <option value="png">PNG</option>
        </select>
      </label>

      {/* Size */}
      <label style={styles.label}>
        Size ({size}px)
        <input
          type="range"
          min={200}
          max={1024}
          step={8}
          value={size}
          onChange={(e) => setSize(Number(e.target.value))}
          style={styles.range}
        />
      </label>

      <button type="submit" disabled={loading || !name.trim()} style={styles.button}>
        {loading ? "Generating…" : "Generate Logo"}
      </button>
    </form>
  );
}

const styles = {
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1.25rem",
    background: "#1e293b",
    padding: "2rem",
    borderRadius: 12,
    minWidth: 300,
    flex: "1 1 340px",
    maxWidth: 420,
  },
  label: {
    display: "flex",
    flexDirection: "column",
    gap: "0.35rem",
    fontSize: "0.875rem",
    fontWeight: 500,
    color: "#cbd5e1",
  },
  input: {
    padding: "0.6rem 0.75rem",
    borderRadius: 8,
    border: "1px solid #334155",
    background: "#0f172a",
    color: "#e2e8f0",
    fontSize: "0.95rem",
    outline: "none",
  },
  colorRow: {
    display: "flex",
    gap: "0.5rem",
    alignItems: "center",
  },
  colorPicker: {
    width: 42,
    height: 42,
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    background: "none",
  },
  range: {
    width: "100%",
    accentColor: "#3b82f6",
  },
  button: {
    marginTop: "0.5rem",
    padding: "0.75rem",
    border: "none",
    borderRadius: 8,
    background: "#3b82f6",
    color: "#fff",
    fontSize: "1rem",
    fontWeight: 600,
    cursor: "pointer",
  },
};
