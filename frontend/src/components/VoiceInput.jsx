import { useState, useRef } from 'react'
import './VoiceInput.css'

function VoiceInput({ onVoiceGenerate, isGenerating }) {
  const [isRecording, setIsRecording] = useState(false)
  const [audioBlob, setAudioBlob] = useState(null)
  const [recordingTime, setRecordingTime] = useState(0)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const timerRef = useRef(null)

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        setAudioBlob(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setRecordingTime(0)

      // start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
    } catch (err) {
      console.error('Error accessing microphone:', err)
      alert('Could not access microphone. Please check permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }

  const handleGenerate = () => {
    if (audioBlob) {
      onVoiceGenerate(audioBlob)
    }
  }

  const handleClear = () => {
    setAudioBlob(null)
    setRecordingTime(0)
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="voice-input-container">
      <div className="voice-input-card">
        <div className="voice-header">
          <h3>🎤 Voice Input</h3>
          <p>Describe your dream house design</p>
        </div>

        <div className="recording-area">
          {!audioBlob ? (
            <>
              {!isRecording ? (
                <button
                  className="record-button"
                  onClick={startRecording}
                  disabled={isGenerating}
                >
                  <span className="mic-icon">🎙️</span>
                  <span>Start Recording</span>
                </button>
              ) : (
                <div className="recording-active">
                  <div className="recording-indicator">
                    <span className="pulse"></span>
                    <span className="recording-text">Recording...</span>
                  </div>
                  <div className="recording-timer">{formatTime(recordingTime)}</div>
                  <button
                    className="stop-button"
                    onClick={stopRecording}
                  >
                    ⏹️ Stop Recording
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="audio-preview">
              <div className="audio-info">
                <span className="check-icon">✅</span>
                <span>Recording complete ({formatTime(recordingTime)})</span>
              </div>
              <audio controls src={URL.createObjectURL(audioBlob)} />
              <div className="audio-actions">
                <button
                  className="clear-button"
                  onClick={handleClear}
                  disabled={isGenerating}
                >
                  🗑️ Clear
                </button>
                <button
                  className="generate-voice-button"
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
                      ✨ Generate Design
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="voice-tips">
          <p><strong>Tips:</strong></p>
          <ul>
            <li>Describe the style (modern, traditional, etc.)</li>
            <li>Mention number of floors and rooms</li>
            <li>Include special features (garage, balcony, etc.)</li>
            <li>Specify colors and materials if desired</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default VoiceInput
