function PredictionCard({prediction,confidence}) {
  return (
    <div className="prediction-card">

      <h2>Prediction</h2>

      <p>{prediction}</p>

      <p>Confidence: {confidence}%</p>

     
    </div>
  );
}

export default PredictionCard;