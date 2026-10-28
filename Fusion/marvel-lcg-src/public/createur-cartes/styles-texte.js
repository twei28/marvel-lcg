// Les styles de texte « en un clic » : declencheurs (Hero Action, Forced Response...), capacites nommees, mots-cles avec leur rappel,
// limites, mise en forme, et les styles de l'utilisateur. Les mots viennent de NOTRE catalogue (donnees/styles-texte.json, produit par
// tools/createur-cartes/extraire-styles.py a partir des cartes officielles anglaises et de leur texte francais) : rien n'est devine.
//
// Deux facons de les choisir : le menu « Styles » (apercu de chaque ligne) et la saisie rapide « / » (liste qu'on filtre en tapant).
import { dialogue, el, S } from './commun.js'

let DONNEES = null
export async function chargerStyles(dossier = 'donnees/') {
  DONNEES ??= await (await fetch(dossier + 'styles-texte.json')).json()
  return DONNEES
}

const sansAccent = (t) => String(t).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
const DEUX_POINTS = { en: ': ', fr: ' : ' }
// sur les cartes, les declencheurs « forces » et le Boost sont precedes d'une etoile
const AVEC_ETOILE = /^(Forced |Boost)/

const LIMITES = {
  en: ['(Limit once per round.)', '(Limit once per phase.)', '(Limit once per round per player.)', '(Limit once per card.)'],
  fr: ['(Limite d’une fois par round.)', '(Limite d’une fois par phase.)', '(Limite d’une fois par round et par joueur.)', '(Limite d’une fois par carte.)'],
}
const TRIGGERS_NOMMES = ['Hero Action', 'Alter-Ego Action', 'Hero Response', 'Alter-Ego Response', 'Hero Interrupt', 'Alter-Ego Interrupt', 'Action', 'Response', 'Interrupt']

/**
 * Le catalogue dans une langue : [{ groupe, titre, apercu (HTML de la carte), html (a inserer) | format ('i' | 'em' | ...) | perso }].
 * `avecRappel` : les mots-cles s'inserent avec leur rappel en italique.
 */
export function catalogue(langue, { avecRappel = true, perso = [] } = {}) {
  const l = langue === 'fr' ? 'fr' : 'en'
  // les titres de groupe sont ceux de la PAGE (traduits par i18n.js), pas de la carte
  const G = { decl: 'Déclencheurs', nomme: 'Capacité nommée', mots: 'Mots-clés', limites: 'Limites', format: 'Mise en forme', perso: 'Mes styles' }
  const liste = []
  const decl = new Map((DONNEES?.declencheurs ?? []).map((d) => [d.en, d]))
  const motDecl = (d, k = 0) => (l === 'fr' ? d.fr[Math.min(k, d.fr.length - 1)] : d.en)
  for (const d of decl.values()) {
    const variantes = l === 'fr' ? d.fr.length : 1
    for (let k = 0; k < variantes; k++) {
      const mot = motDecl(d, k)
      const etoile = AVEC_ETOILE.test(d.en) ? '[star] ' : ''
      const prec = l === 'fr' && d.en === 'When Defeated' ? (k === 0 ? ' (manigance)' : ' (méchant, sbire)') : ''
      liste.push({ groupe: G.decl, titre: mot + prec, apercu: `${etoile}<b>${mot}</b>${DEUX_POINTS[l]}`, html: `${etoile}<b>${mot}</b>${DEUX_POINTS[l]}` })
    }
  }
  for (const nom of TRIGGERS_NOMMES) {
    const d = decl.get(nom)
    if (!d) continue
    const mot = motDecl(d)
    const modele = l === 'fr' ? 'Nom' : 'Ability name'
    liste.push({ groupe: G.nomme, titre: `${modele} — ${mot}`, apercu: `<i>${modele}</i> — <b>${mot}</b>${DEUX_POINTS[l]}`, nomme: (n) => `<i>${n || modele}</i> — <b>${mot}</b>${DEUX_POINTS[l]}` })
  }
  for (const m of DONNEES?.motsCles ?? []) {
    const mot = (l === 'fr' ? m.motFr : m.motEn).replace(/X/g, '1')
    const rappel = (l === 'fr' ? m.rappelFr : m.rappelEn).replace(/\bX\b/g, '1')
    liste.push({ groupe: G.mots, titre: mot.replace(/\.$/, ''), apercu: mot + (rappel ? ` ${rappel}` : ''), html: mot + (avecRappel && rappel ? ` ${rappel}` : '') + ' ' })
  }
  for (const t of LIMITES[l]) liste.push({ groupe: G.limites, titre: t, apercu: `<i>${t}</i>`, html: `<i>${t}</i> ` })
  liste.push(
    { groupe: G.format, titre: 'Texte d’ambiance ou rappel (italique)', apercu: `<i>${l === 'fr' ? 'italique' : 'italic'}</i>`, format: 'i' },
    { groupe: G.format, titre: 'Trait (police des traits)', apercu: '<em>TRAIT.</em>', format: 'em' },
    { groupe: G.format, titre: 'Mot en gras', apercu: '<b>Bold</b>', format: 'b' },
    { groupe: G.format, titre: 'Ligne « Boost » avec étoile', apercu: `[star] <b>Boost</b>${DEUX_POINTS[l]}`, html: `[star] <b>Boost</b>${DEUX_POINTS[l]}` }
  )
  for (const p of perso) liste.push({ groupe: G.perso, titre: p.nom, apercu: `<span style="${cssPerso(p)}">${p.nom}</span>`, perso: p })
  return liste
}

