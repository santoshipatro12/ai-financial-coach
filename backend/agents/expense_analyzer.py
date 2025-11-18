from collections import defaultdict

class ExpenseAnalyzer:
    def __init__(self):
        self.categories = {
            'Food': ['grocery', 'restaurant', 'food', 'cafe', 'dining', 'pizza', 'coffee'],
            'Transportation': ['gas', 'uber', 'lyft', 'transit', 'parking', 'fuel'],
            'Housing': ['rent', 'mortgage', 'property', 'lease'],
            'Utilities': ['electric', 'water', 'internet', 'phone', 'utility', 'bill'],
            'Entertainment': ['movie', 'concert', 'game', 'netflix', 'spotify', 'entertainment'],
            'Shopping': ['amazon', 'store', 'mall', 'clothing', 'clothes', 'shopping']
        }
    
    def categorize(self, description, amount):
        """Categorize a single expense based on description"""
        description_lower = description.lower()
        
        for category, keywords in self.categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        return 'Other'
    
    def analyze(self, expenses):
        """Analyze a list of expenses"""
        # Group by category
        category_totals = defaultdict(float)
        
        for exp in expenses:
            category = exp.get('category', 'Other')
            # If no category, try to auto-categorize
            if not category or category == 'Other':
                description = exp.get('description', '')
                category = self.categorize(description, exp.get('amount', 0))
            
            amount = exp.get('amount', 0)
            category_totals[category] += amount
        
        total = sum(category_totals.values())
        
        # Calculate percentages
        breakdown = []
        for category, amount in category_totals.items():
            percentage = (amount / total * 100) if total > 0 else 0
            breakdown.append({
                'category': category,
                'amount': round(amount, 2),
                'percentage': round(percentage, 2)
            })
        
        # Sort by amount (highest first)
        breakdown.sort(key=lambda x: x['amount'], reverse=True)
        
        insights = self._generate_insights(breakdown, total)
        
        return {
            'categoryBreakdown': breakdown,
            'totalExpenses': round(total, 2),
            'topCategory': breakdown[0]['category'] if breakdown else 'None',
            'insights': insights
        }
    
    def _generate_insights(self, breakdown, total):
        """Generate insights from expense breakdown"""
        if not breakdown:
            return []
        
        insights = []
        top_category = breakdown[0]
        
        if top_category['percentage'] > 40:
            insights.append(f"⚠️ {top_category['category']} expenses are high at {top_category['percentage']:.1f}% of total spending")
        
        if top_category['percentage'] > 30:
            insights.append(f"💡 Consider reviewing your {top_category['category']} spending for potential savings")
        
        # Check for balanced budget (no single category over 35%)
        if all(cat['percentage'] < 35 for cat in breakdown):
            insights.append("✅ Your spending is well-balanced across categories")
        
        return insights