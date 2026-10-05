// LA PLANCHE DU CARTOUCHE DU BAS (refonte de la phase du mechant, D40) :
// une vraie partie par etat, sur le moteur d'ESSAI, une capture et ses mesures.
//
// Lot 3 : les etats SANS question (3, 4, 5, 6, 7, 8, 9, 12) et la variante
// Sobre de l'etat 4. Lot 4 : les etats a question (1, 2, 10, 11 en trois
// prises, 14). Lot 5 : la relecture (13, pendant la phase et depuis le
// journal), le hors phase (15, la defense puis le coup), les variantes Sobre
// des etats 1 et 8, et la loupe sur une petite fenetre.
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : chaque cas cree une partie.
//   UI_CHECK_BASE=http://127.0.0.1:2347 PLANCHE=1 npx playwright test tests/planche-cartouche.spec.ts --project=pc
// Sans PLANCHE, le fichier se saute (il ne fait pas partie des captures de
// reference).
//
// A chaque capture, mesure et verifie (`expect.soft`) : le carre de la phase
// (revirement du 05/10) fait `--carre-l` de large (clamp 560 a 1100, 760 a
// l'echelle de la table), au moins les 3/4 de sa largeur de haut, il est
// centre sur l'ecran, aucun defilement, un seul panneau de premier niveau, la
// main VISIBLE (jamais cachee par le carre), et le CONTENU face a la boite :
// aucun enfant du corps ne deborde du carre (il grandit plutot que de couper).
import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' };

test.skip(!process.env.PLANCHE, 'planche du cartouche : PLANCHE=1 et le moteur d’essai');

const SORTIE = path.resolve('captures-tmp');

type Reglages = { sobre?: boolean; heros?: string[] };

async function partie(page: Page, commandes: string[], reglages: Reglages = {}) {
  const request = page.request;
  const scenario = await (await request.get('/get_scenario_json?rhino')).json();
  const decks = [];
  for (const heros of reglages.heros ?? ['spider_man']) {
    decks.push(JSON.stringify(await (await request.get(`/get_hero_json?${heros}`)).json()));
  }
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: decks, rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321, timeout: 0,
  };
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200);
  await page.addInitScript((sobre) => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1');
      localStorage.setItem('mc_affichage_v1', sobre ? 'sobre' : 'normal');
      localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille');
    } catch { /* */ }
  }, Boolean(reglages.sobre));
  // Plusieurs heros : un siege par page, comme le salon (`?p=N&multi=1`).
  await page.goto(reglages.heros && reglages.heros.length > 1 ? '/app/board.html?p=0&multi=1' : '/app/board.html', {
    waitUntil: 'networkidle',
  });
  if (commandes.length > 0) await commande(page, commandes);
}

async function commande(page: Page, commandes: string[]) {
  const reponse = await page.request.post('/sandbox_command?p=0', { data: { commands: commandes } });
  console.log(`COMMANDES ${JSON.stringify(commandes)} -> ${reponse.status()} ${(await reponse.text()).slice(0, 300)}`);
}

const visible = async (page: Page, nom: RegExp) => {
  const b = page.getByRole('button', { name: nom }).first();
  return (await b.count()) > 0 && (await b.isVisible()) ? b : undefined;
};

/**
 * Un pas de jeu sur une page : la premiere chose utile a cliquer. `choisir` :
 * le choix du cartouche (son `aria-label`) a prendre plutot que de refuser.
 */
/**
 * Le bouton est-il desactive ? Sans attendre : un bouton qui disparait entre
 * deux lectures (la question est partie) faisait attendre `isDisabled`
 * jusqu'au bout du delai du test.
 */
const inactif = (l: ReturnType<Page['locator']>) => l.isDisabled({ timeout: 1000 }).catch(() => true);

async function unPas(page: Page, fini: () => Promise<boolean>, choisir?: RegExp): Promise<void> {
  const defausser = await visible(page, /^Défausser \d/);
  if (defausser && (await inactif(defausser))) {
    // Une carte PAS encore choisie : recliquer la premiere la decochait, et la
    // fin de tour tournait en rond (main trop grande apres CreateHandCards).
    await page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/, pressed: false })
      .first().click({ timeout: 2000 }).catch(() => {});
    return;
  }
  const cartouche = page.locator('.deroule-phase.est-scene');
  // Le choix voulu par l'etat (defendre avec Spider-Man, jouer une carte).
  if (choisir) {
    const n = await cartouche.locator('[data-choix]').count();
    for (let k = 0; k < n; k++) {
      const b = cartouche.locator('[data-choix]').nth(k);
      if (choisir.test((await b.getAttribute('aria-label')) ?? '') && (await b.isVisible())) {
        if (await fini()) return;
        await b.click({ timeout: 2000 }).catch(() => {});
        return;
      }
    }
  }
  // Un ciblage ou un ordre dans le sous-cadre (C29) : chaque carte, puis
  // « Confirmer ».
  const valider = cartouche.locator('.deroule-sous-cadre .deroule-valider').first();
  if ((await valider.count()) > 0 && (await valider.isVisible())) {
    if (!(await inactif(valider))) {
      if (await fini()) return;
      await valider.click({ timeout: 2000 }).catch(() => {});
      return;
    }
    const carte = cartouche.locator('.deroule-sous-cadre [data-choix][aria-pressed="false"]').first();
    if ((await carte.count()) > 0) {
      await carte.click({ timeout: 2000 }).catch(() => {});
      return;
    }
  }
  for (const nom of [
    /^Garder ma main/, /^Défausser \d/, /^Suivant/, /^Terminer$/, /^Ne pas (défendre|utiliser|jouer)/,
    /^Aucune réponse/, /^Continuer sans rien jouer/, /^Passer/, /^Continuer/, /^Fin de phase/i, /Fin du tour/,
  ]) {
    const b = await visible(page, nom);
    if (b && !(await inactif(b))) {
      // L'etape a pu changer sous le bouton (une resolution arrivee entre
      // deux lectures) : on reverifie juste avant de cliquer, sinon le clic
      // validerait l'etat meme qu'on attend.
      if (await fini()) return;
      await b.click({ timeout: 2000 }).catch(() => {});
      return;
    }
  }
  // Une question FORCEE du cartouche (aucun refus) : le premier choix.
  const force = cartouche.locator('[data-choix]').first();
  if ((await force.count()) > 0 && (await cartouche.locator('[data-refus]').count()) === 0 && (await force.isVisible())) {
    if (await fini()) return;
    await force.click({ timeout: 2000 }).catch(() => {});
    return;
  }
  // Une recherche hors phase (la « Prescience » de Black Panther a la mise
  // en place) : une carte du selecteur hors table, puis l'assistant valide.
  const horsTable = page.locator('.plateau-selecteur [role="button"][aria-pressed="false"]').first();
  const confirmerAssistant = page.locator('.assistant-action .assistant-confirmer').first();
  if ((await confirmerAssistant.count()) > 0 && (await confirmerAssistant.isVisible())) {
    if (!(await inactif(confirmerAssistant))) {
      await confirmerAssistant.click({ timeout: 2000 }).catch(() => {});
      return;
    }
    if ((await horsTable.count()) > 0 && (await horsTable.isVisible())) {
      await horsTable.click({ timeout: 2000 }).catch(() => {});
      return;
    }
  }
  // Une question HORS phase a choix unique, que la liste ne nomme pas : son
  // seul bouton.
  const centrale = page.locator('.demande-centrale .af-action').first();
  if ((await centrale.count()) > 0 && (await centrale.isVisible()) && (await page.locator('.demande-centrale .af-action').count()) === 1) {
    if (await fini()) return;
    await centrale.click({ timeout: 2000 }).catch(() => {});
  }
}

