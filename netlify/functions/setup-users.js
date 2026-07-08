// TEMPORARY one-shot setup function — creates/updates CMS users with a password
// and confirm:true, so NO invite email is sent (bypasses the Identity email rate limit).
// Protected by a shared secret and an auto-expiry. DELETE THIS FILE right after use.

const crypto = require("crypto");

// Auto-disable after this instant regardless of anything else (defence in depth).
const EXPIRES_AT = Date.parse("2026-07-09T00:00:00Z");

// Shared secret required as ?secret=... — long and random. Rotate/remove after use.
const SECRET = "s3tup-9f2a7c14e8b04d6fa1c3-ambleside-onceoff";

const EMAILS = [
  "amblesidedurban@gmail.com",
  "jomason80@gmail.com",
  "director@amblesidedurban.com",
  "admin@amblesidedurban.com",
  "csft17@gmail.com",
];

exports.handler = async (event, context) => {
  if (Date.now() > EXPIRES_AT) {
    return { statusCode: 410, body: "Setup window closed." };
  }

  const provided =
    (event.queryStringParameters && event.queryStringParameters.secret) ||
    event.headers["x-setup-secret"];
  if (provided !== SECRET) {
    return { statusCode: 401, body: "Unauthorized." };
  }

  const identity = context.clientContext && context.clientContext.identity;
  if (!identity || !identity.url || !identity.token) {
    return {
      statusCode: 500,
      body: JSON.stringify({
        error:
          "No Identity admin context. Is Identity enabled on this site?",
      }),
    };
  }

  const { url, token } = identity;
  const headers = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };

  // One shared temp password for the workshop, generated fresh at runtime
  // (never stored in the repo). Everyone changes it later via "forgot password".
  const tempPassword = "Amb-" + crypto.randomBytes(6).toString("hex");

  // Map existing users by email so we update rather than error on duplicates.
  let existing = {};
  try {
    const listRes = await fetch(`${url}/admin/users`, { headers });
    const listJson = await listRes.json();
    (listJson.users || []).forEach((u) => {
      if (u.email) existing[u.email.toLowerCase()] = u;
    });
  } catch (e) {
    return {
      statusCode: 502,
      body: JSON.stringify({ error: "Could not list users", detail: String(e) }),
    };
  }

  const results = [];
  for (const email of EMAILS) {
    try {
      const found = existing[email.toLowerCase()];
      let res;
      if (found) {
        res = await fetch(`${url}/admin/users/${found.id}`, {
          method: "PUT",
          headers,
          body: JSON.stringify({ password: tempPassword, confirm: true }),
        });
        results.push({ email, action: "updated", status: res.status });
      } else {
        res = await fetch(`${url}/admin/users`, {
          method: "POST",
          headers,
          body: JSON.stringify({ email, password: tempPassword, confirm: true }),
        });
        results.push({ email, action: "created", status: res.status });
      }
    } catch (e) {
      results.push({ email, action: "error", error: String(e) });
    }
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(
      {
        tempPassword,
        loginUrl: "https://amblesidedurban.com/admin/",
        note: "Share tempPassword with the five users. They log in at loginUrl with their email + this password. Change later via Forgot password once email works.",
        results,
      },
      null,
      2
    ),
  };
};
