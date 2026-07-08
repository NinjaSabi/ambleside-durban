// TEMPORARY one-shot — sets a password (confirm:true, no email) for a single
// account: kurtannall@gmail.com. Password supplied via x-temp-password header so
// it is never stored in the repo. Protected by secret + auto-expiry. DELETE after use.

const crypto = require("crypto");

const EXPIRES_AT = Date.parse("2026-07-09T00:00:00Z");
const SECRET = "s3tup2-b8d41f6a09e7c352-ambleside-kurt-once";
const TARGET_EMAIL = "kurtannall@gmail.com";

exports.handler = async (event, context) => {
  if (Date.now() > EXPIRES_AT) return { statusCode: 410, body: "Setup window closed." };

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

  // find existing
  let found = null;
  try {
    const listRes = await fetch(`${url}/admin/users`, { headers });
    const listJson = await listRes.json();
    found = (listJson.users || []).find(
      (u) => u.email && u.email.toLowerCase() === TARGET_EMAIL.toLowerCase()
    );
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: "list failed", detail: String(e) }) };
  }

  let action, status;
  try {
    let res;
    if (found) {
      res = await fetch(`${url}/admin/users/${found.id}`, {
        method: "PUT",
        headers,
        body: JSON.stringify({ password: tempPassword, confirm: true }),
      });
      action = "updated";
    } else {
      res = await fetch(`${url}/admin/users`, {
        method: "POST",
        headers,
        body: JSON.stringify({ email: TARGET_EMAIL, password: tempPassword, confirm: true }),
      });
      action = "created";
    }
    status = res.status;
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: "write failed", detail: String(e) }) };
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: TARGET_EMAIL, action, status, tempPassword }, null, 2),
  };
};