/** Avance (tour du joueur, puis phase du mechant) jusqu'a ce que `fini` soit vrai. */
async function jouerJusqua(page: Page, fini: () => Promise<boolean>, tours = 300, choisir?: RegExp) {
  let vue = '';
  for (let i = 0; i < tours; i++) {
    if (await fini()) return true;
    // Le fil de la partie, pour relever ce que le moteur a fait (C33, C34).
    const lue = await page.locator('.deroule-phase.est-scene .deroule-corps').first().getAttribute('aria-label', { timeout: 200 }).catch(() => null);
    if (lue && lue !== vue) {
      vue = lue;
      console.log(`  vu : ${lue}`);
    }
    await page.waitForTimeout(250);
    if (await fini()) return true;
    await unPas(page, fini, choisir);
  }
  return fini();
}

const titreCourt = (page: Page) => page.locator('.deroule-phase.est-scene .deroule-titre-court').first();
const titreEst = (page: Page, motif: RegExp) => async () =>
  (await titreCourt(page).count()) > 0 && motif.test((await titreCourt(page).textContent()) ?? '');

/**
 * Les mesures de la planche, imprimees et verifiees. `question` : l'etat
 * montre une question, qui doit avoir au moins un choix ou un refus visible.
 */
async function mesurer(page: Page, nom: string, { question = false }: { question?: boolean } = {}) {
  // Tout de suite : l'etape peut ceder sa place a la suivante quand le moteur
  // l'a deja depassee (sortie d'attente du cartouche).
  await page.waitForTimeout(120);
  // Les annonces de phase et de tour (2,2 s) passent devant le carre : on
  // attend qu'elles s'en aillent, sinon la capture montre l'annonce.
  await page.waitForFunction(() => !document.querySelector('.splash-tour, .bandeau-phase'), undefined, { timeout: 4000 }).catch(() => {});
  await page.waitForTimeout(350);
  fs.mkdirSync(SORTIE, { recursive: true });
  await page.screenshot({ path: path.join(SORTIE, `${nom}.png`) });
  const m = await page.evaluate(() => {
    const section = document.querySelector<HTMLElement>('.deroule-phase.est-scene');
    if (!section) return undefined;
    const r = section.getBoundingClientRect();
    const echelle = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--echelle')) || 1;
    const attendue = Math.min(1100, Math.max(560, 760 * echelle));
    const corps = section.querySelector<HTMLElement>('.deroule-corps');
    const rc = corps?.getBoundingClientRect();
    // Le CONTENU face a la boite : un enfant du corps qui deborde se voit
    // coupe, meme si rien ne defile.
    const debordements = [...(corps?.querySelectorAll<HTMLElement>('.deroule-vignette, .deroule-resultat-gros, .deroule-lignes li, .deroule-etoile, .deroule-colonne, .deroule-vide, .deroule-total, .deroule-sous-cadre, .deroule-sous-cadre-tete, .deroule-sous-cadre-boutons, .deroule-question-carte, .deroule-pulse') ?? [])]
      .map((el) => ({ el, b: el.getBoundingClientRect() }))
      .filter(({ b }) => b.bottom > r.bottom + 1 || b.right > r.right + 1 || b.top < r.top - 1 || b.left < r.left - 1)
      .map(({ el, b }) => `${el.className.split(' ')[0]} ${Math.round(b.top)}-${Math.round(b.bottom)} / carre ${Math.round(r.top)}-${Math.round(r.bottom)}`)
    const panneaux = [...document.querySelectorAll<HTMLElement>('.deroule-phase, .demande-centrale, .cibles-scene, .assistant-action, .couche-revelation, .plateau-selecteur, .evenement-centrale')]
      .filter((el) => el.getBoundingClientRect().height > 0 && getComputedStyle(el).visibility !== 'hidden')
      .filter((el) => !el.parentElement?.closest('.deroule-phase, .demande-centrale, .cibles-scene, .assistant-action'))
      .map((el) => el.className.split(' ').slice(0, 2).join('.'))
    const visibilite = (sel: string) => {
      const el = document.querySelector<HTMLElement>(sel)
      return el ? getComputedStyle(el).visibility : 'absent'
    }
    const languette = document.querySelector<HTMLElement>('.volet-journal-languette')?.getBoundingClientRect();
    const pied = section.querySelector<HTMLElement>('.deroule-boutons')?.getBoundingClientRect();
    return {
      w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y),
      decentreX: Math.round(Math.abs(r.x + r.width / 2 - window.innerWidth / 2)),
      decentreY: Math.round(Math.abs(r.y + r.height / 2 - window.innerHeight / 2)),
      attendue: Math.round(attendue * 10) / 10, echelle: Math.round(echelle * 1000) / 1000,
      largeurEcran: window.innerWidth, hauteurEcran: window.innerHeight,
      defile: section.scrollHeight > section.clientHeight || (corps ? corps.scrollHeight > corps.clientHeight : false),
      scroll: `${section.scrollHeight}/${section.clientHeight} corps ${corps?.scrollHeight}/${corps?.clientHeight}`,
      corps: rc ? `${Math.round(rc.height)}` : '-',
      pied: pied ? `${Math.round(pied.top)}-${Math.round(pied.bottom)} (section ${Math.round(r.top)}-${Math.round(r.bottom)})` : '-',
      debordements, panneaux,
      main: visibilite('.plateau-scene .zone-main'), action: visibilite('.plateau-action'),
      // La main levee : le bas de ses cartes tient dans l'ecran (au repos, la
      // moitie basse sort par le bas).
      mainLevee: (() => {
        const c = document.querySelector('.zone-main .scan-card')?.getBoundingClientRect();
        return c ? c.bottom <= window.innerHeight + 1 : true;
      })(),
      languette: languette ? `${Math.round(languette.top)}-${Math.round(languette.bottom)}` : 'absente',
      languetteAuDessus: languette ? languette.bottom <= r.top + 0.5 : true,
      titre: section.querySelector('.deroule-titre-court')?.textContent ?? '',
      page: section.querySelector('.deroule-page')?.textContent ?? '',
      pastilles: [...section.querySelectorAll('.deroule-pastille')].map((p) => `${p.className.replace('deroule-pastille ', '')}:${p.textContent}`).join(' | '),
      phrase: section.querySelector('.deroule-corps')?.getAttribute('aria-label') ?? '',
      texte: (section.querySelector('.deroule-corps') as HTMLElement | null)?.innerText.replace(/\s+/g, ' ').slice(0, 200) ?? '',
      choix: [...section.querySelectorAll<HTMLElement>('[data-choix], [data-refus]')]
        .filter((el) => el.getBoundingClientRect().width > 0 && el.closest('[aria-hidden="true"]') === null).length,
      apercu: (() => {
        const a = document.querySelector('.carte-apercu')?.getBoundingClientRect();
        return a ? `${Math.round(a.x)},${Math.round(a.y)} ${Math.round(a.width)}x${Math.round(a.height)}` : 'aucun';
      })(),
      // Les cartes d'une rangee alignees par le haut : une carte sans legende,
      // centree, descendait sous ses voisines (planche du lot 6).
      ecartCartes: (() => {
        const hauts = [...section.querySelectorAll('.deroule-rangee-cartes .deroule-vignette .scan-card')].map(
          (c) => c.getBoundingClientRect().top
        );
        // Une rangee a la ligne (deux lignes si besoin) : l'ecart se mesure
        // dans chaque ligne, pas entre elles.
        hauts.sort((x, y) => x - y);
        let pire = 0;
        let debut = 0;
        for (let i = 1; i <= hauts.length; i++) {
          if (i === hauts.length || hauts[i] - hauts[i - 1] > 40) {
            pire = Math.max(pire, hauts[i - 1] - hauts[debut]);
            debut = i;
          }
        }
        return Math.round(pire);
      })(),
      // D35 : le corps entre en glissant, sauf en Sobre (trois gates).
      animation: corps ? getComputedStyle(corps).animationName : '-',
      sobre: document.documentElement.dataset.affichage === 'sobre',
      selecteur: document.querySelector('.plateau-selecteur') ? 'present' : 'absent',
      assistant: document.querySelector('.assistant-action') ? 'present' : 'absent',
    };
  });
  console.log(`${nom} ${JSON.stringify(m, null, 1)}`);
  expect(m, 'le cartouche du bas est a l ecran').toBeDefined();
  if (!m) return;
  expect.soft(Math.abs(m.w - m.attendue), `largeur ${m.w} pour ${m.attendue}`).toBeLessThanOrEqual(1);
  expect.soft(m.h, `hauteur ${m.h} sous les 3/4 de ${m.w}`).toBeGreaterThanOrEqual(Math.round(m.w * 0.75) - 1);
  expect.soft(m.decentreX, 'le carre n est pas centre en largeur').toBeLessThanOrEqual(1);
  expect.soft(m.decentreY, 'le carre n est pas centre en hauteur').toBeLessThanOrEqual(1);
  expect.soft(m.defile, m.scroll).toBe(false);
  expect.soft(m.debordements, 'contenu coupe').toEqual([]);
  expect.soft(m.panneaux, 'un seul panneau de premier niveau').toHaveLength(1);
  // La main reste visible et cliquable (revirement du 05/10) ; la barre
  // d'action n'existe pas dans tous les modes d'affichage.
  expect.soft(['visible', 'absent'], `main ${m.main}`).toContain(m.main);
  expect.soft(m.animation, 'le glissement du corps (D35)').toBe(m.sobre ? 'none' : 'cartouche-page-entre');
  expect.soft(m.ecartCartes, 'les cartes de la rangee desalignees').toBeLessThanOrEqual(1);
  if (question) {
    expect.soft(m.mainLevee, 'la main reste baissee pendant une question').toBe(true);
    expect.soft(m.choix, 'une question sans choix ni refus visible').toBeGreaterThan(0);
    expect.soft(m.assistant, 'l assistant d action hors du cartouche').toBe('absent');
  } else {
    expect.soft(m.choix, 'aucune question dans ces etats').toBe(0);
  }
}

