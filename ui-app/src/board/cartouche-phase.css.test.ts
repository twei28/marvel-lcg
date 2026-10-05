// La feuille du cartouche du bas (refonte du 04/10/2026, scene PC, mode
// « Étape par étape ») : verrous sur la FEUILLE elle-meme. jsdom ne calcule ni
// hauteur, ni couche, ni pseudo-element : la mesure reelle se fait sur le
// moteur d'essai (ui-check/tests/planche-cartouche.spec.ts).
//
// Ce que ces cas tiennent, piege par piege (carte du code) :
//  - 13 : la feuille est HORS COUCHE, sinon `board.css` (en couches) la bat ;
//  - 14 : tout est sous `.deroule-phase.est-scene` : la table
//         (`est-sur-table`) et le telephone n'en heritent rien ;
//  - REVIREMENT DU 05/10/2026 : un carre au milieu, deplacable, qui GRANDIT en
//    hauteur plutot que de couper ; la table, la main et la barre restent
//    visibles et jouables (aucune regle sur le body) ;
//  - 15 : la trame BD vit sur `::before`, jamais sur le fond (la teinte le prend) ;
//  - 16, D39 : le Sobre eteint la trame et rend la police du body ;
//  - 17 : aucune opacite nulle hors d'une animation (l'etat de base est l'arrivee) ;
//  - 18 : `--card-w` se pose SUR `.scan-card`, qui la redeclare ;
//  - 20 : chaque classe `deroule-*` posee par le composant a sa regle ici.
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'

const brut = fs.readFileSync(path.join(__dirname, 'cartouche-phase.css'), 'utf8')
const css = brut.replace(/\/\*[\s\S]*?\*\//g, '')

/** Les regles de premier niveau (hors @keyframes), selecteurs separes. */
function regles(): Array<{ selecteurs: string[]; corps: string }> {
  const sansAnimations = css.replace(/@keyframes[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}/g, '')
  const sansMedia = sansAnimations.replace(/@media[^{]*\{((?:[^{}]*\{[^}]*\})*)[^}]*\}/g, '$1')
  return [...sansMedia.matchAll(/([^{}]+)\{([^}]*)\}/g)].map((m) => ({
    selecteurs: m[1].split(',').map((s) => s.trim()).filter(Boolean),
    corps: m[2],
  }))
}

/** Le corps de la premiere regle dont un selecteur vaut exactement `selecteur`. */
function corpsDe(selecteur: string): string {
  return regles()
    .filter((r) => r.selecteurs.includes(selecteur))
    .map((r) => r.corps)
    .join('\n')
}

