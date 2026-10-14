const { chromium } = require("C:/Users/arnau/Desktop/Marvel LCG/ui-check/node_modules/playwright");
const out = "C:/Users/arnau/Desktop/Marvel LCG/.tmb-captures/";
(async () => {
  const b = await chromium.launch({ channel: "chrome" });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  await p.goto("http://localhost:5199/?sandbox=patches");
  await p.waitForTimeout(2000);
  await p.screenshot({ path: out + "sb0.png" });
  console.log((await p.innerText("body")).replace(/\s+/g, " ").slice(0, 600));
  console.log(JSON.stringify((await p.getByRole("button").allInnerTexts()).map(t => t.replace(/\s+/g, " ")).slice(0, 40)));
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