// Le dessus du paquet rencontre, pose pendant le tour du joueur : chaque carte
// est PRISE DANS LE PAQUET DU SCENARIO et remontee sur le dessus
// (`Puzzle.PutIntoDeck`), la DERNIERE nommee finissant sur le dessus. Le dessus
// sert de boost a l'attaque du mechant, la suivante est distribuee puis
// revelee, la troisieme suit un Renfort.
//
// ⚠ PAS `CreateEncounterDeck` (releve au lot 3) : des cartes creees ainsi en
// cours de partie se revelent SANS LEUR EFFET (Stampede n'a pas fait attaquer
// Rhino, Kree Manipulator et Hard to Keep Down n'ont pas declenche de Renfort :
// aucun second fait de distribution au journal).
const dessus = (...cartes: string[]) => cartes.map((c) => `Puzzle.PutIntoDeck('${c}')`);

test.setTimeout(300_000);

test('etat 03 : attaque resolue, boost colle, total en gros', async ({ page }) => {
  // Boost du dessus : Stampede (1 icone, sans etoile).
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...dessus('01106')]);
  const resolue = page.locator('.deroule-phase.est-scene .deroule-rangee .deroule-resultat-texte');
  expect(await jouerJusqua(page, async () => (await titreEst(page, /attaque/i)()) && (await resolue.count()) > 0)).toBe(true);
  await mesurer(page, 'etat-03');
});

