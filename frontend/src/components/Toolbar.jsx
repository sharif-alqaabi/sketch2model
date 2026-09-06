import './Toolbar.css'

const Toolbar = ({ tool, setTool, color, setColor, brushSize, setBrushSize, onClear, onDownload }) => {
  const colors = [
    '#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF',
    '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#800080'
  ]

  const brushSizes = [2, 5, 10, 15, 20]

  return (
    <div className="toolbar">
      <div className="toolbar-section">
        <label className="toolbar-label">Tool</label>
        <div className="tool-buttons">
          <button
            className={`tool-button ${tool === 'brush' ? 'active' : ''}`}
            onClick={() => setTool('brush')}
            title="Brush"
          >
            ✏️ Brush
          </button>
          <button
            className={`tool-button ${tool === 'eraser' ? 'active' : ''}`}
            onClick={() => setTool('eraser')}
            title="Eraser"
          >
            🧹 Eraser
          </button>
        </div>
      </div>

      <div className="toolbar-section">
        <label className="toolbar-label">Color</label>
        <div className="color-picker">
          {colors.map((c) => (
            <button
              key={c}
              className={`color-button ${color === c ? 'active' : ''}`}
              style={{ backgroundColor: c }}
              onClick={() => setColor(c)}
              title={c}
            />
          ))}
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="color-input"
            title="Custom color"
          />
        </div>
      </div>

      <div className="toolbar-section">
        <label className="toolbar-label">Brush Size: {brushSize}px</label>
        <div className="brush-size-buttons">
          {brushSizes.map((size) => (
            <button
              key={size}
              className={`size-button ${brushSize === size ? 'active' : ''}`}
              onClick={() => setBrushSize(size)}
              title={`${size}px`}
            >
              <div
                className="size-indicator"
                style={{
                  width: `${Math.min(size * 1.5, 20)}px`,
                  height: `${Math.min(size * 1.5, 20)}px`
                }}
              />
            </button>
          ))}
        </div>
        <input
          type="range"
          min="1"
          max="50"
          value={brushSize}
          onChange={(e) => setBrushSize(Number(e.target.value))}
          className="brush-slider"
        />
      </div>

      <div className="toolbar-section">
        <label className="toolbar-label">Actions</label>
        <div className="action-buttons-toolbar">
          <button className="action-button clear" onClick={onClear} title="Clear canvas">
            🗑️ Clear
          </button>
          <button className="action-button download" onClick={onDownload} title="Download drawing">
            💾 Download
          </button>
        </div>
      </div>
    </div>
  )
}

export default Toolbar
