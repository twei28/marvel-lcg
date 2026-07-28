// Les quelques fonctions partagees par comparer.mjs et valider.mjs.
//
// Il n'y a rien a regler ici : c'est de la plomberie (lire la liste des ecrans,
// retrouver les images produites par la derniere verification).
//
// Aucune dependance : Node tout seul suffit.
import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';

const ICI = path.dirname(url.fileURLToPath(import.meta.url));

export const RACINE = path.resolve(ICI, '..');
export const DOSSIER_REFERENCES = path.join(RACINE, 'references');
export const DOSSIER_RESULTATS = path.join(RACINE, 'test-results');
export const DOSSIER_SORTIE = path.join(RACINE, 'comparaison');
export const PAGE_DE_COMPARAISON = path.join(DOSSIER_SORTIE, 'index.html');

// Les 3 formats d'ecran, avec le nom qu'on affiche a l'utilisateur.
// L'ordre de cette liste est l'ordre d'affichage.
export const GABARITS = [
  { cle: 'pc', titre: 'Ordinateur' },
  { cle: 'tablette', titre: 'Tablette' },
  { cle: 'mobile', titre: 'Téléphone' },
];

// Le mode demonstration provoque expres une difference sur tous les ecrans.
export const MODE_DEMONSTRATION = Boolean(process.env.UI_CHECK_DEMO);

// Chemin du programme de captures (Playwright), lance en sous-processus.
export function cheminDeLOutilDeCaptures() {
  const cli = path.join(RACINE, 'node_modules', '@playwright', 'test', 'cli.js');
  if (!fs.existsSync(cli)) {
    console.error(
      "L'outil de captures n'est pas installé.\n" +
        'Ouvre un terminal dans le dossier ui-check et tape : npm install'
    );
    process.exit(1);
  }
  return cli;
}

// ---------------------------------------------------------------------------
// La liste des ecrans : ecrans.ts est le seul fichier qui fait foi.
// ---------------------------------------------------------------------------

export async function lireLesEcrans() {
  const chemin = path.join(RACINE, 'ecrans.ts');
  if (!fs.existsSync(chemin)) {
    console.error(`Fichier introuvable : ${chemin}`);
    process.exit(1);
  }

  // Node sait lire le TypeScript directement depuis la version 22.18.
  try {
    const module = await import(url.pathToFileURL(chemin).href);
    if (Array.isArray(module.ECRANS) && module.ECRANS.length > 0) {
      return module.ECRANS.map((ecran) => ({ cle: ecran.cle, titre: ecran.titre }));
    }
  } catch {
    // Version de Node plus ancienne : on retombe sur une lecture du fichier.
  }

  const source = fs.readFileSync(chemin, 'utf8');
  const motif = /\bcle:\s*'([^']+)'\s*,\s*titre:\s*'([^']+)'/g;
  const ecrans = [];
  let trouve;
  while ((trouve = motif.exec(source)) !== null) {
    ecrans.push({ cle: trouve[1], titre: trouve[2] });
  }
  if (ecrans.length === 0) {
    console.error(`Impossible de lire la liste des écrans dans ${chemin}.`);
    process.exit(1);
  }
  return ecrans;
}

// ---------------------------------------------------------------------------
// Les images produites par la derniere verification
// ---------------------------------------------------------------------------

export function* fichiersRecursifs(dossier) {
  if (!fs.existsSync(dossier)) return;
  for (const entree of fs.readdirSync(dossier, { withFileTypes: true })) {
    const complet = path.join(dossier, entree.name);
    if (entree.isDirectory()) yield* fichiersRecursifs(complet);
    else yield complet;
  }
}

// Playwright range ses fichiers dans test-results/<titre-du-test>-<gabarit>/.
// On repere donc le gabarit par la FIN du nom de dossier, pas par un chemin exact.
export function gabaritDuDossier(nomDeDossier) {
  const trouve = GABARITS.find((gabarit) => nomDeDossier.endsWith(`-${gabarit.cle}`));
  return trouve ? trouve.cle : null;
}

// Renvoie une table : "<ecran>/<gabarit>" -> { apres, difference }
// Un ecran n'y figure QUE s'il a change : Playwright n'ecrit ces fichiers que
// pour les captures qui ne correspondent plus a leur reference.
export function lireLesNouvellesCaptures() {
  const captures = new Map();
  for (const fichier of fichiersRecursifs(DOSSIER_RESULTATS)) {
    const nom = path.basename(fichier);
    let suffixe = null;
    if (nom.endsWith('-actual.png')) suffixe = 'apres';
    else if (nom.endsWith('-diff.png')) suffixe = 'difference';
    else continue;

    const gabarit = gabaritDuDossier(path.basename(path.dirname(fichier)));
    if (!gabarit) continue;

    const cle = nom.replace(/-(actual|diff)\.png$/, '');
    const identifiant = `${cle}/${gabarit}`;
    const entree = captures.get(identifiant) ?? {};
    entree[suffixe] = fichier;
    captures.set(identifiant, entree);
  }
  return captures;
}

// Date de modification la plus recente dans test-results/ (0 si le dossier est vide).
export function dateDuDernierResultat() {
  let plusRecente = 0;
  for (const fichier of fichiersRecursifs(DOSSIER_RESULTATS)) {
    const date = fs.statSync(fichier).mtimeMs;
    if (date > plusRecente) plusRecente = date;
  }
  return plusRecente;
}
