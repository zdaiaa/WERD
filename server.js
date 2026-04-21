const path = require('path');
const express = require('express');
const Stripe = require('stripe');

const app = express();

const PORT = process.env.PORT || 3000;
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;

const stripe = STRIPE_SECRET_KEY ? new Stripe(STRIPE_SECRET_KEY) : null;

app.post('/api/stripe/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];

  if (stripe && STRIPE_WEBHOOK_SECRET) {
    try {
      const event = stripe.webhooks.constructEvent(req.body, sig, STRIPE_WEBHOOK_SECRET);
      console.log(`[stripe] verified webhook event: ${event.type}`);
    } catch (err) {
      console.error('[stripe] webhook signature verification failed:', err.message);
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }
  } else {
    try {
      const event = JSON.parse(req.body.toString('utf8'));
      console.log(`[stripe] received webhook event (unverified): ${event.type || 'unknown'}`);
    } catch {
      console.log('[stripe] received non-JSON webhook payload (unverified)');
    }
  }

  return res.json({ received: true });
});

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/api/health', (_req, res) => {
  res.json({ ok: true, service: 'werd', timestamp: new Date().toISOString() });
});

app.use(express.static(__dirname));

app.get('*', (_req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`WERD server listening on port ${PORT}`);
});