// ETAT 4 (05/10/2026) : le moteur publie desormais un fait `sonne` quand la
// carte Sonne remplace l'activation (can_attack.py, JournaliserActivationEmpechee).
// Le cartouche l'affiche comme une etape « Sonne » (carte du mechant en grand).
test('etat 04 : activation annulee (Rhino sonne)', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", "Puzzle.Stun('01094')"]);
  expect(await jouerJusqua(page, titreEst(page, /Sonn/), 120)).toBe(true);
  await mesurer(page, 'etat-04');
});

// La variante Sobre (D39) se prend sur l'etat 3, faute d'etat 4.
test('etat 03 sobre : meme etat, affichage Sobre', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...dessus('01106')], { sobre: true });
  const resolue = page.locator('.deroule-phase.est-scene .deroule-rangee .deroule-resultat-texte');
  expect(await jouerJusqua(page, async () => (await titreEst(page, /attaque/i)()) && (await resolue.count()) > 0)).toBe(true);
  await mesurer(page, 'etat-03-sobre');
});

// La hauteur suit l'echelle de la table (clamp 200 a 320) : un ecran plus
// petit la ramene vers 200 px, sans rien couper.
test('etat 03 petit ecran : 1280 x 720', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...dessus('01106')]);
  const resolue = page.locator('.deroule-phase.est-scene .deroule-rangee .deroule-resultat-texte');
  expect(await jouerJusqua(page, async () => (await titreEst(page, /attaque/i)()) && (await resolue.count()) > 0)).toBe(true);
  await mesurer(page, 'etat-03-petit');
});

test('etat 05 : manigance du mechant (heros en alter ego)', async ({ page }) => {
  await partie(page, []);
  const resolue = page.locator('.deroule-phase.est-scene .deroule-rangee .deroule-resultat-texte');
  expect(await jouerJusqua(page, async () => (await titreEst(page, /^manigance$/i)()) && (await resolue.count()) > 0)).toBe(true);
  await mesurer(page, 'etat-05');
});

test('etat 06 : deux sbires, le compteur du temps', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01103')"]);
  const compteur = page.locator('.deroule-phase.est-scene .deroule-pastille.est-courant .deroule-pastille-compteur');
  // ⚠ « 1 / 2 » NE PEUT PAS PARAITRE EN JEU (releve au lot 3) : le compteur
  // compte les ETAPES du temps, et l'etape du second sbire n'existe qu'une
  // fois le premier valide. On capture donc « 2 / 2 ».
  // La question de DEFENSE se pose dans la rangee, pas dans le sous-cadre
  // (lot 4) : attendre aussi qu'aucun choix ne reste (verification du lot 4,
  // mineur 2 : la capture tombait sur la defense du second sbire).
  const question = page.locator('.deroule-phase.est-scene .deroule-sous-cadre, .deroule-phase.est-scene [data-choix]');
  expect(
    await jouerJusqua(
      page,
      async () =>
        (await compteur.count()) > 0 &&
        /\/ 2$/.test((await compteur.textContent()) ?? '') &&
        (await question.count()) === 0
    )
  ).toBe(true);
  await mesurer(page, 'etat-06');
});

test('etat 07 : changement de stade', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", "Puzzle.Damage('01094', 13)"]);
  // La phase du mechant ouverte, le coup qui fait passer le stade : le moteur
  // retient sa trame, la commande passe a la reprise (C33, a relever).
  const ouverte = page.locator('.deroule-phase.est-scene');
  expect(await jouerJusqua(page, async () => (await ouverte.count()) > 0)).toBe(true);
  await commande(page, ["Puzzle.Damage('01094', 1)"]);
  // Une question peut s'ouvrir par-dessus le stade (Sens d'Araignee sur
  // l'attaque suivante) : on la refuse, le stade reste a l'ecran.
  const question = page.locator('.deroule-phase.est-scene .deroule-sous-cadre');
  expect(
    await jouerJusqua(page, async () => (await titreEst(page, /^stade/i)()) && (await question.count()) === 0, 120)
  ).toBe(true);
  await mesurer(page, 'etat-07');
});