/** Le CSS (pour l'apercu) et le mini-HTML d'un style perso. */
export function cssPerso(p) {
  return [p.b ? 'font-weight:700' : '', p.i ? 'font-style:italic' : '', p.u ? 'text-decoration:underline' : '', p.taille && p.taille !== 1 ? `font-size:${p.taille}em` : '', p.couleur ? `color:${p.couleur}` : ''].filter(Boolean).join(';')
}
export function enveloppePerso(p, texte) {
  let h = texte
  const css = []
  if (p.taille && p.taille !== 1) css.push(`font-size:${p.taille}em`)
  if (p.couleur) css.push(`color:${p.couleur}`)
  if (css.length) h = `<span style="${css.join(';')}">${h}</span>`
  if (p.trait) h = `<em>${h}</em>`
  if (p.u) h = `<u>${h}</u>`
  if (p.i) h = `<i>${h}</i>`
  if (p.b) h = `<b>${h}</b>`
  return h
}

/** Fenetre de creation d'un style perso. */
export function creerStylePerso(apres) {
  const nom = el('input', { type: 'text', placeholder: 'ex. Mot-clé maison' })
  const cases = ['b', 'i', 'u', 'trait'].map((k) => ({ k, i: el('input', { type: 'checkbox' }), n: { b: 'Gras', i: 'Italique', u: 'Souligné', trait: 'Police des traits' }[k] }))
  const taille = el('select', {}, [0.7, 0.85, 1, 1.25, 1.5, 2].map((v) => el('option', { value: v }, Math.round(v * 100) + ' %')))
  taille.value = '1'
  const couleur = el('input', { type: 'color', value: '#000000' })
  const avecCouleur = el('input', { type: 'checkbox' })
  dialogue('Nouveau style', el('div', { class: 'contenu', style: 'display:flex;flex-direction:column;gap:8px' },
    el('label', {}, 'Nom du style', nom), ...cases.map((c) => el('label', { class: 'ligne' }, c.i, c.n)),
    el('label', {}, 'Taille', taille), el('div', { class: 'rang' }, el('label', { class: 'ligne' }, avecCouleur, 'Couleur'), couleur)),
  [{ texte: 'Annuler' }, {
    texte: 'Créer', principal: true, action: () => {
      if (!nom.value.trim()) return false
      const p = { id: Math.random().toString(36).slice(2, 8), nom: nom.value.trim(), taille: Number(taille.value), couleur: avecCouleur.checked ? couleur.value : null }
      for (const c of cases) p[c.k] = c.i.checked
      apres(p)
    },
  }])
}

/**
 * Branche le menu « Styles » et la saisie « / » sur un editeur riche.
 * `api` : { zone, langue(), perso(), ajouterPerso(p), supprimerPerso(id), inserer(htmlCarte), nommee(htmlCarte), format(nom), enveloppe(p), pousse() }
 */
