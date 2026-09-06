import { useState, useRef, useEffect } from 'react'
import DrawingCanvas from './components/DrawingCanvas'
import Toolbar from './components/Toolbar'
import ResultPanel from './components/ResultPanel'
import VoiceInput from './components/VoiceInput'
import './App.css'

// API URL from environment variable or default to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [inputMode, setInputMode] = useState('drawing') // 'drawing' or 'voice'
  const [tool, setTool] = useState('brush')
  const [color, setColor] = useState('#000000')
  const [brushSize, setBrushSize] = useState(5)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isEstimating, setIsEstimating] = useState(false)
  const [result, setResult] = useState(null)
  const [costEstimation, setCostEstimation] = useState(null)
  const [error, setError] = useState(null)
  const canvasRef = useRef(null)

  const handleGenerate = async () => {
    if (!canvasRef.current) return

    setIsGenerating(true)
    setError(null)
    // Don't clear result - keep previous image visible
    setCostEstimation(null) // Clear only cost estimation for new design

    try {
      // Get canvas as blob
      const canvas = canvasRef.current.getCanvas()
      const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'))
      
      // Create form data
      const formData = new FormData()
      formData.append('file', blob, 'drawing.png')

      // Send to backend
      const response = await fetch(`${API_URL}/api/generate-3d-design`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate design')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'An error occurred while generating the design')
      console.error('Error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleEstimateCost = async () => {
    if (!result || !result.generated_image_url) {
      setError('Please generate a 3D design first')
      return
    }

    setIsEstimating(true)
    setError(null)

    try {
      // fetch the generated image and convert to blob
      const imageResponse = await fetch(result.generated_image_url)
      const blob = await imageResponse.blob()
      
      // create form data with the generated image
      const formData = new FormData()
      formData.append('file', blob, 'generated-design.png')

      // send to backend
      const response = await fetch(`${API_URL}/api/estimate-cost`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to estimate cost')
      }

      const data = await response.json()
      setCostEstimation(data)
    } catch (err) {
      setError(err.message || 'An error occurred while estimating cost')
      console.error('Error:', err)
    } finally {
      setIsEstimating(false)
    }
  }

  const handleVoiceGenerate = async (audioBlob) => {
    setIsGenerating(true)
    setError(null)
    setCostEstimation(null)

    try {
      // Create form data with audio file
      const formData = new FormData()
      formData.append('file', audioBlob, 'recording.webm')

      // Send to backend
      const response = await fetch(`${API_URL}/api/voice-to-design`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate design from voice')
      }

      const data = await response.json()
      console.log('Voice response:', data)
      setResult(data)
    } catch (err) {
      setError(err.message || 'An error occurred while processing voice input')
      console.error('Error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleClear = () => {
    if (canvasRef.current) {
      canvasRef.current.clearCanvas()
    }
    setResult(null)
    setCostEstimation(null)
    setError(null)
  }

  const handleDownload = () => {
    if (!canvasRef.current) return
    const canvas = canvasRef.current.getCanvas()
    const link = document.createElement('a')
    link.download = 'house-drawing.png'
    link.href = canvas.toDataURL()
    link.click()
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏠 Drawing to 3D House Design</h1>
        <p>Draw your house sketch or describe it with your voice</p>
        
        <div className="input-mode-toggle">
          <button
            className={`mode-button ${inputMode === 'drawing' ? 'active' : ''}`}
            onClick={() => setInputMode('drawing')}
          >
            ✏️ Drawing
          </button>
          <button
            className={`mode-button ${inputMode === 'voice' ? 'active' : ''}`}
            onClick={() => setInputMode('voice')}
          >
            🎤 Voice
          </button>
        </div>
      </header>

      <div className="app-container">
        <div className="canvas-section">
          {inputMode === 'drawing' ? (
            <>
              <Toolbar
                tool={tool}
                setTool={setTool}
                color={color}
                setColor={setColor}
                brushSize={brushSize}
                setBrushSize={setBrushSize}
                onClear={handleClear}
                onDownload={handleDownload}
              />
              
              <DrawingCanvas
                ref={canvasRef}
                tool={tool}
                color={color}
                brushSize={brushSize}
              />

              <div className="action-buttons">
                <button
                  className="generate-button"
                  onClick={handleGenerate}
                  disabled={isGenerating}
                >
                  {isGenerating ? (
                    <>
                      <span className="spinner"></span>
                      Generating...
                    </>
                  ) : (
                    <>
                      ✨ Generate 3D Design
                    </>
                  )}
                </button>
                
                {result && (
                  <button
                    className="estimate-button"
                    onClick={handleEstimateCost}
                    disabled={isEstimating}
                  >
                    {isEstimating ? (
                      <>
                        <span className="spinner"></span>
                        Estimating...
                      </>
                    ) : (
                      <>
                        💰 Estimate Materials & Cost
                      </>
                    )}
                  </button>
                )}
              </div>
            </>
          ) : (
            <VoiceInput
              onVoiceGenerate={handleVoiceGenerate}
              isGenerating={isGenerating}
            />
          )}
        </div>

        <ResultPanel
          result={result}
          costEstimation={costEstimation}
          error={error}
          isGenerating={isGenerating}
          isEstimating={isEstimating}
          inputMode={inputMode}
        />
      </div>
      
      {result && inputMode === 'voice' && (
        <div className="voice-estimate-section">
          <button
            className="estimate-button-voice"
            onClick={handleEstimateCost}
            disabled={isEstimating}
          >
            {isEstimating ? (
              <>
                <span className="spinner"></span>
                Estimating...
              </>
            ) : (
              <>
                💰 Estimate Materials & Cost
              </>
            )}
          </button>
        </div>
      )}
    </div>
  )
}

export default App