test('etat 08 : carte revelee en grand', async ({ page }) => {
  // Carte distribuee : Advance (Traîtrise du set Standard, une menace sur la
  // manigance) ; boost du dessus : « I'm Tough ». Stampede, essayee d'abord,
  // fait attaquer Rhino : sa question de defense passe par-dessus la carte.
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...dessus('01186', '01105')]);
  // ⚠ LE RESUME DE L'EFFET NE PARAIT PAS EN JEU (releve au lot 3) : le fait
  // de revelation est inscrit AVANT l'effet, le clic « Suivant » le valide
  // dans cet etat, et le fait reinscrit apres l'effet garde le meme `etat`
  // (undefined) : le cartouche ne le voit pas changer et passe a l'etape
  // suivante (le bilan, souvent). On capture donc la carte telle que le
  // joueur la voit : en grand, son type, sans resume.
  const grande = page.locator('.deroule-phase.est-scene .deroule-revelee .deroule-carte-grande');
  const question = page.locator('.deroule-phase.est-scene .deroule-sous-cadre');
  expect(
    await jouerJusqua(page, async () => (await grande.count()) > 0 && (await question.count()) === 0, 120)
  ).toBe(true);
  await mesurer(page, 'etat-08');
});

// ETAT 9 (05/10/2026) : Renfort = fleche + case vide « ? » a droite de la carte.
test('etat 09 : Renfort, la carte suivante a cote', async ({ page }) => {
  // Exhaustion (01191) porte Renfort dans le catalogue (mot-cle imprime) : le
  // cartouche montre la fleche et la case vide « ? ». Hard to Keep Down ne
  // convient pas : son Renfort vient d'un effet, pas du catalogue.
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...dessus('01191', '01105')]);
  const renfort = page.locator('.deroule-phase.est-scene .deroule-revelee.a-renfort');
  // Le journal du moteur pendant la revelation, pour savoir s'il a revele la
  // carte suivante par Renfort, et quand (lot 3 : D17 a verifier).
  let releves = 0;
  const journal = async () => {
    const lue = await page.locator('.deroule-corps').first().getAttribute('aria-label', { timeout: 200 }).catch(() => null);
    if (!lue || !/révèle/.test(lue) || releves > 6) return;
    releves += 1;
    const monde = await (await page.request.get('/get_world?hot_seat&p=0')).json();
    const faits = (monde.faits_mechant ?? []).filter((f: { genre?: string }) => f.genre === 'revelation' || f.genre === 'distribution');
    console.log(`  JOURNAL (${lue}) : ${JSON.stringify(faits.map((f: Record<string, unknown>) => [f.genre, f.carte, f.par_surge, f.phase]))}`);
  };
  expect(await jouerJusqua(page, async () => { await journal(); return (await renfort.count()) > 0; }, 200)).toBe(true);
  await mesurer(page, 'etat-09');
});

test('etat 12 : le bilan en trois colonnes', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')"]);
  const bilan = page.locator('.deroule-phase.est-scene .deroule-bilan, .deroule-phase.est-scene .deroule-corps > .deroule-vide');
  expect(await jouerJusqua(page, async () => (await titreEst(page, /^bilan$/i)()) && (await bilan.count()) > 0)).toBe(true);
  await mesurer(page, 'etat-12');
});

// ------------------------------------------------------------------ LOT 4 --
// LES ETATS A QUESTION. Le heros reste en forme heros (Rhino attaque), deux
// allies en jeu pour avoir plusieurs defenseurs. Codes verifies dans
// data/cards.json (piege 48) : Black Widow 01075, Hawkeye 01066, Backflip
// 01003, Enhanced Spider-Sense 01004, Genius 01089, Bomb Scare 01109,
// Explosion 01111, Hydra Bomber 01110, Advance 01186, I'm Tough 01105.
const ALLIES = ["Puzzle.PutIntoPlay('01075', True)", "Puzzle.PutIntoPlay('01066', True)"];
const choixDeLaRangee = (page: Page) => page.locator('.deroule-phase.est-scene .deroule-rangee button.deroule-vignette[data-choix]');
const refusVisible = async (page: Page) => {
  const r = page.locator('.deroule-phase.est-scene [data-refus]').first();
  return (await r.count()) > 0 && (await r.isVisible());
};

test('etat 01 : la question de defense, dans la rangee', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...ALLIES]);
  expect(
    await jouerJusqua(page, async () => (await choixDeLaRangee(page).count()) >= 2 && (await refusVisible(page)))
  ).toBe(true);
  await mesurer(page, 'etat-01', { question: true });
  // La loupe au-dessus du cartouche (D29), sur la meme question.
  await page.locator('.deroule-phase.est-scene .deroule-rangee .deroule-vignette [data-card-id]').first().hover();
  await page.waitForTimeout(200);
  const apercu = await page.evaluate(() => {
    const el = document.querySelector('.carte-apercu.au-dessus-du-deroule');
    const a = el?.getBoundingClientRect();
    const c = document.querySelector('.deroule-phase.est-scene');
    return a && c && el
      ? { haut: Math.round(a.top), bas: Math.round(a.bottom), z: Number(getComputedStyle(el).zIndex), zCarre: Number(getComputedStyle(c).zIndex) || 0 }
      : null;
  });
  console.log(`LOUPE ${JSON.stringify(apercu)}`);
  await page.screenshot({ path: path.join(SORTIE, 'etat-01-loupe.png') });
  expect.soft(apercu, 'aucune loupe devant le carre').not.toBeNull();
  if (apercu) {
    expect.soft(apercu.z, 'la loupe passe derriere le carre').toBeGreaterThan(apercu.zCarre);
    expect.soft(apercu.haut, 'la loupe sort par le haut').toBeGreaterThanOrEqual(0);
  }
});

test('etat 02 : pendant la defense, le defenseur retenu et ses cartes', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...ALLIES, "Puzzle.CreateHandCards('01003')"]);
  // Apres la defense : la question de Backflip (Salto Arriere), dans la rangee
  // si le fait `boosts` est servi, dans le sous-cadre sinon. PAS le Sens
  // d'Araignee, qui vient avant la defense.
  const pendant = async () =>
    (await page.getByRole('button', { name: /^Continuer sans rien jouer/ }).count()) > 0 ||
    (await page.locator('.deroule-phase.est-scene .deroule-sous-cadre.est-reponses [data-choix]')
      .filter({ hasText: /Salto|Backflip/ }).count()) > 0;
  expect(await jouerJusqua(page, pendant, 300, /^Défendre avec Spider-Man/)).toBe(true);
  const avecFait = (await page.getByRole('button', { name: /^Continuer sans rien jouer/ }).count()) > 0;
  console.log(`ETAT 02 : ${avecFait ? 'fait boosts servi, rangee « défend »' : 'SANS FAIT BOOSTS : sous-cadre'}`);
  await mesurer(page, avecFait ? 'etat-02' : 'etat-02-sans-fait-boosts', { question: true });
});

