// Fabrique la page de comparaison "avant / apres".
//
// Ce script fait deux choses, dans cet ordre :
//   1. il relance la verification des ecrans (les captures) ;
//   2. il fabrique la page "comparaison/index.html", a ouvrir dans le navigateur.
//
// La page montre TOUS les ecrans, pas seulement ceux qui ont change : quand tout
// va bien, on voit la liste complete avec la mention "Aucun changement".
//
// Ce script ne modifie JAMAIS le dossier "references". Figer de nouvelles images
// de reference, c'est le role de "npm run captures:valider", et seulement apres
// que tu aies ecrit OUI.
//
// Aucune dependance : Node tout seul suffit.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import {
  RACINE,
  DOSSIER_REFERENCES,
  DOSSIER_SORTIE,
  PAGE_DE_COMPARAISON as PAGE,
  GABARITS,
  MODE_DEMONSTRATION,
  cheminDeLOutilDeCaptures,
  lireLesEcrans,
  lireLesNouvellesCaptures,
} from './commun.mjs';

const DOSSIER_IMAGES = path.join(DOSSIER_SORTIE, 'images');

// ---------------------------------------------------------------------------
// 1. Relancer la verification des ecrans
// ---------------------------------------------------------------------------

function relancerLesCaptures() {
  const cli = cheminDeLOutilDeCaptures();
  console.log('Vérification des écrans en cours (une petite minute)...\n');
  const resultat = spawnSync(process.execPath, [cli, 'test', 'tests/captures.spec.ts'], {
    cwd: RACINE,
    stdio: 'inherit',
  });
  // Un ecran qui a change fait "echouer" la verification : ce n'est pas une
  // erreur du script, c'est justement ce qu'on veut regarder dans la page.
  return resultat.status === 0;
}

// ---------------------------------------------------------------------------
// 2. Construire le modele de la page
// ---------------------------------------------------------------------------

function copierImage(source, nomDeDestination) {
  const destination = path.join(DOSSIER_IMAGES, nomDeDestination);
  fs.copyFileSync(source, destination);
  return `images/${nomDeDestination}`;
}

function construireLeModele(ecrans, captures) {
  const sections = [];
  let nombreDeCouples = 0;
  let nombreDeChangements = 0;

  for (const ecran of ecrans) {
    const lignes = [];
    for (const gabarit of GABARITS) {
      const reference = path.join(DOSSIER_REFERENCES, ecran.cle, `${gabarit.cle}.png`);
      const nouvelle = captures.get(`${ecran.cle}/${gabarit.cle}`);
      const referenceExiste = fs.existsSync(reference);

      // Un gabarit sans reference ni nouvelle capture n'existe tout simplement pas.
      if (!referenceExiste && !nouvelle) continue;
      nombreDeCouples += 1;

      const prefixe = `${ecran.cle}--${gabarit.cle}`;
      const ligne = { gabarit: gabarit.titre, aChange: Boolean(nouvelle?.apres) };

      if (referenceExiste) ligne.avant = copierImage(reference, `${prefixe}--avant.png`);
      if (nouvelle?.apres) ligne.apres = copierImage(nouvelle.apres, `${prefixe}--apres.png`);
      if (nouvelle?.difference) {
        ligne.difference = copierImage(nouvelle.difference, `${prefixe}--difference.png`);
      }

      if (ligne.aChange) nombreDeChangements += 1;
      lignes.push(ligne);
    }
    if (lignes.length > 0) sections.push({ titre: ecran.titre, lignes });
  }

  return { sections, nombreDeCouples, nombreDeChangements };
}

// ---------------------------------------------------------------------------
// 3. Ecrire la page
// ---------------------------------------------------------------------------

