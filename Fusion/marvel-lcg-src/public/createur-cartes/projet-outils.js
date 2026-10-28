// Les outils qui travaillent sur plusieurs cartes ou sur le projet entier : versions, chercher / remplacer, appliquer a tout le dossier,
// modeles, controle de lisibilite.
import { dialogue, el, S, nouvelId } from './commun.js'
import { ajouterVersion, listerVersions } from './stockage.js'

// ---------------------------------------------------------------- versions
const dateFr = (t) => new Date(t).toLocaleString('fr-BE', { dateStyle: 'short', timeStyle: 'medium' })

/** La liste des versions gardees ; `restaurer(projet)` remplace le projet (apres avoir garde l'actuel). */
export async function ouvrirVersions(restaurer) {
  const versions = await listerVersions()
  const liste = el('div', { class: 'liste', style: 'max-height:50vh' })
  if (!versions.length) liste.append(el('div', { class: 'aide' }, 'Aucune version gardée pour le moment. Une version est gardée toutes les 5 minutes de travail, et quand tu fermes la page.'))
  for (const v of versions) {
    liste.append(el('div', { class: 'rang', style: 'align-items:center' },
      el('span', { style: 'flex:2' }, `${dateFr(v.date)} · ${v.nb} carte(s)`, el('small', { style: 'color:var(--doux);display:block' }, v.raison === 'auto' ? 'automatique' : v.raison)),
      el('button', {
        class: 'btn petit fixe', type: 'button', onclick: async (e) => {
          await ajouterVersion(S.projet(), 'avant restauration')
          restaurer(v.projet)
          e.target.closest('dialog').close()
        },
      }, 'Restaurer')))
  }
  dialogue('Versions gardées', el('div', {}, el('div', { class: 'aide' }, 'Restaurer remplace le projet actuel (qui est gardé comme version avant de le faire). Les 10 dernières versions sont conservées.'), liste))
}

// ---------------------------------------------------------------- chercher / remplacer
const CHAMPS_TEXTE = [['titre', 'Titre'], ['regles', 'Règles'], ['citation', 'Citation'], ['traits', 'Traits'], ['ligneEnsemble', 'Ligne d’ensemble'], ['createur', 'Mention du créateur']]
const echapperRe = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

/** Remplace dans le texte visible seulement : les balises (<b>...) et les icones ([energy]) ne sont jamais touchees. */
export function remplacerDansTexte(html, re, par) {
  let n = 0
  const sortie = String(html ?? '').split(/(<[^>]*>|\[[a-z_]+\])/i).map((seg, i) => (i % 2 ? seg : seg.replace(re, () => { n++; return par })))
  return { texte: sortie.join(''), n }
}

export function ouvrirRemplacer() {
  const cherche = el('input', { type: 'text', placeholder: 'Texte à chercher' })
  const par = el('input', { type: 'text', placeholder: 'Remplacer par' })
  const casse = el('input', { type: 'checkbox' })
  const mot = el('input', { type: 'checkbox' })
  const portee = el('select', {}, el('option', { value: 'carte' }, 'Cette carte'), el('option', { value: 'dossier' }, 'Tout le dossier de cette carte'), el('option', { value: 'tout' }, 'Toutes les cartes'))
  portee.value = 'dossier'
  const cases = CHAMPS_TEXTE.map(([k, n]) => ({ k, i: el('input', { type: 'checkbox', checked: k !== 'createur' }), n }))
  const bilan = el('div', { class: 'aide', 'aria-live': 'polite' })
  const cartesVisees = () => {
    const c = S.carte()
    const toutes = S.projet().cartes
    return portee.value === 'carte' ? [c] : portee.value === 'dossier' ? toutes.filter((x) => (x.dossier || '') === (c.dossier || '')) : toutes
  }
  const regle = () => {
    if (!cherche.value) return null
    const sourceRe = (mot.checked ? '(?<![\\p{L}\\p{N}])' : '') + echapperRe(cherche.value) + (mot.checked ? '(?![\\p{L}\\p{N}])' : '')
    return new RegExp(sourceRe, 'gu' + (casse.checked ? '' : 'i'))
  }
  const compter = (appliquer) => {
    const re = regle()
    if (!re) return { n: 0, cartes: 0 }
    let n = 0
    let cartes = 0
    for (const c of cartesVisees()) {
      let dans = 0
      for (const { k, i } of cases) {
        if (!i.checked) continue
        const r = remplacerDansTexte(c.contenu[k], re, par.value)
        dans += r.n
        if (appliquer && r.n) c.contenu[k] = r.texte
      }
      if (dans) cartes++
      n += dans
    }
    return { n, cartes }
  }
  const maj = () => { const r = compter(false); bilan.textContent = cherche.value ? `${r.n} occurrence(s) dans ${r.cartes} carte(s).` : '' }
  for (const x of [cherche, casse, mot, portee, ...cases.map((c) => c.i)]) x.addEventListener('input', maj)
  dialogue('Chercher / remplacer',
    el('div', { class: 'contenu', style: 'display:flex;flex-direction:column;gap:8px' },
      el('label', {}, 'Chercher', cherche), el('label', {}, 'Remplacer par', par),
      el('label', { class: 'ligne' }, casse, 'Respecter les majuscules'), el('label', { class: 'ligne' }, mot, 'Mot entier seulement'),
      el('label', {}, 'Où', portee),
      el('div', { class: 'aide' }, 'Dans quels champs :'),
      el('div', { class: 'rang' }, cases.map((c) => el('label', { class: 'ligne', style: 'min-width:140px' }, c.i, c.n))),
      bilan),
    [{ texte: 'Fermer' }, {
      texte: 'Tout remplacer', principal: true, action: () => {
        const r = compter(true)
        S.message(r.n ? `${r.n} remplacement(s) dans ${r.cartes} carte(s).` : 'Rien à remplacer.')
        S.changement()
        S.reconstruire()
        return true
      },
    }])
}

