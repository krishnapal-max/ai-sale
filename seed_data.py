"""
Seed database with sample leads for testing
"""
from app import create_app
from database.db_instance import db
from database.models import Lead, Notification
from datetime import datetime, timedelta

app = create_app()

def seed_data():
    """Add sample leads and notifications."""
    with app.app_context():
        # Check if data already exists
        if Lead.query.count() > 0:
            print("✅ Sample data already exists. Skipping seed.")
            return
        
        # Sample leads data
        sample_leads = [
            {
                'name': 'John Smith',
                'email': 'john.smith@techcorp.com',
                'phone': '+1-555-0101',
                'company': 'TechCorp Inc',
                'job_title': 'VP of Sales',
                'engagement_level': 5,
                'company_size': 'Large',
                'budget_range': '100k-500k',
                'timeline': 'Immediate',
                'source': 'LinkedIn',
                'status': 'Active'
            },
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.j@innovate.io',
                'phone': '+1-555-0102',
                'company': 'Innovate Solutions',
                'job_title': 'Operations Manager',
                'engagement_level': 4,
                'company_size': 'Medium',
                'budget_range': '50k-100k',
                'timeline': '1-2 months',
                'source': 'Referral',
                'status': 'Pending'
            },
            {
                'name': 'Michael Chen',
                'email': 'm.chen@startupx.com',
                'phone': '+1-555-0103',
                'company': 'StartupX Labs',
                'job_title': 'Founder & CEO',
                'engagement_level': 3,
                'company_size': 'Small',
                'budget_range': '10k-50k',
                'timeline': '3-6 months',
                'source': 'Website',
                'status': 'Active'
            },
            {
                'name': 'Emily Rodriguez',
                'email': 'emily.r@enterprise.com',
                'phone': '+1-555-0104',
                'company': 'Enterprise Global',
                'job_title': 'Chief Technology Officer',
                'engagement_level': 5,
                'company_size': 'Large',
                'budget_range': '500k+',
                'timeline': 'Immediate',
                'source': 'Industry Event',
                'status': 'Negotiating'
            },
            {
                'name': 'David Park',
                'email': 'dpark@midmarket.io',
                'phone': '+1-555-0105',
                'company': 'Mid-Market Services',
                'job_title': 'Sales Director',
                'engagement_level': 2,
                'company_size': 'Medium',
                'budget_range': '25k-75k',
                'timeline': '6+ months',
                'source': 'Cold Call',
                'status': 'Pending'
            },
            {
                'name': 'Lisa Anderson',
                'email': 'l.anderson@tech.ventures',
                'phone': '+1-555-0106',
                'company': 'Tech Ventures LLC',
                'job_title': 'Business Development Manager',
                'engagement_level': 4,
                'company_size': 'Small',
                'budget_range': '30k-80k',
                'timeline': '2-3 months',
                'source': 'Email Campaign',
                'status': 'Active'
            },
            {
                'name': 'Robert Taylor',
                'email': 'r.taylor@corporate.net',
                'phone': '+1-555-0107',
                'company': 'Corporate Dynamics',
                'job_title': 'Procurement Lead',
                'engagement_level': 3,
                'company_size': 'Large',
                'budget_range': '200k-400k',
                'timeline': 'Q2 2026',
                'source': 'Partner Referral',
                'status': 'Proposal'
            },
            {
                'name': 'Jennifer Martinez',
                'email': 'j.martinez@digital.co',
                'phone': '+1-555-0108',
                'company': 'Digital Innovations Co',
                'job_title': 'Product Manager',
                'engagement_level': 2,
                'company_size': 'Medium',
                'budget_range': '40k-90k',
                'timeline': 'Q3 2026',
                'source': 'Trade Show',
                'status': 'Active'
            }
        ]
        
        # Create leads with AI scores
        leads = []
        for lead_data in sample_leads:
            lead = Lead(
                name=lead_data['name'],
                email=lead_data['email'],
                phone=lead_data['phone'],
                company=lead_data['company'],
                job_title=lead_data['job_title'],
                engagement_level=lead_data['engagement_level'],
                company_size=lead_data['company_size'],
                budget_range=lead_data['budget_range'],
                timeline=lead_data['timeline'],
                source=lead_data['source'],
                status=lead_data['status']
            )
            leads.append(lead)
            db.session.add(lead)
        
        db.session.commit()
        
        # Calculate AI scores (simple formula: engagement_level * 10 + company_size points + budget points)
        for lead in leads:
            score = lead.engagement_level * 15
            if lead.company_size == 'Large':
                score += 20
            elif lead.company_size == 'Medium':
                score += 10
            
            if 'Immediate' in lead.timeline:
                score += 15
            elif '1-2' in lead.timeline or '2-3' in lead.timeline:
                score += 10
            
            if '500k' in lead.budget_range or '200k' in lead.budget_range:
                score += 10
            elif '100k' in lead.budget_range or '50k' in lead.budget_range:
                score += 5
            
            lead.ai_score = min(score, 100)
        
        db.session.commit()
        
        # Add sample notifications
        for i, lead in enumerate(leads[:4]):
            notification = Notification(
                lead_id=lead.id,
                title=f'Follow-up: {lead.name}',
                message=f'Contact {lead.name} at {lead.company} - High priority lead',
                type='reminder',
                priority='high',
                is_read=False
            )
            db.session.add(notification)
        
        db.session.commit()
        
        print("✅ Database seeded with 8 sample leads and 4 notifications!")
        print(f"   - Sample leads: {Lead.query.count()} total")
        print(f"   - Notifications: {Notification.query.count()} total")

if __name__ == '__main__':
    seed_data()
