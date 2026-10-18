// TEMPORAIRE (capture de la phase du mechant dans les trois presentations). A supprimer.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.use({ launchOptions: { args: ['--disable-features=LocalNetworkAccessChecks,PrivateNetworkAccessChecks'] }, reducedMotion: 'no-preference', video: { mode: 'on', size: { width: 1280, height: 720 } }, viewport: { width: 1280, height: 720 } });
const MODE = process.env.ZZ_MODE ?? 'bis';
const SCEN = process.env.ZZ_SCEN ?? 'rhino';
const HEROS = (process.env.ZZ_HEROS ?? 'spider_man').split(',');
const SEED = Number(process.env.ZZ_SEED ?? 4321);
const CMDS: string[] = JSON.parse(process.env.ZZ_CMDS ?? '[]');
const CMDS_TOUR: string[] = JSON.parse(process.env.ZZ_CMDS_TOUR ?? '[]');
const CMDS_TOUR2: string[] = JSON.parse(process.env.ZZ_CMDS_TOUR2 ?? '[]');
const CHOIX = process.env.ZZ_CHOIX ? new RegExp(process.env.ZZ_CHOIX) : undefined;
const NOM = process.env.ZZ_NOM ?? 'explo';
const PHASES = Number(process.env.ZZ_PHASES ?? 1);
const SORTIE = path.join(process.env.ZZ_SORTIE ?? '/tmp', MODE, NOM);
const MAXPAS = Number(process.env.ZZ_MAXPAS ?? 200);
const THEME = process.env.ZZ_THEME ?? 'epure';
const LARG = Number(process.env.ZZ_L ?? 1280);
const HAUT = Number(process.env.ZZ_H ?? 720);

const monde = async (page: Page) => (await (await page.request.get('/get_world?hot_seat&p=0')).json());
const PHASES_MECHANT = ['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards'];

async function commandes(page: Page, liste: string[], nom: string) {
  const r = await page.request.post('/sandbox_command?p=0', { data: { commands: liste } });
  console.log(nom, r.status(), (await r.text()).slice(0, 300));
}

