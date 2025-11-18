// Chart.js Configuration and Initialization

let expenseChart, incomeExpenseChart, trendsChart, categoryChart;

// Initialize all charts
function initializeCharts() {
    console.log('📊 Initializing charts...');
    initExpenseChart();
    initIncomeExpenseChart();
    initTrendsChart();
    initCategoryChart();
    console.log('✅ All charts initialized');
}

// Expense Breakdown Pie Chart
function initExpenseChart() {
    const ctx = document.getElementById('expenseChart');
    if (!ctx) {
        console.warn('⚠️ expenseChart canvas not found');
        return;
    }

    expenseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Housing', 'Food', 'Transportation', 'Entertainment', 'Utilities', 'Other'],
            datasets: [{
                data: [1500, 600, 300, 200, 150, 250],
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
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#B0B3C1',
                        padding: 15,
                        font: { size: 12, family: 'Inter' }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(29, 31, 37, 0.9)',
                    titleColor: '#FFFFFF',
                    bodyColor: '#B0B3C1',
                    borderColor: 'rgba(179, 91, 255, 0.5)',
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            let value = context.parsed || 0;
                            let total = context.dataset.data.reduce((a, b) => a + b, 0);
                            let percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: $${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Income vs Expenses Bar Chart
function initIncomeExpenseChart() {
    const ctx = document.getElementById('incomeExpenseChart');
    if (!ctx) {
        console.warn('⚠️ incomeExpenseChart canvas not found');
        return;
    }

    incomeExpenseChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                {
                    label: 'Income',
                    data: [5000, 5200, 5000, 5300, 5100, 5000],
                    backgroundColor: 'rgba(0, 255, 179, 0.6)',
                    borderColor: 'rgba(0, 255, 179, 1)',
                    borderWidth: 2,
                    borderRadius: 8
                },
                {
                    label: 'Expenses',
                    data: [3200, 3400, 3100, 3500, 3300, 3000],
                    backgroundColor: 'rgba(179, 91, 255, 0.6)',
                    borderColor: 'rgba(179, 91, 255, 1)',
                    borderWidth: 2,
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(180, 91, 255, 0.1)' },
                    ticks: {
                        color: '#B0B3C1',
                        callback: function(value) { return '$' + value; }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#B0B3C1' }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#B0B3C1',
                        padding: 15,
                        font: { size: 12, family: 'Inter' }
                    }
                }
            }
        }
    });
}

// Monthly Trends Line Chart
function initTrendsChart() {
    const ctx = document.getElementById('trendsChart');
    if (!ctx) {
        console.warn('⚠️ trendsChart canvas not found');
        return;
    }

    trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Savings',
                data: [1800, 1800, 1900, 1800, 1800, 2000],
                borderColor: 'rgba(74, 218, 255, 1)',
                backgroundColor: 'rgba(74, 218, 255, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(74, 218, 255, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(180, 91, 255, 0.1)' },
                    ticks: {
                        color: '#B0B3C1',
                        callback: function(value) { return '$' + value; }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#B0B3C1' }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#B0B3C1',
                        font: { size: 12, family: 'Inter' }
                    }
                }
            }
        }
    });
}

// Category Insights Horizontal Bar Chart
function initCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) {
        console.warn('⚠️ categoryChart canvas not found');
        return;
    }

    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Housing', 'Food', 'Transportation', 'Entertainment', 'Utilities'],
            datasets: [{
                label: 'Monthly Spending',
                data: [1500, 600, 300, 200, 150],
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
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { color: 'rgba(180, 91, 255, 0.1)' },
                    ticks: {
                        color: '#B0B3C1',
                        callback: function(value) { return '$' + value; }
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#B0B3C1' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// Update charts with new data
function updateChartData(chartName, newData) {
    let chart;
    switch(chartName) {
        case 'expense':
            chart = expenseChart;
            break;
        case 'incomeExpense':
            chart = incomeExpenseChart;
            break;
        case 'trends':
            chart = trendsChart;
            break;
        case 'category':
            chart = categoryChart;
            break;
    }
    
    if (chart && newData) {
        if (newData.labels) chart.data.labels = newData.labels;
        if (newData.datasets) chart.data.datasets = newData.datasets;
        chart.update('active');
        console.log(`✅ ${chartName} chart updated`);
    } else {
        console.warn(`⚠️ Could not update ${chartName} chart`);
    }
}

// Export for use in other files
window.chartManager = {
    init: initializeCharts,
    update: updateChartData
};

console.log('✅ Chart manager loaded');