export function brancherStyles(conteneur, api) {
  const popup = el('div', { class: 'popup-styles', hidden: true, role: 'listbox' })
  conteneur.style.position = 'relative'
  conteneur.append(popup)
  let avecRappel = true
  let items = []
  let actif = 0
  let mode = null // 'menu' | 'slash'
  let slash = null // { noeud, debut, fin }

  const fermer = () => { popup.hidden = true; mode = null; slash = null }
  const appliquer = (it) => {
    if (slash) {
      // on retire le « /mot » tape avant d'appliquer
      const r = document.createRange()
      r.setStart(slash.noeud, slash.debut)
      r.setEnd(slash.noeud, slash.fin)
      r.deleteContents()
      const s = getSelection()
      s.removeAllRanges()
      s.addRange(r)
    }
    api.zone.focus()
    if (it.html) api.inserer(it.html)
    else if (it.nomme) api.nommee(it.nomme)
    else if (it.format) api.format(it.format)
    else if (it.perso) api.enveloppe(it.perso)
    api.pousse()
    fermer()
  }
  const dessiner = (filtre = '') => {
    const f = sansAccent(filtre)
    const tous = catalogue(api.langue(), { avecRappel, perso: api.perso() })
    items = tous.filter((it) => !f || sansAccent(it.titre).includes(f) || sansAccent(it.groupe).includes(f))
    actif = Math.min(actif, Math.max(0, items.length - 1))
    popup.replaceChildren()
    if (mode === 'menu') {
      const c = el('input', { type: 'checkbox', checked: avecRappel })
      c.addEventListener('change', () => { avecRappel = c.checked; dessiner(filtre) })
      popup.append(el('label', { class: 'ligne rappel-option', onmousedown: (e) => e.stopPropagation() }, c, 'Mots-clés avec leur rappel'))
    }
    let groupe = null
    items.forEach((it, i) => {
      if (it.groupe !== groupe) { groupe = it.groupe; popup.append(el('div', { class: 'groupe-styles' }, groupe)) }
      const ligne = el('div', { class: 'item-style' + (i === actif ? ' actif' : ''), role: 'option', onmousedown: (e) => { e.preventDefault(); appliquer(it) } },
        el('span', { class: 'titre-style' }, it.titre), el('span', { class: 'apercu-style', 'data-apercu': it.apercu }))
      popup.append(ligne)
    })
    for (const a of popup.querySelectorAll('.apercu-style')) a.innerHTML = apercuHtml(a.dataset.apercu)
    if (mode === 'menu') {
      popup.append(el('div', { class: 'item-style perso', onmousedown: (e) => { e.preventDefault(); fermer(); creerStylePerso((p) => { api.ajouterPerso(p) }) } }, '+ ' + 'Créer un style…'))
      if (api.perso().length) popup.append(el('div', { class: 'item-style perso', onmousedown: (e) => { e.preventDefault(); fermer(); gererPerso(api) } }, 'Gérer mes styles…'))
    }
    if (!items.length) popup.append(el('div', { class: 'aide', style: 'padding:6px' }, 'Aucun résultat.'))
    popup.hidden = false
    popup.querySelector('.actif')?.scrollIntoView({ block: 'nearest' })
  }
  api.ouvrirMenu = () => { mode = 'menu'; slash = null; actif = 0; dessiner(); }
  api.fermerMenu = fermer

  // saisie rapide « / »
  api.zone.addEventListener('input', () => {
    const s = getSelection()
    if (!s.rangeCount || !s.isCollapsed) return fermer()
    const n = s.anchorNode
    if (n?.nodeType !== 3 || !api.zone.contains(n)) return fermer()
    const avant = n.textContent.slice(0, s.anchorOffset)
    const m = /(?:^|[\s\u200b\u00a0])\/([^/]{0,24})$/.exec(avant)
    if (!m) return mode === 'slash' ? fermer() : undefined
    mode = 'slash'
    slash = { noeud: n, debut: s.anchorOffset - m[1].length - 1, fin: s.anchorOffset }
    actif = 0
    dessiner(m[1])
  })
  api.zone.addEventListener('keydown', (e) => {
    if (popup.hidden || mode !== 'slash') return
    if (e.key === 'ArrowDown') { actif = (actif + 1) % items.length; e.preventDefault(); marquer() }
    else if (e.key === 'ArrowUp') { actif = (actif - 1 + items.length) % items.length; e.preventDefault(); marquer() }
    else if (e.key === 'Enter' || e.key === 'Tab') { if (items[actif]) { e.preventDefault(); appliquer(items[actif]) } }
    else if (e.key === 'Escape') { e.preventDefault(); fermer() }
  })
  const marquer = () => {
    popup.querySelectorAll('.item-style').forEach((n, i) => n.classList.toggle('actif', i === actif))
    popup.querySelector('.actif')?.scrollIntoView({ block: 'nearest' })
  }
  document.addEventListener('mousedown', (e) => { if (!popup.hidden && !popup.contains(e.target) && !e.target.closest?.('.bouton-styles')) fermer() })
  api.zone.addEventListener('blur', () => { if (mode === 'slash') setTimeout(fermer, 150) })
}

/** Le mini-HTML d'une carte -> de quoi l'afficher dans la liste (gras, italique, icones...). */
function apercuHtml(src) {
  const echapper = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;')
  return String(src)
    .split(/(<\/?(?:b|i|u|em|span)\b[^>]*>|\[star\])/i)
    .map((p, k) => {
      if (k % 2 === 0) return echapper(p)
      if (/^\[star\]$/i.test(p)) return '<span style="font-family:ChampionsIcons">s</span>'
      if (/^<em/i.test(p)) return '<span style="font-family:KomikaTitle">'
      if (/^<\/em/i.test(p)) return '</span>'
      return p
    })
    .join('')
}

function gererPerso(api) {
  const liste = el('div', { class: 'contenu', style: 'display:flex;flex-direction:column;gap:6px' })
  const maj = () => {
    liste.replaceChildren(...api.perso().map((p) => el('div', { class: 'rang', style: 'align-items:center' },
      el('span', { style: `flex:2;${cssPerso(p)}` }, p.nom),
      el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { api.supprimerPerso(p.id); maj() } }, 'Supprimer'))))
    if (!api.perso().length) liste.append(el('div', { class: 'aide' }, 'Aucun style pour le moment.'))
  }
  maj()
  dialogue('Mes styles', liste)
}