async function partie(page: Page) {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?' + SCEN)).json();
  const decks = [];
  for (const h of HEROS) decks.push(JSON.stringify(await (await request.get('/get_hero_json?' + h)).json()));
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: decks, rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: SEED, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.setViewportSize({ width: LARG, height: HAUT });
  await page.addInitScript(([m, theme]) => {
    try {
      localStorage.setItem('mc_affichage_v1', theme);
      localStorage.setItem('mc_phase_presentation', m === 'dynamique' ? 'dynamique' : (m === 'bis' || m === 'table') ? 'bis' : 'etape');
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('marvel-langue', 'fr');
      localStorage.setItem('marvel-board-mode-phase-mechant', m === 'table' ? 'sur-table' : 'detaille');
      localStorage.setItem('mc_aide_bulle_table', 'vue');
    } catch { /* */ }
    const style = () => {
      const s = document.createElement('style');
      s.textContent = '.bandeau-maj{display:none!important}';
      document.head.appendChild(s);
    };
    if (document.head) style(); else document.addEventListener('DOMContentLoaded', style);
  }, [MODE, THEME]);
  // ZZ_DIST : un plateau compile a part (vite build --outDir), servi a la place de /app/ pour voir le code
  // courant sans toucher a public/app, que sert peut-etre une partie en cours.
  if (process.env.ZZ_DIST) {
    const dist = process.env.ZZ_DIST;
    const types: Record<string, string> = { '.js': 'text/javascript', '.css': 'text/css', '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.ttf': 'font/ttf' };
    await page.route('**/app/**', (route) => {
      const u = new URL(route.request().url());
      const f = path.join(dist, u.pathname.replace(/^\/app\//, ''));
      if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) return route.continue();
      return route.fulfill({ status: 200, contentType: types[path.extname(f)] ?? 'application/octet-stream', body: fs.readFileSync(f) });
    });
  }
  await page.goto('/app/board.html' + (MODE === 'table' ? '?phase=sur-table' : ''), { waitUntil: 'networkidle' });
  if (process.env.ZZ_CSS) await page.addStyleTag({ content: process.env.ZZ_CSS });
  if (CMDS.length) await commandes(page, CMDS, 'CMDS');
}

const visible = async (page: Page, nom: RegExp) => {
  const b = page.getByRole('button', { name: nom }).first();
  return (await b.count()) > 0 && (await b.isVisible().catch(() => false)) ? b : undefined;
};
const cliquer = async (b: ReturnType<Page['locator']>) => b.click({ timeout: 2500 }).then(() => true).catch(() => false);

async function unPas(page: Page, enPhase: boolean) {
  const defausser = await visible(page, /^Défausser \d/);
  if (defausser && (await defausser.isDisabled().catch(() => true))) {
    await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/, pressed: false })
      .first().click({ timeout: 1000 }).catch(() => {});
    return;
  }
  // « Sur la table » : un ciblage en cours (ordre des sbires) se fait en cliquant les cartes vertes.
  const aCibler = page.locator('.tsm-utilisable:not(.est-choisie):not([disabled])');
  if ((await page.locator('.tsm-bandeau.est-question .tsm-compte').count()) > 0 && (await aCibler.count()) > 0) {
    if (await cliquer(aCibler.first())) return;
  }
  // La fenetre de recherche (ouverte par la pile) : la premiere carte, puis son Valider.
  const carteSel = page.locator('.plateau-selecteur.est-fenetre .plateau-selecteur-carte:not(.est-choisie)');
  const validerSel = page.locator('.plateau-selecteur-valider:not([disabled])');
  if ((await validerSel.count()) > 0 && (await cliquer(validerSel.first()))) return;
  if ((await carteSel.count()) > 0 && (await cliquer(carteSel.first()))) return;
  const validerTable = page.locator('.tsm-bandeau .tsm-bouton:not([disabled])', { hasText: /^Valider/ });
  if ((await validerTable.count()) > 0 && (await cliquer(validerTable.first()))) return;
  const confirmer = await visible(page, /^Confirmer$/);
  if (confirmer && !(await confirmer.isDisabled().catch(() => true)) && (await cliquer(confirmer))) return;
  if (enPhase && CHOIX) {
    const b = await visible(page, CHOIX);
    if (b && !(await b.isDisabled().catch(() => true)) && (await cliquer(b))) return 'choix';
    const n = await page.locator('[data-choix]:visible').count();
    for (let k = 0; k < n; k++) {
      const c = page.locator('[data-choix]:visible').nth(k);
      if (CHOIX.test((await c.getAttribute('aria-label')) ?? (await c.textContent()) ?? '') && (await cliquer(c))) return 'choix';
    }
  }
  const liste = [/^Oui, garder/, /^Garder ma main/, /^Défausser \d/, /(^|— )Suivant/, /^Ne pas (défendre|utiliser|jouer)/, /(^|— )Ne pas/, /^Aucune réponse/, /^Continuer sans rien jouer/, /^Passer/, /(^|— )Continuer/, /^OK$/, /^Terminer/, /(^|— )Terminer/, /^Fin de phase/i, /Fin du tour/];
  for (const nom of liste) {
    const b = await visible(page, nom);
    if (b && !(await b.isDisabled().catch(() => true)) && (await cliquer(b))) return;
  }
  const choix = page.locator('[data-choix]:visible').first();
  if ((await choix.count()) > 0 && (await page.locator('[data-refus]:visible').count()) === 0) await cliquer(choix);
}

