// Rendile Travels: tiny server step in front of the static site.
//
//   POST /api/enquiry   contact / reservation form
//   POST /api/subscribe newsletter signup
//
// Each submission is
//   1. saved in Dira (Supabase `customers` table) as a new lead, and
//   2. emailed to the team via Resend.
// Either one working is enough to accept the submission. Everything else
// (pages, CSS, images, video) is served straight from the built site.
//
// Secrets (set once, never committed):
//   npx wrangler secret put SUPABASE_SECRET_KEY   Supabase secret key (sb_secret_...)
//   npx wrangler secret put RESEND_API_KEY        Resend API key (re_...)
// Plain settings live in wrangler.jsonc "vars".

const MAX = { name: 120, email: 200, phone: 60, trip: 200, when: 120, party: 80, interest: 400, message: 4000 };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/enquiry' || url.pathname === '/api/subscribe') {
      if (request.method !== 'POST') return json({ ok: false, error: 'method' }, 405);
      try {
        return url.pathname === '/api/enquiry'
          ? await handleEnquiry(request, env)
          : await handleSubscribe(request, env);
      } catch (err) {
        console.error('form error', err && err.stack ? err.stack : err);
        return json({ ok: false, error: 'server' }, 500);
      }
    }
    return env.ASSETS.fetch(request);
  },
};

async function readForm(request) {
  const type = request.headers.get('content-type') || '';
  if (type.includes('application/json')) {
    const data = await request.json();
    const out = {};
    for (const [k, v] of Object.entries(data || {})) out[k] = Array.isArray(v) ? v.map(String) : String(v ?? '');
    return out;
  }
  const fd = await request.formData();
  const out = {};
  for (const [k, v] of fd.entries()) {
    if (typeof v !== 'string') continue;
    if (k in out) out[k] = [].concat(out[k], v);
    else out[k] = v;
  }
  return out;
}

const clean = (v, n) => String(Array.isArray(v) ? v.join(', ') : v || '').replace(/\s+/g, ' ').trim().slice(0, n);
const cleanText = (v, n) => String(v || '').replace(/\r/g, '').trim().slice(0, n);
const validEmail = (e) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e);

async function handleEnquiry(request, env) {
  const f = await readForm(request);
  // Honeypot: real people never fill this hidden field. Pretend success for bots.
  if (clean(f['bot-field'], 10)) return json({ ok: true });

  const d = {
    name: clean(f.name, MAX.name),
    email: clean(f.email, MAX.email).toLowerCase(),
    phone: clean(f.phone, MAX.phone),
    trip: clean(f.trip, MAX.trip),
    when: clean(f.when, MAX.when),
    party: clean(f.party, MAX.party),
    interest: clean(f.interest, MAX.interest),
    message: cleanText(f.message, MAX.message),
    page: clean(f.page || request.headers.get('referer'), 300),
  };
  if (!d.name || !validEmail(d.email)) return json({ ok: false, error: 'invalid' }, 400);

  const lines = [
    ['Trip of interest', d.trip],
    ['When', d.when],
    ["Who's travelling", d.party],
    ['Interested in', d.interest],
    ['Phone', d.phone],
    ['Message', d.message],
    ['Sent from', d.page],
  ].filter(([, v]) => v);
  const summary = lines.map(([k, v]) => `${k}: ${v}`).join('\n');

  const results = await Promise.allSettled([
    saveToDira(env, {
      name: d.name,
      email: d.email,
      phone: d.phone,
      source: 'Website enquiry',
      status: 'enquiry',
      notes: `Website enquiry, ${new Date().toISOString().slice(0, 10)}\n${summary}`,
    }),
    sendEmail(env, {
      subject: `New enquiry: ${d.name}${d.trip ? `, ${d.trip}` : ''}`,
      replyTo: d.email,
      text: `New website enquiry\n\nName: ${d.name}\nEmail: ${d.email}\n${summary}\n\nReply to this email to answer ${d.name.split(' ')[0]} directly.\nThis enquiry has also been added to Dira as a new customer.`,
    }),
  ]);
  return finish(results);
}

async function handleSubscribe(request, env) {
  const f = await readForm(request);
  if (clean(f['bot-field'], 10)) return json({ ok: true });
  const email = clean(f.email, MAX.email).toLowerCase();
  if (!validEmail(email)) return json({ ok: false, error: 'invalid' }, 400);
  const results = await Promise.allSettled([
    saveToDira(env, {
      name: email,
      email,
      source: 'Newsletter signup',
      status: 'lead',
      notes: `Signed up for travel notes on the website, ${new Date().toISOString().slice(0, 10)}`,
    }),
    sendEmail(env, {
      subject: `New newsletter signup: ${email}`,
      replyTo: email,
      text: `${email} signed up for travel notes on rendiletravels.com.\nThey have also been added to Dira as a new lead.`,
    }),
  ]);
  return finish(results);
}

function finish(results) {
  const ok = results.filter((r) => r.status === 'fulfilled' && r.value === true).length;
  results.forEach((r, i) => {
    if (r.status === 'rejected') console.error(i === 0 ? 'dira' : 'email', String(r.reason));
  });
  return ok > 0 ? json({ ok: true, saved: ok }) : json({ ok: false, error: 'delivery' }, 502);
}

// Insert a row into Dira's customers table. Returns true on success,
// false if not configured, throws on a real failure.
async function saveToDira(env, row) {
  if (!env.SUPABASE_URL || !env.SUPABASE_SECRET_KEY) return false;
  const res = await fetch(`${env.SUPABASE_URL}/rest/v1/customers`, {
    method: 'POST',
    headers: {
      apikey: env.SUPABASE_SECRET_KEY,
      'Content-Type': 'application/json',
      Prefer: 'return=minimal',
    },
    body: JSON.stringify(row),
  });
  if (!res.ok) throw new Error(`supabase ${res.status}: ${(await res.text()).slice(0, 300)}`);
  return true;
}

// Send a notification email through Resend. Same return contract as above.
async function sendEmail(env, { subject, text, replyTo }) {
  if (!env.RESEND_API_KEY || !env.NOTIFY_TO) return false;
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.NOTIFY_FROM || 'Rendile Travels website <onboarding@resend.dev>',
      to: String(env.NOTIFY_TO).split(',').map((s) => s.trim()).filter(Boolean),
      reply_to: replyTo,
      subject,
      text,
    }),
  });
  if (!res.ok) throw new Error(`resend ${res.status}: ${(await res.text()).slice(0, 300)}`);
  return true;
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  });
}
