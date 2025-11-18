class DebtAgent:
    def __init__(self):
        pass
    
    def analyze(self, debts):
        """Analyze debt situation and provide recommendations"""
        if not debts:
            return {
                'totalDebt': 0,
                'totalMinPayment': 0,
                'averageRate': 0,
                'recommendations': '✅ Great! You have no debts.',
                'priorityDebt': None
            }
        
        total_debt = sum(d.get('balance', 0) for d in debts)
        total_min_payment = sum(d.get('minPayment', 0) for d in debts)
        avg_interest = sum(d.get('rate', 0) for d in debts) / len(debts)
        
        # Sort by interest rate (highest first) for avalanche method
        sorted_debts = sorted(debts, key=lambda x: x.get('rate', 0), reverse=True)
        
        # Calculate total interest per year
        annual_interest = sum(d.get('balance', 0) * d.get('rate', 0) / 100 for d in debts)
        
        recommendations = f"""
📊 Debt Analysis Summary:
        
Total Debt: ${total_debt:,.2f}
Monthly Minimum Payments: ${total_min_payment:,.2f}
Average Interest Rate: {avg_interest:.2f}%
Annual Interest Cost: ${annual_interest:,.2f}

🎯 Recommended Strategy (Avalanche Method):

Priority Order (Highest Interest First):
"""
        for i, debt in enumerate(sorted_debts, 1):
            recommendations += f"\n{i}. {debt['name']} - ${debt['balance']:,.2f} at {debt['rate']}% APR"
        
        recommendations += f"""

💡 Action Plan:
1. Pay minimums on all debts
2. Put extra money toward '{sorted_debts[0]['name']}' (highest interest)
3. Once paid off, roll that payment to the next debt
4. This saves the most on interest charges!
        """
        
        return {
            'totalDebt': round(total_debt, 2),
            'totalMinPayment': round(total_min_payment, 2),
            'averageRate': round(avg_interest, 2),
            'annualInterest': round(annual_interest, 2),
            'recommendations': recommendations,
            'priorityDebt': sorted_debts[0]['name'] if sorted_debts else None,
            'debtCount': len(debts)
        }
    
    def create_payoff_plan(self, debts, extra_payment, method='avalanche'):
        """Create a debt payoff plan"""
        if not debts:
            return {
                'method': method,
                'order': [],
                'estimatedMonths': 0,
                'totalInterest': 0,
                'plan': 'No debts to pay off!'
            }
        
        # Sort debts based on method
        if method == 'avalanche':
            sorted_debts = sorted(debts, key=lambda x: x.get('rate', 0), reverse=True)
            method_description = "Highest Interest First (Saves Most Money)"
        else:  # snowball
            sorted_debts = sorted(debts, key=lambda x: x.get('balance', 0))
            method_description = "Smallest Balance First (Quick Wins)"
        
        # Simple payoff calculation
        total_payment = sum(d.get('minPayment', 0) for d in debts) + extra_payment
        total_debt = sum(d.get('balance', 0) for d in debts)
        
        # Rough estimate (doesn't account for interest accumulation)
        estimated_months = int(total_debt / total_payment) if total_payment > 0 else 999
        
        # Rough interest calculation
        avg_rate = sum(d.get('rate', 0) for d in debts) / len(debts) / 100 / 12
        total_interest = total_debt * avg_rate * estimated_months
        
        plan = f"""
🎯 {method.upper()} METHOD: {method_description}

Payoff Order:
"""
        for i, debt in enumerate(sorted_debts, 1):
            plan += f"{i}. {debt['name']} - ${debt['balance']:,.2f}\n"
        
        plan += f"""
Monthly Payment: ${total_payment:,.2f}
Estimated Payoff Time: {estimated_months} months ({estimated_months // 12} years, {estimated_months % 12} months)
Estimated Interest Paid: ${total_interest:,.2f}
        """
        
        return {
            'method': method,
            'order': [d['name'] for d in sorted_debts],
            'estimatedMonths': estimated_months,
            'totalInterest': round(total_interest, 2),
            'monthlyPayment': round(total_payment, 2),
            'plan': plan
        }
    
    def compare_methods(self, debts, extra_payment):
        """Compare avalanche vs snowball methods"""
        avalanche = self.create_payoff_plan(debts, extra_payment, 'avalanche')
        snowball = self.create_payoff_plan(debts, extra_payment, 'snowball')
        
        # Determine which saves more
        interest_savings = avalanche['totalInterest'] - snowball['totalInterest']
        time_savings = snowball['estimatedMonths'] - avalanche['estimatedMonths']
        
        comparison = f"""
📊 METHOD COMPARISON

AVALANCHE (Pay Highest Interest First):
- Payoff Time: {avalanche['estimatedMonths']} months
- Total Interest: ${avalanche['totalInterest']:,.2f}
- Saves: ${abs(interest_savings):,.2f} in interest

SNOWBALL (Pay Smallest Balance First):
- Payoff Time: {snowball['estimatedMonths']} months
- Total Interest: ${snowball['totalInterest']:,.2f}
- Motivation: Faster wins (pay off debts quicker)

💡 RECOMMENDATION: 
{"Avalanche method saves more money!" if interest_savings < 0 else "Both methods are similar - choose based on preference!"}
        """
        
        return {
            'avalanche': avalanche,
            'snowball': snowball,
            'interestSavings': abs(round(interest_savings, 2)),
            'timeDifference': abs(time_savings),
            'recommendation': 'avalanche' if interest_savings < -100 else 'either',
            'comparison': comparison
        }