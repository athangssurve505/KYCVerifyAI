import { Check, Zap, Star, X } from 'lucide-react';
import { useState } from 'react';
import './Pricing.css';

const Pricing = () => {
  const [showComingSoon, setShowComingSoon] = useState(false);

  const plans = [
    {
      name: 'Starter',
      price: '$49',
      period: '/month',
      description: 'Perfect for small businesses',
      features: [
        '1,000 verifications/month',
        'Basic facial recognition',
        'Liveness detection',
        'Email support',
        '99.5% uptime SLA',
        'API access'
      ],
      popular: false,
      color: 'cyan'
    },
    {
      name: 'Professional',
      price: '$149',
      period: '/month',
      description: 'For growing companies',
      features: [
        '10,000 verifications/month',
        'Advanced facial recognition',
        'Liveness detection',
        'Deduplication system',
        'Priority support',
        '99.9% uptime SLA',
        'API access',
        'Custom webhooks',
        'Analytics dashboard'
      ],
      popular: true,
      color: 'green'
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      description: 'For large organizations',
      features: [
        'Unlimited verifications',
        'Enterprise-grade recognition',
        'Advanced liveness detection',
        'Full deduplication suite',
        'Dedicated support',
        '99.99% uptime SLA',
        'API access',
        'Custom integrations',
        'Advanced analytics',
        'On-premise deployment',
        'Custom ML models',
        'SLA guarantees'
      ],
      popular: false,
      color: 'orange'
    }
  ];

  const handlePlanClick = () => {
    setShowComingSoon(true);
  };

  return (
    <div className="pricing">
      <div className="page-header pricing-header">
        <h2 className="page-title">Simple, Transparent Pricing</h2>
        <p className="page-description">
          Choose the perfect plan for your verification needs
        </p>
      </div>

      <div className="pricing-grid">
        {plans.map((plan, idx) => (
          <div 
            key={idx} 
            className={`pricing-card card ${plan.popular ? 'popular' : ''}`}
          >
            {plan.popular && (
              <div className="popular-badge">
                <Star size={14} />
                Most Popular
              </div>
            )}

            <div className="pricing-card-header">
              <h3 className="plan-name">{plan.name}</h3>
              <p className="plan-description">{plan.description}</p>
              <div className="plan-price">
                <span className="price">{plan.price}</span>
                <span className="period">{plan.period}</span>
              </div>
            </div>

            <div className="pricing-card-body">
              <ul className="features-list">
                {plan.features.map((feature, index) => (
                  <li key={index} className="feature-item">
                    <Check size={18} className="check-icon" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="pricing-card-footer">
              <button 
                className={`plan-btn ${plan.popular ? 'primary' : 'secondary'}`}
                onClick={handlePlanClick}
              >
                {plan.name === 'Enterprise' ? 'Contact Sales' : 'Get Started'}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="pricing-faq">
        <h3>Frequently Asked Questions</h3>
        <div className="faq-grid">
          <div className="faq-item">
            <h4>What counts as a verification?</h4>
            <p>One verification equals one successful facial recognition or liveness detection check.</p>
          </div>
          <div className="faq-item">
            <h4>Can I upgrade anytime?</h4>
            <p>Yes! You can upgrade or downgrade your plan at any time with prorated billing.</p>
          </div>
          <div className="faq-item">
            <h4>Is there a free trial?</h4>
            <p>Yes, we offer a 14-day free trial with 100 verifications included.</p>
          </div>
          <div className="faq-item">
            <h4>What payment methods do you accept?</h4>
            <p>We accept all major credit cards, PayPal, and wire transfers for enterprise plans.</p>
          </div>
        </div>
      </div>

      {/* Coming Soon Modal */}
      {showComingSoon && (
        <div className="coming-soon-overlay" onClick={() => setShowComingSoon(false)}>
          <div className="coming-soon-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowComingSoon(false)}>
              <X size={24} />
            </button>
            
            <div className="coming-soon-content">
              <div className="coming-soon-icon">
                <Zap size={64} />
              </div>
              <h2>Coming Soon!</h2>
              <p>We're working hard to bring you this feature.</p>
              <p className="coming-soon-subtitle">
                Sign up for our waitlist to be notified when pricing goes live.
              </p>
              
              <div className="waitlist-form">
                <input 
                  type="email" 
                  placeholder="Enter your email" 
                  className="waitlist-input"
                />
                <button className="waitlist-btn">Join Waitlist</button>
              </div>

              <div className="coming-soon-features">
                <h4>What to expect:</h4>
                <ul>
                  <li>✨ Flexible pricing plans</li>
                  <li>🚀 14-day free trial</li>
                  <li>💳 Secure payment processing</li>
                  <li>📊 Usage-based billing</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Pricing;