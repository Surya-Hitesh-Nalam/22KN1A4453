import Url from "../models/Url.js";
import { Log } from '../Logging_Middleware/src/index.js';
import fetch from "node-fetch";
import {generateShortCode,validateUrl,Expiry} from "../utils/helpers.js";

function getClientIP(req) {
  let ip =
    req.headers["x-forwarded-for"] || req.connection?.remoteAddress || req.ip;
  if (ip.includes(",")) ip = ip.split(",")[0].trim();
  if (ip.startsWith("::ffff:")) ip = ip.substring(7);
  if (ip === "::1" || ip === "127.0.0.1") return "localhost";
  return ip || "unknown";
}

async function getCoarseLocation(ip) {
  if (!ip || ip === "127.0.0.1" || ip === "::1" || ip === "localhost")
    return "Localhost";

  try {
    const res = await fetch(`https://ipapi.co/${ip}/json/`, { timeout: 1000 });
    if (!res.ok) return "Unknown";

    const data = await res.json();
    return (
      [data.city, data.country_name].filter(Boolean).join(", ") || "Unknown"
    );
  } catch {
    return "Unknown";
  }
}

export class UrlController {
    async crateShortUrl(req, res) {
        const {url,validity=30,shortCode} = req.body;

        if(!url){
            Log('backend', 'error', 'controller', `URL is required`);
            return res.status(400).json({sucess,error: 'URL is required'});
        }
         if (!validateUrl(url)) {
      Log('backend', 'warn', 'controller', 'Invalid URL format');
      return res.status(400).json({ success: false, error: 'Invalid URL format' });
    }
     const existingUrl = await Url.findOne({ originalUrl: url, expiresAt: { $gt: new Date() } });
    if (existingUrl) {
      Log('backend', 'info', 'controller', `Returning existing short URL for ${url}`);
      return res.status(200).json({
        success: true,
        data: {
          shortLink: existingUrl.shortUrl,
          expiry: existingUrl.expiresAt.toISOString()
        }
      });
    }
    let code;
    try {
      code = generateShortCode(shortcode);
    } catch (e) {
      Log('backend', 'warn', 'controller', `Invalid shortcode format: ${e.message}`);
      return res.status(400).json({ success: false, error: 'Invalid shortcode format' });
    }
    let attempts = 0;
    const maxAttempts = 5;
    while (attempts < maxAttempts) {
      const found = await Url.findOne({ shortCode: code });
      if (!found) break;
      if (shortCode) {
        Log('backend', 'warn', 'controller', 'Custom shortcode collision');
        return res.status(409).json({ success: false, error: 'Custom shortcode already exists' });
      }
      code = generateShortCode();
      attempts++;
    }
    if (attempts >= maxAttempts) {
      Log('backend', 'error', 'controller', 'Failed to generate unique shortcode');
      return res.status(500).json({ success: false, error: 'Failed to generate unique shortcode' });
    }

    const expiresAt = Expiry(Number(validity));
    const shortUrl = `${req.protocol}://${req.get('host')}/${code}`;

    const newUrl = new Url({
      originalUrl: url,
      shortCode: code,
      shortUrl,
      validityPeriod: Number(validity),
      expiresAt,
      analytics: {
        totalClicks: 0,
        clickDetails: []
      }
    });

    await newUrl.save();

    Log('backend', 'info', 'controller', `Short URL created: ${shortUrl}`);
    return res.status(201).json({
      success: true,
      data: {
        shortLink: shortUrl,
        expiry: expiresAt.toISOString()
      }
    });
  }
  async getUrlStats(req, res) {
    const { shortId } = req.params;
    Log('backend', 'info', 'controller', `getUrlStats for ${shortId}`);

    const urlEntry = await Url.findOne({ shortCode: shortId });
    if (!urlEntry) {
      Log('backend', 'warn', 'controller', 'Statistics requested for nonexistent shortcode');
      return res.status(404).json({ success: false, error: 'Short URL not found' });
    }
    if (urlEntry.expiresAt < new Date()) {
      Log('backend', 'warn', 'controller', 'Statistics requested for expired shortcode');
      return res.status(410).json({ success: false, error: 'Short URL has expired' });
    }

    res.status(200).json({
      success: true,
      data: {
        originalUrl: urlEntry.originalUrl,
        shortUrl: urlEntry.shortUrl,
        createdAt: urlEntry.createdAt,
        expiresAt: urlEntry.expiresAt,
        totalClicks: urlEntry.analytics.totalClicks,
        clickDetails: urlEntry.analytics.clickDetails
      }
    });
  }
   async redirectToOriginal(req, res) {
    const { shortId } = req.params;
    Log('backend', 'info', 'controller', `Redirect request for ${shortId}`);

    const urlEntry = await Url.findOne({ shortCode: shortId });
    if (!urlEntry) {
      Log('backend', 'warn', 'controller', 'Redirect requested for nonexistent shortcode');
      return res.status(404).json({ success: false, error: 'Short URL not found' });
    }
    if (urlEntry.expiresAt < new Date()) {
      Log('backend', 'warn', 'controller', 'Redirect requested for expired shortcode');
      return res.status(410).json({ success: false, error: 'Short URL has expired' });
    }

    const ip = getClientIP(req);
    const userAgent = req.get('User-Agent');
    const referer = req.get('Referer') || 'direct';

    let location = 'Unknown';
    try {
      location = await getCoarseLocation(ip);
    } catch {
    }

    urlEntry.analytics.totalClicks++;
    urlEntry.analytics.clickDetails.push({
      timestamp: new Date(),
      ip,
      userAgent,
      referer,
      location
    });

    await urlEntry.save();

    Log('backend', 'info', 'controller', `Redirecting to ${urlEntry.originalUrl}`);
    res.redirect(urlEntry.originalUrl);
  }
}

