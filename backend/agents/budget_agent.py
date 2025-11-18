import google.generativeai as genai
from config import Config

class BudgetAgent:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        except Exception as e:
            print(f"Warning: Could not initialize Gemini model: {e}")
            self.model = None
    
    def analyze(self, income, expenses, goals):
        total_expenses = sum(exp.get('amount', 0) for exp in expenses)
        savings = income - total_expenses
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        # Create prompt for AI
        prompt = f"""
        Analyze this budget and provide recommendations:
        
        Monthly Income: ${income}
        Total Expenses: ${total_expenses}
        Savings: ${savings}
        Savings Rate: {savings_rate:.1f}%
        
        Provide 3-5 actionable recommendations to improve this budget.
        Be specific and practical.
        """
        
        recommendations = ""
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                recommendations = response.text
            except Exception as e:
                print(f"AI Error: {e}")
                recommendations = self._get_default_recommendations(savings_rate)
        else:
            recommendations = self._get_default_recommendations(savings_rate)
        
        return {
            'income': income,
            'totalExpenses': total_expenses,
            'savings': savings,
            'savingsRate': round(savings_rate, 2),
            'recommendations': recommendations,
            'budgetHealth': 'Good' if savings_rate >= 20 else 'Fair' if savings_rate >= 10 else 'Needs Improvement'
        }
    
    def _get_default_recommendations(self, savings_rate):
        if savings_rate >= 20:
            return "✅ Great job! Your savings rate is healthy. Consider increasing investments."
        elif savings_rate >= 10:
            return "⚠️ Your savings rate is fair. Try to reduce discretionary spending by 10%."
        else:
            return "🚨 Your savings rate is low. Review your expenses and find areas to cut back."