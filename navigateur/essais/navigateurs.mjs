// Parcours du mode navigateur dans Chromium / Firefox / WebKit (Playwright), bureau ou mobile 390x844.
// Usage : node navigateur/essais/navigateurs.mjs <chromium|firefox|webkit> [mobile|bureau] [etape] [url]
//   etape : "charge" (page + moteur prets) ou "partie" (par defaut : jusqu'a un tour joue)
// Serveur attendu : python3 navigateur/serveur-local.py 8770   (voir navigateur/construire.py)
// Playwright est pris dans ui-check/node_modules (variable PLAYWRIGHT_DIR pour le changer).
import { createRequire } from "module";
import path from "path";
import { fileURLToPath } from "url";
const ICI = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(process.env.PLAYWRIGHT_DIR || path.join(ICI, "../../ui-check/") );
const pw = require("playwright-core");
const nav = process.argv[2] || "chromium";
const mobile = process.argv[3] === "mobile";
const etape = process.argv[4] || "partie";
const URL_ = process.argv[5] || "http://localhost:8770/navigateur.html";
const OUT = path.join(ICI, "captures") + "/";
const tag = nav + (mobile ? "-mobile" : "");
const log = (...a) => console.log(`[${tag}]`, ...a);
// WebKit Playwright (build WPE, Linux) : sans cette variable, le processus de rendu s'ABORTE (« Could not negotiate a
// suitable buffer format ») des qu'une page affiche 5 images ou plus (voir docs/rapports/play-webkit-plantage-2026-10-20.md).
// Defaut du banc : atlas DMA-BUF coupe. Pour reproduire le plantage : WEBKIT_DISABLE_DMABUF_ATLAS=0 node ... webkit
const b = await pw[nav].launch(nav === "webkit" ? { env: { ...process.env, WEBKIT_DISABLE_DMABUF_ATLAS: process.env.WEBKIT_DISABLE_DMABUF_ATLAS ?? "1" } } : {});
const ctx = await b.newContext(mobile
  ? { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: nav !== "firefox", deviceScaleFactor: 2 }
  : { viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
const erreurs = [];
page.on("console", (m) => { if (m.type() === "error") erreurs.push("console: " + m.text().slice(0, 300)); });
page.on("pageerror", (e) => erreurs.push("pageerror: " + String(e).slice(0, 300)));
page.on("requestfailed", (r) => erreurs.push("requestfailed: " + r.url().slice(0, 150) + " " + (r.failure()?.errorText || "")));
page.on("response", (r) => { if (r.status() >= 400) erreurs.push("http " + r.status() + " " + r.url().slice(0, 150)); });
const res = { navigateur: tag };
const t0 = Date.now();
await page.goto(URL_);
res.isole = await page.evaluate(() => self.crossOriginIsolated);
res.sab = await page.evaluate(() => typeof SharedArrayBuffer);
// Telephone : panneau d'avertissement a passer
if (mobile) {
  const bt = page.getByRole("button", { name: /Continuer quand meme|Continue anyway/ });
  try { await bt.waitFor({ timeout: 5000 }); res.avertissement_mobile = true; await page.screenshot({ path: OUT + tag + "-0-avertissement.png" }); await bt.click(); } catch (e) { res.avertissement_mobile = false; }
}
try {
  await page.waitForFunction(() => window.__pret === true, null, { timeout: 420000 });
  res.moteur_pret_s = (Date.now() - t0) / 1000;
} catch (e) {
  res.moteur_pret_s = "ECHEC";
  res.splash = await page.evaluate(() => document.body.innerText.slice(0, 400));
}
await page.screenshot({ path: OUT + tag + "-1-chargement.png" });
if (etape !== "charge" && res.moteur_pret_s !== "ECHEC") {
  try { await (await import("./parcours.mjs")).jouer({ page, tag, OUT, res, log, mobile }); }
  catch (e) { res.parcours_echec = String(e).slice(0, 1500); try { await page.screenshot({ path: OUT + tag + "-9-echec.png", timeout: 20000 }); } catch (e2) { res.capture_echec = String(e2).slice(0, 200); } }
}
res.erreurs = erreurs.slice(0, 15);
log(JSON.stringify(res, null, 1));
await b.close();
