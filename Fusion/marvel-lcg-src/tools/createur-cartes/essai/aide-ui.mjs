// Gestes communs aux scripts Chromium du createur (interface du 30/10/2026 : page des dossiers, editeur d'un dossier, wizard).
// La page est en anglais par defaut : les libelles cherches sont les anglais.
export const att = (p, ms = 500) => p.waitForTimeout(ms)

/** Attend que la page soit prete (l'accueil des dossiers est affiche). */
export async function attendreAccueil(p) { await p.waitForSelector('#vue-accueil:not([hidden]) #grilles'); await att(p, 800) }
/** Depuis l'accueil : cree un dossier VIDE et l'ouvre. genre : « Heroes » | « Scenario » | « Modular » (les trois tuiles de cartes). */
export async function dossierVide(p, nom, genre = 'Heroes') {
  const cle = { Heroes: 'heros', Scenario: 'scenario', Modular: 'modulaire' }[genre] ?? genre
  await p.click(`.tuile-creer.cartes[data-creer="${cle}"]`); await att(p, 300)
  await p.fill('dialog[open] input', nom)
  await p.click('dialog[open] button:has-text("Empty folder")'); await att(p, 700)
}
/** Dans l'editeur : une carte vide, sans wizard (le lien du bas de la premiere etape). */
export async function carteVide(p) {
  await p.click('#c-nouvelle'); await att(p, 500)
  await p.click('dialog[open] button.lien'); await att(p, 700)
}
export async function versAccueil(p) { await p.click('#fil button:has-text("Folders")'); await att(p, 700) }
export async function ouvrirTuile(p, nom) { await p.click(`.tuile:has-text("${nom}")`); await att(p, 900) }
/** Les rubriques du formulaire sont repliees a l'ouverture d'une carte : on les ouvre pour agir dedans. */
export const ouvrirSections = (p) => p.evaluate(() => document.querySelectorAll('#champs details').forEach((d) => { d.open = true }))
/** Toutes les cartes du projet (la liste ne montre que le dossier ouvert). */
export const nbCartes = (p) => p.evaluate(() => Number(document.querySelector('#liste')?.dataset.total ?? 0))
/** Les exports sont dans le menu « Export ▾ » du bandeau : on l'ouvre, puis on clique l'entree voulue (selecteur du bouton). */
export async function exporterVia(p, selecteur) { await p.click('#b-exporter'); await p.click(selecteur) }
