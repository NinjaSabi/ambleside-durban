// TEMPORARY read-only — lists current Identity users so we send recovery
// emails to the exact right addresses. No writes. Secret + auto-expiry. DELETE after use.

const EXPIRES_AT = Date.parse("2026-07-09T00:00:00Z");
const SECRET = "lst-3a9f22c7e18b04d6-ambleside-list";

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
  const headers = { Authorization: `Bearer ${identity.token}` };

  try {
    const res = await fetch(`${identity.url}/admin/users`, { headers });
    const json = await res.json();
    const users = (json.users || []).map((u) => ({
      email: u.email,
      confirmed: !!u.confirmed_at,
      created_at: u.created_at,
    }));
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ count: users.length, users }, null, 2),
    };
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: String(e) }) };
  }
};
