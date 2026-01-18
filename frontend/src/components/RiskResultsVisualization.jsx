import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FiAlertCircle, FiCheckCircle, FiTrendingUp } from 'react-icons/fi';

function RiskResultsVisualization({ riskData }) {
  const getRiskColor = (level) => {
    const colors = {
      low: '#10b981',
      medium: '#f59e0b',
      high: '#ef4444',
      critical: '#7c3aed',
    };
    return colors[level] || '#gray-500';
  };

  const getRiskIcon = (level) => {
    if (level === 'critical' || level === 'high') {
      return <FiAlertCircle className="w-8 h-8" />;
    }
    return <FiCheckCircle className="w-8 h-8" />;
  };

  const pieData = [
    { name: 'Risk Score', value: riskData.risk_score },
    { name: 'Safety', value: 100 - riskData.risk_score },
  ];

  return (
    <div className="space-y-8">
      {/* Risk Level Card */}
      <div
        className="bg-white rounded-lg shadow-lg p-8 border-l-4"
        style={{ borderColor: getRiskColor(riskData.risk_level) }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-2">
              Risk Level: {riskData.risk_level.toUpperCase()}
            </h2>
            <p className="text-gray-600">
              Confidence Score: {(riskData.confidence_score * 100).toFixed(1)}%
            </p>
          </div>
          <div style={{ color: getRiskColor(riskData.risk_level) }} className="text-4xl">
            {getRiskIcon(riskData.risk_level)}
          </div>
        </div>
      </div>

      {/* Risk Score Visualization */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h3 className="text-2xl font-semibold text-gray-800 mb-6">Risk Score Analysis</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={pieData} cx="50%" cy="50%" innerRadius={80} outerRadius={120} dataKey="value">
              <Cell fill={getRiskColor(riskData.risk_level)} />
              <Cell fill="#e0e7ff" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <p className="text-center text-2xl font-bold mt-4">
          {riskData.risk_score.toFixed(1)} / 100
        </p>
      </div>

      {/* Contributing Factors */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h3 className="text-2xl font-semibold text-gray-800 mb-6">Contributing Factors</h3>
        <div className="space-y-3">
          {riskData.contributing_factors && riskData.contributing_factors.length > 0 ? (
            riskData.contributing_factors.map((factor, idx) => (
              <div key={idx} className="flex items-center p-3 bg-red-50 rounded-lg">
                <FiTrendingUp className="w-5 h-5 text-red-600 mr-3" />
                <span className="text-gray-700">{factor}</span>
              </div>
            ))
          ) : (
            <p className="text-gray-600">No significant contributing factors identified.</p>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h3 className="text-2xl font-semibold text-gray-800 mb-6">Personalized Recommendations</h3>
        <div className="space-y-3">
          {riskData.recommendations && riskData.recommendations.length > 0 ? (
            riskData.recommendations.map((rec, idx) => (
              <div key={idx} className="flex items-start p-4 bg-blue-50 rounded-lg">
                <input
                  type="checkbox"
                  className="mr-3 mt-1"
                />
                <span className="text-gray-700">{rec}</span>
              </div>
            ))
          ) : (
            <p className="text-gray-600">No recommendations at this time.</p>
          )}
        </div>
      </div>

      {/* Model Info */}
      <div className="bg-gray-50 rounded-lg p-6 text-center text-gray-600">
        <p>Assessment generated using: {riskData.ml_model_used || 'Advanced AI Model'}</p>
      </div>
    </div>
  );
}

export default RiskResultsVisualization;