function echapper(texte) {
  return String(texte)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const STYLE = `
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0 24px 64px;
  font-family: "Segoe UI", system-ui, -apple-system, Arial, sans-serif;
  color: #1c1f26; background: #f4f5f7; line-height: 1.5;
}
header { max-width: 1400px; margin: 0 auto; padding: 32px 0 8px; }
h1 { font-size: 28px; margin: 0 0 4px; }
.date { color: #5a6172; font-size: 14px; margin: 0 0 20px; }
.mode-emploi {
  max-width: 1400px; margin: 0 auto 24px; background: #fff; border: 1px solid #dfe2e8;
  border-radius: 10px; padding: 16px 20px;
}
.mode-emploi p { margin: 6px 0; }
.mode-emploi code {
  background: #eef0f4; border-radius: 4px; padding: 2px 6px; font-size: 14px;
}
.bilan {
  max-width: 1400px; margin: 0 auto 8px; font-size: 20px; font-weight: 600;
  padding: 14px 20px; border-radius: 10px;
}
.bilan.calme { background: #e6f6ec; color: #17603a; border: 1px solid #b7e2c7; }
.bilan.alerte { background: #fdeeea; color: #8c2f18; border: 1px solid #f4c4b6; }
.demonstration {
  max-width: 1400px; margin: 0 auto 24px; background: #fff8e1; border: 1px solid #f0d99a;
  border-radius: 10px; padding: 14px 20px; color: #6b5316;
}
section {
  max-width: 1400px; margin: 0 auto 28px; background: #fff; border: 1px solid #dfe2e8;
  border-radius: 12px; padding: 8px 24px 24px;
}
h2 { font-size: 22px; margin: 20px 0 4px; }
.ligne { border-top: 1px solid #eceef2; padding: 18px 0 4px; }
.ligne:first-of-type { border-top: none; }
.entete-ligne { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.entete-ligne h3 { font-size: 17px; margin: 0; font-weight: 600; }
.badge { font-size: 13px; font-weight: 600; border-radius: 999px; padding: 3px 12px; }
.badge.calme { background: #e6f6ec; color: #17603a; border: 1px solid #b7e2c7; }
.badge.alerte { background: #fdeeea; color: #8c2f18; border: 1px solid #f4c4b6; }
.trio { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
figure { margin: 0; }
figcaption { font-size: 14px; color: #5a6172; margin-bottom: 6px; font-weight: 600; }
.cadre {
  border: 1px solid #dfe2e8; border-radius: 8px; overflow: hidden; background: #fbfbfc;
  max-height: 60vh; overflow-y: auto;
}
.cadre img { display: block; width: 100%; height: auto; }
.seule .cadre { max-width: 640px; }
.superposition-bloc { margin-top: 18px; }
.superposition {
  position: relative; border: 1px solid #dfe2e8; border-radius: 8px; overflow: hidden;
  max-height: 70vh; overflow-y: auto; background: #fbfbfc;
}
.superposition .dessous { display: block; width: 100%; height: auto; }
.superposition .dessus { position: absolute; top: 0; left: 0; width: 100%; height: auto; }
.reglage { display: flex; align-items: center; gap: 12px; margin-top: 10px; font-size: 14px; color: #5a6172; }
.reglage input { flex: 1; }
a.agrandir { font-size: 13px; color: #2a63c4; text-decoration: none; }
a.agrandir:hover { text-decoration: underline; }
`;

function rendreLigne(ligne, numero) {
  const badge = ligne.aChange
    ? '<span class="badge alerte">A changé</span>'
    : '<span class="badge calme">Aucun changement</span>';

  const entete =
    `<div class="entete-ligne"><h3>${echapper(ligne.gabarit)}</h3>${badge}</div>`;

  if (!ligne.aChange) {
    if (!ligne.avant) {
      return `<div class="ligne">${entete}<p>Aucune image disponible pour ce format.</p></div>`;
    }
    return (
      `<div class="ligne">${entete}` +
      `<div class="seule"><div class="cadre"><img src="${ligne.avant}" alt="${echapper(ligne.gabarit)}"></div>` +
      `<p><a class="agrandir" href="${ligne.avant}" target="_blank">Voir en grand</a></p></div>` +
      `</div>`
    );
  }

  const vignette = (source, legende) =>
    source
      ? `<figure><figcaption>${legende}</figcaption>` +
        `<div class="cadre"><img src="${source}" alt="${legende}"></div>` +
        `<a class="agrandir" href="${source}" target="_blank">Voir en grand</a></figure>`
      : `<figure><figcaption>${legende}</figcaption>` +
        `<div class="cadre"><p style="padding:16px">Pas d'image : cet écran n'avait pas encore de référence.</p></div></figure>`;

  const trio =
    `<div class="trio">` +
    vignette(ligne.avant, 'Avant (référence)') +
    vignette(ligne.apres, 'Après (nouvelle capture)') +
    vignette(ligne.difference, 'Ce qui a changé') +
    `</div>`;

  const superposition =
    ligne.avant && ligne.apres
      ? `<div class="superposition-bloc">` +
        `<div class="superposition">` +
        `<img class="dessous" src="${ligne.avant}" alt="Avant">` +
        `<img class="dessus" id="dessus-${numero}" src="${ligne.apres}" alt="Après">` +
        `</div>` +
        `<label class="reglage">Avant` +
        `<input type="range" min="0" max="100" value="100" data-cible="dessus-${numero}">` +
        `Après</label>` +
        `<p style="font-size:14px;color:#5a6172;margin:4px 0 0">` +
        `Fais glisser le curseur pour passer de l'ancienne image à la nouvelle, au même endroit.</p>` +
        `</div>`
      : '';

  return `<div class="ligne">${entete}${trio}${superposition}</div>`;
}

function rendreLaPage(modele) {
  const { sections, nombreDeCouples, nombreDeChangements } = modele;
  const maintenant = new Date().toLocaleString('fr-FR', {
    dateStyle: 'full',
    timeStyle: 'short',
  });

  const bilan =
    nombreDeChangements === 0
      ? `<div class="bilan calme">Aucun écran n'a changé : les ${nombreDeCouples} images sont identiques aux références.</div>`
      : `<div class="bilan alerte">${nombreDeChangements} écran${nombreDeChangements > 1 ? 's' : ''} sur ${nombreDeCouples} ${nombreDeChangements > 1 ? 'ont' : 'a'} changé.</div>`;

  const banniereDemonstration = MODE_DEMONSTRATION
    ? `<div class="demonstration"><strong>Mode démonstration.</strong> La différence que tu vois ci-dessous a été provoquée exprès, pour te montrer à quoi ressemble un changement détecté. Il n'y a rien à corriger et surtout rien à valider.</div>`
    : '';

  let numero = 0;
  const corps = sections
    .map((section) => {
      const lignes = section.lignes.map((ligne) => rendreLigne(ligne, numero++)).join('\n');
      return `<section><h2>${echapper(section.titre)}</h2>\n${lignes}</section>`;
    })
    .join('\n');

  return `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Comparaison des écrans - avant / après</title>
<style>${STYLE}</style>
</head>
<body>
<header>
  <h1>Comparaison des écrans &mdash; avant / après</h1>
  <p class="date">Vérification du ${echapper(maintenant)}</p>
</header>

<div class="mode-emploi">
  <p><strong>Ce que tu regardes :</strong> chaque écran du jeu, dans les 3 formats (ordinateur, tablette, téléphone), tel qu'il était avant et tel qu'il est maintenant.</p>
  <p><strong>Si tout va bien :</strong> ferme cette page, il n'y a rien à valider.</p>
  <p><strong>Si un changement est voulu :</strong> lance la commande <code>npm run captures:valider</code> dans le dossier ui-check et écris OUI.</p>
</div>

${banniereDemonstration}
${bilan}

${corps}

<script>
document.querySelectorAll('input[type=range][data-cible]').forEach(function (curseur) {
  var cible = document.getElementById(curseur.dataset.cible);
  if (!cible) return;
  var appliquer = function () { cible.style.opacity = String(curseur.value / 100); };
  curseur.addEventListener('input', appliquer);
  appliquer();
});
</script>
</body>
</html>
`;
}

// ---------------------------------------------------------------------------
// Deroule
// ---------------------------------------------------------------------------

const toutEtaitVert = relancerLesCaptures();

if (!fs.existsSync(DOSSIER_REFERENCES)) {
  console.error(
    "Le dossier des images de référence n'existe pas encore.\n" +
      'Il faut avoir lancé la vérification des écrans au moins une fois.'
  );
  process.exit(1);
}

const ecrans = await lireLesEcrans();
const captures = lireLesNouvellesCaptures();

// Le dossier de sortie est entierement refait a chaque fois : pas de vieille
// image qui traine et qui ferait croire a un changement qui n'existe plus.
if (path.basename(DOSSIER_SORTIE) !== 'comparaison') {
  throw new Error('Garde-fou : refus de supprimer un dossier autre que "comparaison".');
}
fs.rmSync(DOSSIER_SORTIE, { recursive: true, force: true });
fs.mkdirSync(DOSSIER_IMAGES, { recursive: true });

const modele = construireLeModele(ecrans, captures);
fs.writeFileSync(PAGE, rendreLaPage(modele), 'utf8');

console.log('');
console.log('-------------------------------------------------------------');
if (modele.nombreDeChangements === 0) {
  console.log(`Aucun écran n'a changé : les ${modele.nombreDeCouples} images sont identiques.`);
} else {
  console.log(
    `${modele.nombreDeChangements} écran(s) sur ${modele.nombreDeCouples} ont changé.`
  );
}
console.log('');
console.log('La page de comparaison est prête :');
console.log(`  ${PAGE}`);
console.log('');
console.log('Pour l\'ouvrir, tape :');
console.log(`  start "" "${PAGE}"`);
console.log('-------------------------------------------------------------');

if (!toutEtaitVert && modele.nombreDeChangements === 0) {
  // Cas rare : la verification a echoue pour une autre raison qu'une image
  // (page introuvable, jeu eteint...). Mieux vaut le dire franchement.
  console.log('');
  console.log(
    "Attention : la vérification s'est arrêtée sur une erreur qui n'est pas une\n" +
      "différence d'image. Regarde le message rouge plus haut dans le terminal."
  );
  process.exit(1);
}
