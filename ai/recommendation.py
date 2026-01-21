"""
AI Recommendation System
Generates action recommendations based on lead scores and characteristics
"""
from database.models import Lead, Notification
from database.db_instance import db
from datetime import datetime, timedelta

class RecommendationEngine:
    """AI-powered recommendation system for sales actions."""
    
    # Score thresholds
    HIGH_SCORE_THRESHOLD = 70
    MEDIUM_SCORE_THRESHOLD = 40
    
    # Action templates
    ACTIONS = {
        'call_immediately': {
            'action': 'Call Immediately',
            'priority': 'high',
            'description': 'This is a hot lead. Call within 24 hours.',
            'icon': '📞'
        },
        'follow_up_email': {
            'action': 'Send Follow-up Email',
            'priority': 'medium',
            'description': 'Send a personalized follow-up email.',
            'icon': '📧'
        },
        'schedule_meeting': {
            'action': 'Schedule Meeting',
            'priority': 'high',
            'description': 'Schedule a demo or discovery call.',
            'icon': '📅'
        },
        'nurture_campaign': {
            'action': 'Add to Nurture Campaign',
            'priority': 'low',
            'description': 'Add to email nurture sequence.',
            'icon': '📬'
        },
        'escalate': {
            'action': 'Escalate to Manager',
            'priority': 'high',
            'description': 'This lead requires manager attention.',
            'icon': '⚠️'
        },
        'reconnect': {
            'action': 'Reconnect Later',
            'priority': 'low',
            'description': 'Reconnect in a few weeks.',
            'icon': '🔄'
        }
    }
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize recommendation rules."""
        return [
            {
                'condition': lambda lead: (
                    lead.ai_score >= self.HIGH_SCORE_THRESHOLD and
                    lead.engagement_level >= 4 and
                    lead.timeline in ['immediate', 'short_term']
                ),
                'action_key': 'call_immediately'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score >= self.HIGH_SCORE_THRESHOLD and
                    lead.timeline == 'immediate'
                ),
                'action_key': 'schedule_meeting'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score >= self.HIGH_SCORE_THRESHOLD and
                    lead.source == 'referral'
                ),
                'action_key': 'call_immediately'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score >= self.MEDIUM_SCORE_THRESHOLD and
                    lead.ai_score < self.HIGH_SCORE_THRESHOLD and
                    lead.engagement_level >= 3
                ),
                'action_key': 'follow_up_email'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score >= self.MEDIUM_SCORE_THRESHOLD and
                    lead.budget_range in ['high', 'enterprise']
                ),
                'action_key': 'schedule_meeting'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score < self.MEDIUM_SCORE_THRESHOLD and
                    lead.ai_score >= 25 and
                    lead.source == 'referral'
                ),
                'action_key': 'follow_up_email'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score < 25 and
                    lead.engagement_level <= 2
                ),
                'action_key': 'reconnect'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score < self.MEDIUM_SCORE_THRESHOLD and
                    lead.status == 'new'
                ),
                'action_key': 'nurture_campaign'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score >= self.HIGH_SCORE_THRESHOLD and
                    lead.company_size == 'enterprise'
                ),
                'action_key': 'escalate'
            },
            {
                'condition': lambda lead: (
                    lead.ai_score >= self.MEDIUM_SCORE_THRESHOLD and
                    lead.status == 'qualified'
                ),
                'action_key': 'schedule_meeting'
            }
        ]
    
    def get_recommendation(self, lead):
        """
        Get recommended action for a lead.
        
        Args:
            lead: Lead object
            
        Returns:
            dict: Recommendation with action, priority, and description
        """
        # Try to find a matching rule
        for rule in self.rules:
            if rule['condition'](lead):
                action_key = rule['action_key']
                recommendation = self.ACTIONS[action_key].copy()
                recommendation['reason'] = self._get_reason(lead, action_key)
                return recommendation
        
        # Default action based on score
        if lead.ai_score >= self.HIGH_SCORE_THRESHOLD:
            recommendation = self.ACTIONS['call_immediately'].copy()
        elif lead.ai_score >= self.MEDIUM_SCORE_THRESHOLD:
            recommendation = self.ACTIONS['follow_up_email'].copy()
        else:
            recommendation = self.ACTIONS['nurture_campaign'].copy()
        
        recommendation['reason'] = 'Default recommendation based on score'
        return recommendation
    
    def _get_reason(self, lead, action_key):
        """Generate a reason for the recommendation."""
        reasons = {
            'call_immediately': f"High score ({lead.ai_score}) and {lead.timeline} timeline",
            'follow_up_email': f"Medium score ({lead.ai_score}) with good engagement",
            'schedule_meeting': f"Strong potential - {lead.budget_range} budget",
            'nurture_campaign': f"Low score ({lead.ai_score}) - needs nurturing",
            'escalate': f"Enterprise lead ({lead.company_size}) requires attention",
            'reconnect': f"Low engagement ({lead.engagement_level}/5) - reconnect later"
        }
        return reasons.get(action_key, 'Based on lead characteristics')
    
    def apply_recommendation(self, lead):
        """
        Apply recommendation to a lead and create notification.
        
        Args:
            lead: Lead object
            
        Returns:
            Lead: Updated lead with recommendation
        """
        recommendation = self.get_recommendation(lead)
        lead.recommended_action = recommendation['action']
        
        # Create notification for high priority actions
        if recommendation['priority'] == 'high':
            notification = Notification(
                lead_id=lead.id,
                title=f"Action Required: {lead.name}",
                message=f"{recommendation['icon']} {recommendation['action']} - {recommendation['description']}",
                notification_type='alert',
                priority='high',
                action_date=datetime.utcnow().date() + timedelta(days=1)
            )
            db.session.add(notification)
        
        return lead
    
    def get_bulk_recommendations(self):
        """Get recommendations for all leads that need attention."""
        leads = Lead.query.filter(
            Lead.status.in_(['new', 'qualified'])
        ).all()
        
        recommendations = []
        for lead in leads:
            rec = self.get_recommendation(lead)
            recommendations.append({
                'lead': lead.to_dict(),
                'recommendation': rec
            })
        
        return recommendations
    
    def generate_report(self):
        """Generate a summary report of recommendations."""
        leads = Lead.query.all()
        
        report = {
            'total_leads': len(leads),
            'high_priority': 0,
            'medium_priority': 0,
            'low_priority': 0,
            'action_counts': {},
            'status_breakdown': {}
        }
        
        for lead in leads:
            if lead.ai_score >= self.HIGH_SCORE_THRESHOLD:
                report['high_priority'] += 1
            elif lead.ai_score >= self.MEDIUM_SCORE_THRESHOLD:
                report['medium_priority'] += 1
            else:
                report['low_priority'] += 1
            
            # Count actions
            action = lead.recommended_action or 'Pending'
            report['action_counts'][action] = report['action_counts'].get(action, 0) + 1
            
            # Status breakdown
            status = lead.status
            report['status_breakdown'][status] = report['status_breakdown'].get(status, 0) + 1
        
        return report


# Singleton instance
recommendation_engine = RecommendationEngine()

