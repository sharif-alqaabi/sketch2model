import { useRef, useEffect, useState, forwardRef, useImperativeHandle } from 'react'
import './DrawingCanvas.css'

const DrawingCanvas = forwardRef(({ tool, color, brushSize }, ref) => {
  const canvasRef = useRef(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [context, setContext] = useState(null)
  const [lastPos, setLastPos] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d', { willReadFrequently: true })
    
    // Set canvas size
    const resizeCanvas = () => {
      const container = canvas.parentElement
      const rect = container.getBoundingClientRect()
      canvas.width = rect.width
      canvas.height = rect.height
      
      // Fill with white background
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
    }

    resizeCanvas()
    setContext(ctx)

    window.addEventListener('resize', resizeCanvas)
    return () => window.removeEventListener('resize', resizeCanvas)
  }, [])

  useEffect(() => {
    if (!context) return

    context.lineCap = 'round'
    context.lineJoin = 'round'
    context.lineWidth = brushSize

    if (tool === 'eraser') {
      context.globalCompositeOperation = 'destination-out'
    } else {
      context.globalCompositeOperation = 'source-over'
      context.strokeStyle = color
    }
  }, [context, tool, color, brushSize])

  const getMousePos = (e) => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const scaleX = canvas.width / rect.width
    const scaleY = canvas.height / rect.height

    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    }
  }

  const getTouchPos = (e) => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const scaleX = canvas.width / rect.width
    const scaleY = canvas.height / rect.height
    const touch = e.touches[0]

    return {
      x: (touch.clientX - rect.left) * scaleX,
      y: (touch.clientY - rect.top) * scaleY
    }
  }

  const startDrawing = (e) => {
    e.preventDefault()
    setIsDrawing(true)
    const pos = e.type.includes('mouse') ? getMousePos(e) : getTouchPos(e)
    setLastPos(pos)
    
    if (context) {
      context.beginPath()
      context.moveTo(pos.x, pos.y)
    }
  }

  const draw = (e) => {
    if (!isDrawing || !context) return
    e.preventDefault()

    const pos = e.type.includes('mouse') ? getMousePos(e) : getTouchPos(e)

    context.lineTo(pos.x, pos.y)
    context.stroke()

    setLastPos(pos)
  }

  const stopDrawing = (e) => {
    if (!isDrawing) return
    e.preventDefault()
    setIsDrawing(false)
    
    if (context) {
      context.closePath()
    }
  }

  const clearCanvas = () => {
    if (!context || !canvasRef.current) return
    const canvas = canvasRef.current
    context.fillStyle = '#ffffff'
    context.fillRect(0, 0, canvas.width, canvas.height)
  }

  const getCanvas = () => canvasRef.current

  // Expose methods to parent component
  useImperativeHandle(ref, () => ({
    clearCanvas,
    getCanvas
  }))

  return (
    <div className="canvas-container">
      <canvas
        ref={canvasRef}
        className="drawing-canvas"
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        onTouchStart={startDrawing}
        onTouchMove={draw}
        onTouchEnd={stopDrawing}
      />
    </div>
  )
})

DrawingCanvas.displayName = 'DrawingCanvas'

export default DrawingCanvas
