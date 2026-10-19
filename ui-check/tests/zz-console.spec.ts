import { test } from '@playwright/test';
test('console', async ({ page }) => {
  page.on('pageerror', (e) => console.log('PAGEERR', e.message.slice(0, 400)));
  page.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE', m.text().slice(0, 300)); });
  await page.goto('/app/board.html?phase=sur-table', { waitUntil: 'networkidle' });
  await page.waitForTimeout(4000);
  console.log('BTN', await page.locator('button:visible').count());
});
