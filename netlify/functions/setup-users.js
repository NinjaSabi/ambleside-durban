// TEMPORARY one-shot — force EVERY current Identity user to confirmed + shared
// temp password (no email). Fixes any account stuck as "Email not confirmed".
// Password via x-temp-password header. Secret + auto-expiry. DELETE after use.

const crypto = require("crypto");

const EXPIRES_AT = Date.parse("2026-07-09T00:00:00Z");
const SECRET = "s3tup4-e71c9a3f28d0b64a-ambleside-confirmall";

exports.handler = async (event, context) => {
  if (Date.now() > EXPIRES_AT) return { statusCode: 410, body: "closed" };

  const provided =
    (event.queryStringParameters && event.queryStringParameters.secret) ||
    event.headers["x-setup-secret"];
  if (provided !== SECRET) return { statusCode: 401, body: "Unauthorized." };

  const identity = context.clientContext && context.clientContext.identity;
  if (!identity || !identity.url || !identity.token) {
    return { statusCode: 500, body: JSON.stringify({ error: "No Identity admin context." }) };
  }
  const { url, token } = identity;
  const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
  const tempPassword = event.headers["x-temp-password"] || "Amb-" + crypto.randomBytes(6).toString("hex");

  let users = [];
  try {
    const listRes = await fetch(`${url}/admin/users`, { headers });
    const listJson = await listRes.json();
    users = listJson.users || [];
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: "list failed", detail: String(e) }) };
  }

  const results = [];
  for (const u of users) {
    try {
      const res = await fetch(`${url}/admin/users/${u.id}`, {
        method: "PUT",
        headers,
        body: JSON.stringify({ password: tempPassword, confirm: true }),
      });
      results.push({ email: u.email, was_confirmed: !!u.confirmed_at, status: res.status });
    } catch (e) {
      results.push({ email: u.email, error: String(e) });
    }
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tempPassword, count: results.length, results }, null, 2),
  };
};
