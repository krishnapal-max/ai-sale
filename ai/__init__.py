"""
AI Lead Scoring Module
Uses Machine Learning to score leads based on their characteristics
"""
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta

class LeadScoringAI:
    """AI-powered lead scoring system."""
    
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.model_path = os.path.join(os.path.dirname(__file__), 'lead_scoring_model.pkl')
        self.is_trained = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load the ML model."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model = data['model']
                    self.encoders = data['encoders']
                    self.is_trained = True
                    print("✅ AI Model loaded from file")
            except:
                self._train_initial_model()
        else:
            self._train_initial_model()
    
    def _train_initial_model(self):
        """Train the initial model with sample data."""
        print("🎯 Training initial AI model...")
        
        # Create and train the model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        # Train with sample data
        X_train, y_train = self._generate_training_data()
        
        # Fit the model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Save the model
        self._save_model()
        print("✅ AI Model trained and saved!")
    
    def _generate_training_data(self):
        """Generate synthetic training data for the model."""
        # Sample training data - using numeric encoding
        # Features: source_code, company_size_code, engagement_level, budget_code, timeline_code
        training_samples = [
            # High-value leads
            ([0, 2, 5, 2, 0], 95),  # referral, large, 5, high, immediate
            ([1, 2, 5, 2, 1], 88),  # website, large, 5, high, short_term
            ([0, 1, 4, 2, 0], 82),  # referral, medium, 4, high, immediate
            ([2, 2, 5, 1, 0], 78),  # cold_call, large, 5, medium, immediate
            ([3, 1, 5, 2, 1], 85),  # linkedin, medium, 5, high, short_term
            
            # Medium-value leads
            ([1, 1, 3, 1, 1], 65),  # website, medium, 3, medium, short_term
            ([2, 1, 4, 1, 1], 60),  # cold_call, medium, 4, medium, short_term
            ([0, 0, 4, 1, 2], 55),  # referral, small, 4, medium, long_term
            ([3, 2, 3, 1, 1], 58),  # linkedin, large, 3, medium, short_term
            ([1, 0, 4, 0, 0], 52),  # website, small, 4, low, immediate
            
            # Low-value leads
            ([2, 0, 2, 3, 2], 35),  # cold_call, small, 2, unknown, long_term
            ([1, 0, 1, 3, 2], 25),  # website, small, 1, unknown, long_term
            ([2, 1, 2, 3, 2], 30),  # cold_call, medium, 2, unknown, long_term
            ([3, 0, 2, 0, 2], 28),  # linkedin, small, 2, low, long_term
            ([1, 1, 1, 3, 2], 22),  # website, medium, 1, unknown, long_term
        ]
        
        X = []
        y = []
        
        for features, score in training_samples:
            X.append(features)
            y.append(score)
        
        return np.array(X), np.array(y)
    
    def _save_model(self):
        """Save the trained model to file."""
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'encoders': self.encoders
            }, f)
    
    def _encode_feature(self, feature, feature_name, categories):
        """Encode a categorical feature using simple mapping."""
        # Create mapping if not exists
        if feature_name not in self.encoders:
            self.encoders[feature_name] = {cat: idx for idx, cat in enumerate(categories)}
        
        # Get encoded value
        mapping = self.encoders[feature_name]
        return mapping.get(feature, 0)  # Default to 0 if unknown
    
    def score_lead(self, lead):
        """
        Calculate AI score for a lead.
        
        Args:
            lead: Lead object with attributes
            
        Returns:
            int: Score between 0-100
        """
        # Extract features from lead
        features = {
            'source': lead.source,
            'company_size': lead.company_size,
            'engagement_level': lead.engagement_level,
            'budget_range': lead.budget_range,
            'timeline': lead.timeline
        }
        
        # Encode features using direct mappings
        encoded_features = []
        
        # Source encoding
        source_map = {'website': 1, 'referral': 0, 'cold_call': 2, 'linkedin': 3, 'advertisement': 4, 'other': 5}
        encoded_features.append(source_map.get(features['source'], 1))
        
        # Company size encoding
        size_map = {'small': 0, 'medium': 1, 'large': 2, 'enterprise': 3}
        encoded_features.append(size_map.get(features['company_size'], 1))
        
        # Engagement level (already numeric)
        encoded_features.append(int(features['engagement_level']))
        
        # Budget encoding
        budget_map = {'unknown': 3, 'low': 0, 'medium': 1, 'high': 2, 'enterprise': 2}
        encoded_features.append(budget_map.get(features['budget_range'], 3))
        
        # Timeline encoding
        timeline_map = {'unknown': 2, 'long_term': 2, 'short_term': 1, 'immediate': 0}
        encoded_features.append(timeline_map.get(features['timeline'], 2))
        
        # Make prediction
        features_array = np.array([encoded_features])
        
        if self.is_trained and self.model is not None:
            # Use ML model for prediction
            predicted_score = self.model.predict(features_array)[0]
            # Add some variance based on engagement
            engagement_boost = (features['engagement_level'] - 1) * 2
            final_score = min(100, max(0, int(predicted_score + engagement_boost)))
        else:
            # Fallback to rule-based scoring
            final_score = self._rule_based_scoring(lead)
        
        return final_score
    
    def _rule_based_scoring(self, lead):
        """Fallback rule-based scoring if ML model is not available."""
        score = 0
        
        # Source scoring
        source_scores = {
            'referral': 25,
            'linkedin': 20,
            'website': 15,
            'cold_call': 10,
            'advertisement': 10,
            'other': 5
        }
        score += source_scores.get(lead.source, 5)
        
        # Company size scoring
        size_scores = {
            'enterprise': 25,
            'large': 20,
            'medium': 15,
            'small': 10
        }
        score += size_scores.get(lead.company_size, 10)
        
        # Engagement scoring (max 25 points)
        score += (lead.engagement_level * 5)
        
        # Budget scoring
        budget_scores = {
            'high': 25,
            'medium': 15,
            'low': 10,
            'unknown': 5
        }
        score += budget_scores.get(lead.budget_range, 5)
        
        # Timeline scoring
        timeline_scores = {
            'immediate': 20,
            'short_term': 15,
            'long_term': 10,
            'unknown': 5
        }
        score += timeline_scores.get(lead.timeline, 5)
        
        return min(100, score)
    
    def score_all_leads(self):
        """Score all leads in the database."""
        leads = Lead.query.all()
        scored_count = 0
        
        for lead in leads:
            new_score = self.score_lead(lead)
            if lead.ai_score != new_score:
                lead.ai_score = new_score
                scored_count += 1
        
        db.session.commit()
        return scored_count
    
    def get_feature_importance(self):
        """Get feature importance from the model."""
        if self.model is not None:
            importance = self.model.feature_importances_
            feature_names = ['source', 'company_size', 'engagement', 'budget', 'timeline']
            return dict(zip(feature_names, importance))
        return None


# Singleton instance
lead_scorer = LeadScoringAI()

