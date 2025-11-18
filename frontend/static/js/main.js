// Main Application Logic

// Global state
let appState = {
    income: 0,
    expenses: [],
    debts: [],
    goals: [],
    currentUser: null
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM Loaded - Starting app...');
    initializeApp();
});

async function initializeApp() {
    console.log('⚙️ Initializing app...');
    
    // Show loading screen
    showLoading();

    // Typing animation for AI demo
    startTypingAnimation();

    // Initialize charts after a short delay
    setTimeout(() => {
        if (typeof window.chartManager !== 'undefined') {
            window.chartManager.init();
        } else {
            console.error('❌ chartManager not available!');
        }
    }, 500);

    // Setup event listeners
    setupEventListeners();

    // Load initial data
    await loadInitialData();

    // Hide loading screen
    setTimeout(() => {
        hideLoading();
        console.log('✅ App initialized successfully');
    }, 1500);
}

// ===== Loading Screen =====
function showLoading() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.classList.remove('hidden');
    }
}

function hideLoading() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.classList.add('hidden');
    }
}

// ===== Typing Animation =====
function startTypingAnimation() {
    const text = "I've analyzed your spending patterns and found you could save $450/month by optimizing your subscriptions and dining expenses. Would you like me to create a detailed plan?";
    const element = document.getElementById('aiDemoText');
    if (!element) {
        console.warn('⚠️ aiDemoText element not found');
        return;
    }
    
    let index = 0;
    element.textContent = ''; // Clear first

    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, 30);
        }
    }

    setTimeout(type, 1000);
}

// ===== Event Listeners =====
function setupEventListeners() {
    console.log('🎧 Setting up event listeners...');
    
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href').substring(1);
            scrollToSection(target);
            updateActiveNav(this);
        });
    });

    // CSV Upload
    const csvInput = document.getElementById('csvFileInput');
    const uploadArea = document.getElementById('uploadArea');

    if (csvInput) {
        csvInput.addEventListener('change', handleFileUpload);
    }

    if (uploadArea) {
        uploadArea.addEventListener('click', () => {
            csvInput.click();
        });

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#B35BFF';
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = '';
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '';
            const file = e.dataTransfer.files[0];
            if (file && file.name.endsWith('.csv')) {
                handleFileUpload({ target: { files: [file] } });
            }
        });
    }

    // Chat input
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('click', function() {
            const agent = this.dataset.agent;
            handleFeatureCardClick(agent);
        });
    });

    console.log('✅ Event listeners set up');
}

// ===== Navigation =====
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offset = 80;
        const targetPosition = section.offsetTop - offset;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
}

