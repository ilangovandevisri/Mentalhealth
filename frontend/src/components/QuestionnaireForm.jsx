import React, { useState } from 'react';

function QuestionnaireForm({ questionnaire, onSubmit, loading }) {
  const [responses, setResponses] = useState({});

  const handleResponseChange = (questionId, value) => {
    setResponses({
      ...responses,
      [questionId]: parseInt(value),
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(responses);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        {questionnaire.name}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {questionnaire.questions.map((question, idx) => (
          <div key={question.id} className="border-b pb-6">
            <label className="block text-lg font-medium text-gray-700 mb-3">
              {idx + 1}. {question.text}
            </label>

            <div className="grid grid-cols-4 gap-2">
              {question.labels.map((label, i) => (
                <label key={i} className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name={question.id}
                    value={question.scale[i]}
                    onChange={(e) => handleResponseChange(question.id, e.target.value)}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-600">{label}</span>
                </label>
              ))}
            </div>
          </div>
        ))}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold rounded-lg hover:shadow-lg transition disabled:opacity-50"
        >
          {loading ? 'Submitting...' : 'Submit Assessment'}
        </button>
      </form>
    </div>
  );
}

export default QuestionnaireForm;
