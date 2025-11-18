import google.generativeai as genai
from config import Config

class SavingsAgent:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        except Exception as e:
            print(f"Warning: Could not initialize Gemini model: {e}")
            self.model = None
    
    def create_strategy(self, income, expenses, goals):
        """Create a personalized savings strategy"""
        total_expenses = sum(exp.get('amount', 0) for exp in expenses)
        available = income - total_expenses
        
        # Emergency fund recommendation (3-6 months of expenses)
        emergency_fund_target = total_expenses * 6
        
        # Calculate recommended savings (50/30/20 rule: 20% for savings)
        recommended_savings = income * 0.20
        
        prompt = f"""
        Create a personalized savings strategy for someone with:
        
        Monthly Income: ${income}
        Monthly Expenses: ${total_expenses}
        Currently Available for Savings: ${available}
        
        Emergency Fund Target: ${emergency_fund_target} (6 months of expenses)
        Recommended Monthly Savings (20% rule): ${recommended_savings}
        
        Provide:
        1. Realistic monthly savings amount
        2. How to build emergency fund
        3. Actionable tips to increase savings
        4. Timeline to reach emergency fund goal
        
        Keep it practical and encouraging.
        """
        
        strategy = ""
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                strategy = response.text
            except Exception as e:
                print(f"AI Error: {e}")
                strategy = self._get_default_strategy(available, recommended_savings, emergency_fund_target)
        else:
            strategy = self._get_default_strategy(available, recommended_savings, emergency_fund_target)
        
        # Calculate timeline
        monthly_savings = min(available * 0.8, recommended_savings)
        months_to_emergency_fund = (emergency_fund_target / monthly_savings) if monthly_savings > 0 else 999
        
        return {
            'recommendedMonthlySavings': round(monthly_savings, 2),
            'emergencyFundTarget': round(emergency_fund_target, 2),
            'currentSavingsCapacity': round(available, 2),
            'strategy': strategy,
            'timeline': f"{int(months_to_emergency_fund)} months" if months_to_emergency_fund < 100 else "Increase income to save faster"
        }
    
    def _get_default_strategy(self, available, recommended, emergency_target):
        """Default strategy when AI is unavailable"""
        if available <= 0:
            return """
            🚨 You're currently spending more than you earn. 
            
            Priority actions:
            1. Review all expenses and cut non-essentials
            2. Look for ways to increase income
            3. Create a strict budget to track spending
            """
        elif available < recommended:
            return f"""
            💡 You can save ${available:.2f}/month, but aim for ${recommended:.2f} (20% of income).
            
            Strategy:
            1. Save ${available * 0.8:.2f} automatically each month
            2. Build emergency fund of ${emergency_target:.2f}
            3. Review expenses monthly to increase savings
            """
        else:
            return f"""
            ✅ Great! You can save ${available:.2f}/month.
            
            Recommended allocation:
            1. Emergency Fund: ${available * 0.5:.2f}/month
            2. Goals/Investments: ${available * 0.3:.2f}/month
            3. Buffer: ${available * 0.2:.2f}/month
            
            You'll reach your emergency fund in {int(emergency_target / (available * 0.5))} months!
            """