describe('la feuille du cartouche du bas', () => {
  it('est hors couche', () => {
    expect(css).not.toMatch(/@layer/)
  })

  it('ne vise que la scene PC : plus aucune regle sur le body, ni sur la loupe', () => {
    const tous = regles().flatMap((r) => r.selecteurs)
    expect(tous.length).toBeGreaterThan(10)
    for (const s of tous) expect(s.includes('.deroule-phase.est-scene'), s).toBe(true)
    expect(css).not.toMatch(/body\.cartouche-scene|body:has\(|au-dessus-du-cartouche|--cartouche-hauteur|--cartouche-haut\b/)
  })

  it('un carre au milieu : fixe, centre sans transform, 4/3 au moins, qui grandit en hauteur', () => {
    expect(css).toContain('--carre-l: clamp(560px, calc(760px * var(--echelle, 1)), 1100px)')
    const section = corpsDe('.deroule-phase.est-scene')
    expect(section).toContain('position: fixed')
    expect(section).toContain('inset: 0')
    expect(section).toContain('margin: auto')
    expect(section).toContain('box-sizing: border-box')
    expect(section).toContain('width: var(--carre-l)')
    expect(section).toContain('height: fit-content')
    expect(section).toContain('min-height: calc(var(--carre-l) * 0.75)')
    expect(section).toContain('max-height: none')
    expect(section).not.toMatch(/(^|[;\s])height:\s*var\(/)
  })

  it('jamais de defilement, jamais de rognage de la table : ni overflow auto, ni main cachee', () => {
    expect(css).not.toMatch(/overflow(-y)?:\s*(auto|scroll)/)
    expect(css).not.toMatch(/visibility:\s*hidden/)
    expect(css).not.toMatch(/-webkit-line-clamp/)
    expect(css).not.toMatch(/text-overflow:\s*ellipsis/)
  })

  it('la table est visible, sans voile : le carre ne pose qu une ombre', () => {
    expect(css).not.toMatch(/rgba\(\s*\d+,\s*\d+,\s*\d+,\s*0?\.\d+\)\s*;?\s*pointer-events/)
    expect(css).not.toMatch(/\.plateau-scene|\.zone-main|\.plateau-action|\.bouton-fin-tour/)
  })

  it('on l attrape sur tout fond libre : curseur main sur la section, pas sur ses cartes ni ses boutons', () => {
    expect(corpsDe('.deroule-phase.est-scene')).toContain('cursor: grab')
    expect(corpsDe('.deroule-phase.est-scene .scan-card')).toContain('cursor:')
    expect(corpsDe('.deroule-phase.est-scene .bh-bouton')).toContain('cursor: pointer')
  })

  it('la section ne declare jamais son fond, ni un transform autre que none', () => {
    for (const regle of regles()) {
      if (!regle.selecteurs.some((s) => /\.deroule-phase\.est-scene$/.test(s))) continue
      expect(regle.corps, regle.selecteurs.join(', ')).not.toMatch(/(^|[;\s])background(-color|-image)?\s*:/)
      for (const [, valeur] of regle.corps.matchAll(/(?:^|[;\s])transform\s*:\s*([^;]+)/g)) {
        expect(valeur.trim()).toBe('none')
      }
    }
  })

  it('pose la trame BD sur ::before, et le Sobre l eteint avec le selecteur complet', () => {
    const trame = corpsDe('.deroule-phase.est-scene::before')
    expect(trame).toContain('display: block')
    expect(trame).toContain('radial-gradient(')
    expect(trame).toContain('pointer-events: none')
    expect(corpsDe("html[data-affichage='sobre'] .deroule-phase.est-scene::before")).toContain('display: none')
  })

  it('le Sobre rend la police du body au titre, aux pastilles, aux boutons et aux vignettes', () => {
    const sobre = regles().filter((r) =>
      r.selecteurs.some((s) => s.startsWith("html[data-affichage='sobre'] .deroule-phase.est-scene"))
    )
    const police = sobre.find((r) => r.corps.includes('font-family: inherit'))
    expect(police).toBeDefined()
    const cibles = police?.selecteurs.join(' ') ?? ''
    for (const classe of ['.deroule-titre-court', '.deroule-pastille', '.bh-bouton', '.deroule-vignette']) {
      expect(cibles, classe).toContain(classe)
    }
  })

  it('les cartes sont grandes : revelee 260 px, rangee 170 px a l echelle 1, --card-w posee sur .scan-card', () => {
    expect(css).toContain('--vignette-h: clamp(120px, calc(170px * var(--echelle, 1)), 240px)')
    expect(css).toContain('--grande-h: clamp(190px, calc(260px * var(--echelle, 1)), 360px)')
    const carte = regles().find((r) =>
      r.selecteurs.some((s) => /\.deroule-phase\.est-scene .*\.deroule-vignette .*\.scan-card$/.test(s))
    )
    expect(carte?.corps).toMatch(/--card-w:\s*calc\(var\(--vignette-h\)/)
  })

  it('l en-tete tient sur deux lignes : la frise (qui passe a la ligne), puis le titre', () => {
    expect(corpsDe('.deroule-phase.est-scene .deroule-ligne-haut')).toContain('flex-direction: column')
    const frise = corpsDe('.deroule-phase.est-scene .deroule-frise')
    expect(frise).toContain('flex-wrap: wrap')
    expect(corpsDe('.deroule-phase.est-scene .deroule-pastilles')).toContain('flex-wrap: wrap')
    expect(corpsDe('.deroule-phase.est-scene .deroule-titre-court')).not.toContain('nowrap')
  })

  it('la rangee passe sur deux lignes si besoin', () => {
    expect(corpsDe('.deroule-phase.est-scene .deroule-rangee-cartes')).toContain('flex-wrap: wrap')
    expect(corpsDe('.deroule-phase.est-scene .deroule-question-choix')).toContain('flex-wrap: wrap')
    expect(corpsDe('.deroule-phase.est-scene .deroule-sous-cadre-cartes')).toContain('flex-wrap: wrap')
  })

  it('les textes longs passent a la ligne : aucun ne se coupe', () => {
    for (const classe of ['.deroule-legende', '.deroule-etoile', '.deroule-colonne-nom', '.deroule-sous-cadre-titre', '.deroule-choix-nom']) {
      const corps = corpsDe(`.deroule-phase.est-scene ${classe}`)
      expect(corps, classe).not.toBe('')
      expect(corps, classe).not.toMatch(/white-space:\s*nowrap/)
      expect(corps, classe).not.toMatch(/overflow:\s*hidden/)
    }
  })

  it('le corps est une grille a cellule unique : le sous-cadre s y superpose, le carre grandit', () => {
    expect(corpsDe('.deroule-phase.est-scene .deroule-corps')).toContain('display: grid')
    const sous = corpsDe('.deroule-phase.est-scene .deroule-sous-cadre')
    expect(sous).toContain('grid-area: 1 / 1')
    expect(sous).not.toMatch(/position:\s*absolute/)
    expect(corpsDe('.deroule-phase.est-scene .deroule-corps')).toContain('grid-template-columns: minmax(0, 1fr)')
  })

  it('la barre de boutons reste en bas : le refus a gauche, « Suivant » a droite', () => {
    const barre = corpsDe('.deroule-phase.est-scene > .deroule-boutons')
    expect(barre).toContain('margin-top: auto')
    expect(barre).toContain('flex-wrap: wrap')
    expect(corpsDe('.deroule-phase.est-scene .deroule-boutons [data-refus]')).toContain('order: -1')
  })

  // LOT 6 (planche, etats 3, 5, 6, 13, 15b) : une carte SANS legende (le
  // heros vise), centree dans la rangee, descendait de la hauteur d'une ligne
  // sous ses voisines legendees. La mesure vraie est dans la planche
  // (`ecartCartes`) ; ce cas tient la regle.
  it('une carte sans legende garde la place de la ligne : les cartes de la rangee s alignent', () => {
    const place = corpsDe('.deroule-phase.est-scene .deroule-rangee-cartes .deroule-vignette:not(:has(> .deroule-legende))::after')
    expect(place).toMatch(/content:\s*''/)
    // La hauteur d'une ligne de legende : sa taille de police par son interligne.
    const legende = corpsDe('.deroule-phase.est-scene .deroule-legende')
    const taille = legende.match(/font-size:\s*([\d.]+rem)/)?.[1]
    const interligne = legende.match(/line-height:\s*([\d.]+)/)?.[1]
    expect(place).toContain(`height: calc(${taille} * ${interligne})`)
  })

  // LOT 6 (planche, etat 7) : « PV 14 → 15, ATQ 2 → 3 » est le resultat du
  // stade (D25) ; en petit texte gris, il se lisait comme une note de bas de
  // page a cote de « 3 DÉGÂTS SUBIS » des autres etats.
  it('les stats du stade se lisent comme un resultat, et le Sobre leur rend la police du body', () => {
    const stats = corpsDe('.deroule-phase.est-scene .deroule-stade .deroule-lignes')
    expect(stats).toContain("font-family: 'Bangers'")
    expect(stats).toMatch(/text-shadow:/)
    const sobre = regles().find(
      (r) =>
        r.corps.includes('font-family: inherit') &&
        r.selecteurs.includes("html[data-affichage='sobre'] .deroule-phase.est-scene .deroule-stade .deroule-lignes")
    )
    expect(sobre).toBeDefined()
  })

  it('aucune opacite nulle hors d une animation', () => {
    for (const regle of regles()) {
      expect(regle.corps, regle.selecteurs.join(', ')).not.toMatch(/opacity:\s*0(?![.\d])/)
    }
  })

  it('le titre court en Bangers, en capitales par la feuille', () => {
    const titre = corpsDe('.deroule-phase.est-scene .deroule-titre-court')
    expect(titre).toContain("font-family: 'Bangers'")
    expect(titre).toContain('text-transform: uppercase')
  })

  // LOT 5 (D35) : le corps entre par la droite en 250 ms, comme une page. Seule
  // l'ENTREE glisse (la cle du corps demonte l'ancien) ; l'etat de base est
  // l'arrivee, rien n'est pose hors de l'animation (lecon de board.css).
  it('le corps glisse en entrant, en 250 ms, et son etat de base est l arrivee (D35)', () => {
    const corps = corpsDe('.deroule-phase.est-scene .deroule-corps')
    expect(corps).toMatch(/animation:\s*cartouche-page-entre 250ms ease-out/)
    expect(corps).not.toMatch(/(^|[;\s])(opacity|translate|transform)\s*:/)
    const images = css.match(/@keyframes cartouche-page-entre\s*\{([\s\S]*?\}\s*)\}/)
    expect(images, '@keyframes cartouche-page-entre').not.toBeNull()
    expect(images?.[1]).toMatch(/from\s*\{[^}]*translate:\s*40px 0/)
    expect(images?.[1]).toMatch(/from\s*\{[^}]*opacity:\s*0/)
  })

  // Le carre est FIXE : il s'ouvre en fondu de 150 ms, et seul son contenu glisse.
  it('le carre s ouvre en fondu de 150 ms, sans glisser ; son etat de base est l arrivee', () => {
    const section = corpsDe('.deroule-phase.est-scene')
    expect(section).toMatch(/animation:\s*cartouche-fondu 150ms ease-out/)
    expect(section).not.toMatch(/(^|[;\s])(opacity|translate)\s*:/)
    const images = css.match(/@keyframes cartouche-fondu\s*\{([\s\S]*?\}\s*)\}/)
    expect(images, '@keyframes cartouche-fondu').not.toBeNull()
    expect(images?.[1]).toMatch(/from\s*\{[^}]*opacity:\s*0/)
    expect(images?.[1]).not.toMatch(/translate|transform/)
  })

  it('fondu et glissement se coupent sans animations, en Sobre et en mouvement reduit (trois gates)', () => {
    for (const cible of ['', ' .deroule-corps']) {
      expect(corpsDe(`body.plateau-sans-animations .deroule-phase.est-scene${cible}`), cible).toMatch(/animation:\s*none/)
      expect(corpsDe(`html[data-affichage='sobre'] .deroule-phase.est-scene${cible}`), cible).toMatch(/animation:\s*none/)
    }
    const reduit = [...css.matchAll(/@media \(prefers-reduced-motion: reduce\)\s*\{([\s\S]*?\n\})/g)].map((m) => m[1]).join('\n')
    expect(reduit).toMatch(/\.deroule-phase\.est-scene \.deroule-corps[^{]*\{[^}]*animation:\s*none/)
    expect(reduit).toMatch(/\.deroule-phase\.est-scene[,\s{][^}]*animation:\s*none/)
  })

  // LOT 6 (menage) : ces classes ne sont plus posees par aucun composant
  // (grep du 05/10/2026 : seuls des tests qui verifient leur absence et des
  // fixtures HTML de ui-check les citaient). Leurs regles de board.css sont
  // mortes ; deroule-onglets.css, teinte.css et affichage-sobre.css ne sont
  // pas touches.
  it('board.css ne garde aucune regle des classes retirees du cartouche d avant', () => {
    const board = fs.readFileSync(path.join(__dirname, 'board.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')
    for (const morte of ['deroule-boosts', 'deroule-regle', 'deroule-a-toi', 'deroule-fleche', 'deroule-boost-entre']) {
      expect(board, morte).not.toMatch(new RegExp(`${morte}(?![a-z-])|${morte}-`))
    }
  })

  it('chaque classe deroule-* du composant a sa regle (piege 20)', () => {
    const composant =
      fs.readFileSync(path.join(__dirname, 'CartouchePhase.tsx'), 'utf8') +
      fs.readFileSync(path.join(__dirname, 'SousCadre.tsx'), 'utf8')
    // Les noms de classe ecrits en toutes lettres dans le composant : dans un
    // `className`, dans une expression, ou poussees dans une liste.
    const classes = new Set(
      [...composant.matchAll(/['"`]([^'"`]*\bderoule-[a-z-]+[^'"`]*)['"`]/g)]
        // Un chemin d'import (« ./deroule-textes ») n'est pas une classe.
        .filter((m) => !m[1].startsWith('.'))
        .flatMap((m) => m[1].match(/\bderoule-[a-z]+(?:-[a-z]+)*(?![a-z-]*\$)/g) ?? [])
    )
    expect(classes.size).toBeGreaterThan(10)
    // Les boutons gardent la feuille commune des boutons BD (coins coupes,
    // ambre) : `deroule-suivant` y a deja sa regle.
    const boutons = fs.readFileSync(path.join(__dirname, 'boutons-bd.css'), 'utf8')
    for (const classe of classes) {
      const motif = new RegExp(`\\.${classe}(?![a-z-])`)
      expect(motif.test(css) || motif.test(boutons), classe).toBe(true)
    }
  })
})