async function signature(page: Page) {
  return page.evaluate(() => {
    const vis = (e: Element) => e.getClientRects().length > 0;
    const t = (s: string) => Array.from(document.querySelectorAll(s)).filter(vis).map((e) => ((e as HTMLElement).innerText || e.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim()).join(' | ');
    const diag = (() => {
      const p = document.querySelector('.deroule-phase.est-dynamique') as HTMLElement | null;
      if (!p || !vis(p)) return { panneau: false };
      const vw = window.innerWidth, vh = window.innerHeight;
      const r = p.getBoundingClientRect();
      const dansEcran = (b: DOMRect) => b.left >= -0.5 && b.top >= -0.5 && b.right <= vw + 0.5 && b.bottom <= vh + 0.5;
      const dansPanneau = (b: DOMRect) => b.left >= r.left - 1 && b.right <= r.right + 1 && b.top >= r.top - 1 && b.bottom <= r.bottom + 1;
      const boutons = Array.from(p.querySelectorAll('button')).filter(vis).map((b) => {
        const bb = b.getBoundingClientRect();
        return { t: (b.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 44), ecran: dansEcran(bb), panneau: dansPanneau(bb), coupe: (b as HTMLElement).scrollWidth > (b as HTMLElement).clientWidth + 2 };
      });
      const corps = p.querySelector('.deroule-corps') as HTMLElement | null;
      const anglais = ((p.innerText || '').match(/\b(reveals?|revealed|attacks?|scheme|threat|deck|discard|choose|empty|paquet-vide)\b/gi) || []).slice(0, 6);
      const sous = Array.from(document.querySelectorAll('.scan-card')).filter((e) => !p.contains(e)).filter((e) => {
        const c = e.getBoundingClientRect();
        const cx = c.left + c.width / 2, cy = c.top + c.height / 2;
        return cx > r.left && cx < r.right && cy > r.top && cy < r.bottom;
      }).length;
      return {
        panneau: true, rect: [r.left, r.top, r.right, r.bottom].map(Math.round), panneauDansEcran: dansEcran(r),
        boutons, anglais, scrollHorizontal: document.documentElement.scrollWidth > vw, cartesSousLePanneau: sous,
        defilementInterne: corps ? corps.scrollHeight > corps.clientHeight + 1 : false,
      };
    })();
    const bulle = ((document.querySelector('.deroule-bulle-table') ?? document.querySelector('.deroule-phase')) as HTMLElement | null)?.outerHTML.slice(0, 2500);
    const jetons = Array.from(document.querySelectorAll('.jeton-coup')).map((e) => { const r = e.getBoundingClientRect(); return { t: e.textContent, vis: (e as HTMLElement).style.visibility, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width) }; });
    const cls = Array.from(document.querySelectorAll('.scan-card')).filter((e) => /active|actif|highlight|pulse|target|play/i.test(e.className)).map((e) => e.getAttribute('data-card-id') + ':' + e.className);
    const cadresVus = Array.from(document.querySelectorAll('.scan-card.is-highlighted, .scan-card.is-target-pulse')).slice(0, 2).flatMap((c) => [c, ...Array.from(c.querySelectorAll('*'))].map((e) => { const cs = getComputedStyle(e); const r = e.getBoundingClientRect(); return { e: (e.className || e.tagName).toString().slice(0, 40), o: cs.outlineStyle !== 'none' ? cs.outlineColor + ' ' + cs.outlineWidth + ' off ' + cs.outlineOffset : '', b: cs.boxShadow !== 'none' ? cs.boxShadow.slice(0, 80) : '', bd: cs.borderTopStyle !== 'none' && cs.borderTopWidth !== '0px' ? cs.borderTopWidth + ' ' + cs.borderTopColor : '', r: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)] }; }).filter((x) => x.o || x.b || x.bd));
    const rr = (e: Element | null) => { if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
    const mesuresActeur = { nbActeurs: document.querySelectorAll('.tsm-acteur').length, tousActeurs: Array.from(document.querySelectorAll('.tsm-acteur')).map((e) => rr(e)), acteur: rr(document.querySelector('.tsm-acteur')), cible: rr(document.querySelector('.tsm-cible')), cadre: rr(document.querySelector('.plateau-cadre')), frames: Array.from(document.querySelectorAll('.scan-card.is-highlighted .scan-frame, .scan-card.is-target-pulse .scan-frame')).map((e) => rr(e)) };
    const ptsHaut = document.elementsFromPoint(263, 150).concat(document.elementsFromPoint(321, 62)).map((e) => (e.tagName + '.' + (e.className || '')).toString().slice(0, 60));
    const pseudos = Array.from(document.querySelectorAll('.scan-card[data-card-id="49"], .scan-card[data-card-id="49"] *')).flatMap((e) => ['::before', '::after'].map((p) => { const cs = getComputedStyle(e, p); return { e: (e.className || e.tagName).toString().slice(0, 30), p, c: cs.content, bd: cs.borderTopWidth + ' ' + cs.borderTopStyle + ' ' + cs.borderTopColor, bs: cs.boxShadow.slice(0, 60), ol: cs.outlineStyle, w: cs.width, h: cs.height }; })).filter((x) => x.c !== 'none' && x.c !== 'normal');
    const candidats = Array.from(document.querySelectorAll('body *')).filter((e) => { const r = e.getBoundingClientRect(); return ((Math.abs(r.x - 263) < 14 && Math.abs(r.y - 62) < 14) || (Math.abs(r.x - 265) < 12 && Math.abs(r.y - 497) < 12)) && r.width > 80 && r.width < 160 && r.height > 150 && r.height < 260; }).map((e) => (e.tagName + '.' + (e.className || '')).toString().slice(0, 80) + ' ' + JSON.stringify([Math.round(e.getBoundingClientRect().x), Math.round(e.getBoundingClientRect().y), Math.round(e.getBoundingClientRect().width), Math.round(e.getBoundingClientRect().height)]));
    const zones = Array.from(document.querySelectorAll('.plateau-emplacement')).map((e) => { const cs = getComputedStyle(e); return e.className + ' | bd ' + cs.borderTopWidth + ' ' + cs.borderTopColor + ' | ol ' + cs.outlineStyle + ' ' + cs.outlineColor + ' | bs ' + cs.boxShadow.slice(0, 70) + ' | bg ' + cs.backgroundColor; }).filter((x) => /rgb\(2[0-9][0-9]|rgba\(24|rgba\(2[0-9][0-9]/.test(x));
    const tsmTous = Array.from(document.querySelectorAll('[class*="tsm-"]')).map((e) => (e.className || '').toString() + ' ' + JSON.stringify(rr(e)));
    const ac = document.querySelector('.tsm-acteur');
    const acStyle = ac ? (() => { const cs = getComputedStyle(ac); return { bs: cs.boxShadow, ol: cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + cs.outlineColor + ' off ' + cs.outlineOffset, bd: cs.borderTopWidth + ' ' + cs.borderTopColor, w: cs.width, h: cs.height, minh: cs.minHeight, pad: cs.padding, bsz: cs.boxSizing, an: cs.animationName, foc: document.activeElement === ac, tf: cs.transform }; })() : null;
    const et = (window as unknown as { __et?: unknown }).__et;
    const dep = document.querySelector('.tsm-depart')?.getBoundingClientRect();
    const dbg = [(window as unknown as { __dbg?: unknown }).__dbg, (window as unknown as { __j?: string[] }).__j];
    return {
      et, acStyle, tsmTous, zones, candidats, pseudos, ptsHaut, mesuresActeur, cadresVus, cls, dbg, jetons, dep: dep ? [Math.round(dep.x), Math.round(dep.y), Math.round(dep.width)] : null,
      bulle,
      diag,
      cartouche: t('.deroule-phase, .tsm-bandeau').slice(0, 400),
      demande: t('.demande-centrale').slice(0, 200),
      annonce: t('.bandeau-annonce').slice(0, 160),
      dialogues: Array.from(document.querySelectorAll('[role="dialog"]')).filter(vis).map((d) => d.getAttribute('aria-label') || '').filter(Boolean).join(','),
      boutons: Array.from(document.querySelectorAll('button')).filter(vis).map((b) => (b.getAttribute('aria-label') || b.textContent || '').trim().slice(0, 50)).filter(Boolean).slice(0, 40),
    };
  });
}

test('explo', async ({ page }) => {
  test.setTimeout(900_000);
  fs.rmSync(SORTIE, { recursive: true, force: true });
  fs.mkdirSync(SORTIE, { recursive: true });
  const journal = fs.createWriteStream(path.join(SORTIE, 'journal.jsonl'));
  const T0 = Date.now();
  await partie(page);
  let vu = '';
  let rang = 0;
  let phasesVues = 0;
  let dansPhase = false;
  let tours = 0;
  let volProchain = false;
  let volDejaVu = false;
  let boostVu = false;
  let questionVue = false;
  let boostOcc = 0;
  let toutN = 0;
  for (let i = 0; i < 2500 && rang < MAXPAS; i++) {
    await page.waitForTimeout(Number(process.env.ZZ_PAUSE ?? 300));
    const w = await monde(page);
    if (i % 60 === 0) {
      const s = await signature(page);
      await page.screenshot({ path: path.join(SORTIE, `pas-${String(i).padStart(4, '0')}.png`) });
      fs.writeFileSync(path.join(SORTIE, `pas-${String(i).padStart(4, '0')}.html`), await page.evaluate(() => {
        const e = Array.from(document.querySelectorAll('body *')).find((x) => /capacités forcées/i.test((x as HTMLElement).innerText || '') && x.children.length < 12 && (x as HTMLElement).innerText.length < 200);
        let a: Element | null = e ?? null; for (let k = 0; k < 3 && a?.parentElement; k++) a = a.parentElement;
        return a ? a.outerHTML.slice(0, 6000) : 'rien';
      }));
      console.log(`PAS ${i} phase=${w.phase} round=${w.round_id} boutons=${JSON.stringify(s.boutons)}`);
    }
    const enPhase = PHASES_MECHANT.includes(w.phase ?? '') || (await page.locator('.deroule-phase, .tsm-bandeau').filter({ visible: true }).count()) > 0;
    if (enPhase && !dansPhase) dansPhase = true;
    if (!enPhase && dansPhase) {
      dansPhase = false; phasesVues++;
      if (phasesVues >= PHASES) { await page.waitForTimeout(1500); await page.screenshot({ path: path.join(SORTIE, `${String(++rang).padStart(3, '0')}-apres.png`) }); break; }
    }
    if (w.game_over) {
      for (let k = 0; k < 3; k++) {
        await page.waitForTimeout(1800);
        await page.screenshot({ path: path.join(SORTIE, `${String(++rang).padStart(3, '0')}-fin.png`) });
        const s = await signature(page);
        journal.write(JSON.stringify({ rang, fin: true, raison: w.game_over_reason, gagne: w.players_won, ...s }) + '\n');
        if (k === 1) await unPas(page, true);
      }
      break;
    }
    if (!dansPhase) {
      // Phase du joueur : poser les commandes du tour avant « Fin du tour ».
      const fin = await visible(page, /Fin du tour/);
      if ((/^Player(?: \d+)? Turn$/.test(w.phase ?? '') && tours === 0) || (fin && !(await fin.isDisabled().catch(() => true)) && !/Mulligan|Setup|^$/i.test(w.phase ?? ''))) {
        const liste = tours === 0 ? CMDS_TOUR : tours === 1 ? CMDS_TOUR2 : [];
        if (liste.length) { await commandes(page, liste, `TOUR${tours} (${w.phase})`); await page.waitForTimeout(1500); }
        tours++;
      }
    }
    if (dansPhase) {
      const s = await signature(page);
      const cle = s.cartouche + '#' + s.demande + '#' + s.annonce + '#' + s.dialogues;
      if (cle !== vu) {
        vu = cle;
        if (process.env.ZZ_BOOSTRE && new RegExp(process.env.ZZ_BOOSTRE, 'i').test(s.cartouche ?? '')) boostOcc++;
        if (/Qui défend/.test(s.cartouche ?? '')) questionVue = true;
        else if (((process.env.ZZ_BOOSTRE && boostOcc >= Number(process.env.ZZ_BOOSTN ?? 2)) || (!process.env.ZZ_BOOSTRE && questionVue && /attaque/i.test(s.cartouche ?? ''))) && !boostVu) {
          boostVu = true;
          for (const k of [1, 2, 3, 4, 5]) { await page.waitForTimeout(380); await page.screenshot({ path: path.join(SORTIE, `boost-${k}.png`) }); }
        }
        volProchain = /gagne \d+ menace/i.test(s.cartouche ?? '') && !volDejaVu;
        await page.waitForTimeout(Number(process.env.ZZ_ATTENTE ?? 800));
        rang++;
        await page.screenshot({ path: path.join(SORTIE, `${String(rang).padStart(3, '0')}.png`) });
        const faits = (w.faits_mechant ?? []).map((f: Record<string, unknown>) => `${f.genre}:${f.etat ?? ''}:${f.carte ?? f.auteur ?? ''}:b${Array.isArray(f.boosts) ? f.boosts.length : '-'}:subi${f.subi ?? '-'}:base${f.base ?? '-'}:inf${f.inflige ?? '-'}`);
        const s2 = await signature(page);
        journal.write(JSON.stringify({ rang, t: Date.now() - T0, i, phase: w.phase, round: w.round_id, ...s, bulle: s2.bulle, jetons: s2.jetons, acStyle: s2.acStyle, tsmTous: s2.tsmTous, zones: s2.zones, candidats: s2.candidats, pseudos: s2.pseudos, ptsHaut: s2.ptsHaut, mesuresActeur: s2.mesuresActeur, cadresVus: s2.cadresVus, cls: s2.cls, dbg: s2.dbg, dep: s2.dep, faits: faits.slice(-5) }) + '\n');
      }
    }
    if (process.env.ZZ_TOUT && dansPhase && toutN < 40) {
      const sg = await signature(page);
      if (new RegExp(process.env.ZZ_TOUT, 'i').test(sg.cartouche ?? '')) { await page.screenshot({ path: path.join(SORTIE, `tout-${String(++toutN).padStart(2, '0')}.png`) }); journal.write(JSON.stringify({ tout: toutN, c: (sg.cartouche ?? '').slice(0, 90), et: (sg as { et?: unknown }).et }) + '\n'); }
    }
    await unPas(page, dansPhase);
    if (volProchain) {
      volProchain = false; volDejaVu = true;
      for (const k of [1, 2, 3]) { await page.waitForTimeout(220); await page.screenshot({ path: path.join(SORTIE, `vol-${k}.png`) }); }
    }
  }
  journal.end();
});