test('etat 10 : la carte revelee pose sa question, a sa droite', async ({ page }) => {
  // Hydra Bomber distribue (« subir 2 degats ou placer 1 menace »), boost I'm Tough.
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...dessus('01110', '01105')]);
  const aDroite = page.locator('.deroule-phase.est-scene .deroule-revelee .deroule-question-carte [data-choix]');
  expect(await jouerJusqua(page, async () => (await aDroite.count()) >= 2)).toBe(true);
  expect.soft(await page.locator('.deroule-phase.est-scene .deroule-sous-cadre').count(), 'un sous-cadre en plus').toBe(0);
  await mesurer(page, 'etat-10', { question: true });
});

test('etat 11a : une interruption dans le sous-cadre (Sens d Araignee)', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...ALLIES]);
  const reponses = page.locator('.deroule-phase.est-scene .deroule-sous-cadre.est-reponses');
  expect(await jouerJusqua(page, async () => (await reponses.count()) > 0)).toBe(true);
  await mesurer(page, 'etat-11a', { question: true });
});

test('etat 11b : un ciblage dans le sous-cadre (Explosion)', async ({ page }) => {
  // Bomb Scare en jeu, Explosion distribuee : « repartis X degats parmi les
  // heros et les allies ». Boost I'm Tough.
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...ALLIES, "Puzzle.PutIntoPlay('01109')", ...dessus('01111', '01105')]);
  const cibles = page.locator('.deroule-phase.est-scene .deroule-sous-cadre.est-cibles');
  expect(await jouerJusqua(page, async () => (await cibles.count()) > 0)).toBe(true);
  expect.soft(await page.locator('.plateau-selecteur').count(), 'le selecteur de cibles hors du cartouche').toBe(0);
  await mesurer(page, 'etat-11b', { question: true });
});

test('etat 11c : un paiement dans le sous-cadre (Enhanced Spider-Sense)', async ({ page }) => {
  // Advance distribuee (une traitrise) : Enhanced Spider-Sense peut l'annuler,
  // et se paie avec Genius.
  await partie(page, ["Puzzle.ChangeForm('01001b')", "Puzzle.CreateHandCards('01004', '01089')", ...dessus('01186', '01105')]);
  const paiement = page.locator('.deroule-phase.est-scene .deroule-sous-cadre.est-paiement');
  // La modale d'accord du paiement automatique, si elle s'ouvre : refusee, pour
  // payer a la main dans le sous-cadre.
  const fini = async () => {
    const modale = page.getByRole('button', { name: /^Non/ }).first();
    if ((await modale.count()) > 0 && (await modale.isVisible())) await modale.click().catch(() => {});
    return (await paiement.count()) > 0;
  };
  expect(await jouerJusqua(page, fini, 300, /amélior|Enhanced/i)).toBe(true);
  expect.soft(await page.locator('.assistant-action').count(), 'l assistant d action hors du cartouche').toBe(0);
  await mesurer(page, 'etat-11c', { question: true });
});

test('etat 14 : un autre joueur choisit (deux sieges)', async ({ page, browser }) => {
  test.setTimeout(600_000);
  // Spider-Man (siege 0, en heros : Rhino l'attaque) et Black Panther (siege
  // 1, la page capturee). Deux pages, une par siege, chacune fait avancer la
  // sienne (piege 49).
  await partie(page, ["Puzzle.ChangeForm('01001b')"], { heros: ['spider_man', 'black_panther'] });
  const ctx = page.context();
  const autre = await ctx.newPage();
  await autre.goto('/app/board.html?p=1&multi=1', { waitUntil: 'networkidle' });
  void browser;
  const attente = autre.locator('.deroule-phase.est-scene .deroule-rangee.est-attente .deroule-pulse');
  const fini = async () => (await attente.count()) > 0;
  let ok = false;
  let vu = '';
  for (let i = 0; i < 120 && !ok; i++) {
    if (await fini()) {
      ok = true;
      break;
    }
    // Le fil des deux sieges, pour relever ou la partie en est (C28).
    const lu = async (p: Page) =>
      (await p.locator('.deroule-phase.est-scene .deroule-corps').first().getAttribute('aria-label', { timeout: 200 }).catch(() => null)) ??
      (await p.locator('.bandeau-tour, .plateau-entete').first().textContent({ timeout: 200 }).catch(() => null)) ??
      '-';
    const monde = (await (await page.request.get('/get_world?hot_seat&p=0')).json().catch(() => ({}))) as { phase?: string; round_id?: number };
    const ligne = `${monde.phase} r${monde.round_id} | siege 0 : ${await lu(page)} | siege 1 : ${await lu(autre)}`;
    if (ligne !== vu) {
      vu = ligne;
      console.log(`  vu : ${ligne}`);
    }
    // Le siege 0 ne repond JAMAIS a sa defense : c'est elle que le siege 1 attend.
    const defenseSiege0 = (await page.getByRole('button', { name: /^Défendre avec/ }).count()) > 0;
    if (!defenseSiege0) await unPas(page, fini);
    await unPas(autre, fini);
    await page.waitForTimeout(200);
  }
  expect(ok, 'le siege 1 ne voit jamais le siege 0 choisir').toBe(true);
  console.log(`ETAT 14 : ${await attente.textContent()}`);
  await mesurer(autre, 'etat-14');
  await autre.close();
});

// ------------------------------------------------------------------ LOT 5 --
// LA RELECTURE (13) ET LE HORS PHASE (15), les variantes Sobre (1 et 8), la
// loupe sur une petite fenetre.

