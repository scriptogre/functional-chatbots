import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import { PNG } from 'pngjs';

const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
await p.goto('https://djangocon2024.christiantanul.com/', { waitUntil: 'networkidle' });
await p.click('#dark-mode-toggle');
await p.waitForTimeout(2000);

const decode = async (x, y) => {
  const buf = await p.screenshot({ clip: { x, y, width: 1, height: 1 } });
  return new Promise((resolve) => {
    new PNG().parse(buf, (err, png) => resolve([png.data[0], png.data[1], png.data[2], png.data[3]]));
  });
};
console.log('chat container area (600,350):', await decode(600, 350));
console.log('input area (600,575):       ', await decode(600, 575));
console.log('page bg (60,60):            ', await decode(60, 60));
console.log('typing indicator (565,440): ', await decode(565, 440));
// Try to force main to z-stack: add position: relative
await p.evaluate(() => { document.querySelector('main').style.position = 'relative'; document.querySelector('main').style.zIndex = '10'; });
await p.waitForTimeout(300);
console.log('---- after adding position: relative to <main> ----');
console.log('chat container area (600,350):', await decode(600, 350));
await b.close();
