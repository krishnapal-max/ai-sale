"""
Lead Management Routes
Handles all lead CRUD operations and AI scoring
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from database.models import Lead
from database.db_instance import db
from ai import lead_scorer
from ai.recommendation import recommendation_engine
from datetime import datetime, timedelta
from functools import wraps

leads_bp = Blueprint('leads', __name__)

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@leads_bp.route('/')
@login_required
def index():
    """List all leads."""
    leads = Lead.query.order_by(Lead.ai_score.desc()).all()
    return render_template('leads.html', leads=leads, title='Lead Management')

@leads_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_lead():
    """Add a new lead."""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            company = request.form.get('company', '').strip()
            job_title = request.form.get('job_title', '').strip()
            
            # Validation
            if not name or len(name) < 2:
                flash('Name must be at least 2 characters', 'error')
                return render_template('lead_form.html', lead=None, title='Add New Lead')
            
            if not email or '@' not in email:
                flash('Please enter a valid email address', 'error')
                return render_template('lead_form.html', lead=None, title='Add New Lead')
            
            # Check if email already exists
            existing_lead = Lead.query.filter_by(email=email).first()
            if existing_lead:
                flash(f'A lead with email {email} already exists', 'error')
                return render_template('lead_form.html', lead=None, title='Add New Lead')
            
            # Create new lead
            lead = Lead(
                name=name,
                email=email,
                phone=phone if phone else None,
                company=company if company else 'Unknown',
                job_title=job_title if job_title else None,
                source=request.form.get('source', 'website'),
                company_size=request.form.get('company_size', 'medium'),
                engagement_level=int(request.form.get('engagement_level', 1)),
                budget_range=request.form.get('budget_range', 'unknown'),
                timeline=request.form.get('timeline', 'unknown'),
                status='new'
            )
            
            db.session.add(lead)
            db.session.commit()
            
            # AI Scoring
            lead.ai_score = lead_scorer.score_lead(lead)
            
            # Get recommendation
            recommendation = recommendation_engine.get_recommendation(lead)
            lead.recommended_action = recommendation['action']
            
            # Set follow-up date
            if recommendation['priority'] == 'high':
                lead.next_followup = datetime.utcnow().date() + timedelta(days=1)
            elif recommendation['priority'] == 'medium':
                lead.next_followup = datetime.utcnow().date() + timedelta(days=3)
            else:
                lead.next_followup = datetime.utcnow().date() + timedelta(days=7)
            
            db.session.commit()
            
            flash(f'✅ Lead {lead.name} added successfully! AI Score: {lead.ai_score}/100', 'success')
            return redirect(url_for('leads.index'))
            
        except ValueError as e:
            flash(f'Invalid input: Please check your form fields', 'error')
            db.session.rollback()
        except Exception as e:
            flash(f'❌ Error adding lead: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('lead_form.html', lead=None, title='Add New Lead')

@leads_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_lead(id):
    """Edit an existing lead."""
    lead = Lead.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Update lead fields
            lead.name = request.form['name']
            lead.email = request.form['email']
            lead.phone = request.form.get('phone')
            lead.company = request.form.get('company')
            lead.job_title = request.form.get('job_title')
            lead.source = request.form.get('source', 'website')
            lead.company_size = request.form.get('company_size', 'medium')
            lead.engagement_level = int(request.form.get('engagement_level', 1))
            lead.budget_range = request.form.get('budget_range', 'unknown')
            lead.timeline = request.form.get('timeline', 'unknown')
            lead.status = request.form.get('status', 'new')
            
            # Re-score with AI
            lead.ai_score = lead_scorer.score_lead(lead)
            
            # Get new recommendation
            recommendation = recommendation_engine.get_recommendation(lead)
            lead.recommended_action = recommendation['action']
            
            db.session.commit()
            
            flash(f'Lead {lead.name} updated successfully!', 'success')
            return redirect(url_for('leads.index'))
            
        except Exception as e:
            flash(f'Error updating lead: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('lead_form.html', lead=lead, title='Edit Lead')

@leads_bp.route('/delete/<int:id>')
@login_required
def delete_lead(id):
    """Delete a lead."""
    lead = Lead.query.get_or_404(id)
    
    try:
        db.session.delete(lead)
        db.session.commit()
        flash(f'Lead {lead.name} deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting lead: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('leads.index'))

@leads_bp.route('/view/<int:id>')
@login_required
def view_lead(id):
    """View lead details."""
    lead = Lead.query.get_or_404(id)
    return render_template('lead_detail.html', lead=lead, title='Lead Details')

@leads_bp.route('/score/<int:id>')
@login_required
def rescore_lead(id):
    """Re-score a lead with AI."""
    lead = Lead.query.get_or_404(id)
    
    lead.ai_score = lead_scorer.score_lead(lead)
    recommendation = recommendation_engine.get_recommendation(lead)
    lead.recommended_action = recommendation['action']
    
    db.session.commit()
    
    flash(f'Lead {lead.name} re-scored. New score: {lead.ai_score}', 'info')
    return redirect(url_for('leads.index'))

@leads_bp.route('/status/<int:id>/<status>')
@login_required
def update_status(id, status):
    """Update lead status."""
    lead = Lead.query.get_or_404(id)
    lead.status = status
    
    db.session.commit()
    flash(f'Lead status updated to {status}', 'success')
    return redirect(url_for('leads.index'))

@leads_bp.route('/api/lead/<int:id>')
def api_get_lead(id):
    """API endpoint to get lead data as JSON."""
    lead = Lead.query.get_or_404(id)
    return jsonify(lead.to_dict())

@leads_bp.route('/api/score/<int:id>')
def api_score_lead(id):
    """API endpoint to score a lead."""
    lead = Lead.query.get_or_404(id)
    score = lead_scorer.score_lead(lead)
    recommendation = recommendation_engine.get_recommendation(lead)
    
    return jsonify({
        'lead_id': id,
        'ai_score': score,
        'recommendation': recommendation
    })

@leads_bp.route('/batch-score')
@login_required
def batch_score():
    """Score all leads with AI."""
    count = lead_scorer.score_all_leads()
    flash(f'{count} leads scored successfully!', 'success')
    return redirect(url_for('leads.index'))

