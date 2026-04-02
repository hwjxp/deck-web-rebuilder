#!/usr/bin/env node
import { chromium } from 'playwright';
import { dirname, resolve } from 'node:path';
import { mkdirSync } from 'node:fs';

if (process.argv.length < 5) {
  console.error('Usage: render_preview.js <url> <slide-id> <output.png> [width] [height]');
  process.exit(1);
}

const [, , url, slideId, outputPath, widthArg, heightArg] = process.argv;
const width = Number(widthArg || 1600);
const height = Number(heightArg || 900);

mkdirSync(dirname(resolve(outputPath)), { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width, height } });
await page.emulateMedia({ reducedMotion: 'reduce' });
await page.goto(`${url}#${slideId}`, { waitUntil: 'networkidle' });
await page.waitForTimeout(250);
await page.screenshot({ path: resolve(outputPath), fullPage: false });
await browser.close();
