// Releve et compare les styles CALCULES de l'ancienne preparation.
//
//   node scripts/releve-styles.mjs relever  <sortie.json>
//   node scripts/releve-styles.mjs comparer <avant.json> <apres.json>
//
// POURQUOI CET OUTIL
// ------------------
// `npm run captures` compare des PIXELS, sur l'ecran tel qu'il se presente au
// chargement. Il ne voit ni le survol, ni une carte selectionnee, ni un paquet
// indisponible — c'est-a-dire une bonne partie de ce que la cascade CSS decide.
// Le plan 02-04 (purge des !important) a eu besoin de savoir quelle
// DECLARATION gagnait, pas seulement si l'image avait bouge ; les plans qui
// posent @layer puis les tokens auront exactement le meme besoin.
//
// Mode d'emploi typique, autour d'un changement de feuille de style :
//   1. etat de depart en place        -> relever avant.json
//   2. changement applique et deploye -> relever apres.json
//   3. comparer : la sortie doit etre « 0 difference ».
//
// Les fichiers produits sont volumineux (de l'ordre de 200 Mo : tous les
// elements x toutes les proprietes calculees). Les ecrire dans test-results/,
// qui est ignore par git et vide a chaque execution de Playwright.
import { chromium } from '@playwright/test';
import fs from 'node:fs';

const BASE = process.env.UI_CHECK_BASE || 'http://127.0.0.1:2345';

// Etats que la page ne montre pas d'elle-meme. On les pose a la main plutot
// que de dependre d'une partie en cours ou d'un contenu particulier.
const ETATS = [
  { selecteur: '#modular-sets button', index: 0, classes: ['click'] },
  { selecteur: '#modular-sets button', index: 1, classes: ['lock', 'click'] },
  { selecteur: '#encounter-sets button', index: 0, classes: ['click'] },
  { selecteur: '#set-images div', index: 0, classes: ['disable'] },
  { selecteur: '#set-images div', index: 1, classes: ['click'] },
];

const SURVOLS = [
  { selecteur: '#set-images div.set', etape: 0 },
  { selecteur: '#set-images div.disable', etape: 0 },
  { selecteur: '#modular-sets button', etape: 1 },
  { selecteur: '#modular-sets button.click', etape: 1 },
  { selecteur: '#modular-sets button.lock.click', etape: 1 },
  { selecteur: '#encounter-sets button', etape: 1 },
  { selecteur: '#encounter-sets button.click', etape: 1 },
  { selecteur: '#starter-gallery .starter-hero', etape: 2 },
  { selecteur: '#play-buttons button', etape: 3 },
];

// Valeurs qui bougent d'un passage a l'autre sans rapport avec la cascade.
const BRUIT = new Set(['perspective-origin', 'transform-origin', '-webkit-locale']);

function tousLesStyles(racineSelecteur) {
  const elements = racineSelecteur
    ? (() => {
        const racine = document.querySelector(racineSelecteur);
        return racine ? [racine, ...racine.querySelectorAll('*')] : [];
      })()
    : [...document.querySelectorAll('*')];
  const resultat = {};
  elements.forEach((el, i) => {
    // Les <style> et <link> ne sont pas les memes d'une version a l'autre :
    // les garder decalerait l'alignement des deux releves.
    if (el.tagName === 'STYLE' || el.tagName === 'LINK') return;
    for (const pseudo of [null, '::before', '::after']) {
      const style = getComputedStyle(el, pseudo);
      const propres = {};
      for (let k = 0; k < style.length; k++) propres[style[k]] = style.getPropertyValue(style[k]);
      resultat[`${i}|${el.tagName.toLowerCase()}|${pseudo ?? ''}`] = propres;
    }
  });
  return resultat;
}

