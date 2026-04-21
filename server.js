const path = require('path');
const express = require('express');
const Stripe = require('stripe');

const app = express();

const PORT = process.env.PORT || 3000;
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;
const WEALTHX_STRIPE_MONTHLY_PRICE_ID = process.env.WEALTHX_STRIPE_MONTHLY_PRICE_ID;
const WEALTHX_STRIPE_YEARLY_PRICE_ID = process.env.WEALTHX_STRIPE_YEARLY_PRICE_ID;
const WEALTHX_PUBLIC_BASE_URL = process.env.WEALTHX_PUBLIC_BASE_URL;

if (!STRIPE_SECRET_KEY) {
  console.warn('[startup] STRIPE_SECRET_KEY is not configured. Stripe API endpoints will be disabled.');
}

const stripe = STRIPE_SECRET_KEY ? new Stripe(STRIPE_SECRET_KEY) : null;

app.post('/api/stripe/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];

  if (!stripe || !STRIPE_WEBHOOK_SECRET) {
    return res.status(503).json({
      error: 'Stripe webhook is not configured',
      missing: {
        STRIPE_SECRET_KEY: !STRIPE_SECRET_KEY,
        STRIPE_WEBHOOK_SECRET: !STRIPE_WEBHOOK_SECRET
      }
    });
  }

  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('[stripe] webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  switch (event.type) {
    case 'checkout.session.completed':
    case 'customer.subscription.updated':
    case 'customer.subscription.deleted':
      console.log(`[stripe] received event: ${event.type}`);
      break;
    default:
      console.log(`[stripe] ignored event: ${event.type}`);
  }

  return res.json({ received: true });
});

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/api/health', (_req, res) => {
  res.json({ ok: true, service: 'werd', timestamp: new Date().toISOString() });
});

app.post('/api/stripe/create-checkout-session', async (req, res) => {
  if (!stripe) {
    return res.status(503).json({ error: 'STRIPE_SECRET_KEY is not configured' });
  }

  if (!WEALTHX_PUBLIC_BASE_URL) {
    return res.status(500).json({ error: 'WEALTHX_PUBLIC_BASE_URL is not configured' });
  }

  const { plan } = req.body || {};
  const planToPriceMap = {
    monthly: WEALTHX_STRIPE_MONTHLY_PRICE_ID,
    yearly: WEALTHX_STRIPE_YEARLY_PRICE_ID
  };

  const price = planToPriceMap[plan];

  if (!price) {
    return res.status(400).json({ error: 'Invalid plan. Use "monthly" or "yearly".' });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price, quantity: 1 }],
      success_url: `${WEALTHX_PUBLIC_BASE_URL}/?checkout=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${WEALTHX_PUBLIC_BASE_URL}/?checkout=cancelled`
    });

    return res.json({ url: session.url, id: session.id });
  } catch (err) {
    console.error('[stripe] checkout session creation failed:', err.message);
    return res.status(500).json({ error: 'Failed to create checkout session' });
  }
});

app.use(express.static(__dirname));

app.get('*', (_req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`WERD server listening on port ${PORT}`);
});