/** Le cartouche est-il sur une etape sans question, une pastille passee a relire ? */
const pastilleARelire = (page: Page) => page.locator('.deroule-phase.est-scene li.deroule-pastille.est-passe button').first();

test('etat 13 : relecture d une pastille passee, pendant la phase', async ({ page }) => {
  // Deux sbires : la pastille ② se relit pendant la ③.
  await partie(page, ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01101')"]);
  const question = page.locator('.deroule-phase.est-scene .deroule-sous-cadre, .deroule-phase.est-scene [data-choix]');
  expect(
    await jouerJusqua(
      page,
      async () =>
        (await titreEst(page, /mercenaire|hydra/i)()) &&
        (await pastilleARelire(page).count()) > 0 &&
        (await question.count()) === 0 &&
        (await page.getByRole('button', { name: /^Suivant \(espace\)/ }).count()) > 0
    )
  ).toBe(true);
  // La derniere pastille passee : celle juste avant l'etape en cours.
  const passees = page.locator('.deroule-phase.est-scene li.deroule-pastille.est-passe button');
  await passees.nth((await passees.count()) - 1).click();
  await expect(page.locator('.deroule-phase.est-scene.est-relecture')).toHaveCount(1);
  await page.waitForTimeout(300);
  const revenir = page.getByRole('button', { name: /^Revenir à / });
  expect.soft(await revenir.count(), 'le bouton « Revenir à … »').toBe(1);
  console.log(`ETAT 13 : ${await revenir.textContent()}`);
  await mesurer(page, 'etat-13');
  // Revenir : l'etape en cours, sans rien valider.
  await revenir.click();
  await expect(page.locator('.deroule-phase.est-scene.est-relecture')).toHaveCount(0);
});

test('etat 13 journal : la phase precedente rouverte depuis le journal', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')"]);
  // Une phase entiere, jusqu'au tour suivant : « Revoir la phase du méchant »
  // n'existe qu'une fois la phase finie.
  const revoir = async () => {
    const tour = (await page.locator('.deroule-phase.est-scene').count()) === 0;
    if (!tour) return false;
    const monde = (await (await page.request.get('/get_world?hot_seat&p=0')).json().catch(() => ({}))) as { phase?: string; round_id?: number };
    return /Player/.test(monde.phase ?? '') && (monde.round_id ?? 0) >= 2;
  };
  expect(await jouerJusqua(page, revoir)).toBe(true);
  await page.locator('.volet-journal-languette').click();
  await page.getByRole('button', { name: 'Revoir la phase du méchant' }).click();
  await expect(page.locator('.deroule-phase.est-scene.est-relecture')).toHaveCount(1);
  await expect(page.locator('.volet-journal')).toHaveCount(0);
  await page.waitForTimeout(300);
  // Les cinq pastilles se relisent ; la deuxieme pour la capture.
  const boutons = page.locator('.deroule-phase.est-scene li.deroule-pastille button');
  expect.soft(await boutons.count(), 'cinq pastilles cliquables').toBe(5);
  await boutons.nth(1).click();
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(SORTIE, 'etat-13-journal.png') });
  const m = await page.evaluate(() => {
    const section = document.querySelector<HTMLElement>('.deroule-phase.est-scene.est-relecture');
    const r = section?.getBoundingClientRect();
    const corps = section?.querySelector<HTMLElement>('.deroule-corps');
    return {
      w: Math.round(r?.width ?? 0), h: Math.round(r?.height ?? 0), largeurEcran: window.innerWidth,
      defile: section ? section.scrollHeight > section.clientHeight : true,
      titre: section?.querySelector('.deroule-titre-court')?.textContent ?? '',
      bandeau: section?.querySelector('.deroule-bandeau')?.textContent ?? '',
      phrase: corps?.getAttribute('aria-label') ?? '',
      boutons: [...(section?.querySelectorAll('.deroule-boutons button') ?? [])].map((b) => b.textContent),
    };
  });
  console.log(`etat-13-journal ${JSON.stringify(m)}`);
  expect.soft(m.w, `largeur ${m.w}`).toBeLessThanOrEqual(m.largeurEcran);
  expect.soft(m.defile, 'defilement').toBe(false);
  expect.soft(m.bandeau).toBe('Relecture');
  expect.soft(m.boutons).toContain('Fermer');
  await page.getByRole('button', { name: 'Fermer' }).click();
  await expect(page.locator('.deroule-phase.est-scene')).toHaveCount(0);
});

// ⚠ LE BAC A SABLE NE SAIT PAS FAIRE REPONDRE UNE QUESTION POSEE PAR SA PROPRE
// COMMANDE (releve au lot 5, 05/10/2026). Une commande `Puzzle.*` s'execute
// DANS l'attente de la question du tour (`DoGetInput`, manager/base.py) : la
// question qu'elle pose (Sens d'Araignee, defense) s'affiche, mais la reponse
// du joueur n'est jamais consommee (POST /post parti, `get_ask` inchange) ; le
// refus du Sens d'Araignee l'est, puis le moteur se fige. Meme blocage avec le
// panneau central d'avant : c'est le harnais, pas le cartouche. La planche
// prend donc trois parties : la question de defense (15), le coup resolu avec
// un defenseur arme d'avance (15b), une carte revelee sans question (15c).
// Spider-Man reste en ALTER EGO (pas de Sens d'Araignee avant la defense, pas
// de `ChangeForm` dont la reponse « Tu fais de la muscu ? » de She-Hulk
// figeait aussi le moteur) : ses deux allies defendent.
const auTourDuJoueur = (page: Page) => async () => {
  const monde = (await (await page.request.get('/get_world?hot_seat&p=0')).json().catch(() => ({}))) as { phase?: string };
  return /^Player/.test(monde.phase ?? '') && (await page.locator('.demande-centrale').count()) === 0;
};

