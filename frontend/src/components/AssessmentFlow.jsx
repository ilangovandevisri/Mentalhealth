import React, { useState } from 'react';
import { assessmentService, resultsService } from '../services/apiService';
import QuestionnaireForm from './QuestionnaireForm';
import RiskResultsVisualization from './RiskResultsVisualization';

function AssessmentFlow() {
  const [currentStep, setCurrentStep] = useState('questionnaire-selection');
  const [selectedQuestionnaire, setSelectedQuestionnaire] = useState(null);
  const [questionnaires, setQuestionnaires] = useState([]);
  const [riskResults, setRiskResults] = useState(null);
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    fetchQuestionnaires();
  }, []);

  const fetchQuestionnaires = async () => {
    setLoading(true);
    try {
      const data = await assessmentService.getQuestionnaires();
      setQuestionnaires(data);
    } catch (error) {
      console.error('Error fetching questionnaires:', error);
    }
    setLoading(false);
  };

  const handleSelectQuestionnaire = async (questionnaiId) => {
    setLoading(true);
    try {
      const questionnaire = await assessmentService.getQuestionnaire(questionnaiId);
      setSelectedQuestionnaire(questionnaire);
      setCurrentStep('assessment');
    } catch (error) {
      console.error('Error fetching questionnaire:', error);
    }
    setLoading(false);
  };

  const handleSubmitAssessment = async (responses) => {
    setLoading(true);
    try {
      const result = await assessmentService.submitAssessment({
        questionnaire_id: selectedQuestionnaire.id,
        responses,
      });

      // Fetch the risk score
      const riskScore = await resultsService.getRiskScore(result.assessment_id);
      setRiskResults(riskScore);
      setCurrentStep('results');
    } catch (error) {
      console.error('Error submitting assessment:', error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          Mental Health Risk Assessment
        </h1>

        {currentStep === 'questionnaire-selection' && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">
              Select an Assessment
            </h2>
            <div className="grid gap-4">
              {questionnaires.map((q) => (
                <button
                  key={q.id}
                  onClick={() => handleSelectQuestionnaire(q.id)}
                  className="p-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg hover:shadow-lg transition"
                >
                  <h3 className="text-lg font-semibold">{q.name}</h3>
                  <p className="text-sm opacity-90">{q.description}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {currentStep === 'assessment' && selectedQuestionnaire && (
          <QuestionnaireForm
            questionnaire={selectedQuestionnaire}
            onSubmit={handleSubmitAssessment}
            loading={loading}
          />
        )}

        {currentStep === 'results' && riskResults && (
          <RiskResultsVisualization riskData={riskResults} />
        )}
      </div>
    </div>
  );
}

export default AssessmentFlow;
