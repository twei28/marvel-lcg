// Fige les nouvelles captures comme images de reference.
//
// C'est la SEULE commande du projet qui a le droit de toucher au dossier
// "references". Elle ne le fait qu'apres que tu aies ecrit OUI en toutes lettres.
//
// Il n'existe volontairement aucun drapeau du genre --yes ou --force : la
// question, c'est justement la fonctionnalite. Si un jour tu la vois passer
// toute seule, c'est un bug.
//
// Aucune dependance : Node tout seul suffit.
import fs from 'node:fs';
import readline from 'node:readline';
import { spawnSync } from 'node:child_process';
import {
  RACINE,
  PAGE_DE_COMPARAISON,
  GABARITS,
  MODE_DEMONSTRATION,
  cheminDeLOutilDeCaptures,
  lireLesEcrans,
  lireLesNouvellesCaptures,
  dateDuDernierResultat,
} from './commun.mjs';

const QUESTION =
  'Tu as bien regardé la page de comparaison et tous ces changements sont voulus ?\n' +
  'Écris OUI en majuscules pour figer les nouvelles images comme référence.\n' +
  'Toute autre réponse annule.\n> ';

function refuser(message) {
  console.error('');
  console.error(message);
  console.error('');
  process.exit(1);
}

// --- Garde-fou 1 : jamais pendant une demonstration ---------------------------
// Sinon on figerait une difference fabriquee de toutes pieces comme etant la
// nouvelle apparence normale du jeu.
if (MODE_DEMONSTRATION) {
  refuser(
    "Le mode démonstration est actif, on ne fige pas une différence factice.\n" +
      'Ferme ce terminal (ou tape : set UI_CHECK_DEMO=) puis recommence.'
  );
}

// --- Garde-fou 2 : la page de comparaison doit exister ------------------------
if (!fs.existsSync(PAGE_DE_COMPARAISON)) {
  refuser(
    "Il n'y a rien à valider : lance d'abord `npm run captures:comparer` " +
      'et regarde la page de comparaison.'
  );
}

// --- Garde-fou 3 : la page doit correspondre a la derniere verification -------
// On ne valide pas des images qu'on n'a pas regardees.
const dateDeLaPage = fs.statSync(PAGE_DE_COMPARAISON).mtimeMs;
if (dateDeLaPage < dateDuDernierResultat()) {
  refuser(
    "La page de comparaison n'est pas à jour. Relance `npm run captures:comparer`."
  );
}

// --- Ce qui va changer --------------------------------------------------------
const ecrans = await lireLesEcrans();
const captures = lireLesNouvellesCaptures();

const titreDeLEcran = new Map(ecrans.map((ecran) => [ecran.cle, ecran.titre]));
const titreDuGabarit = new Map(GABARITS.map((gabarit) => [gabarit.cle, gabarit.titre]));

const aChanger = [];
for (const [identifiant, images] of captures) {
  if (!images.apres) continue;
  const [cle, gabarit] = identifiant.split('/');
  aChanger.push({
    ecran: titreDeLEcran.get(cle) ?? cle,
    gabarit: titreDuGabarit.get(gabarit) ?? gabarit,
  });
}
aChanger.sort((a, b) => a.ecran.localeCompare(b.ecran, 'fr') || a.gabarit.localeCompare(b.gabarit, 'fr'));

if (aChanger.length === 0) {
  console.log('');
  console.log("Aucun écran n'a changé : il n'y a rien à figer.");
  console.log('');
  process.exit(0);
}

console.log('');
console.log('Les images de référence suivantes vont être remplacées :');
console.log('');
for (const ligne of aChanger) {
  console.log(`  - ${ligne.ecran} (${ligne.gabarit})`);
}
console.log('');
console.log(`Soit ${aChanger.length} image(s). Les autres écrans ne bougeront pas.`);
console.log('');

// --- La question --------------------------------------------------------------
// On passe par l'ancienne forme de readline (avec fonction de rappel) : la forme
// "promise" ne se termine jamais quand l'entree est fermee sans reponse, et le
// script resterait bloque. Ici, entree fermee = refus.
function poserLaQuestion(texte) {
  return new Promise((resoudre) => {
    const dialogue = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    let aRepondu = false;
    dialogue.question(texte, (reponse) => {
      aRepondu = true;
      dialogue.close();
      resoudre(reponse);
    });
    dialogue.on('close', () => {
      if (!aRepondu) resoudre('');
    });
  });
}

const reponse = await poserLaQuestion(QUESTION);

if (reponse.trim() !== 'OUI') {
  console.log('');
  console.log("Annulé : aucune référence n'a été modifiée.");
  console.log('');
  process.exit(0);
}

// --- Seulement maintenant : on fige ------------------------------------------
const cli = cheminDeLOutilDeCaptures();

function lancerLesCaptures(argumentsEnPlus) {
  return spawnSync(
    process.execPath,
    [cli, 'test', 'tests/captures.spec.ts', ...argumentsEnPlus],
    { cwd: RACINE, stdio: 'inherit' }
  ).status;
}

console.log('');
console.log('Enregistrement des nouvelles images de référence...\n');
if (lancerLesCaptures(['--update-snapshots=changed']) !== 0) {
  refuser(
    "L'enregistrement s'est mal passé. Regarde le message rouge ci-dessus.\n" +
      'Vérifie ensuite avec `npm run captures` où en sont les images.'
  );
}

console.log('');
console.log('Contre-vérification...\n');
if (lancerLesCaptures([]) !== 0) {
  refuser(
    "Les images viennent d'être enregistrées, mais la vérification qui suit n'est\n" +
      "pas verte. C'est le signe d'un écran instable (une animation, une date, un\n" +
      'nombre tiré au hasard). Signale-le : il faut le neutraliser avant de figer.'
  );
}

console.log('');
console.log("C'est figé. Les nouvelles images sont maintenant la référence.");
console.log('');
console.log(
  'La page de comparaison que tu viens de regarder est maintenant périmée :\n' +
    'relance `npm run captures:comparer` si tu veux la revoir.'
);
console.log('');