function updateActiveNav(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

// ===== Data Loading =====
async function loadInitialData() {
    console.log('📥 Loading initial data...');
    try {
        const data = await financeAPI.getDashboardData();
        if (data) {
            appState = { ...appState, ...data };
            updateDashboard();
            console.log('✅ Initial data loaded');
        }
    } catch (error) {
        console.error('❌ Error loading initial data:', error);
        showNotification('Using demo data', 'info');
    }
}

async function loadSampleData() {
    console.log('📊 Loading sample data...');
    try {
        showLoading();
        const data = await financeAPI.loadSampleData();
        
        console.log('📦 Sample data received:', data);
        
        if (data && data.success) {
            appState.expenses = data.expenses || [];
            appState.income = data.income || 5000;
            
            console.log(`✅ Loaded ${appState.expenses.length} expenses`);
            console.log(`💰 Income: $${appState.income}`);
            
            showNotification(`Loaded ${data.count} transactions!`, 'success');
            updateDashboard();
            updateCharts();
        } else {
            throw new Error('Invalid data format');
        }
    } catch (error) {
        console.error('❌ Error loading sample data:', error);
        showNotification('Error loading sample data: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// ===== File Upload =====
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
        showNotification('Please upload a CSV file', 'error');
        return;
    }

    try {
        showLoading();
        console.log('📤 Uploading file:', file.name);
        const result = await financeAPI.uploadCSV(file);
        
        if (result.expenses) {
            appState.expenses = result.expenses;
            showNotification(`Uploaded ${result.expenses.length} transactions`, 'success');
            updateDashboard();
            updateCharts();
        }
    } catch (error) {
        console.error('❌ Error uploading file:', error);
        showNotification('Error uploading file', 'error');
    } finally {
        hideLoading();
    }
}

// ===== Income Management =====
async function updateIncome() {
    const incomeInput = document.getElementById('incomeInput');
    const income = parseFloat(incomeInput.value);

    console.log('💰 Updating income to:', income);

    if (!income || income <= 0) {
        showNotification('Please enter a valid income amount', 'error');
        return;
    }

    try {
        await financeAPI.updateIncome(income);
        appState.income = income;
        showNotification('Income updated successfully!', 'success');
        updateDashboard();
        updateCharts();
    } catch (error) {
        console.error('❌ Error updating income:', error);
        showNotification('Error updating income', 'error');
    }
}

// ===== Dashboard Updates =====
function updateDashboard() {
    console.log('📊 Updating dashboard...');
    updateStats();
    updateCharts();
    updateDebtList();
}

function updateStats() {
    const totalExpenses = appState.expenses.reduce((sum, exp) => sum + (exp.amount || 0), 0);
    const savings = appState.income - totalExpenses;
    const savingsRate = appState.income > 0 ? (savings / appState.income * 100).toFixed(0) : 0;

    console.log('📈 Stats:', { income: appState.income, expenses: totalExpenses, savings, savingsRate });

    // Update hero stats
    const statItems = document.querySelectorAll('.hero-stats .stat-item');
    if (statItems.length >= 3) {
        statItems[0].querySelector('.stat-number').textContent = `$${appState.income.toLocaleString()}`;
        statItems[1].querySelector('.stat-number').textContent = `$${totalExpenses.toLocaleString()}`;
        statItems[2].querySelector('.stat-number').textContent = `${savingsRate}%`;
    }
}

function updateCharts() {
    console.log('📊 Updating charts with expenses:', appState.expenses.length);
    
    if (appState.expenses.length === 0) {
        console.warn('⚠️ No expenses to chart');
        return;
    }

    if (!window.chartManager) {
        console.error('❌ chartManager not available');
        return;
    }

    // Group expenses by category
    const categoryTotals = {};
    appState.expenses.forEach(exp => {
        const category = exp.category || 'Other';
        categoryTotals[category] = (categoryTotals[category] || 0) + (exp.amount || 0);
    });

    const labels = Object.keys(categoryTotals);
    const data = Object.values(categoryTotals);

    console.log('📊 Category data:', categoryTotals);

    // Update expense chart
    window.chartManager.update('expense', {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: [
                'rgba(179, 91, 255, 0.8)',
                'rgba(74, 218, 255, 0.8)',
                'rgba(0, 255, 179, 0.8)',
                'rgba(255, 107, 107, 0.8)',
                'rgba(255, 184, 77, 0.8)',
                'rgba(168, 168, 168, 0.8)'
            ],
            borderColor: 'rgba(26, 31, 47, 1)',
            borderWidth: 2
        }]
    });

    // Update category chart
    window.chartManager.update('category', {
        labels: labels,
        datasets: [{
            label: 'Monthly Spending',
            data: data,
            backgroundColor: [
                'rgba(179, 91, 255, 0.8)',
                'rgba(74, 218, 255, 0.8)',
                'rgba(0, 255, 179, 0.8)',
                'rgba(255, 107, 107, 0.8)',
                'rgba(255, 184, 77, 0.8)'
            ],
            borderRadius: 8,
            borderWidth: 2,
            borderColor: 'rgba(26, 31, 47, 1)'
        }]
    });
}

