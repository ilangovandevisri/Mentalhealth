import apiClient from './api';

export const authService = {
  register: async (userData) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  login: async (email, password) => {
    const response = await apiClient.post('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
};

export const assessmentService = {
  getQuestionnaires: async () => {
    const response = await apiClient.get('/assessment/questionnaires');
    return response.data;
  },

  getQuestionnaire: async (id) => {
    const response = await apiClient.get(`/assessment/questionnaires/${id}`);
    return response.data;
  },

  startAssessment: async (questionnaireId) => {
    const response = await apiClient.post('/assessment/start', {
      questionnaire_id: questionnaireId,
    });
    return response.data;
  },

  submitAssessment: async (assessmentData) => {
    const response = await apiClient.post('/assessment/submit', assessmentData);
    return response.data;
  },
};

export const resultsService = {
  getRiskScore: async (assessmentId) => {
    const response = await apiClient.get(`/results/assessment/${assessmentId}`);
    return response.data;
  },

  getLatestAssessment: async () => {
    const response = await apiClient.get('/results/user/latest');
    return response.data;
  },

  getAssessmentHistory: async (limit = 10) => {
    const response = await apiClient.get(`/results/user/history?limit=${limit}`);
    return response.data;
  },

  getResources: async (riskLevel) => {
    const response = await apiClient.get(`/results/resources/${riskLevel}`);
    return response.data;
  },
};