// ---------------------------------------------------------------- appliquer a tout le dossier
export function ouvrirAppliquer(rolesDe) {
  const src = S.carte()
  const portee = el('select', {}, el('option', { value: 'dossier' }, 'Tout le dossier de cette carte'), el('option', { value: 'tout' }, 'Toutes les cartes'))
  const choix = [
    ['couleurs', 'Les couleurs (et le préréglage)'], ['cadre', 'Le style de cadre'], ['fissures', 'Fissures du cadre'], ['createur', 'La mention du créateur'],
    ['langue', 'La langue (traits et textes par défaut traduits)'], ['echelle', 'La taille des règles (réglage manuel)'], ['tete', 'Réglages de la tête d’angle (zoom, position, étoile)'],
  ].map(([k, n]) => ({ k, n, i: el('input', { type: 'checkbox' }) }))
  dialogue('Appliquer à tout le dossier',
    el('div', { class: 'contenu', style: 'display:flex;flex-direction:column;gap:8px' },
      el('div', { class: 'aide' }, `Recopie ces réglages de « ${src.contenu.titre || 'cette carte'} » sur les autres cartes.`),
      el('label', {}, 'Cartes concernées', portee),
      ...choix.map((c) => el('label', { class: 'ligne' }, c.i, c.n))),
    [{ texte: 'Annuler' }, {
      texte: 'Appliquer', principal: true, action: async () => {
        const cibles = S.projet().cartes.filter((x) => x.id !== src.id && (portee.value === 'tout' || (x.dossier || '') === (src.dossier || '')))
        const actifs = new Set(choix.filter((c) => c.i.checked).map((c) => c.k))
        for (const x of cibles) {
          if (actifs.has('couleurs')) {
            const roles = new Set(rolesDe(S.types[x.type]))
            x.couleurs = Object.fromEntries(Object.entries(src.couleurs).filter(([r]) => roles.has(r)))
            x.preset = src.preset
          }
          if (actifs.has('cadre')) x.cadre = src.cadre
          if (actifs.has('fissures')) x.fissures = src.fissures
          if (actifs.has('createur')) x.contenu.createur = src.contenu.createur
          if (actifs.has('langue') && x.langue !== src.langue) await S.changerLangueDe(x, src.langue)
          if (actifs.has('echelle')) x.contenu.echelleTexte = src.contenu.echelleTexte
          if (actifs.has('tete')) x.tete = { ...x.tete, zoom: src.tete.zoom, x: src.tete.x, y: src.tete.y, etoile: src.tete.etoile, rotation: src.tete.rotation, afficher: src.tete.afficher }
        }
        S.message(`${cibles.length} carte(s) mise(s) à jour.`)
        S.changement()
        S.reconstruire()
      },
    }])
}

// ---------------------------------------------------------------- modeles
/** Garde la carte comme modele (sans son identite : titre, dossier). */
export function enregistrerModele(nom) {
  const p = S.projet()
  p.modeles ??= []
  const c = structuredClone(S.carte())
  delete c.id
  p.modeles.push({ id: nouvelId(), nom: nom || c.contenu.titre || 'Modèle', carte: c })
}

// ---------------------------------------------------------------- lisibilite
/** Les alertes d'un rendu : [{ niveau: 'alerte' | 'info', texte }]. */
export function alertesLisibilite(carte, spec, infos, images) {
  const a = []
  const ct = carte.contenu
  if (!ct.titre?.trim()) a.push({ niveau: 'alerte', texte: 'Le titre est vide.' })
  if (infos?.deborde) a.push({ niveau: 'alerte', texte: 'Le texte déborde du cadre, même réduit : raccourcis les règles ou la citation.' })
  else if (infos && infos.facteurTexte < 0.85 && !(Number(ct.echelleTexte) > 0)) a.push({ niveau: infos.facteurTexte < 0.65 ? 'alerte' : 'info', texte: `Le texte est réduit à ${Math.round(infos.facteurTexte * 100)} % pour tenir : il sera petit à l’impression.` })
  if (Number(ct.echelleTexte) > 0 && Number(ct.echelleTexte) < 0.65) a.push({ niveau: 'info', texte: `Taille du texte réglée à ${Math.round(Number(ct.echelleTexte) * 100)} % : très petit.` })
  for (const l of infos?.lignesReduites ?? []) if (l.facteur < 0.7) a.push({ niveau: 'info', texte: `${l.cls === 'title' ? 'Le titre' : 'Une ligne'} est réduit à ${Math.round(l.facteur * 100)} % : plus court, ce sera plus lisible.` })
  for (const [nom, im] of [['L’illustration', images.art], ['Le premier plan', images.artDevant]]) {
    if (im && (im.naturalWidth < spec.largeur * 0.6 || im.naturalHeight < spec.hauteur * 0.6)) a.push({ niveau: 'info', texte: `${nom} est petite (${im.naturalWidth} × ${im.naturalHeight}) : elle sera floue à l’impression (carte : ${spec.largeur} × ${spec.hauteur}).` })
  }
  const pasTexte = !(ct.regles || '').replace(/<[^>]*>/g, '').trim() && spec.elements.some((e) => e.cls === 'rules')
  if (pasTexte && !['starter-deck'].includes(carte.type)) a.push({ niveau: 'info', texte: 'Pas de texte de règles.' })
  return a
}
