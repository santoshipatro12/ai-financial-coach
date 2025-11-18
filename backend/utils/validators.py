def validate_expense_data(expenses):
    """Validate expense data structure"""
    if not isinstance(expenses, list):
        return False
    
    for exp in expenses:
        if not isinstance(exp, dict):
            return False
        if 'amount' not in exp:
            return False
        try:
            float(exp['amount'])
        except (ValueError, TypeError):
            return False
    
    return True


def validate_debt_data(debts):
    """Validate debt data structure"""
    if not isinstance(debts, list):
        return False
    
    required_fields = ['name', 'balance', 'rate', 'minPayment']
    
    for debt in debts:
        if not isinstance(debt, dict):
            return False
        if not all(field in debt for field in required_fields):
            return False
        try:
            float(debt['balance'])
            float(debt['rate'])
            float(debt['minPayment'])
        except (ValueError, TypeError):
            return False
    
    return True