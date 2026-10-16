// TEMPORAIRE (capture de la phase du mechant dans les trois presentations). A supprimer.
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.use({ reducedMotion: 'no-preference' });
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
const THEME = process.env.ZZ_THEME ?? 'normal';
const LARG = Number(process.env.ZZ_L ?? 1600);
const HAUT = Number(process.env.ZZ_H ?? 900);

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
      localStorage.setItem('mc_phase_presentation', m === 'dynamique' ? 'dynamique' : m === 'bis' ? 'bis' : 'etape');
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
  await page.goto('/app/board.html' + (MODE === 'table' ? '?phase=sur-table' : ''), { waitUntil: 'networkidle' });
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
  const liste = [/^Garder ma main/, /^Défausser \d/, /(^|— )Suivant/, /^Ne pas (défendre|utiliser|jouer)/, /(^|— )Ne pas/, /^Aucune réponse/, /^Continuer sans rien jouer/, /^Passer/, /(^|— )Continuer/, /^OK$/, /^Terminer/, /(^|— )Terminer/, /^Fin de phase/i, /Fin du tour/];
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
    return {
      diag,
      cartouche: t('.deroule-phase').slice(0, 400),
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
  await partie(page);
  let vu = '';
  let rang = 0;
  let phasesVues = 0;
  let dansPhase = false;
  let tours = 0;
  for (let i = 0; i < 2500 && rang < MAXPAS; i++) {
    await page.waitForTimeout(300);
    const w = await monde(page);
    if (i % 60 === 0) {
      const s = await signature(page);
      console.log(`PAS ${i} phase=${w.phase} round=${w.round_id} boutons=${JSON.stringify(s.boutons)}`);
    }
    const enPhase = PHASES_MECHANT.includes(w.phase ?? '') || (await page.locator('.deroule-phase').filter({ visible: true }).count()) > 0;
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
      if (fin && !(await fin.isDisabled().catch(() => true)) && !/Mulligan|Setup|^$/i.test(w.phase ?? '')) {
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
        await page.waitForTimeout(800);
        rang++;
        await page.screenshot({ path: path.join(SORTIE, `${String(rang).padStart(3, '0')}.png`) });
        const faits = (w.faits_mechant ?? []).map((f: Record<string, unknown>) => `${f.genre}:${f.etat ?? ''}:${f.carte ?? f.auteur ?? ''}`);
        journal.write(JSON.stringify({ rang, i, phase: w.phase, round: w.round_id, ...s, faits: faits.slice(-5) }) + '\n');
      }
    }
    await unPas(page, dansPhase);
  }
  journal.end();
});
