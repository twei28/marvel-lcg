// La langue de la PAGE (pas de la carte) : l'anglais par defaut, le francais d'un clic.
//
// Le code ecrit ses textes en francais ; ce module les traduit a la volee : il parcourt les textes et les attributs (title, placeholder,
// aria-label) de la page, et un observateur traduit tout ce qui apparait ensuite. En francais il ne touche a rien. Une chaine absente du
// dictionnaire reste telle quelle (le test de la page liste celles qui manquent).

export const DICO = {
  // en-tete
  'Créateur de cartes': 'Card Maker',
  'Langue de la carte': 'Card language',
  'Texte, libellé du type et traits en français': 'Text, type label and traits in French',
  'Texte, libellé du type et traits en anglais': 'Text, type label and traits in English',
  'Annuler (Ctrl+Z)': 'Undo (Ctrl+Z)',
  'Rétablir (Ctrl+Y)': 'Redo (Ctrl+Y)',
  "⬇ Exporter l'image": '⬇ Export image',
  '⬇ FR + EN': '⬇ FR + EN',
  'Une image dans chaque langue (traits traduits)': 'One image per language (traits translated)',
  '🖨 Imprimer / PDF': '🖨 Print / PDF',
  'Planche à imprimer (63 × 88 mm) ou à enregistrer en PDF': 'Print sheet (63 × 88 mm) or save as PDF',
  '🎲 Planche TTS': '🎲 TTS sheet',
  'Planche de cartes pour Tabletop Simulator (10 colonnes)': 'Card sheet for Tabletop Simulator (10 columns)',
  // colonne de gauche
  'Cartes': 'Cards',
  '+ Nouvelle': '+ New',
  'Dupliquer': 'Duplicate',
  'Supprimer': 'Delete',
  'Chercher une carte…': 'Search cards…',
  'Chercher une carte': 'Search cards',
  'Aucune carte ne correspond.': 'No card matches.',
  'Sans dossier': 'No folder',
  'Modèles': 'Templates',
  'Enregistrer': 'Save',
  'Utiliser': 'Use',
  'Garder la carte actuelle (couleurs, nombres, mise en page) comme modèle': 'Keep the current card (colours, numbers, layout) as a template',
  'Nouvelle carte à partir du modèle choisi': 'New card from the chosen template',
  'Projet': 'Project',
  'Enregistrer (.json)': 'Save (.json)',
  'Versions…': 'Versions…',
  'Les versions gardées automatiquement': 'The versions kept automatically',
  'Chercher / remplacer…': 'Find / replace…',
  'Chercher et remplacer un mot sur une carte, un dossier ou tout le projet': 'Find and replace a word on a card, a folder or the whole project',
  'Appliquer au dossier…': 'Apply to folder…',
  'Recopier couleurs, cadre, mention… sur les autres cartes du dossier': 'Copy colours, frame, credit line… to the other cards of the folder',
  'Importer…': 'Import…',
  'Nos fichiers .json, ou ceux du Card Maker de Landstander (carte .json ou « Save .zip »)': 'Our .json files, or those of Landstander’s Card Maker (a card .json or “Save .zip”)',
  'Les cartes sont gardées dans ce navigateur. Enregistre un fichier pour les sauvegarder ou les passer à un autre appareil. « Importer » lit aussi les fichiers (.json ou .zip) du Card Maker de Landstander.': 'Your cards are kept in this browser. Save a file to back them up or move them to another device. “Import” also reads the files (.json or .zip) of Landstander’s Card Maker.',
  // formulaire
  'Type de carte': 'Card type',
  'Dossier (un héros, un set…)': 'Folder (a hero, a set…)',
  'Texte': 'Text',
  'Titre': 'Title',
  'Carte unique (✦)': 'Unique card (✦)',
  'Libellé du type (vide = automatique)': 'Type label (empty = automatic)',
  'Traits (séparés par des points)': 'Traits (separated by full stops)',
  'Règles': 'Rules text',
  'Citation': 'Flavor text',
  'Étape du méchant (I, II, A, B…)': 'Villain stage (I, II, A, B…)',
  'Ligne d’ensemble': 'Set line',
  'Créateur / mention': 'Creator / credit line',
  'Taille des règles et de la citation': 'Size of rules and flavor text',
  'Automatique (réduit pour tenir)': 'Automatic (shrinks to fit)',
  'automatique': 'automatic',
  'Nombres': 'Numbers',
  'Coût': 'Cost',
  'Contrer / manigance (THW / SCH)': 'Thwart / scheme (THW / SCH)',
  'Attaque (ATK)': 'Attack (ATK)',
  'Défense (DEF)': 'Defense (DEF)',
  'Récupération (REC)': 'Recover (REC)',
  'Points de vie': 'Hit points',
  'Taille de main': 'Hand size',
  'Menace de départ': 'Starting threat',
  'Menace cible': 'Target threat',
  'Accélération': 'Acceleration',
  'Attachement : bonus d’attaque': 'Attachment: attack bonus',
  'Attachement : bonus de manigance': 'Attachment: scheme bonus',
  'Phase : numéro': 'Phase: number',
  'Phase : lettre': 'Phase: letter',
  'Dégâts conséquents (contrer)': 'Consequential damage (thwart)',
  'Dégâts conséquents (attaque)': 'Consequential damage (attack)',
  'Dégâts conséquents': 'Consequential damage',
  'Renforts et ressources': 'Boost and resources',
  'Icônes de renfort': 'Boost icons',
  'Ressource 1': 'Resource 1',
  'Ressource 2': 'Resource 2',
  'Ressource 3': 'Resource 3',
  'Aucune': 'None',
  'Énergie': 'Energy',
  'Mental': 'Mental',
  'Physique': 'Physical',
  'Joker': 'Wild',
  'Étoile': 'Star',
  'Crise': 'Crisis',
  'Danger': 'Hazard',
  'Renfort': 'Boost',
  'Par héros': 'Per hero',
  'Unique': 'Unique',
  'Amplification': 'Amplify',
  'Infini': 'Infinity',
  // barre de mise en forme
  'Gras (Ctrl+B)': 'Bold (Ctrl+B)',
  'Italique (Ctrl+I)': 'Italic (Ctrl+I)',
  'Souligné (Ctrl+U)': 'Underline (Ctrl+U)',
  'Taille': 'Size',
  'Taille de la sélection': 'Size of the selection',
  '100 % (normale)': '100 % (normal)',
  'Couleur de la sélection': 'Colour of the selection',
  'Police des traits': 'Traits font',
  'Retirer la mise en forme de la sélection': 'Clear formatting of the selection',
  'Voir / modifier le code (balises)': 'View / edit the code (tags)',
  'Saut de paragraphe': 'Paragraph break',
  'Filet horizontal': 'Horizontal rule',
  'Gras': 'Bold',
  'Italique': 'Italic',
  'Trait': 'Trait',
  // couleurs
  'Couleurs': 'Colours',
  'Préréglage': 'Preset',
  '— couleurs du gabarit —': '— template colours —',
  'Aspects': 'Aspects',
  'Héros': 'Heroes',
  'Méchants et rencontres': 'Villains and encounters',
  'Basic (gris)': 'Basic (grey)',
  'Agression': 'Aggression',
  'Direction': 'Leadership',
  'Revenir aux couleurs du gabarit': 'Back to the template colours',
  'Gauche': 'Left',
  'Gauche (accent)': 'Left (accent)',
  'Droite': 'Right',
  'Droite (accent)': 'Right (accent)',
  'Séparateur': 'Divider',
  'Cases claires': 'Light boxes',
  'Éclat de la tête': 'Head splash',
  'Fond (haut)': 'Background (top)',
  'Fond (bas)': 'Background (bottom)',
  'Ombrage': 'Shading',
  'Milieu': 'Middle',
  'Contour': 'Outline',
  'Accent': 'Accent',
  'Fissures': 'Cracks',
  // illustration, tete, calques
  'Illustration': 'Artwork',
  'Image derrière la carte': 'Image behind the card',
  'Premier plan (devant le cadre)': 'Foreground (in front of the frame)',
  'Zoom': 'Zoom',
  'Décalage X': 'Offset X',
  'Décalage Y': 'Offset Y',
  'Rotation (°)': 'Rotation (°)',
  'Rotation': 'Rotation',
  'Déplacer à la souris': 'Move with the mouse',
  'Retirer': 'Remove',
  'Tête d’angle': 'Corner headshot',
  'Image de la tête (cadrage carré)': 'Headshot image (square crop)',
  'Afficher la tête': 'Show the headshot',
  'Éclat en étoile': 'Star splash',
  'Calques PNG': 'PNG layers',
  'Ajouter des PNG (ou glisse-les sur l’aperçu)': 'Add PNGs (or drop them on the preview)',
  'Aucun calque. Ajoute un PNG (ou glisse-le sur l’aperçu) ou prends une icône dans la bibliothèque.': 'No layers yet. Add a PNG (or drop one on the preview) or pick an icon from the library.',
  'Bibliothèque (icônes, formes, images du jeu)': 'Library (icons, shapes, game images)',
  'Icônes du jeu': 'Game icons',
  'Formes (teintables)': 'Shapes (tintable)',
  'Images du jeu': 'Game images',
  'Rond': 'Circle',
  'Carré arrondi': 'Rounded square',
  'Bandeau': 'Banner',
  'Losange': 'Diamond',
  'Bulle': 'Speech bubble',
  'Explosion': 'Burst',
  'Ressource énergie': 'Energy resource',
  'Ressource mental': 'Mental resource',
  'Ressource physique': 'Physical resource',
  'Ressource joker': 'Wild resource',
  'Icône de renfort': 'Boost icon',
  'Étoile de renfort': 'Boost star',
  'Monter': 'Move up',
  'Descendre': 'Move down',
  'Afficher / masquer': 'Show / hide',
  'Nom': 'Name',
  'Position': 'Position',
  'Derrière le cadre': 'Behind the frame',
  'Devant le cadre': 'In front of the frame',
  'Au-dessus du texte': 'Above the text',
  'Opacité': 'Opacity',
  'Miroir ↔': 'Flip ↔',
  'Miroir ↕': 'Flip ↕',
  'Teinte': 'Tint',
  'Couleur de la teinte': 'Tint colour',
  'Couleur du contour': 'Outline colour',
  'Épaisseur du contour': 'Outline thickness',
  'Ombre': 'Shadow',
  'Couleur de l’ombre': 'Shadow colour',
  'Flou de l’ombre': 'Shadow blur',
  'Centrer': 'Centre',
  'Remettre droit': 'Straighten',
  // style du cadre
  'Style du cadre': 'Frame style',
  'Style': 'Style',
  'Officiel (gabarit du jeu)': 'Official (game template)',
  'Cadre sombre': 'Dark frame',
  'Pleine illustration (sans cadre)': 'Full artwork (no frame)',
  'Fissures dans le cadre': 'Cracks in the frame',
  '« Cadre sombre » remplace les couleurs par un gris-bleu foncé avec des accents dorés (tu peux encore les modifier dans Couleurs). « Pleine illustration » enlève le cadre : l’image remplit la carte et le texte repose sur des panneaux translucides.': '“Dark frame” replaces the colours with a dark blue-grey and gold accents (you can still change them under Colours). “Full artwork” removes the frame: the image fills the card and the text sits on translucent panels.',
  // apercu
  'Glisse sur l\'aperçu pour déplacer l\'illustration ou un calque, molette pour zoomer. Glisse-y des images pour les ajouter.': 'Drag on the preview to move the artwork or a layer, mouse wheel to zoom. Drop images on it to add them.',
  'Glisse sur l’aperçu pour déplacer l’illustration (molette : zoom).': 'Drag on the preview to move the artwork (wheel: zoom).',
  'Glisse sur l’aperçu pour déplacer le premier plan (molette : zoom).': 'Drag on the preview to move the foreground (wheel: zoom).',
  'Glisse sur l’aperçu pour déplacer la tête d’angle (molette : zoom).': 'Drag on the preview to move the headshot (wheel: zoom).',
  // types de carte
  'Allié': 'Ally', 'Événement': 'Event', 'Amélioration': 'Upgrade', 'Soutien': 'Support', 'Ressource': 'Resource', 'Alter-ego': 'Alter-Ego',
  'Identité de héros': 'Hero identity', 'Obligation (héros)': 'Obligation (hero)', 'Manigance annexe de joueur': 'Player side scheme',
  'Méchant': 'Villain', 'Sbire': 'Minion', 'Trahison': 'Treachery', 'Environnement': 'Environment', 'Attachement': 'Attachment',
  'Manigance annexe': 'Side scheme', 'Manigance principale (face A)': 'Main scheme (side A)', 'Manigance principale (face B)': 'Main scheme (side B)',
  'Obligation (rencontre)': 'Obligation (encounter)', 'Promo générique': 'Generic promo', 'Promo générique (verticale)': 'Generic promo (vertical)',
  'Promo alter-ego': 'Alter-ego promo', 'Promo héros': 'Hero promo', 'Paquet de départ': 'Starter deck',
  // dialogues
  'Fermer': 'Close', 'Annuler': 'Cancel', 'Appliquer': 'Apply', 'Exporter': 'Export', 'Format': 'Format',
  'Chercher / remplacer': 'Find / replace', 'Chercher': 'Find', 'Remplacer par': 'Replace with', 'Texte à chercher': 'Text to find',
  'Respecter les majuscules': 'Match case', 'Mot entier seulement': 'Whole word only', 'Où': 'Where', 'Cette carte': 'This card',
  'Tout le dossier de cette carte': 'The whole folder of this card', 'Toutes les cartes': 'All cards', 'Dans quels champs :': 'In which fields:',
  'Mention du créateur': 'Credit line', 'Tout remplacer': 'Replace all',
  'Appliquer à tout le dossier': 'Apply to the whole folder', 'Cartes concernées': 'Cards affected',
  'Les couleurs (et le préréglage)': 'Colours (and preset)', 'Le style de cadre': 'Frame style', 'Fissures du cadre': 'Frame cracks',
  'La mention du créateur': 'The credit line', 'La langue (traits et textes par défaut traduits)': 'The language (traits and default texts translated)',
  'La taille des règles (réglage manuel)': 'The rules text size (manual setting)',
  'Réglages de la tête d’angle (zoom, position, étoile)': 'Corner headshot settings (zoom, position, star)',
  'Versions gardées': 'Saved versions', 'Restaurer': 'Restore',
  'Restaurer remplace le projet actuel (qui est gardé comme version avant de le faire). Les 10 dernières versions sont conservées.': 'Restoring replaces the current project (which is saved as a version first). The 10 latest versions are kept.',
  'Aucune version gardée pour le moment. Une version est gardée toutes les 5 minutes de travail, et quand tu fermes la page.': 'No saved version yet. A version is saved every 5 minutes of work, and when you close the page.',
  'Exporter l’image': 'Export image', 'JPEG': 'JPEG',
  'Fond perdu de 3 mm (bords étirés)': '3 mm bleed (edges stretched)',
  'Annulé.': 'Undone.', 'Rétabli.': 'Redone.', 'Rien à annuler.': 'Nothing to undo.', 'Rien à rétablir.': 'Nothing to redo.',
  'Rien à remplacer.': 'Nothing to replace.', 'Modèle enregistré.': 'Template saved.', 'Choisis d’abord un modèle.': 'Pick a template first.',
  'Version restaurée.': 'Version restored.', 'Export…': 'Exporting…', 'Export terminé.': 'Export finished.',
  'Nom du modèle': 'Template name', '(sans titre)': '(untitled)', 'Nom de la carte': 'Card name',
  'Aucune carte portrait à mettre sur la planche.': 'No portrait card to put on the sheet.',
  'Préparation de la planche…': 'Preparing the sheet…', 'Préparation de la planche TTS…': 'Preparing the TTS sheet…',
  'Le navigateur a bloqué la fenêtre d’impression.': 'The browser blocked the print window.',
  // styles de texte
  'Styles': 'Styles', 'Déclencheurs': 'Triggers', 'Capacité nommée': 'Named ability', 'Mots-clés': 'Keywords', 'Limites': 'Limits', 'Mise en forme': 'Formatting', 'Mes styles': 'My styles',
  'Texte d’ambiance ou rappel (italique)': 'Flavor or reminder text (italic)', 'Trait (police des traits)': 'Trait (traits font)', 'Mot en gras': 'Bold word',
  'Ligne « Boost » avec étoile': '“Boost” line with star', 'Mots-clés avec leur rappel': 'Keywords with their reminder text', 'Aucun résultat.': 'No match.',
  'Créer un style…': 'Create a style…', 'Gérer mes styles…': 'Manage my styles…', 'Aucun style pour le moment.': 'No style yet.', 'Nouveau style': 'New style',
  'Nom du style': 'Style name', 'Créer': 'Create', 'ex. Mot-clé maison': 'e.g. House keyword', 'Souligné': 'Underlined', 'Police des traits': 'Traits font',
  'Couleur': 'Colour', 'Styles de texte : menu, ou tape « / » dans le texte': 'Text styles: menu, or type “/” in the text',
  // recadrage
  'Détourer / recadrer…': 'Cut out / crop…', 'Détourer et recadrer': 'Cut out and crop', 'Original (clique sur le fond pour le choisir)': 'Original (click the background to pick it)',
  'Résultat': 'Result', 'Retirer le fond': 'Remove the background', 'Tolérance': 'Tolerance', 'Rogner sur le sujet': 'Crop to the subject',
  'Cadrer en carré (tête d’angle)': 'Make it square (corner headshot)', 'Clique pour choisir la couleur du fond à retirer': 'Click to pick the background colour to remove',
  // lisibilite
  'Le titre est vide.': 'The title is empty.',
  'Le texte déborde du cadre, même réduit : raccourcis les règles ou la citation.': 'The text overflows the frame even when shrunk: shorten the rules or the flavor text.',
  'Pas de texte de règles.': 'No rules text.',
}

