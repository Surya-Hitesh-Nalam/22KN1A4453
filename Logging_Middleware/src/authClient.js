import fetch from 'node-fetch';

const AUTH_URL = process.env.AUTH_URL;
let cachedToken = null;
let expiryTime = 0;

export async function getAuthToken() {
    const now = Date.now();
    if (cachedToken && now < expiryTime) return cachedToken;
    const payload = {
    email: process.env.EMAIL,
    name: process.env.NAME,
    rollNo: process.env.ROLL_NO,
    accessCode: process.env.ACCESS_CODE,
    clientID: process.env.CLIENT_ID,
    clientSecret: process.env.CLIENT_SECRET
  };
  const res = await fetch(AUTH_URL, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(`Auth failed`);
  }
  const { access_token, expires_in } = await res.json();
  cachedToken = access_token;
  expiryTimestamp = now + (expires_in - 60) * 1000;
  return cachedToken;
}