async function relever(sortie) {
  const navigateur = await chromium.launch();
  const page = await navigateur.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(`${BASE}/scene.html`, { waitUntil: 'networkidle' });

  // Garde-fou : sans lui, une page d'authentification ou d'avertissement de
  // cache (servies en 200 OK) produirait un releve vide, donc une comparaison
  // verte qui ne prouve rien.
  if (!(await page.evaluate(() => typeof window.wizardShow === 'function'))) {
    await navigateur.close();
    throw new Error(
      `${BASE}/scene.html ne sert pas l'ancienne preparation (titre : "${await page.title()}"). ` +
        `Verifie le port : UI_CHECK_BASE, relaye par WSLENV depuis WSL.`
    );
  }

  const tout = {};

  // 1. Les 4 panneaux, tels qu'ils se presentent.
  for (let etape = 0; etape < 4; etape++) {
    await page.evaluate((i) => window.wizardShow(i), etape);
    if (etape === 1) {
      const expand = page.locator('button[onclick*="hide-not-click"]').first();
      if (await expand.count()) await expand.click();
    }
    await page.waitForTimeout(400);
    tout[`etape ${etape}`] = await page.evaluate(tousLesStyles, null);
  }

  // 2. Les memes panneaux, etats de selection poses.
  await page.evaluate((etats) => {
    for (const { selecteur, index, classes } of etats) {
      const el = document.querySelectorAll(selecteur)[index];
      if (el) el.classList.add(...classes);
    }
  }, ETATS);
  // Les cartes ont une transition de box-shadow (.16s) : sans cette pause, le
  // releve attrape une valeur en cours d'animation, differente a chaque fois.
  await page.waitForTimeout(600);
  tout['etats poses'] = await page.evaluate(tousLesStyles, null);

  // 3. Un survol a la fois, sur le sous-arbre concerne.
  for (const { selecteur, etape } of SURVOLS) {
    await page.evaluate((i) => window.wizardShow(i), etape);
    await page.waitForTimeout(250);
    const cible = page.locator(selecteur).first();
    if (!(await cible.count())) continue;
    try {
      await cible.hover({ force: true, timeout: 5000 });
    } catch {
      console.log(`survol impossible, ignore : ${selecteur}`);
      continue;
    }
    await page.waitForTimeout(300);
    tout[`survol ${selecteur}`] = await page.evaluate(tousLesStyles, selecteur);
  }

  fs.writeFileSync(sortie, JSON.stringify(tout));
  await navigateur.close();
  console.log(`Releve ecrit : ${sortie}`);
}

function ordonner(releve) {
  return Object.entries(releve)
    .map(([cle, styles]) => {
      const [index, balise, pseudo] = cle.split('|');
      return { index: Number(index), balise, pseudo, styles };
    })
    .sort((a, b) => a.index - b.index || a.pseudo.localeCompare(b.pseudo));
}

function comparer(cheminAvant, cheminApres) {
  const avant = JSON.parse(fs.readFileSync(cheminAvant, 'utf-8'));
  const apres = JSON.parse(fs.readFileSync(cheminApres, 'utf-8'));
  let total = 0;

  for (const scene of Object.keys(avant)) {
    const a = ordonner(avant[scene]);
    const b = ordonner(apres[scene] ?? {});
    if (a.length !== b.length) {
      console.log(`### ${scene} : ${a.length} elements avant, ${b.length} apres — comparaison impossible`);
      total += 1;
      continue;
    }
    const differences = [];
    for (let i = 0; i < a.length; i++) {
      for (const [prop, valeur] of Object.entries(a[i].styles)) {
        if (BRUIT.has(prop)) continue;
        const autre = b[i].styles[prop];
        if (autre !== valeur) {
          differences.push(`${a[i].balise}${a[i].pseudo} — ${prop} : « ${valeur} » devient « ${autre} »`);
        }
      }
    }
    total += differences.length;
    console.log(`### ${scene} : ${differences.length} difference(s)`);
    for (const ligne of differences.slice(0, 12)) console.log(`      ${ligne}`);
    if (differences.length > 12) console.log(`      … et ${differences.length - 12} autres`);
  }

  console.log(total === 0 ? '\nAucun style calcule n a change.' : `\n${total} differences au total.`);
  process.exitCode = total === 0 ? 0 : 1;
}

const [mode, ...arguments_] = process.argv.slice(2);
if (mode === 'relever' && arguments_[0]) await relever(arguments_[0]);
else if (mode === 'comparer' && arguments_.length === 2) comparer(arguments_[0], arguments_[1]);
else {
  console.error('Usage : node scripts/releve-styles.mjs relever <sortie.json>');
  console.error('        node scripts/releve-styles.mjs comparer <avant.json> <apres.json>');
  process.exitCode = 2;
}