// Les messages qui portent un nombre ou un nom : [expression, remplacement].
const MOTIFS = [
  [/^(\d+) carte\(s\) importée\(s\)\.$/, '$1 card(s) imported.'],
  [/^(\d+) carte\(s\) mise\(s\) à jour\.$/, '$1 card(s) updated.'],
  [/^(\d+) remplacement\(s\) dans (\d+) carte\(s\)\.$/, '$1 replacement(s) in $2 card(s).'],
  [/^(\d+) occurrence\(s\) dans (\d+) carte\(s\)\.$/, '$1 match(es) in $2 card(s).'],
  [/^(.+) · (FR|EN)$/, null], // type de carte + langue : le type est traduit
  [/^— modèles \((\d+)\) —$/, '— templates ($1) —'],
  [/^(\d+) % \(normale\)$/, '$1 % (normal)'],
  [/^Planche TTS : (\d+) carte\(s\), (\d+) colonnes \(taille de cellule (\d+) × (\d+)\)\.$/, 'TTS sheet: $1 card(s), $2 columns (cell size $3 × $4).'],
  [/^(.+) · (\d+) carte\(s\)$/, '$1 · $2 card(s)'],
  [/^Largeur \(px\) — taille d’origine (\d+)$/, 'Width (px) — original size $1'],
  [/^Recopie ces réglages de « (.*) » sur les autres cartes\.$/, 'Copy these settings from “$1” to the other cards.'],
  [/^Le texte est réduit à (\d+) % pour tenir : il sera petit à l’impression\.$/, 'The text is shrunk to $1 % to fit: it will be small in print.'],
  [/^Taille du texte réglée à (\d+) % : très petit\.$/, 'Text size set to $1 %: very small.'],
  [/^(Le titre|Une ligne) est réduit à (\d+) % : plus court, ce sera plus lisible\.$/, (m, qui, n) => `${qui === 'Le titre' ? 'The title' : 'A line'} is shrunk to ${n} %: shorter text will be easier to read.`],
  [/^(L’illustration|Le premier plan) est petite \((\d+) × (\d+)\) : elle sera floue à l’impression \(carte : (\d+) × (\d+)\)\.$/, (m, qui, w, h, cw, ch) => `${qui === 'L’illustration' ? 'The artwork' : 'The foreground'} is small (${w} × ${h}): it will look blurry in print (card: ${cw} × ${ch}).`],
  [/^Sauvegarde dans le navigateur impossible : (.*)$/, 'Could not save in the browser: $1'],
  [/^Rendu impossible : (.*)$/, 'Could not render: $1'],
  [/^Ouverture impossible : (.*)$/, 'Could not open: $1'],
  [/^Démarrage impossible : (.*)$/, 'Could not start: $1'],
  [/^Supprimer « (.*) » \?$/, 'Delete “$1”?'],
  [/^aucune carte reconnue dans ces fichiers$/, 'no card recognised in these files'],
  [/^(\S+) \((\d+) × (\d+)\)$/, null],
]