function updateDebtList() {
    const debtList = document.getElementById('debtList');
    if (!debtList) return;

    if (appState.debts.length === 0) {
        debtList.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                <i class="fas fa-check-circle" style="font-size: 3rem; color: var(--accent); margin-bottom: 1rem;"></i>
                <p>No debts added yet!</p>
            </div>
        `;
        return;
    }

    debtList.innerHTML = appState.debts.map(debt => `
        <div class="debt-item" style="margin-bottom: 1rem; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">${debt.name}</span>
                <span style="color: #FF6B6B;">$${debt.balance.toLocaleString()}</span>
            </div>
            <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: var(--text-secondary);">
                <span>APR: ${debt.rate}%</span>
                <span>Min: $${debt.minPayment}</span>
            </div>
        </div>
    `).join('');
}

// ===== Chat Functionality =====
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    console.log('💬 Sending message:', message);

    if (!message) return;

    addMessageToChat(message, 'user');
    input.value = '';

    showTypingIndicator();

    try {
        const response = await financeAPI.sendChatMessage(message, {
            income: appState.income,
            expenses: appState.expenses,
            debts: appState.debts
        });

        hideTypingIndicator();

        console.log('🤖 AI Response:', response);

        if (response && response.message) {
            addMessageToChat(response.message, 'ai');
        } else {
            addMessageToChat('Sorry, I got an empty response. Please try again.', 'ai');
        }

        if (response.suggestions) {
            handleAISuggestions(response.suggestions);
        }
    } catch (error) {
        hideTypingIndicator();
        addMessageToChat('Sorry, I encountered an error: ' + error.message, 'ai');
        console.error('❌ Chat error:', error);
    }
}

function sendQuickMessage(message) {
    const input = document.getElementById('chatInput');
    if (input) {
        input.value = message;
        sendMessage();
    }
}

function addMessageToChat(message, type) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    const avatar = type === 'ai' 
        ? '<i class="fas fa-robot"></i>'
        : '<i class="fas fa-user"></i>';

    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${avatar}
        </div>
        <div class="message-content">
            <p>${message}</p>
        </div>
    `;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;

    const indicator = document.createElement('div');
    indicator.className = 'message ai-message typing-indicator-message';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    messagesContainer.appendChild(indicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

// ===== Goals Management =====
function openGoalModal() {
    document.getElementById('goalModal').classList.add('active');
}

function closeGoalModal() {
    document.getElementById('goalModal').classList.remove('active');
}

async function addGoal() {
    const name = document.getElementById('goalName').value;
    const amount = parseFloat(document.getElementById('goalAmount').value);
    const current = parseFloat(document.getElementById('goalCurrent').value) || 0;

    if (!name || !amount) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    try {
        const goal = { name, targetAmount: amount, currentAmount: current };
        await financeAPI.createSavingsGoal(goal);
        
        appState.goals.push(goal);
        showNotification('Goal added successfully!', 'success');
        closeGoalModal();
        
        document.getElementById('goalName').value = '';
        document.getElementById('goalAmount').value = '';
        document.getElementById('goalCurrent').value = '';
    } catch (error) {
        console.error('❌ Error adding goal:', error);
        showNotification('Error adding goal', 'error');
    }
}

// ===== Debt Management =====
function openDebtModal() {
    document.getElementById('debtModal').classList.add('active');
}

function closeDebtModal() {
    document.getElementById('debtModal').classList.remove('active');
}

async function addDebt() {
    const name = document.getElementById('debtName').value;
    const balance = parseFloat(document.getElementById('debtBalance').value);
    const rate = parseFloat(document.getElementById('debtRate').value);
    const minPayment = parseFloat(document.getElementById('debtMinPayment').value);

    if (!name || !balance || !rate || !minPayment) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    const debt = { name, balance, rate, minPayment };
    appState.debts.push(debt);
    
    showNotification('Debt added successfully!', 'success');
    closeDebtModal();
    updateDebtList();
    
    document.getElementById('debtName').value = '';
    document.getElementById('debtBalance').value = '';
    document.getElementById('debtRate').value = '';
    document.getElementById('debtMinPayment').value = '';

    try {
        const analysis = await financeAPI.analyzeDebt(appState.debts);
        if (analysis.recommendations) {
            addMessageToChat(analysis.recommendations, 'ai');
            scrollToSection('chat');
        }
    } catch (error) {
        console.error('❌ Error analyzing debt:', error);
    }
}

// ===== Feature Cards =====
async function handleFeatureCardClick(agent) {
    scrollToSection('chat');

    let message = '';
    switch(agent) {
        case 'budget':
            message = 'Can you analyze my budget and give me recommendations?';
            break;
        case 'expense':
            message = 'Please analyze my expense patterns';
            break;
        case 'savings':
            message = 'Help me create a savings strategy';
            break;
        case 'debt':
            message = 'Show me the best way to pay off my debts';
            break;
    }

    document.getElementById('chatInput').value = message;
    setTimeout(() => sendMessage(), 500);
}

// ===== Utility Functions =====
function refreshDashboard() {
    showLoading();
    loadInitialData().then(() => {
        hideLoading();
        showNotification('Dashboard refreshed!', 'success');
    });
}

function exportData() {
    const data = {
        income: appState.income,
        expenses: appState.expenses,
        debts: appState.debts,
        goals: appState.goals,
        exportDate: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `finance-data-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);

    showNotification('Data exported successfully!', 'success');
}

function showNotification(message, type = 'info') {
    console.log(`📢 Notification (${type}): ${message}`);
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#00FFB3' : type === 'error' ? '#FF6B6B' : '#4ADAFF'};
        color: #0A0F1F;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        font-weight: 600;
        animation: slideInRight 0.3s ease;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function attachFile() {
    document.getElementById('csvFileInput').click();
}

function toggleVoice() {
    showNotification('Voice input coming soon!', 'info');
}

function handleAISuggestions(suggestions) {
    console.log('💡 AI Suggestions:', suggestions);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideOutRight {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(100px); }
    }
    .hidden { display: none !important; }
`;
document.head.appendChild(style);

console.log('✅ Main app loaded');