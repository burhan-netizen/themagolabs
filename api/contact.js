// Contact form handler for themagolabs.com
// Sends two emails through Resend:
//   1. the enquiry, to burhan@themagolabs.com (an alias of burhan@magolabs.in)
//   2. a short thank-you to the visitor, only when they gave an email address
// Needs one Vercel environment variable: RESEND_API_KEY

const TO = 'burhan@themagolabs.com';
const FROM_FORM = 'the Mago Labs website <forms@themagolabs.com>';
const FROM_BURHAN = 'Burhan, the Mago Labs <burhan@themagolabs.com>';
const WHATSAPP = '+91 90992 45605';
const WHATSAPP_LINK = 'https://wa.me/919099245605';

const ALLOWED_ORIGINS = [/^https:\/\/(www\.)?themagolabs\.com$/, /^https:\/\/[a-z0-9-]+\.vercel\.app$/];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const clean = (v, max) => String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const oneLine = (s) => s.replace(/[\r\n]+/g, ' ');

// The site has three form styles that post slightly different field names. Normalise them here.
function normalise(b) {
  const contact = clean(b.contact || b.reach || '', 200);
  const email = clean(b.email || '', 200) || (EMAIL_RE.test(contact) ? contact : '');
  const phone = clean(b.phone || '', 60) || (contact && !EMAIL_RE.test(contact) ? contact : '');
  const has = clean(b.has_website || b.has_site || '', 5).toLowerCase();
  return {
    name: clean(b.name, 120),
    business: clean(b.business, 160),
    website: clean(b.website, 300),
    hasWebsite: has === 'no' ? 'no' : 'yes',
    wantsMore: clean(b.wants_more || b.goals || '', 200),
    email,
    phone,
    message: clean(b.message, 4000),
    page: clean(b.page, 200),
    trap: clean(b.company_site || '', 200),
  };
}

async function send(payload) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error('Resend ' + r.status + ': ' + (await r.text()).slice(0, 300));
}

function enquiryEmail(d) {
  const rows = [
    ['Name', d.name],
    ['Business', d.business],
    ['Website', d.hasWebsite === 'no' ? 'Not yet' : d.website || 'Yes (no address given)'],
    ['Wants more', d.wantsMore],
    ['Email', d.email],
    ['Phone / WhatsApp', d.phone],
    ['Page', d.page],
  ].filter((r) => r[1]);
  const table = rows
    .map((r) => `<tr><td style="padding:8px 16px 8px 0;color:#6E6C66;font:12px/1.4 monospace;text-transform:uppercase;letter-spacing:.04em;vertical-align:top;white-space:nowrap">${esc(r[0])}</td><td style="padding:8px 0;color:#111110;font:15px/1.5 Arial,sans-serif">${esc(r[1])}</td></tr>`)
    .join('');
  const msg = d.message ? `<p style="margin:24px 0 0;padding:16px;background:#E5E3DD;border-radius:12px;color:#111110;font:15px/1.6 Arial,sans-serif;white-space:pre-wrap">${esc(d.message)}</p>` : '';
  const html = `<div style="background:#F2F1EC;padding:32px"><div style="max-width:560px;margin:0 auto;background:#fff;border-radius:16px;padding:28px">
<p style="margin:0 0 4px;color:#6E6C66;font:12px monospace;text-transform:uppercase;letter-spacing:.06em">New enquiry · themagolabs.com</p>
<h1 style="margin:0 0 20px;color:#111110;font:500 22px/1.3 Arial,sans-serif">${esc(d.business || d.name || 'Website enquiry')}</h1>
<table style="border-collapse:collapse">${table}</table>${msg}
<p style="margin:24px 0 0;color:#6E6C66;font:13px/1.5 Arial,sans-serif">${d.email ? 'Hit reply to answer them directly.' : 'They left a phone number, not an email. Call or WhatsApp them.'}</p>
</div></div>`;
  const text = rows.map((r) => r[0] + ': ' + r[1]).join('\n') + (d.message ? '\n\n' + d.message : '');
  const subject = oneLine('New enquiry: ' + (d.business || d.name || 'website') + (d.hasWebsite === 'no' ? ' (no website yet)' : ''));
  return { from: FROM_FORM, to: [TO], subject, html, text, ...(d.email ? { reply_to: d.email } : {}) };
}

function thankYouEmail(d) {
  const first = (d.name.split(/\s+/)[0] || 'there');
  const forBiz = d.business ? ` for ${d.business}` : '';
  const next = d.hasWebsite === 'no'
    ? 'I will look into your business and come back with ideas for your new website.'
    : `I will take a look at ${d.website || 'your current website'} before I get back to you, so we can talk about what is costing you enquiries.`;
  const lines = [
    `Hi ${first},`,
    `Thanks for reaching out to the Mago Labs. Your enquiry${forBiz} is with me now, and I will reply within one business day.`,
    next,
    `If it is urgent, message me on WhatsApp: ${WHATSAPP}.`,
  ];
  const html = `<div style="background:#F2F1EC;padding:32px"><div style="max-width:520px;margin:0 auto;background:#fff;border-radius:16px;padding:28px;color:#111110;font:16px/1.6 Arial,sans-serif">
${lines.map((l, i) => `<p style="margin:0 0 16px">${i === 3 ? `If it is urgent, message me on <a href="${WHATSAPP_LINK}" style="color:#111110">WhatsApp: ${WHATSAPP}</a>.` : esc(l)}</p>`).join('')}
<p style="margin:24px 0 0">Burhan Kapasi<br><span style="color:#6E6C66"><i style="font-family:Georgia,serif">the</i> Mago Labs · <a href="https://themagolabs.com" style="color:#6E6C66">themagolabs.com</a></span></p>
</div></div>`;
  const text = lines.join('\n\n') + '\n\nBurhan Kapasi\nthe Mago Labs · themagolabs.com';
  return { from: FROM_BURHAN, to: [d.email], reply_to: TO, subject: oneLine(`Thanks, ${first}. We've got your message`), html, text };
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ ok: false }); }
  const origin = req.headers.origin || '';
  if (!ALLOWED_ORIGINS.some((re) => re.test(origin))) return res.status(403).json({ ok: false });
  if (!process.env.RESEND_API_KEY) { console.error('RESEND_API_KEY is not set'); return res.status(500).json({ ok: false }); }

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ ok: false });

  const d = normalise(body);
  if (d.trap) return res.status(200).json({ ok: true }); // bot filled the hidden field: pretend it worked
  if (!d.name || (!d.email && !d.phone)) return res.status(400).json({ ok: false });

  try {
    await send(enquiryEmail(d));
  } catch (e) {
    console.error(e);
    return res.status(502).json({ ok: false }); // the site falls back to WhatsApp
  }
  if (d.email) {
    try { await send(thankYouEmail(d)); } catch (e) { console.error('Thank-you email failed', e); }
  }
  return res.status(200).json({ ok: true });
};
