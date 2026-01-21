"""
Sample Data Generator for AI Sales Agent
Populates the database with sample leads for testing
"""
from app import app
from database.models import Lead
from database.db_instance import db
from ai import lead_scorer
from ai.recommendation import recommendation_engine
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate sample leads for testing."""
    
    sample_leads = [
        # High Priority Leads
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.johnson@techcorp.com',
            'phone': '+1 (555) 123-4567',
            'company': 'TechCorp Solutions',
            'job_title': 'VP of Operations',
            'source': 'referral',
            'company_size': 'large',
            'engagement_level': 5,
            'budget_range': 'high',
            'timeline': 'immediate',
            'status': 'qualified'
        },
        {
            'name': 'Michael Chen',
            'email': 'mchen@innovate.io',
            'phone': '+1 (555) 234-5678',
            'company': 'Innovate.io',
            'job_title': 'CEO',
            'source': 'linkedin',
            'company_size': 'medium',
            'engagement_level': 5,
            'budget_range': 'high',
            'timeline': 'immediate',
            'status': 'new'
        },
        {
            'name': 'Emily Rodriguez',
            'email': 'emily.r@globalenterprise.com',
            'phone': '+1 (555) 345-6789',
            'company': 'Global Enterprise',
            'job_title': 'Director of IT',
            'source': 'website',
            'company_size': 'enterprise',
            'engagement_level': 4,
            'budget_range': 'enterprise',
            'timeline': 'short_term',
            'status': 'qualified'
        },
        {
            'name': 'David Kim',
            'email': 'david.kim@startupxyz.co',
            'phone': '+1 (555) 456-7890',
            'company': 'StartupXYZ',
            'job_title': 'Founder',
            'source': 'referral',
            'company_size': 'small',
            'engagement_level': 5,
            'budget_range': 'medium',
            'timeline': 'immediate',
            'status': 'new'
        },
        
        # Medium Priority Leads
        {
            'name': 'Jessica Thompson',
            'email': 'jthompson@midmarket.com',
            'phone': '+1 (555) 567-8901',
            'company': 'MidMarket Inc',
            'job_title': 'Marketing Manager',
            'source': 'website',
            'company_size': 'medium',
            'engagement_level': 3,
            'budget_range': 'medium',
            'timeline': 'short_term',
            'status': 'new'
        },
        {
            'name': 'Robert Williams',
            'email': 'rwilliams@businessgroup.com',
            'phone': '+1 (555) 678-9012',
            'company': 'Business Group LLC',
            'job_title': 'Sales Director',
            'source': 'cold_call',
            'company_size': 'medium',
            'engagement_level': 4,
            'budget_range': 'medium',
            'timeline': 'short_term',
            'status': 'qualified'
        },
        {
            'name': 'Amanda Foster',
            'email': 'afoster@retailchain.com',
            'phone': '+1 (555) 789-0123',
            'company': 'Retail Chain Co',
            'job_title': 'Operations Head',
            'source': 'linkedin',
            'company_size': 'large',
            'engagement_level': 3,
            'budget_range': 'high',
            'timeline': 'short_term',
            'status': 'new'
        },
        {
            'name': 'Christopher Lee',
            'email': 'clee@consultingfirm.com',
            'phone': '+1 (555) 890-1234',
            'company': 'Consulting Firm',
            'job_title': 'Senior Consultant',
            'source': 'advertisement',
            'company_size': 'medium',
            'engagement_level': 3,
            'budget_range': 'medium',
            'timeline': 'long_term',
            'status': 'new'
        },
        
        # Low Priority Leads
        {
            'name': 'Daniel Brown',
            'email': 'dbrown@smallbiz.net',
            'phone': '+1 (555) 901-2345',
            'company': 'Small Biz Net',
            'job_title': 'Owner',
            'source': 'cold_call',
            'company_size': 'small',
            'engagement_level': 2,
            'budget_range': 'low',
            'timeline': 'long_term',
            'status': 'new'
        },
        {
            'name': 'Michelle Davis',
            'email': 'mdavis@localstore.com',
            'phone': '+1 (555) 012-3456',
            'company': 'Local Store',
            'job_title': 'Manager',
            'source': 'website',
            'company_size': 'small',
            'engagement_level': 1,
            'budget_range': 'unknown',
            'timeline': 'unknown',
            'status': 'new'
        },
        {
            'name': 'James Wilson',
            'email': 'jwilson@freelance.co',
            'phone': '+1 (555) 111-2222',
            'company': 'Freelance Co',
            'job_title': 'Independent',
            'source': 'cold_call',
            'company_size': 'small',
            'engagement_level': 2,
            'budget_range': 'unknown',
            'timeline': 'long_term',
            'status': 'new'
        },
        {
            'name': 'Lisa Anderson',
            'email': 'landerson@newstartup.com',
            'phone': '+1 (555) 222-3333',
            'company': 'New Startup',
            'job_title': 'Founder',
            'source': 'linkedin',
            'company_size': 'small',
            'engagement_level': 2,
            'budget_range': 'low',
            'timeline': 'long_term',
            'status': 'new'
        }
    ]
    
    return sample_leads

def seed_database():
    """Seed the database with sample data."""
    with app.app_context():
        # Check if leads already exist
        existing_leads = Lead.query.count()
        if existing_leads > 0:
            print(f"⚠️  Database already has {existing_leads} leads. Skipping seed.")
            return
        
        print("🌱 Seeding database with sample leads...")
        
        sample_data = generate_sample_data()
        created_count = 0
        
        for lead_data in sample_data:
            # Create lead
            lead = Lead(**lead_data)
            db.session.add(lead)
            db.session.flush()  # Get the lead ID
            
            # Score with AI
            lead.ai_score = lead_scorer.score_lead(lead)
            
            # Get recommendation
            recommendation = recommendation_engine.get_recommendation(lead)
            lead.recommended_action = recommendation['action']
            
            # Set follow-up date based on priority
            if lead.ai_score >= 70:
                lead.next_followup = datetime.utcnow().date() + timedelta(days=1)
            elif lead.ai_score >= 40:
                lead.next_followup = datetime.utcnow().date() + timedelta(days=3)
            else:
                lead.next_followup = datetime.utcnow().date() + timedelta(days=7)
            
            created_count += 1
            print(f"  ✓ Created: {lead.name} (Score: {lead.ai_score})")
        
        db.session.commit()
        print(f"\n✅ Successfully created {created_count} sample leads!")
        print(f"\n📊 Score Distribution:")
        
        high = Lead.query.filter(Lead.ai_score >= 70).count()
        medium = Lead.query.filter(Lead.ai_score >= 40, Lead.ai_score < 70).count()
        low = Lead.query.filter(Lead.ai_score < 40).count()
        
        print(f"  🔥 High Priority (70+): {high}")
        print(f"  ⚡ Medium Priority (40-69): {medium}")
        print(f"  📉 Low Priority (<40): {low}")

if __name__ == '__main__':
    seed_database()

