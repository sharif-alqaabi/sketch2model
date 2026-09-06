import './ResultPanel.css'

const ResultPanel = ({ result, costEstimation, error, isGenerating, isEstimating, inputMode = 'drawing' }) => {
  const parseDesignDescription = (description) => {
    try {
      // Try to parse as JSON first
      const parsed = JSON.parse(description)
      return parsed
    } catch {
      // If not JSON, return as plain text
      return { text: description }
    }
  }

  const flattenMaterials = (materials) => {
    const flattened = []
    if (typeof materials === 'object' && materials !== null) {
      Object.entries(materials).forEach(([category, items]) => {
        if (Array.isArray(items)) {
          // Handle array format: [{material: "...", quantity: "...", cost: "..."}]
          items.forEach(item => {
            flattened.push({
              category,
              material: item.material,
              quantity: item.quantity,
              cost: item.cost || 'N/A'
            })
          })
        } else if (typeof items === 'object') {
          // Handle object format: {material: quantity}
          Object.entries(items).forEach(([material, quantity]) => {
            flattened.push({
              category,
              material,
              quantity: String(quantity),
              cost: 'N/A'
            })
          })
        }
      })
    }
    return flattened
  }

  const renderContent = () => {
    if (isGenerating) {
      return (
        <div className="result-loading">
          <div className="loading-spinner"></div>
          <h3>{inputMode === 'voice' ? 'Processing your voice description...' : 'Analyzing your drawing...'}</h3>
          <p>Our AI is creating a detailed 3D design description</p>
        </div>
      )
    }

    if (error) {
      return (
        <div className="result-error">
          <div className="error-icon">⚠️</div>
          <h3>Oops! Something went wrong</h3>
          <p>{error}</p>
          <div className="error-hint">
            <strong>Tip:</strong> Make sure the backend server is running and your API key is configured.
          </div>
        </div>
      )
    }

    if (!result) {
      return (
        <div className="result-empty">
          <div className="empty-icon">{inputMode === 'voice' ? '🎤' : '🎨'}</div>
          <h3>Ready to create!</h3>
          <p>
            {inputMode === 'voice' 
              ? 'Record your voice description and click "Generate Design" to see the AI magic happen.'
              : 'Draw your house design on the canvas and click "Generate 3D Design" to see the AI magic happen.'
            }
          </p>
          <div className="tips">
            <h4>Tips for better results:</h4>
            {inputMode === 'voice' ? (
              <ul>
                <li>Describe the architectural style (modern, traditional, etc.)</li>
                <li>Mention the number of floors and rooms</li>
                <li>Include special features (garage, balcony, pool, etc.)</li>
                <li>Specify colors and materials if desired</li>
              </ul>
            ) : (
              <ul>
                <li>Draw clear outlines of walls and structure</li>
                <li>Include windows, doors, and roof details</li>
                <li>Add perspective if possible</li>
                <li>Use different colors for different elements</li>
              </ul>
            )}
          </div>
        </div>
      )
    }

    const designData = parseDesignDescription(result.design_description)

    return (
      <div className="result-wrapper">
        {/* Transcribed Text Section - Only for voice input */}
        {result.transcribed_text && (
          <div className="transcribed-section">
            <div className="section-header">
              <h3>🎤 Your Voice Input</h3>
            </div>
            <div className="transcribed-text">
              <p>{result.transcribed_text}</p>
            </div>
          </div>
        )}

        {/* SECTION 1: Generated Image - Always visible when result exists */}
        {result.generated_image_url && (
          <div className="image-section">
            <div className="section-header">
              <h3>🏠 Generated 3D Rendering</h3>
            </div>
            <div className="image-container">
              <img 
                src={result.generated_image_url} 
                alt="Generated 3D House Design" 
                className="generated-image"
                onError={(e) => {
                  e.target.style.display = 'none'
                  console.error('Failed to load generated image')
                }}
              />
            </div>
          </div>
        )}

        {/* SECTION 2: Materials Table - Shows below image when estimating or estimation complete */}
        {(isEstimating || costEstimation) && (
          <div className="materials-section">
            {isEstimating ? (
              <div className="result-loading">
                <div className="loading-spinner"></div>
                <h3>Analyzing materials...</h3>
                <p>Calculating quantities of bricks, cement, paint, and other materials</p>
              </div>
            ) : costEstimation ? (
              <>
                <div className="section-header">
                  <h3>📦 Raw Materials & Cost Breakdown</h3>
                </div>

                {/* Total Cost Card - Prominent Display */}
                {costEstimation.cost_estimation_json?.total_cost && (
                  <div className="total-cost-card">
                    <span className="cost-label">💰 Total Estimated Cost</span>
                    <span className="cost-value">{costEstimation.cost_estimation_json.total_cost}</span>
                    {costEstimation.cost_estimation_json?.material_cost && costEstimation.cost_estimation_json?.labor_cost && (
                      <div className="cost-breakdown">
                        <span className="breakdown-item">Materials: {costEstimation.cost_estimation_json.material_cost}</span>
                        <span className="breakdown-item">Labor: {costEstimation.cost_estimation_json.labor_cost}</span>
                      </div>
                    )}
                  </div>
                )}

                {costEstimation.cost_estimation_json?.total_area && (
                  <div className="area-card">
                    <span className="area-label">Total Construction Area</span>
                    <span className="area-value">
                      {typeof costEstimation.cost_estimation_json.total_area === 'object' && !Array.isArray(costEstimation.cost_estimation_json.total_area)
                        ? Object.entries(costEstimation.cost_estimation_json.total_area)
                            .map(([key, value]) => `${key.replace(/_/g, ' ')}: ${value}`)
                            .join(', ')
                        : String(costEstimation.cost_estimation_json.total_area)
                      }
                    </span>
                  </div>
                )}

                {costEstimation.cost_estimation_json?.materials ? (
                  <div className="table-wrapper">
                    <table className="materials-table">
                      <thead>
                        <tr>
                          <th>Category</th>
                          <th>Material</th>
                          <th>Quantity</th>
                          <th>Estimated Cost</th>
                        </tr>
                      </thead>
                      <tbody>
                        {flattenMaterials(costEstimation.cost_estimation_json.materials).map((item, idx) => (
                          <tr key={idx} className={idx % 2 === 0 ? 'even' : 'odd'}>
                            <td className="category-cell">{item.category}</td>
                            <td className="material-cell">{item.material}</td>
                            <td className="quantity-cell">{item.quantity}</td>
                            <td className="cost-cell">{item.cost}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="cost-text">
                    <pre>{costEstimation.cost_estimation}</pre>
                  </div>
                )}

                {costEstimation.cost_estimation_json?.notes && (
                  <div className="notes-section">
                    <h4>📝 Notes & Assumptions</h4>
                    <p>{costEstimation.cost_estimation_json.notes}</p>
                  </div>
                )}
              </>
            ) : null}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="result-panel">
      {renderContent()}
    </div>
  )
}

export default ResultPanel
