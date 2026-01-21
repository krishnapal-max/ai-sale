"""
Help Assistant / Recommendation Chatbot Routes
Focused chatbot for Call, Email, Follow-up, and Manage actions
"""
from flask import Blueprint, request, jsonify, session, render_template
from database.models import Lead, Notification
from database.db_instance import db
from functools import wraps

help_assistant_bp = Blueprint('help_assistant', __name__)

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Knowledge base for help and recommendations
HELP_RESPONSES = {
    'call': {
        'keywords': ['call', 'phone', 'contact', 'reach out', 'dial', 'phone call', 'calling'],
        'responses': [
            '📞 **Making a Call**\n\n1. Go to Leads section\n2. Select a lead\n3. Click "Call" button\n4. Log the call duration and notes\n5. System auto-updates lead status\n\nTip: Log calls to track engagement! 💡',
            '📞 **Call Best Practices**\n\n✅ Call during business hours (9 AM - 5 PM)\n✅ Have lead details ready\n✅ Keep notes during call\n✅ Update lead status after call\n✅ Schedule follow-up if needed\n\nHigh-score leads first! 🎯'
        ]
    },
    'email': {
        'keywords': ['email', 'send', 'message', 'mail', 'correspondence', 'compose', 'newsletter'],
        'responses': [
            '📧 **Sending an Email**\n\n1. Go to Leads section\n2. Find the lead\n3. Click "Email" button\n4. Compose message\n5. Add template or custom text\n6. Send and log\n\nSystem tracks email history! 📨',
            '📧 **Email Templates**\n\nUse pre-made templates for:\n✉️ Introduction emails\n✉️ Follow-up emails\n✉️ Proposal emails\n✉️ Closing emails\n\nPersonalize before sending! ✨'
        ]
    },
    'followup': {
        'keywords': ['follow up', 'followup', 'follow-up', 'reminder', 'schedule', 'next step', 'next action', 'reschedule'],
        'responses': [
            '⏰ **Setting Follow-ups**\n\n1. Open a lead\n2. Click "Schedule Follow-up"\n3. Choose date/time\n4. Add follow-up type (call/email/meet)\n5. Save and get reminders\n\nNever miss a deadline! ✅',
            '⏰ **Follow-up Strategy**\n\n📅 Quick calls: 1-2 days after initial contact\n📅 Proposals: 3 days after sending\n📅 Hot leads: Same day if possible\n📅 Cold leads: Weekly\n\nSet reminders to stay organized! 🔔'
        ]
    },
    'manage': {
        'keywords': ['manage', 'manage lead', 'update', 'edit', 'status', 'priority', 'assign', 'organize', 'change status'],
        'responses': [
            '📋 **Managing Leads**\n\n✏️ Update lead info anytime\n🏷️ Set priority (High/Med/Low)\n📊 Track status changes\n✅ Mark as completed\n🔄 Reassign to team members\n📝 Add notes and comments\n\nKeep data fresh! 🔄',
            '📊 **Lead Status Updates**\n\n🟢 Active - Currently working\n🟡 Pending - Waiting for response\n🔵 Negotiating - Deal discussions\n🟣 Proposal - Proposal sent\n⚫ Closed - Deal completed\n\nUpdate regularly for accurate analytics! 📈'
        ]
    },
    'recommendation': {
        'keywords': ['recommend', 'suggestion', 'advice', 'help me', 'what should', 'best practice', 'recommendation', 'suggest', 'recommend me', 'priority'],
        'responses': [
            '💡 **AI Recommendations**\n\nOur AI suggests:\n✨ Best leads to contact first\n🎯 Optimal follow-up timing\n📈 Upsell opportunities\n🔥 High-value prospects\n⏰ Urgent follow-ups needed\n\nCheck your recommendations daily! 🚀',
            '🎯 **Smart Prioritization**\n\nFocus on:\n1️⃣ High-score leads (70+) → Call immediately\n2️⃣ Medium leads (40-69) → Schedule follow-up\n3️⃣ Low leads (<40) → Add to nurture list\n\nMax efficiency = More sales! 💰'
        ]
    },
    'scoring': {
        'keywords': ['score', 'ai score', 'scoring', 'how score', 'calculate', 'scoring system', 'lead score', 'rating'],
        'responses': [
            '🤖 **AI Lead Scoring**\n\nScores based on:\n✅ Engagement Level (0-5)\n💼 Company Size\n💰 Budget Range\n📅 Timeline\n🌐 Source\n\n**Score Meaning:**\n🔥 70+ = Hot (Contact NOW)\n⚡ 40-69 = Warm (Follow up soon)\n📉 <40 = Cold (Nurture later)\n\nHigher score = Better prospect! 🎯',
            '📊 **Understanding Scores**\n\nLead Score Formula:\n• Engagement: +15 per level\n• Large company: +20\n• Immediate timeline: +15\n• High budget: +10\n• Source quality: +5-10\n\nMax score: 100\nMin score: 0\n\nUse to prioritize your time! ⏱️'
        ]
    },
    'dashboard': {
        'keywords': ['dashboard', 'overview', 'statistics', 'stats', 'metrics', 'analytics', 'reports'],
        'responses': [
            '📊 **Dashboard Overview**\n\nSee at a glance:\n📈 Total leads count\n🔥 High priority leads\n⚡ Medium priority leads\n📉 Low priority leads\n💼 Recent leads added\n🎯 Top prospects\n\nMonitor your pipeline! 📊',
            '📈 **Dashboard Widgets**\n\n1. **Stats Card** - Quick metrics\n2. **Top Leads** - Best prospects\n3. **Recent Leads** - Latest additions\n4. **Notifications** - Action items\n5. **Recommendations** - Next steps\n\nEverything at your fingertips! 👀'
        ]
    },
    'help': {
        'keywords': ['help', 'how to', 'what is', 'explain', 'support', 'guide', 'tutorial', 'how does', 'question'],
        'responses': [
            '🆘 **Available Commands**\n\n❓ Ask about:\n- 📞 Calling leads\n- 📧 Sending emails\n- ⏰ Setting follow-ups\n- 📋 Managing leads\n- 💡 Recommendations\n- 🤖 Scoring system\n- 📊 Dashboard\n- 🎯 Best practices\n\nWhat do you need help with? 🤔',
            '📚 **Getting Started**\n\n1. View all leads in "Leads" section\n2. Check lead scores and AI ratings\n3. Start with high-priority leads\n4. Log all interactions\n5. Use follow-ups for consistency\n6. Check recommendations daily\n7. Monitor dashboard metrics\n\nYou got this! 💪'
        ]
    }
}


