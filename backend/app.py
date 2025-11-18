from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Read your keys
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

print("Keys loaded:", GOOGLE_KEY is not None, OPENAI_KEY is not None)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import agents
from agents.budget_agent import BudgetAgent
from agents.expense_analyzer import ExpenseAnalyzer
from agents.savings_agent import SavingsAgent
from agents.debt_agent import DebtAgent
from utils.csv_processor import CSVProcessor
from utils.validators import validate_expense_data, validate_debt_data

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ============================================
# CONFIGURE GOOGLE AI - UPDATED FOR 2025
# ============================================
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
GEMINI_MODEL = None
AI_ENABLED = False
MODEL_NAME = None

def initialize_gemini():
    """Try to initialize Google Gemini AI with latest model names"""
    global GEMINI_MODEL, AI_ENABLED, MODEL_NAME
    
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == 'your_google_api_key_here':
        print("⚠️ No valid Google API Key")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Updated model names for 2024/2025
        models_to_try = [
            'models/gemini-2.5-flash',
            'gemini-2.5-flash',
            'models/gemini-flash-latest',
            'gemini-flash-latest',
            'models/gemini-2.0-flash',
            'models/gemini-2.5-pro',
            'models/gemini-pro-latest',
        ]
        
        for model_name in models_to_try:
            try:
                print(f"🔄 Trying: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # Quick test
                test_response = model.generate_content(
                    "Say 'ready' in one word",
                    generation_config={'max_output_tokens': 10}
                )
                
                # Success!
                GEMINI_MODEL = model
                MODEL_NAME = model_name
                AI_ENABLED = True
                
                print(f"✅ SUCCESS! Using: {model_name}")
                print(f"   API Key: {GOOGLE_API_KEY[:15]}...")
                print(f"   Test: {test_response.text.strip()}")
                return True
                
            except Exception as e:
                error_msg = str(e)[:80]
                print(f"   ❌ Failed: {error_msg}")
                continue
        
        print("❌ All models failed")
        return False
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

# Initialize on startup
initialize_gemini()

# Initialize agents
budget_agent = BudgetAgent()
expense_analyzer = ExpenseAnalyzer()
savings_agent = SavingsAgent()
debt_agent = DebtAgent()
csv_processor = CSVProcessor()

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    return jsonify({
        'message': 'AI Financial Coach API',
        'version': '1.0.0',
        'status': 'running',
        'ai_enabled': AI_ENABLED,
        'ai_model': MODEL_NAME
    })

@app.route('/api/budget/analyze', methods=['POST'])
def analyze_budget():
    try:
        data = request.json
        result = budget_agent.analyze(
            data.get('income', 0),
            data.get('expenses', []),
            data.get('goals', [])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/expenses/upload', methods=['POST'])
def upload_expenses():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            expenses = csv_processor.process_file(filepath)
            return jsonify({
                'success': True,
                'expenses': expenses,
                'count': len(expenses)
            })
        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/expenses/analyze', methods=['POST'])
def analyze_expenses():
    try:
        data = request.json
        expenses = data.get('expenses', [])
        if not validate_expense_data(expenses):
            return jsonify({'error': 'Invalid expense data'}), 400
        result = expense_analyzer.analyze(expenses)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/expenses/categorize', methods=['POST'])
def categorize_expense():
    try:
        data = request.json
        category = expense_analyzer.categorize(
            data.get('description', ''),
            data.get('amount', 0)
        )
        return jsonify({'category': category, 'confidence': 0.85})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/savings/strategy', methods=['POST'])
def get_savings_strategy():
    try:
        data = request.json
        result = savings_agent.create_strategy(
            data.get('income', 0),
            data.get('expenses', []),
            data.get('goals', [])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/savings/goals', methods=['GET', 'POST'])
def handle_goals():
    try:
        if request.method == 'POST':
            goal = request.json
            return jsonify({'success': True, 'goalId': 'goal_123'})
        else:
            return jsonify({'goals': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/debt/analyze', methods=['POST'])
def analyze_debt():
    try:
        data = request.json
        debts = data.get('debts', [])
        if not validate_debt_data(debts):
            return jsonify({'error': 'Invalid debt data'}), 400
        result = debt_agent.analyze(debts)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/debt/payoff-plan', methods=['POST'])
def get_payoff_plan():
    try:
        data = request.json
        result = debt_agent.create_payoff_plan(
            data.get('debts', []),
            data.get('extraPayment', 0),
            data.get('method', 'avalanche')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/debt/compare', methods=['POST'])
def compare_methods():
    try:
        data = request.json
        result = debt_agent.compare_methods(
            data.get('debts', []),
            data.get('extraPayment', 0)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================
# CHAT ROUTE - WORKING VERSION
# ============================================
@app.route('/api/chat', methods=['POST'])
def chat():
    global GEMINI_MODEL, AI_ENABLED
    
    try:
        data = request.json
        message = data.get('message', '')
        context = data.get('context', {})
        
        print(f"\n{'='*60}")
        print(f"💬 CHAT REQUEST")
        print(f"{'='*60}")
        print(f"Message: {message}")
        print(f"AI Enabled: {AI_ENABLED}")
        print(f"Model: {MODEL_NAME}")
        print(f"{'='*60}")
        
        # Check if AI is ready
        if not AI_ENABLED or not GEMINI_MODEL:
            print("⚠️ AI not enabled - returning fallback")
            return jsonify({
                'message': generate_fallback_response(message, context),
                'suggestions': [],
                'ai_powered': False
            })
        
        # Generate AI response
        try:
            total_expenses = sum(exp.get('amount', 0) for exp in context.get('expenses', []))
            
            prompt = f"""You are FinMate, a friendly financial advisor AI.

USER'S FINANCES:
- Income: ${context.get('income', 0):,.2f}
- Expenses: ${total_expenses:,.2f}
- Debts: {len(context.get('debts', []))}

QUESTION: {message}

Provide helpful, specific advice in 2-3 paragraphs. Use emojis. Be friendly and actionable."""

            print("🔄 Generating response...")
            
            response = GEMINI_MODEL.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 1024,
                }
            )
            
            ai_message = response.text
            
            print(f"✅ Success! Length: {len(ai_message)} chars")
            print(f"{'='*60}\n")
            
            return jsonify({
                'message': ai_message,
                'suggestions': [],
                'ai_powered': True,
                'model': MODEL_NAME
            })
            
        except Exception as ai_error:
            print(f"❌ AI Error: {ai_error}")
            print(f"{'='*60}\n")
            
            return jsonify({
                'message': generate_fallback_response(message, context, str(ai_error)),
                'suggestions': [],
                'ai_powered': False,
                'error': str(ai_error)
            })
        
    except Exception as e:
        print(f"❌ Route Error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'message': f"Sorry, I encountered an error: {str(e)}",
            'error': str(e)
        }), 500

def generate_fallback_response(message, context, error=None):
    """Generate a helpful fallback response when AI is unavailable"""
    
    total_expenses = sum(exp.get('amount', 0) for exp in context.get('expenses', []))
    income = context.get('income', 0)
    savings = income - total_expenses
    
    response = f"""📊 **Financial Summary**

Based on your data:
- Monthly Income: ${income:,.2f}
- Total Expenses: ${total_expenses:,.2f}
- Current Savings: ${savings:,.2f}
- Savings Rate: {(savings/income*100) if income > 0 else 0:.1f}%

"""
    
    if 'expense' in message.lower() or 'analyze' in message.lower():
        response += """💡 **Quick Analysis:**
- Track every expense for 30 days
- Categorize spending (housing, food, transport)
- Aim for 50% needs, 30% wants, 20% savings

"""
    
    if 'budget' in message.lower():
        response += """💰 **Budget Basics:**
1. List all income sources
2. Track all expenses
3. Set limits per category
4. Review monthly

"""
    
    if 'save' in message.lower() or 'saving' in message.lower():
        response += """🎯 **Savings Tips:**
- Emergency fund: 3-6 months expenses
- Automate savings transfers
- Pay yourself first

"""
    
    if 'debt' in message.lower():
        response += """💳 **Debt Strategy:**
- Pay minimums on all
- Extra to highest rate (avalanche)
- Or smallest balance (snowball)

"""
    
    if error:
        response += f"""
⚠️ AI temporarily unavailable.

Get API key: https://makersuite.google.com/app/apikey
Add to backend/.env
"""
    
    return response

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    try:
        expenses = [
            {'date': '2024-01-01', 'category': 'Housing', 'amount': 1500.00, 'description': 'Monthly Rent'},
            {'date': '2024-01-02', 'category': 'Food', 'amount': 85.50, 'description': 'Grocery Store'},
            {'date': '2024-01-03', 'category': 'Transportation', 'amount': 45.00, 'description': 'Gas'},
            {'date': '2024-01-05', 'category': 'Food', 'amount': 32.50, 'description': 'Restaurant'},
            {'date': '2024-01-07', 'category': 'Entertainment', 'amount': 120.00, 'description': 'Movie'},
            {'date': '2024-01-08', 'category': 'Utilities', 'amount': 150.00, 'description': 'Electric'},
            {'date': '2024-01-10', 'category': 'Shopping', 'amount': 200.00, 'description': 'Amazon'},
            {'date': '2024-01-12', 'category': 'Food', 'amount': 95.00, 'description': 'Groceries'},
            {'date': '2024-01-15', 'category': 'Transportation', 'amount': 50.00, 'description': 'Uber'},
            {'date': '2024-01-18', 'category': 'Entertainment', 'amount': 45.00, 'description': 'Netflix'},
        ]
        return jsonify({'success': True, 'income': 5000, 'expenses': expenses, 'count': len(expenses)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    return jsonify({
        'income': 5000,
        'expenses': [],
        'debts': [],
        'goals': [],
        'insights': {'savingsRate': 0, 'topCategory': 'N/A', 'monthlyAverage': 0}
    })

@app.route('/api/user/income', methods=['POST'])
def update_income():
    try:
        data = request.json
        return jsonify({'success': True, 'income': data.get('income', 0)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Server error'}), 500

# ============================================
# RUN
# ============================================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AI FINANCIAL COACH - Backend Server")
    print("="*60)
    print("📍 Server: http://localhost:5000")
    print(f"🤖 AI Status: {'✅ ENABLED' if AI_ENABLED else '❌ DISABLED'}")
    if AI_ENABLED:
        print(f"🤖 Model: {MODEL_NAME}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)