test('etat 15 : pendant ton tour, la question de defense dans le cartouche', async ({ page }) => {
  await partie(page, ALLIES);
  expect(await jouerJusqua(page, auTourDuJoueur(page), 60)).toBe(true);
  await commande(page, ["Puzzle.Attack('01094')"]);
  const horsPhase = page.locator('.deroule-phase.est-scene.est-hors-phase');
  const defense = horsPhase.locator('.deroule-rangee button.deroule-vignette[data-choix]');
  await expect(defense.first()).toBeVisible({ timeout: 15_000 });
  expect.soft(await horsPhase.locator('.deroule-bandeau').textContent()).toBe('Pendant ton tour');
  expect.soft(await page.locator('.demande-centrale').count(), 'le panneau central en double').toBe(0);
  await page.mouse.move(960, 300);
  await page.waitForTimeout(300);
  await mesurer(page, 'etat-15', { question: true });
});

test('etat 15b : pendant ton tour, le coup resolu, puis « Continuer »', async ({ page }) => {
  await partie(page, ALLIES);
  expect(await jouerJusqua(page, auTourDuJoueur(page), 60)).toBe(true);
  // Le defenseur est arme d'avance : aucune question, le coup se resout seul.
  await commande(page, ["Puzzle.Attack('01094', '01075')"]);
  const horsPhase = page.locator('.deroule-phase.est-scene.est-hors-phase');
  const resolu = horsPhase.locator('.deroule-rangee .deroule-resultat-texte');
  await expect(resolu.first()).toBeVisible({ timeout: 15_000 });
  await page.mouse.move(960, 300);
  await page.waitForTimeout(300);
  await mesurer(page, 'etat-15b');
  await horsPhase.getByRole('button', { name: 'Continuer' }).click();
  await expect(horsPhase).toHaveCount(0);
});

test('etat 15c : pendant ton tour, une carte revelee en grand', async ({ page }) => {
  // Sans allie : Black Widow pose une interruption sur une traitrise revelee,
  // et sa reponse figerait le moteur (bac a sable, voir plus haut).
  await partie(page, []);
  expect(await jouerJusqua(page, auTourDuJoueur(page), 60)).toBe(true);
  // Advance (01186) : une menace sur la manigance, aucune question.
  await commande(page, ["Puzzle.Reveal('01186')"]);
  const horsPhase = page.locator('.deroule-phase.est-scene.est-hors-phase');
  await expect(horsPhase.locator('.deroule-revelee .deroule-carte-grande').first()).toBeVisible({ timeout: 15_000 });
  expect.soft(await page.locator('.couche-revelation').count(), 'la revelation en grand en double').toBe(0);
  await page.mouse.move(960, 300);
  await page.waitForTimeout(300);
  await mesurer(page, 'etat-15c');
  expect.soft(await horsPhase.locator('.deroule-revelee .deroule-carte-grande').count(), 'la carte a quitte l ecran sans un clic').toBeGreaterThan(0);
  // Advance fait manigancer Rhino : ce coup-la suit, chacun son « Continuer ».
  for (let i = 0; i < 4 && (await horsPhase.count()) > 0; i++) {
    console.log(`  15c, coup ${i + 1} : ${await horsPhase.locator('.deroule-titre-court').textContent()}`);
    await horsPhase.getByRole('button', { name: 'Continuer' }).click();
    await page.waitForTimeout(400);
  }
  await expect(horsPhase).toHaveCount(0);
});

test('etat 01 sobre : la question de defense, affichage Sobre', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...ALLIES], { sobre: true });
  expect(
    await jouerJusqua(page, async () => (await choixDeLaRangee(page).count()) >= 2 && (await refusVisible(page)))
  ).toBe(true);
  await mesurer(page, 'etat-01-sobre', { question: true });
});

test('etat 08 sobre : carte revelee en grand, affichage Sobre', async ({ page }) => {
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...dessus('01186', '01105')], { sobre: true });
  const grande = page.locator('.deroule-phase.est-scene .deroule-revelee .deroule-carte-grande');
  const question = page.locator('.deroule-phase.est-scene .deroule-sous-cadre');
  expect(
    await jouerJusqua(page, async () => (await grande.count()) > 0 && (await question.count()) === 0, 120)
  ).toBe(true);
  await mesurer(page, 'etat-08-sobre');
});

// D29 : sur une petite fenetre (1009 x 663), la loupe retrecit plutot que de
// sortir par le haut, et reste au-dessus du cadre du cartouche.
test('survol 1009 x 663 : la loupe au-dessus du cartouche, entiere', async ({ page }) => {
  await page.setViewportSize({ width: 1009, height: 663 });
  await partie(page, ["Puzzle.ChangeForm('01001b')", ...ALLIES]);
  expect(
    await jouerJusqua(page, async () => (await choixDeLaRangee(page).count()) >= 2 && (await refusVisible(page)))
  ).toBe(true);
  await page.locator('.deroule-phase.est-scene .deroule-rangee .deroule-vignette [data-card-id]').first().hover();
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(SORTIE, 'survol-petit.png') });
  const m = await page.evaluate(() => {
    const a = document.querySelector('.carte-apercu.au-dessus-du-deroule')?.getBoundingClientRect();
    return a ? { x: Math.round(a.x), y: Math.round(a.y), w: Math.round(a.width), h: Math.round(a.height), largeur: window.innerWidth, hauteur: window.innerHeight } : null;
  });
  console.log(`SURVOL PETIT ${JSON.stringify(m)}`);
  expect(m, 'aucune loupe devant le carre').not.toBeNull();
  if (!m) return;
  expect.soft(m.y, 'la loupe sort par le haut').toBeGreaterThanOrEqual(0);
  expect.soft(m.y + m.h, 'la loupe sort par le bas').toBeLessThanOrEqual(m.hauteur);
  expect.soft(m.x, 'la loupe sort par la gauche').toBeGreaterThanOrEqual(0);
  expect.soft(m.x + m.w, 'la loupe sort par la droite').toBeLessThanOrEqual(m.largeur);
});
