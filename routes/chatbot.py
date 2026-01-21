"""
Chatbot Routes
AI-powered help assistant for the sales agent
"""
from flask import Blueprint, request, jsonify, session
from database.models import Lead
from database.db_instance import db
from functools import wraps

chatbot_bp = Blueprint('chatbot', __name__)

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Chatbot knowledge base
CHATBOT_RESPONSES = {
    'ai_scoring': {
        'keywords': ['score', 'ai', 'scoring', 'how does scoring work', 'calculate score'],
        'response': '🤖 **AI Scoring System**\n\nOur AI scores leads from 0-100 based on:\n\n✅ **Engagement Level** (0-5) - How interested the lead is\n💼 **Company Size** - Small/Medium/Large companies\n💰 **Budget Range** - Available budget level\n📅 **Timeline** - Urgency of purchase\n🌐 **Source** - How they found us\n\n**Score Interpretation:**\n🔥 70+ = High Priority (Hot leads!)\n⚡ 40-69 = Medium Priority (Follow up soon)\n📉 <40 = Low Priority (Nurture for later)\n\nTip: Update lead details to improve their score!'
    },
    'add_lead': {
        'keywords': ['add', 'create', 'new lead', 'how to add', 'add a lead'],
        'response': '➕ **How to Add a Lead**\n\n1. Click "➕ Add New Lead" button\n2. Fill in basic information:\n   - Name\n   - Email\n   - Phone\n   - Company\n   - Job Title\n\n3. Add AI Scoring Factors:\n   - Engagement Level (1-5)\n   - Company Size\n   - Budget Range\n   - Timeline\n   - Source\n\n4. Click "Save Lead"\n\nThe AI will automatically score your lead! 🎯'
    },
    'leads': {
        'keywords': ['leads', 'manage leads', 'view leads', 'lead list', 'all leads'],
        'response': '👥 **Lead Management**\n\nAccess leads from the sidebar or dashboard:\n\n📊 **Dashboard**: See top priority leads\n👥 **Leads Page**: View all leads with filters\n\n**Features:**\n- 🔍 Filter by Priority (High/Medium/Low)\n- 📈 Filter by Status (New/Qualified/Converted/Lost)\n- 🤖 Re-score individual leads\n- ✏️ Edit lead details\n- 🗑️ Delete leads\n- 📋 View detailed lead info\n\nClick on any lead to see full details!'
    },
    'priority': {
        'keywords': ['priority', 'high priority', 'urgent', 'important', 'top leads'],
        'response': '🔥 **Lead Priority Levels**\n\n**High Priority (70+)**\n- Ready to convert soon\n- High engagement\n- Good budget\n- Action: Contact immediately!\n\n**Medium Priority (40-69)**\n- Interested but not urgent\n- May need nurturing\n- Action: Follow up in 1-2 weeks\n\n**Low Priority (<40)**\n- Early stage leads\n- Lower engagement\n- Action: Keep in nurture list\n\nUse filters to focus on high-priority leads first! ⚡'
    },
    'recommendations': {
        'keywords': ['recommend', 'suggestion', 'action', 'what to do', 'next step'],
        'response': '💡 **AI Recommendations**\n\nOur AI provides smart actions for each lead:\n\n✉️ **Send Email** - Best for initial contact\n📞 **Schedule Call** - For interested leads\n🎁 **Special Offer** - To close deals\n📧 **Follow-up** - Keep engagement going\n🎯 **Demo** - Show product features\n\nEach recommendation is based on:\n- Lead engagement level\n- Company size\n- Budget\n- Timeline\n\nCheck the dashboard for personalized recommendations! 🎯'
    },
    'notifications': {
        'keywords': ['notification', 'remind', 'alert', 'reminder', 'follow up'],
        'response': '🔔 **Notifications & Reminders**\n\n**Types:**\n📋 **Reminder** - Follow-up needed\n⚠️ **Alert** - Important action\n💡 **Suggestion** - AI recommendation\n📅 **Meeting** - Scheduled event\n\n**How to use:**\n1. Go to "Notifications" tab\n2. View all reminders\n3. Click "Mark as Read" when done\n4. Generate new reminders anytime\n\nStay on top of your leads! 📌'
    },
    'help': {
        'keywords': ['help', 'support', 'how to', 'guide', 'tutorial'],
        'response': '❓ **Help & Support**\n\n**I can help with:**\n- 🤖 AI Scoring System\n- ➕ Adding new leads\n- 👥 Managing leads\n- 🔥 Lead priorities\n- 💡 AI recommendations\n- 🔔 Notifications\n- 🌙 Dark/Light mode\n- ⚙️ Settings\n\nJust ask me anything about the system! 😊\n\n**Quick Tips:**\n💡 Toggle sidebar with ☰ button\n🌙 Switch themes with 🌙/☀️ button\n🚪 Logout anytime\n\nWhat else can I help you with?'
    },
    'theme': {
        'keywords': ['dark mode', 'light mode', 'theme', 'mode', 'appearance'],
        'response': '🌙 **Dark/Light Mode**\n\n**How to switch:**\n1. Click 🌙 (moon) in top-right for Dark Mode\n2. Click ☀️ (sun) in top-right for Light Mode\n\n**Your preference is saved!** 💾\n\nThe theme applies to:\n- Dashboard\n- All pages\n- Login/Register\n\nSwitch anytime you prefer! 🎨'
    },
    'default': {
        'keywords': [],
        'response': '🤔 I\'m not sure about that. Here are things I can help with:\n\n📝 Ask about:\n- **AI Scoring** - How leads are scored\n- **Adding Leads** - How to create new leads\n- **Managing Leads** - View and edit leads\n- **Priorities** - Understanding lead importance\n- **Recommendations** - AI-suggested actions\n- **Notifications** - Reminders & alerts\n- **Theme** - Dark/Light mode\n- **Help** - General guidance\n\nTry asking one of these! 😊'
    }
}

def find_best_response(user_input):
    """Find the best matching response based on user input."""
    user_input_lower = user_input.lower().strip()
    
    # Check each keyword category
    for key, data in CHATBOT_RESPONSES.items():
        if key == 'default':
            continue
        
        # Check if any keyword matches
        for keyword in data['keywords']:
            if keyword.lower() in user_input_lower:
                return data['response']
    
    # If no match found, return default response
    return CHATBOT_RESPONSES['default']['response']

@chatbot_bp.route('/api/message', methods=['POST'])
@login_required
def chat_message():
    """Handle chatbot messages."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get AI response
        bot_response = find_best_response(user_message)
        
        return jsonify({
            'status': 'success',
            'user_message': user_message,
            'bot_response': bot_response,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/api/stats', methods=['GET'])
@login_required
def chatbot_stats():
    """Get dashboard stats for chatbot context."""
    try:
        total_leads = Lead.query.count()
        high_priority = Lead.query.filter(Lead.ai_score >= 70).count()
        medium_priority = Lead.query.filter(Lead.ai_score >= 40, Lead.ai_score < 70).count()
        
        return jsonify({
            'total_leads': total_leads,
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': total_leads - high_priority - medium_priority
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
