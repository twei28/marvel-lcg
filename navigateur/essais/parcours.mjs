// Parcours joue par navigateurs.mjs : langue, assistant solo (Spider-Man contre Rhino), plateau,
// mulligan, un tour du heros, fin de tour, phase du mechant, retour au tour du heros (round 2).
// Le jeu vit dans un iframe de meme origine : tout passe par page.evaluate sur son document. Playwright Firefox
// ne sait pas piloter ce cadre (il le garde sur « about:blank » et ses locators n'y trouvent rien), et le plateau
// est un bundle sans identifiants stables : les elements se cherchent par leur texte visible.
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function jouer({ page, tag, OUT, res, log, mobile }) {
  const tDebut = Date.now();
  const etapes = {};
  const marque = (n) => { etapes[n] = true; res.etapes = Object.keys(etapes); };
  const photo = (n) => page.screenshot({ path: OUT + `${tag}-${n}.png`, timeout: 60000 }).catch(() => { (res.captures_echec ||= []).push(n); });

  const dansJeu = (fn, arg) => page.evaluate(({ src, arg }) => {
    const d = document.getElementById("jeu").contentDocument;
    if (!d) return null;
    return (new Function("d", "arg", "return (" + src + ")(d, arg)"))(d, arg);
  }, { src: fn.toString(), arg });
  const TOUS = "*";
  // Clique l'element visible le plus profond dont le texte correspond (portee : zone CSS cherchee).
  const cliquer = async (re, { tags = TOUS, portee = "body", exact = false, timeout = 60000 } = {}) => {
    const t0 = Date.now();
    while (Date.now() - t0 < timeout) {
      const ok = await dansJeu((d, a) => {
        const re = new RegExp(a.re, "i");
        const visible = (e) => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== "hidden" && getComputedStyle(e).display !== "none";
        const cands = [];
        for (const z of [...d.querySelectorAll(a.portee)].filter(visible)) for (const e of z.querySelectorAll(a.tags)) {
          const txt = (e.textContent || "").replace(/\s+/g, " ").trim();
          if (visible(e) && !e.disabled && re.test(txt)) cands.push(e);
        }
        const profond = cands.filter((e) => !cands.some((o) => o !== e && e.contains(o)));
        if (!profond.length) return false;
        profond[0].click();
        return true;
      }, { re: exact ? "^" + re.source + "$" : re.source, portee, tags }).catch(() => null);
      if (ok) return true;
      await sleep(400);
    }
    throw new Error("introuvable : " + re + (portee !== "body" ? " dans " + portee : ""));
  };
  const remplir = (placeholderRe, valeur) => dansJeu((d, a) => {
    const i = [...d.querySelectorAll("input")].find((e) => new RegExp(a.p, "i").test(e.placeholder));
    if (!i) return false;
    Object.getOwnPropertyDescriptor(i.ownerDocument.defaultView.HTMLInputElement.prototype, "value").set.call(i, a.v);
    i.dispatchEvent(new Event("input", { bubbles: true }));
    return true;
  }, { p: placeholderRe, v: valeur });

  for (let i = 0; i < 240 && !(await dansJeu((d) => d.body && /Français|solo/i.test(d.body.innerText)).catch(() => 0)); i++) await sleep(500);
  res.accueil_apres_pret_s = (Date.now() - tDebut) / 1000;
  await sleep(1500);
  // langue (premiere visite) puis phase du mechant (premiere visite)
  await cliquer(/Français/, { exact: true }); await sleep(800);
  await cliquer(/valider/, { portee: ".deck-modal-panel", tags: "button" }); await sleep(800);
  marque("accueil");
  await photo("2-accueil");
  if (mobile) { await cliquer(/^jouer/, { tags: "button,a,div" }); await sleep(1200); await photo("2b-jouer"); }
  await cliquer(mobile ? /^solo/ : /^solo/, { tags: mobile ? "button,a,div,li" : "button" }); await sleep(2000);
  await remplir("Rechercher", "Spider-Man"); await sleep(800);
  await cliquer(/spider-man/, { exact: true });
  if (mobile) { await sleep(800); await photo("2c-fiche-heros"); await cliquer(/^choisir/, { tags: "button" }); }
  else await cliquer(/valider/, { portee: ".deck-modal", tags: "button" });
  await sleep(800);
  await cliquer(/continuer/, { tags: "button" }); await sleep(1500);   // equipe -> decks
  await cliquer(/continuer/, { tags: "button", timeout: mobile ? 8000 : 60000 }).catch((e) => { if (!mobile) throw e; }); await sleep(1500);   // decks -> mechant (mobile : peut deja y etre)
  await cliquer(/rhino/, { exact: true }); await sleep(800);
  if (mobile) { await photo("3b-fiche-mechant"); await cliquer(/^choisir/, { tags: "button" }); await sleep(800); }
  await cliquer(/continuer/, { tags: "button" }); await sleep(1500);   // mechant -> final
  marque("assistant");
  await photo("3-assistant-final");
  await cliquer(/lancer la partie/, { tags: "button" });
  await sleep(8000);
  marque("plateau");
  await photo("4-plateau-lancement");

  // Boucle : on avance (Continuer / Garder ma main...), on joue "FIN DU TOUR" une fois, on s'arrete au round 2.
  let finTourFait = false, passes = 0, retourHeros = false;
  const t0 = Date.now();
  while (Date.now() - t0 < 240000) {
    const info = await dansJeu((d) => {
      const vis = (e) => e.getClientRects().length > 0 && !e.disabled && getComputedStyle(e).pointerEvents !== "none";
      return { bt: [...d.querySelectorAll("button")].filter(vis).map((e) => e.textContent.replace(/\s+/g, " ").trim()), texte: d.body.innerText.slice(0, 1500) };
    }).catch(() => null);
    if (!info) { await sleep(500); continue; }
    if (process.env.DEBUG_PARCOURS) log(Math.round((Date.now() - t0) / 1000) + "s", JSON.stringify(info.bt.filter((t) => !/menu|annuler|sauver|^auto|manuel|^fr$|⚙/i.test(t))), info.texte.replace(/\n/g, " | ").slice(0, 60));
    const cherche = (re) => info.bt.find((t) => re.test(t));
    const suite = cherche(/^continuer/i) || cherche(/^(étape suivante|fin de phase|garder ma main|valider|ok|confirmer|suivant|défausser)/i);
    const fin = cherche(/fin du tour/i);
    if (suite) {
      await cliquer(new RegExp("^" + suite.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")), { tags: "button", timeout: 5000 }).catch(() => {});
      passes++; if (finTourFait) marque("phase-mechant");
      await sleep(900); continue;
    }
    if (fin && !finTourFait && /action|ton tour|à toi/i.test(info.texte)) {
      marque("tour-du-heros");
      await photo("5-tour-heros");
      await cliquer(/fin du tour/, { tags: "button", timeout: 5000 }).catch(() => {});
      finTourFait = true; marque("fin-de-tour"); await sleep(1500); continue;
    }
    if (finTourFait && !fin && /choisir|choix/i.test(info.texte) && await cliquer(/^\(1\)/, { timeout: 3000 }).catch(() => false)) { passes++; (res.choix_repondus ||= []).push(info.texte.replace(/\n/g, " ").slice(0, 50)); await sleep(1200); continue; }
    if (finTourFait && !fin) { await page.keyboard.press("Space"); passes++; marque("phase-mechant"); await sleep(1200); continue; }
    if (finTourFait && fin && passes > 8) { retourHeros = true; break; }
    await sleep(900);
  }
  res.clics_de_suite = passes;
  res.texte_final = String(await dansJeu((d) => d.body.innerText).catch(() => "")).replace(/\n/g, " | ").slice(0, 90);
  if (retourHeros && /round 2/i.test(res.texte_final)) marque("retour-tour-heros-round-2");
  await photo("6-fin-parcours");
}
