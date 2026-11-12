import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/FounderGate/);
});

test('navigate to new analysis', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Start New Analysis');
  await expect(page).toHaveURL(/.*\/analysis\/new/);
  await expect(page.locator('h1').first()).toContainText('New Analysis');
});

test('navigate to analysis view', async ({ page }) => {
  await page.goto('/analysis');
  await expect(page.locator('h2').first()).toContainText('Source Evidence');
});

test('navigate to report view', async ({ page }) => {
  await page.goto('/report');
  await expect(page.locator('h1').first()).toContainText('Strategic Decision Record');
});
