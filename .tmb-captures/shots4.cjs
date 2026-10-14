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
  let last = "";
  for (let i = 0; i < 40; i++) {
    const txt = (await p.innerText("body")).replace(/\s+/g, " ");
    const sig = txt.slice(0, 200);
    const btns = (await p.getByRole("button").allInnerTexts()).map(t => t.replace(/\s+/g, " ")).filter(Boolean).slice(0, 10);
    console.log(i, "|", txt.slice(70, 230), "|", JSON.stringify(btns));
    if (sig !== last) await p.screenshot({ path: out + `s${String(i).padStart(2, "0")}.png` });
    last = sig;
    const has = async (loc) => (await loc.count()) > 0;
    if (/Loot — choisissez/.test(txt)) {
      await p.getByRole("button", { name: /Infused Incense/ }).click().catch(() => {});
      await p.getByRole("button", { name: "patches" }).click().catch(() => {});
      await p.getByRole("button", { name: "Garder" }).click().catch(() => {});
    } else if (await has(p.getByRole("button", { name: "Terminer l'entraînement" }))) {
      await p.getByRole("button", { name: "Terminer l'entraînement" }).click();
    } else if (await has(p.getByRole("button", { name: "Piocher la rencontre suivante" }))) {
      await p.getByRole("button", { name: "Piocher la rencontre suivante" }).click();
    } else if (/CLIQUEZ POUR CHOISIR/.test(txt)) {
      await p.getByText("CLIQUEZ POUR CHOISIR").first().click();
    } else if (/Clique ta décision sur la carte/.test(txt)) {
      await p.mouse.click(770, 135);
    } else { console.log("ETAT INCONNU"); if (i > 2) { await p.waitForTimeout(2500); } }
    await p.waitForTimeout(2200);
  }
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