def get_random_response(category):
    """Get a response from the category."""
    import random
    if category in HELP_RESPONSES:
        responses = HELP_RESPONSES[category]['responses']
        return random.choice(responses)
    return None

def find_best_response(user_message):
    """Find best matching response based on keywords."""
    message = user_message.lower().strip()
    
    # Check each category
    for category, data in HELP_RESPONSES.items():
        keywords = data['keywords']
        for keyword in keywords:
            if keyword in message:
                return get_random_response(category)
    
    # Default responses if no match
    defaults = [
        '🤔 I can help with:\n\n📞 **Call** - How to contact leads\n📧 **Email** - Sending messages\n⏰ **Follow-up** - Schedule reminders\n📋 **Manage** - Organize leads\n💡 **Recommendation** - Get suggestions\n\nWhat would you like to know? 😊',
        '💬 Try asking about:\n\n"How to call a lead?"\n"How to send email?"\n"Set a follow-up"\n"Manage my leads"\n"What do you recommend?"\n\nI\'m here to help! 👋'
    ]
    import random
    return random.choice(defaults)

@help_assistant_bp.route('/api/message', methods=['POST'])
@login_required
def send_message():
    """Handle chatbot messages."""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Get response
    bot_response = find_best_response(user_message)
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response,
        'success': True
    })

@help_assistant_bp.route('/chat')
@login_required
def chat_page():
    """Render dedicated chatbot page if needed."""
    return render_template('help_chat.html', title='Help & Recommendations')
