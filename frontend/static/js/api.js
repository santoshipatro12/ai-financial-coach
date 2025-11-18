// API Integration Layer
const API_BASE_URL = 'http://localhost:5000/api';

class FinanceAPI {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        console.log(`🔄 API Request: ${url}`);

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            console.log(`✅ API Response:`, data);
            
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error(`❌ API Error (${endpoint}):`, error);
            throw error;
        }
    }

    // Budget Analysis
    async analyzeBudget(data) {
        return await this.request('/budget/analyze', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // Expense Analysis
    async uploadCSV(file) {
        const formData = new FormData();
        formData.append('file', file);

        console.log('📤 Uploading CSV...');
        const response = await fetch(`${this.baseURL}/expenses/upload`, {
            method: 'POST',
            body: formData
        });

        return await response.json();
    }

    async analyzeExpenses(expenses) {
        return await this.request('/expenses/analyze', {
            method: 'POST',
            body: JSON.stringify({ expenses })
        });
    }

    async categorizeExpense(description, amount) {
        return await this.request('/expenses/categorize', {
            method: 'POST',
            body: JSON.stringify({ description, amount })
        });
    }

    // Savings Strategy
    async getSavingsStrategy(data) {
        return await this.request('/savings/strategy', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async createSavingsGoal(goal) {
        return await this.request('/savings/goals', {
            method: 'POST',
            body: JSON.stringify(goal)
        });
    }

    async getSavingsGoals() {
        return await this.request('/savings/goals', {
            method: 'GET'
        });
    }

    // Debt Management
    async analyzeDebt(debts) {
        return await this.request('/debt/analyze', {
            method: 'POST',
            body: JSON.stringify({ debts })
        });
    }

    async getDebtPayoffPlan(debts, extraPayment, method = 'avalanche') {
        return await this.request('/debt/payoff-plan', {
            method: 'POST',
            body: JSON.stringify({ debts, extraPayment, method })
        });
    }

    async compareDebtMethods(debts, extraPayment) {
        return await this.request('/debt/compare', {
            method: 'POST',
            body: JSON.stringify({ debts, extraPayment })
        });
    }

    // AI Chat
    async sendChatMessage(message, context = {}) {
        return await this.request('/chat', {
            method: 'POST',
            body: JSON.stringify({ message, context })
        });
    }

    // Sample Data
    async loadSampleData() {
        return await this.request('/sample-data', {
            method: 'GET'
        });
    }

    // Dashboard Data
    async getDashboardData() {
        return await this.request('/dashboard', {
            method: 'GET'
        });
    }

    async updateIncome(income) {
        return await this.request('/user/income', {
            method: 'POST',
            body: JSON.stringify({ income })
        });
    }
}

// Create global API instance
const financeAPI = new FinanceAPI();
console.log('✅ Finance API initialized');