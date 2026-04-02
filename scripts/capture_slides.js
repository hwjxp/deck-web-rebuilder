#!/usr/bin/env node
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

if (process.argv.length < 5) {
  console.error('Usage: capture_slides.js <url> <slide-count> <output-dir> [width] [height]');
  process.exit(1);
}

const [, , url, slideCountArg, outputDirArg, widthArg, heightArg] = process.argv;
const slideCount = Number(slideCountArg);
const width = Number(widthArg || 1600);
const height = Number(heightArg || 900);
const outputDir = resolve(outputDirArg);

mkdirSync(outputDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width, height } });
await page.emulateMedia({ reducedMotion: 'reduce' });

for (let index = 1; index <= slideCount; index += 1) {
  const slideId = `slide-${String(index).padStart(2, '0')}`;
  await page.goto(`${url}#${slideId}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(250);
  await page.screenshot({ path: join(outputDir, `${slideId}.png`), fullPage: false });
}

await browser.close();