let langue = 'en'
const originaux = new WeakMap() // noeud (ou [element, attribut]) -> texte francais d'origine
const ATTRS = ['title', 'placeholder', 'aria-label']

/** Le texte dans la langue de la page. */
export function t(fr) {
  if (langue !== 'en' || typeof fr !== 'string') return fr
  const net = fr.replace(/\s+/g, ' ').trim()
  if (!net) return fr
  // les alertes commencent par une pastille (⚠ / ℹ) : on traduit le reste
  const pastille = /^([⚠ℹ] )(.+)$/u.exec(net)
  if (pastille) { const r = t(pastille[2]); return r === pastille[2] ? fr : fr.replace(net, pastille[1] + r) }
  let en = DICO[net]
  if (en === undefined) {
    for (const [re, rep] of MOTIFS) {
      const m = re.exec(net)
      if (!m) continue
      if (rep === null) {
        if (m[2] === 'FR' || m[2] === 'EN') en = `${DICO[m[1]] ?? m[1]} · ${m[2]}`
        else continue
      } else en = typeof rep === 'function' ? rep(...m) : net.replace(re, rep)
      break
    }
  }
  if (en === undefined) return fr
  // on garde les espaces de bord du texte d'origine
  return fr.replace(net, en)
}

function traduireNoeud(n) {
  if (n.nodeType === 3) {
    if (n.parentElement?.closest('script,style,.editeur,textarea')) return
    // on retient le texte d'origine ET ce qu'on y a ecrit : si le noeud contient autre chose, c'est un nouveau texte
    let m = originaux.get(n)
    if (!m || n.textContent !== m.sortie) originaux.set(n, (m = { src: n.textContent, sortie: n.textContent }))
    const sortie = langue === 'en' ? t(m.src) : m.src
    m.sortie = sortie
    if (n.textContent !== sortie) n.textContent = sortie
  } else if (n.nodeType === 1) {
    if (n.matches?.('script,style,.editeur')) return
    for (const a of ATTRS) {
      if (!n.hasAttribute?.(a)) continue
      let m = originaux.get(n)
      if (!m) originaux.set(n, (m = {}))
      const actuel = n.getAttribute(a)
      if (!m[a] || actuel !== m[a].sortie) m[a] = { src: actuel, sortie: actuel }
      const sortie = langue === 'en' ? t(m[a].src) : m[a].src
      m[a].sortie = sortie
      if (actuel !== sortie) n.setAttribute(a, sortie)
    }
    for (const c of n.childNodes) traduireNoeud(c)
  }
}

let observateur = null
export function appliquer(racine = document.body) {
  document.documentElement.lang = langue
  traduireNoeud(racine)
}

export const langueUI = () => langue

/** Demarre le traducteur ; `choix` : 'en' (defaut) ou 'fr'. */
export function demarrerI18n(choix) {
  langue = choix === 'fr' ? 'fr' : 'en'
  appliquer()
  if (observateur) return
  observateur = new MutationObserver((muts) => {
    observateur.disconnect()
    for (const m of muts) {
      if (m.type === 'characterData') traduireNoeud(m.target)
      else if (m.type === 'attributes') traduireNoeud(m.target)
      else for (const n of m.addedNodes) traduireNoeud(n)
    }
    observateur.observe(document.body, OPTIONS)
  })
  observateur.observe(document.body, OPTIONS)
}
const OPTIONS = { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS }

export function changerLangueUI(choix) {
  langue = choix === 'fr' ? 'fr' : 'en'
  try { localStorage.setItem('createur-langue-ui', langue) } catch {}
  appliquer()
}

/** La langue choisie la derniere fois (anglais par defaut). */
export function langueMemorisee() {
  try { return localStorage.getItem('createur-langue-ui') === 'fr' ? 'fr' : 'en' } catch { return 'en' }
}
