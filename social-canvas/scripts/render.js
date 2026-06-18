#!/usr/bin/env node
/**
 * render.js — Playwright HTML→PNG renderer for social-canvas skill (the agent runtime).
 *
 * Uses playwright-core with the container's bundled Chromium.
 * Renders a local HTML file to a PNG at exact pixel dimensions.
 *
 * Forces deviceScaleFactor=1 to prevent 2x output.
 * Waits for font loading (waitUntil: 'networkidle' + document.fonts.ready)
 * so Google Fonts @imports finish before screenshot.
 *
 * Usage:
 *   node render.js input.html output.png --width 1080 --height 1350
 */

const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: node render.js input.html output.png --width W --height H');
    process.exit(1);
  }

  const inputHtml = args[0];
  const outputPng = args[1];
  let width = 1080;
  let height = 1350;

  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--width' && args[i + 1]) width = parseInt(args[i + 1], 10);
    if (args[i] === '--height' && args[i + 1]) height = parseInt(args[i + 1], 10);
  }

  if (!fs.existsSync(inputHtml)) {
    console.error(`Error: Input file not found: ${inputHtml}`);
    process.exit(1);
  }

  const outputDir = path.dirname(outputPng);
  if (outputDir && outputDir !== '.') {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // The container's Playwright cache may be a different version than the
  // playwright-core module expects (e.g. cache has chromium-1208 but module
  // looks for chromium-1217). Walk the cache and pick the newest available
  // chrome-headless-shell, then chrome. Falls back to default discovery if
  // nothing is found (e.g. on a Mac developer machine).
  function findChromium() {
    const cache = '~/.cache/ms-playwright';
    if (!fs.existsSync(cache)) return null;
    const dirs = fs.readdirSync(cache).filter(d => d.startsWith('chromium'));
    const headlessDirs = dirs.filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse();
    const fullDirs = dirs.filter(d => d.startsWith('chromium-')).sort().reverse();
    for (const d of headlessDirs) {
      const p = path.join(cache, d, 'chrome-headless-shell-linux64', 'chrome-headless-shell');
      if (fs.existsSync(p)) return p;
    }
    for (const d of fullDirs) {
      const p = path.join(cache, d, 'chrome-linux64', 'chrome');
      if (fs.existsSync(p)) return p;
    }
    return null;
  }
  const launchOpts = {
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--font-render-hinting=none',
      '--disable-font-subpixel-positioning',
    ],
  };
  const detected = findChromium();
  if (detected) {
    launchOpts.executablePath = detected;
  }
  const browser = await chromium.launch(launchOpts);

  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
  });

  const page = await context.newPage();
  const fileUrl = `file://${path.resolve(inputHtml)}`;
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  await page.screenshot({ path: outputPng, fullPage: false });
  await browser.close();

  console.log(`OK: ${outputPng} (${width}x${height})`);
}

main().catch(err => {
  console.error('Render error:', err.message);
  process.exit(1);
});
