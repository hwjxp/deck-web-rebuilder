#!/usr/bin/env node
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

if (process.argv.length < 5) {
  console.error('Usage: capture_slides.js <url> <slide-count> <output-dir> [width] [height] [lang]');
  process.exit(1);
}

const [, , url, slideCountArg, outputDirArg, widthArg, heightArg, langArg] = process.argv;
const slideCount = Number(slideCountArg);
const width = Number(widthArg || 1600);
const height = Number(heightArg || 900);
const lang = langArg || 'zh';
const outputDir = resolve(outputDirArg);

mkdirSync(outputDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width, height } });
await page.emulateMedia({ reducedMotion: 'reduce' });
await page.goto(`${url}${url.includes('?') ? '&' : '?'}lang=${lang}`, { waitUntil: 'networkidle' });
await page.waitForFunction(() => !!window.presentation);

for (let index = 1; index <= slideCount; index += 1) {
  const slideId = `slide-${String(index).padStart(2, '0')}`;
  await page.evaluate((targetIndex, targetLang) => {
    if (window.presentation?.setLanguage) {
      window.presentation.setLanguage(targetLang);
    }
    if (window.presentation?.goToSlide) {
      window.presentation.goToSlide(targetIndex - 1);
    } else {
      window.location.hash = `#slide-${String(targetIndex).padStart(2, '0')}`;
    }
  }, index, lang);
  await page.waitForTimeout(250);
  await page.screenshot({ path: join(outputDir, `${slideId}-${lang}.png`), fullPage: false });
}

await browser.close();
