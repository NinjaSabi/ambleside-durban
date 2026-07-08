// TEMPORARY one-shot — confirms + sets password (no email) for the two unconfirmed
// accounts so they can log in with the shared temp password. Password via
// x-temp-password header (never in repo). Secret + auto-expiry. DELETE after use.

const crypto = require("crypto");

const EXPIRES_AT = Date.parse("2026-07-09T00:00:00Z");
const SECRET = "s3tup3-4d19a7f2c60b8e35-ambleside-newtwo";
const TARGETS = ["Lizaender@gmail.com", "principal@amblesidedurban.com"];

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

  // index existing users by lowercased email
  let existing = {};
  try {
    const listRes = await fetch(`${url}/admin/users`, { headers });
    const listJson = await listRes.json();
    (listJson.users || []).forEach((u) => {
      if (u.email) existing[u.email.toLowerCase()] = u;
    });
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: "list failed", detail: String(e) }) };
  }

  const results = [];
  for (const email of TARGETS) {
    try {
      const found = existing[email.toLowerCase()];
      let res, action;
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
          body: JSON.stringify({ email, password: tempPassword, confirm: true }),
        });
        action = "created";
      }
      results.push({ email, action, status: res.status });
    } catch (e) {
      results.push({ email, action: "error", error: String(e) });
    }
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tempPassword, loginUrl: "https://amblesidedurban.com/admin/", results }, null, 2),
  };
};
