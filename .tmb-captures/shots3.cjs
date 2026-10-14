const { chromium } = require("C:/Users/arnau/Desktop/Marvel LCG/ui-check/node_modules/playwright");
const out = "C:/Users/arnau/Desktop/Marvel LCG/.tmb-captures/";
(async () => {
  const b = await chromium.launch({ channel: "chrome" });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  await p.goto("http://localhost:5199/");
  await p.waitForTimeout(1500);
  await p.getByRole("button", { name: /^Patches/ }).click();
  await p.getByRole("button", { name: /^Picket/ }).click();
  await p.getByRole("button", { name: "Commencer l'aventure" }).click();
  await p.waitForTimeout(2500);
  for (let i = 0; i < 30; i++) {
    const txt = (await p.innerText("body")).replace(/\s+/g, " ").slice(0, 260);
    const btns = (await p.getByRole("button").allInnerTexts()).map(t => t.replace(/\s+/g, " ")).filter(Boolean).slice(0, 12);
    console.log(i, "|", txt, "|", JSON.stringify(btns));
    await p.screenshot({ path: out + `step-${String(i).padStart(2, "0")}.png` });
    if (/COMBAT|INITIATIVE|Round|ROUND|Dés/i.test(txt) && i > 3) { console.log("COMBAT?"); }
    const tryClick = async (loc) => { if (await loc.count()) { await loc.first().click({ timeout: 3000 }).catch(() => {}); return true; } return false; };
    if (await tryClick(p.getByRole("button", { name: /Terminer l'entraînement|Terminer|Continuer|Suivant|Valider|Confirmer|Lancer|Combattre|Fuir|Commencer/ }))) {}
    else if (await tryClick(p.getByRole("button", { name: "Piocher la rencontre suivante" }))) {}
    else if (await tryClick(p.getByText("CLIQUEZ POUR CHOISIR"))) {}
    else await p.mouse.click(770, 135);
    await p.waitForTimeout(2200);
  }
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
