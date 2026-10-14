const { chromium } = require("C:/Users/arnau/Desktop/Marvel LCG/ui-check/node_modules/playwright");
const out = "C:/Users/arnau/Desktop/Marvel LCG/.tmb-captures/";
(async () => {
  const b = await chromium.launch({ channel: "chrome" });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  await p.goto("http://localhost:5199/?sandbox=patches");
  await p.waitForTimeout(1500);
  await p.getByText("Tantrum", { exact: true }).first().click();
  await p.getByText("Picket", { exact: true }).first().click();
  const all = (await p.getByRole("button").allInnerTexts()).map(t => t.replace(/\s+/g, " "));
  console.log(JSON.stringify(all.filter(t => t !== "Tester")));
  console.log((await p.innerText("body")).replace(/\s+/g, " ").slice(600, 1800));
  await p.screenshot({ path: out + "sb1.png", fullPage: true });
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
