// Le cartouche du deroule detaille : une etape a la fois.
//
// FIXE en bas au centre, il ne bouge jamais d'une etape a l'autre : l'oeil sait
// ou lire et la main ou cliquer des le deuxieme tour. Un cartouche colle a la
// carte concernee aurait deplace le bouton a chaque clic.
//
// « Precedent » RELIT, il ne rejoue rien : le monde du moteur ne recule pas.
// C'est « Annuler la derniere action » qui fait cela, et il reste disponible.

import { useEffect, useLayoutEffect, useState } from 'react'
import {
  arreterSurDefaite,
  avecBilan,
  rangDansLeTemps,
  type EtapeDeroule,
  type TempsPhase,
} from './deroule-phase'
import {
  compteurEtape,
  compteurLigneBilan,
  regleEtape,
  resultatEtape,
  texteArretDefaite,
  texteBilanVide,
  texteDefaite,
  texteLigneBilan,
  titreEtape,
} from './deroule-textes'
import { t } from './langue'
import { ecrireRegleDepliee, lireRegleDepliee } from './moteur'
import { TraitCible } from './TraitCible'
import { useDerouleScene } from './useDerouleScene'

/** Le temps de lire un boost a capacite avant le suivant. */
const DELAI_BOOST_MS = 1500

/**
 * De combien le cartouche se tient au-dessus de la main, et le plancher qu'il
 * garde quand aucune main n'est mesurable.
 *
 * `--deroule-bas` est lue par `.deroule-phase` (board.css) comme sa propriete
 * `bottom`. Le repli du CSS (16 px) est le meme que BAS_MINIMUM : le cartouche
 * retombe alors exactement ou il etait avant cette correction.
 */
const VARIABLE_BAS = '--deroule-bas'
const ECART_MAIN = 10
const BAS_MINIMUM = 16

/**
 * Les cinq temps de la carte de reference, dans l'ordre.
 *
 * Le mechant et ses sbires sont deux moments distincts du tour (le vilain
 * s'active AVANT ses sbires) : les fondre dans un seul « Activations »
 * cachait ou l'on en etait. Arbitrage de l'utilisateur, qui a decrit la
 * phase exactement dans ces termes.
 */
const TEMPS: { cle: TempsPhase; libelle: string }[] = [
  { cle: 'menace', libelle: 'Menace' },
  { cle: 'mechant', libelle: 'Méchant' },
  { cle: 'sbires', libelle: 'Sbires' },
  { cle: 'distribution', libelle: 'Distribution' },
  { cle: 'revelation', libelle: 'Révélation' },
]

export function DeroulePhase({
  etapes,
  identitePhase,
  phaseMechantEnCours = false,
  partieFinie = false,
  pvMaxParNom,
  onSuivant,
  onTerminer,
  onToutDerouler,
  onVisible,
}: {
  etapes: EtapeDeroule[]
  /**
   * L'identite de la phase en cours, et le SEUL declencheur legitime de la
   * remise a zero du cartouche. board.tsx y passe `etat.monde.round_id` : il y
   * a une phase du mechant par round, donc le round suffit a distinguer deux
   * phases. La longueur de la liste ne peut PAS jouer ce role, puisqu'elle
   * grossit legitimement pendant la phase (chaque validation relache une trame
   * du moteur, qui produit l'etape suivante).
   */
  identitePhase?: number
  /**
   * Vrai tant que le moteur est encore dans la phase du mechant (board.tsx :
   * `PHASES_DU_MECHANT.has(etat.monde.phase)`). Arriver au bout des etapes
   * CONNUES ne veut pas dire que la phase est finie : tant que celle-ci court,
   * le cartouche attend la suite au lieu de se masquer.
   */
  phaseMechantEnCours?: boolean
  /**
   * La partie est finie (board.tsx : `etat.monde.game_over`, la SEULE source
   * de cet etat, celle-la meme dont l'ecran de fin de partie se sert).
   *
   * Constate en partie : la manigance principale etait allee au bout, l'ecran
   * de defaite etait affiche, et le cartouche restait par-dessus le plateau a
   * annoncer « La suite arrive… » indefiniment. Il n'y a plus de suite : la
   * partie est finie, le cartouche s'efface.
   */
  partieFinie?: boolean
  /**
   * Les PV maximum des personnages, par nom (board.tsx, qui lit le monde) :
   * sans eux le bilan de fin de phase dit « 8 » au lieu de « 8/14 ». Ils ne
   * peuvent pas venir des etapes, le moteur ne les publie pas a cote de ses
   * faits. Absents, ou muets sur une cible : le bilan montre le restant seul.
   */
  pvMaxParNom?: Map<string, number>
  /**
   * Appele a CHAQUE etape validee (clic ou clavier), avant de passer a la
   * suivante. C'est lui qui relache le moteur cote reseau
   * (`avancerMaintenant`) : optionnel pour ne pas casser les appelants qui ne
   * pilotent pas le moteur (tests, previsualisation).
   */
  onSuivant?: () => void
  /** Appele une fois la derniere etape validee. */
  onTerminer: () => void
  /** « Tout derouler » : les etapes restantes defilent sans attendre. */
  onToutDerouler?: () => void
  /**
   * Appele des que le cartouche apparait ou disparait de l'ecran.
   *
   * Il sert a EMPECHER QUE DEUX PANNEAUX SE DISPUTENT L'ECRAN : le recap de
   * fin de phase (RecapPhaseMechant) est un bilan d'apres-phase, le cartouche
   * un guide pendant la phase, et les deux se recouvriraient sans cela. C'est
   * le cartouche qui parle, parce que lui seul sait s'il est a l'ecran
   * (`etape`, `termine`, `partieFinie` sont son etat interne) ; board.tsx s'en
   * sert pour retenir le recap tant que le cartouche est la.
   *
   * Doit etre STABLE d'un rendu a l'autre (board.tsx passe un `setState`) :
   * une fonction recreee a chaque rendu relancerait l'effet a chaque trame.
   */
  onVisible?: (visible: boolean) => void
}) {
  const [index, setIndex] = useState(0)
  // Vrai une fois la derniere etape validee : le cartouche doit alors
  // disparaitre de lui-meme. `onTerminer` relache desormais vraiment le
  // moteur (board.tsx), mais cela ne le fait pas disparaitre de l'ecran pour
  // autant : c'est toujours au composant de se masquer, plutot que de rester
  // affiche indefiniment sur la derniere etape, y compris pendant le tour du
  // joueur suivant.
  const [termine, setTermine] = useState(false)
  // Vrai quand le joueur a valide la derniere etape CONNUE alors que la phase
  // du mechant court encore : le moteur, relache par cette validation, est en
  // train de calculer la suite. Le cartouche reste alors affiche sur place et
  // n'annonce surtout pas la fin de la phase.
  const [enAttente, setEnAttente] = useState(false)

  // Le dépliant de la règle sous l'étape : un choix qu'on ne fait qu'une
  // fois (voir lireRegleDepliee dans moteur.ts). Lu une seule fois a l'etat
  // initial, PAS reinitialise a chaque nouvelle phase (contrairement a
  // `index`, `termine`, etc. ci-dessous) : il doit rester replie sur toutes
  // les etapes et toutes les parties, jusqu'a ce que le joueur le replie.
  const [regleDepliee, setRegleDepliee] = useState(() => lireRegleDepliee())

  const basculerRegle = () => {
    setRegleDepliee((avant) => {
      const apres = !avant
      ecrireRegleDepliee(apres)
      return apres
    })
  }

  // Une nouvelle phase repart de sa premiere etape, et RIEN D'AUTRE ne remet
  // le cartouche a zero. La remise a zero suivait auparavant le contenu de la
  // liste d'etapes : depuis que chaque validation relache une trame du moteur,
  // cette liste s'allonge PENDANT la phase, et le cartouche repartait donc de
  // la premiere etape a chaque nouvelle activation. Le joueur relisait en
  // boucle des etapes deja validees.
  //
  // `termine` doit se reinitialiser ICI, pas seulement `index` : sinon le
  // cartouche ne reapparaitrait plus jamais a la phase du mechant suivante, ce
  // qui est le piege symetrique et pire que le defaut d'origine.
  useEffect(() => {
    setIndex(0)
    setTermine(false)
    setEnAttente(false)
  }, [identitePhase])

  // Les etapes REELLEMENT parcourues : celles du moteur, plus le bilan de fin
  // de phase quand la phase est finie.
  //
  // `phaseMechantEnCours` est la seule chose qui distingue proprement une phase
  // en cours d'une phase terminee (board.tsx la calcule sur `monde.phase`) :
  // arriver au bout des etapes CONNUES ne dit rien, puisque la liste s'allonge
  // pendant la phase. Le bilan n'existe donc que quand la phase est finie, et
  // c'est ce qui en fait le terminateur naturel du cartouche : il est toujours
  // la derniere etape, et le valider, c'est finir.
  //
  // `arreterSurDefaite` vient EN DERNIER, et l'ordre tranche la question : un
  // heros tombe coupe le deroule a son etape, bilan compris. Le bilan de fin de
  // phase ne s'affiche donc jamais derriere une defaite.
  const etapesAffichees = arreterSurDefaite(
    phaseMechantEnCours ? etapes : avecBilan(etapes, pvMaxParNom)
  )

  const etape = etapesAffichees[index]

  const avancer = () => {
    // Hors phase du mechant, etapes est vide et il n'y a rien a avancer : une
    // touche pressee ne doit alors rien declencher.
    if (!etape) return
    // Partie finie : le cartouche n'est plus a l'ecran, sa touche Entree ne
    // doit pas continuer a relacher le moteur derriere l'ecran de fin.
    if (partieFinie) return
    // Relache le moteur AVANT de savoir si c'est la derniere etape : chaque
    // validation (clic ou clavier) correspond au plus a une trame retenue
    // cote moteur (`avancerMaintenant` ne fait rien sans trame en attente),
    // donc l'appeler ici a chaque fois est sans risque, y compris sur la
    // derniere etape ou `onTerminer` l'appelle une seconde fois juste apres.
    onSuivant?.()
    // Un heros est tombe : le deroule s'arrete la, et « Continuer » rend la
    // main tout de suite. Sans ce court-circuit, la validation aurait bascule
    // le cartouche en « La suite arrive… » tant que la phase du mechant court
    // encore (elle continue pour les autres joueurs), sur une suite que
    // `arreterSurDefaite` ne lui donnera jamais.
    if (etape.defaite) {
      setTermine(true)
      onTerminer()
      return
    }
    // Une etape suivante est deja connue : on y va.
    if (index + 1 < etapesAffichees.length) {
      setEnAttente(false)
      setIndex(index + 1)
      return
    }
    // Bout des etapes CONNUES, mais la phase du mechant court encore : le
    // moteur vient d'etre relache et va produire la suite. On reste sur place
    // en attente, sans appeler `onTerminer` et sans masquer le cartouche.
    if (phaseMechantEnCours) {
      setEnAttente(true)
      return
    }
    // Bout des etapes ET phase terminee : la, c'est vraiment fini.
    setTermine(true)
    onTerminer()
  }

  const reculer = () => {
    // Relire, c'est renoncer a l'attente en cours : sans cela, la sortie
    // d'attente ci-dessous repousserait aussitot le joueur en avant et
    // « Precedent » n'aurait aucun effet visible. La suite reste atteignable
    // au bouton « Suivant », comme apres tout « Precedent ».
    setEnAttente(false)
    setIndex(index - 1)
  }

  // Sortie d'attente. Deux issues, et deux seulement :
  //  - une etape de plus arrive : on avance dessus TOUT SEUL. Le joueur a deja
  //    clique pour l'obtenir, il ne doit pas avoir a recliquer ;
  //  - la phase du mechant se termine sans rien produire de plus : le
  //    cartouche ne doit pas rester affiche par-dessus le plateau pendant tout
  //    le tour du joueur.
  //
  // En pratique, la fin de la phase fait apparaitre le bilan, donc c'est la
  // PREMIERE issue qui joue : le joueur atterrit sur le bilan et le valide.
  // La seconde reste un filet, pour le cas ou la phase se terminerait sans
  // qu'aucune etape n'ait ete produite.
  useEffect(() => {
    if (!enAttente) return
    if (index + 1 < etapesAffichees.length) {
      setEnAttente(false)
      setIndex(index + 1)
      return
    }
    if (!phaseMechantEnCours) {
      setEnAttente(false)
      setTermine(true)
      onTerminer()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `onTerminer` est
    // recree a chaque rendu par board.tsx : en dependre relancerait cet effet
    // a chaque trame du moteur, donc appellerait `onTerminer` en boucle. Les
    // quatre dependances ci-dessous sont des primitifs et decrivent a elles
    // seules la sortie d'attente.
  }, [enAttente, index, etapesAffichees.length, phaseMechantEnCours])

  useEffect(() => {
    const auClavier = (evenement: KeyboardEvent) => {
      // On ecrit peut-etre ailleurs : le tchat est a portee de main pendant la
      // phase, et un espace tape dedans ne doit pas la faire avancer.
      const cible = evenement.target
      if (
        cible instanceof HTMLElement &&
        (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)
      ) {
        return
      }
      // On ne confisque pas Entree/Espace a un bouton du PLATEAU : seul un
      // element interactif EXTERIEUR au cartouche doit garder son activation
      // au clavier normale. Un bouton du cartouche lui-meme (Suivant,
      // Precedent) reste pris en charge ici, comme avant.
      if (
        cible instanceof HTMLElement &&
        cible.closest('button, a, select, [role="button"]') &&
        !cible.closest('.deroule-phase')
      ) {
        return
      }
      if (evenement.key === 'Enter' || evenement.key === ' ') {
        evenement.preventDefault()
        avancer()
        return
      }
      if (evenement.key === 'Escape' && onToutDerouler) {
        evenement.preventDefault()
        onToutDerouler()
      }
    }
    document.addEventListener('keydown', auClavier)
    return () => document.removeEventListener('keydown', auClavier)
  })

  // Combien de boosts sont deja retournes sur l'etape courante. Ils
  // s'enchainent SEULS : c'est l'etape qui attend la validation, pas chaque
  // carte. Une attaque a trois boosts couterait sinon quatre clics.
  const [boostsMontres, setBoostsMontres] = useState(0)

  useEffect(() => {
    setBoostsMontres(etape?.boosts.length ? 1 : 0)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `etape` est
    // reconstruit a chaque trame du moteur (meme piege que dans
    // useDerouleScene.ts et TraitCible.tsx) : en dependre remettrait
    // `boostsMontres` a 1 en boucle et aucun boost ne s'enchainerait jamais. `etape?.cle` identifie l'etape, et
    // `etape?.boosts.length` reagit si son compte de boosts change.
  }, [etape?.cle, etape?.boosts.length])

  useEffect(() => {
    const total = etape?.boosts.length ?? 0
    if (boostsMontres === 0 || boostsMontres >= total) return
    const minuteur = window.setTimeout(
      () => setBoostsMontres((n) => n + 1),
      DELAI_BOOST_MS
    )
    return () => window.clearTimeout(minuteur)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- meme raison :
    // `etape?.cle` et `etape?.boosts.length` suffisent a piloter le
    // minuteur, l'identite de `etape` ne doit pas le redeclencher.
  }, [boostsMontres, etape?.cle, etape?.boosts.length])

  // Le cartouche est-il a l'ecran ? Calcule ICI parce que les hooks ci-dessous
  // en dependent, et que la sortie `return null` qui l'applique vient bien plus
  // bas : un hook place apres elle ferait tomber tout le plateau.
  const visible = Boolean(etape) && !termine && !partieFinie

  // Mise en scene de l'etape courante. Appele ici, avec les autres hooks :
  // ce composant a un `return null` plus bas, et un hook place apres lui fait
  // tomber tout le plateau (React compte alors un hook de plus au rendu
  // suivant).
  useDerouleScene(etape, visible)

  // Un seul panneau a la fois : on dit a l'exterieur si l'on est a l'ecran.
  // Le nettoyage annonce la disparition, sans quoi un demontage (sortie du
  // mode detaille, fin de partie) laisserait le recap retenu pour toujours.
  useEffect(() => {
    onVisible?.(visible)
    return () => onVisible?.(false)
  }, [visible, onVisible])

  // Le cartouche ne recouvre JAMAIS la main du joueur.
  //
  // Mesure faite en partie : le cartouche occupait 715 a 873 px, la main 623 a
  // 806, soit 91 px de recouvrement, et l'utilisateur ne voyait plus ses
  // cartes. Des trois issues possibles (remonter le cartouche, le decaler sur
  // un cote, reduire sa hauteur), une seule tient :
  //
  //  - le DECALER SUR UN COTE ne sert a rien : la main occupe toute la largeur
  //    du bas de la table (`--place: 1850px`, board.css), donc aucune colonne
  //    n'est libre a cette hauteur ;
  //  - REDUIRE SA HAUTEUR ne suffirait pas : sous la main il ne reste que 83 px
  //    de fond d'ecran, et le cartouche en demande le double rien que pour ses
  //    quatre lignes. Le raccourcir jusqu'a tenir la reviendrait a ne plus rien
  //    y ecrire ;
  //  - le REMONTER au-dessus de la main est donc le seul choix, et c'est aussi
  //    le plus stable : il ne touche ni a l'echelle de la table ni au contenu
  //    du cartouche.
  //
  // On ne remonte pas d'une valeur en dur : on lit la position REELLE de la
  // zone de main. `.zone-main` est une case de la grille de la scene, donc sa
  // boite ne bouge ni avec le nombre de cartes (elles sont rognees a
  // l'interieur, voir `overflow: hidden` sur `.zone-main`) ni avec la taille de
  // l'ecran (la scene se met a l'echelle, et le rect suit l'echelle). C'est la
  // meme facon de lire le plateau que `useDerouleScene` et `placement/boites`.
  //
  // Aucune zone de main trouvee (plateau mobile, plateau pas encore monte) : on
  // ne devine pas une geometrie absente, la variable est retiree et le CSS
  // reprend sa valeur de repli.
  useLayoutEffect(() => {
    const corps = document.body
    const oublier = () => corps.style.removeProperty(VARIABLE_BAS)
    if (!visible) {
      oublier()
      return
    }
    const mesurer = () => {
      const main = document.querySelector('.plateau-scene .zone-main')
      if (!main) {
        oublier()
        return
      }
      const boite = main.getBoundingClientRect()
      // Hauteur nulle : la mise en page n'a pas encore eu lieu (ou l'on est
      // dans un environnement sans mise en page). Une mesure fausse serait pire
      // que pas de mesure du tout.
      if (boite.height === 0) {
        oublier()
        return
      }
      const bas = Math.round(window.innerHeight - boite.top + ECART_MAIN)
      corps.style.setProperty(VARIABLE_BAS, `${Math.max(bas, BAS_MINIMUM)}px`)
    }
    mesurer()
    // La scene se remet a l'echelle a chaque redimensionnement : la main change
    // alors de place, et le cartouche doit la suivre.
    window.addEventListener('resize', mesurer)
    return () => {
      window.removeEventListener('resize', mesurer)
      oublier()
    }
  }, [visible])

  // Le `return null` vient APRES tous les hooks, jamais avant : React exige
  // le meme nombre de hooks, dans le meme ordre, a chaque rendu. Ce composant
  // est monte des que le mode "detaille" est actif, donc hors phase du
  // mechant avec `etapes` vide, puis se remplit sans etre demonte quand la
  // phase commence. Un `return null` place plus haut sauterait le second
  // useEffect a un rendu et le rajouterait au suivant, ce que React refuse.
  // `termine` fait disparaitre le cartouche une fois la phase VRAIMENT finie
  // (bout des etapes connues et phase du mechant terminee) ; il est remis a
  // false des que l'identite de phase change (voir le useEffect ci-dessus),
  // donc le deroule reapparait bien a la phase du mechant suivante.
  // `partieFinie` le fait disparaitre pour de bon : plus rien n'arrive apres.
  if (!etape || termine || partieFinie) return null

  // Position du temps COURANT dans la chronologie : elle seule dit qui est
  // deja passe. Calculee une fois pour les cinq temps, pas a chaque `<li>`.
  //
  // Un temps absent de la chronologie (le bilan) compte comme place APRES tous
  // les autres : sur la derniere etape, les cinq temps s'affichent alors tous
  // valides, ce qui est exactement ce qui vient de se passer. Sans cela, le
  // `-1` rendu par findIndex n'en aurait marque aucun.
  const trouve = TEMPS.findIndex((item) => item.cle === etape.temps)
  const positionCourante = trouve === -1 ? TEMPS.length : trouve

  // « 1 sur 3 » : combien d'etapes ce temps compte, et ou l'on en est.
  // `undefined` quand il n'en compte qu'une, et rien ne s'affiche alors.
  const rang = rangDansLeTemps(etapesAffichees, index)
  const resultat = resultatEtape(etape)
  const compteur = compteurEtape(etape)
  const regle = regleEtape(etape)

  return (
    <>
      <TraitCible etape={etape} actif={!termine} />
      <section className="deroule-phase" role="dialog" aria-label={t('Phase du méchant')}>
        <div className="deroule-chrono">
          <ol className="deroule-temps">
            {TEMPS.map((temps, position) => {
              // Vide : aucune etape de la phase ne porte ce temps. Il n'a
              // coute aucun clic (etapesDeroule ne cree pas de placeholder pour
              // lui) ; le joueur doit seulement voir qu'il a ete saute, et
              // pourquoi.
              const estVide = !etapesAffichees.some((e) => e.temps === temps.cle)
              const estCourant = !estVide && temps.cle === etape.temps
              const estPasse = !estVide && !estCourant && position < positionCourante
              const classe = estVide ? 'est-vide' : estCourant ? 'est-courant' : estPasse ? 'est-passe' : ''
              return (
                <li key={temps.cle} className={classe}>
                  {t(temps.libelle)}
                  {/* Motif deja utilise pour « Fin du tour » (board.tsx) : un
                      symbole colle au texte, pas une traduction a part. */}
                  {estPasse ? ' ✓' : null}
                  {estVide ? <span className="deroule-temps-vide-detail"> ({t('Aucun')})</span> : null}
                </li>
              )
            })}
          </ol>
          {rang ? (
            <span className="deroule-rang">
              {/* Cle a trous plutot qu'une concatenation : « sur » se traduit
                  deja par « on » ailleurs dans le dictionnaire, et « 1 on 3 »
                  ne veut rien dire. */}
              {t('%1 sur %2').replace('%1', String(rang.rang)).replace('%2', String(rang.total))}
            </span>
          ) : null}
        </div>

        {/* Le titre dit le fait, et le compteur de la cible se lit a sa
            droite. Un titre generique suivi de la meme chose en dessous
            faisait dire une seule chose a trois lignes. */}
        <div className="deroule-entete">
          {/* Le bilan porte le meme titre que les autres etapes, en capitales :
              il annonce la fin de la phase, pas un coup de plus. */}
          <p className={`deroule-titre${etape.temps === 'bilan' ? ' est-bilan' : ''}`}>
            {titreEtape(etape)}
          </p>
          {compteur ? <span className="deroule-compteur">{compteur}</span> : null}
        </div>
        {resultat ? <p className="deroule-resultat">{resultat}</p> : null}
        {/* La chute du heros. Elle ne ressemble a aucune autre ligne du
            cartouche, et c'est voulu : c'est le moment le plus important d'une
            partie, il ne doit pas defiler comme les autres. Le crane est
            decoratif (aria-hidden) : la phrase dit deja tout, et un lecteur
            d'ecran n'a pas a epeler un symbole. */}
        {etape.defaite ? (
          <p className="deroule-defaite">
            <span aria-hidden="true">☠</span> {texteDefaite(etape)}
          </p>
        ) : null}
        {etape.boosts.length > 0 ? (
          <ul className="deroule-boosts">
            {etape.boosts.slice(0, boostsMontres).map((boost) => (
              <li key={boost.cle}>
                <b>{boost.nom}</b>
                <span>+{boost.apport}</span>
              </li>
            ))}
          </ul>
        ) : null}
        {/* Le bilan de fin de phase : ce que le joueur vient d'encaisser, en
            deux lignes, au moment ou il decide de son tour. Une liste VIDE
            n'est pas une absence : elle dit que la phase n'a rien coute, et le
            cartouche le dit plutot que de rester muet. */}
        {etape.bilan ? (
          <ul className="deroule-bilan">
            {etape.bilan.length === 0 ? (
              <li className="deroule-bilan-rien">{texteBilanVide()}</li>
            ) : (
              etape.bilan.map((ligne) => (
                <li key={ligne.cle}>
                  <span className="deroule-bilan-fait">{texteLigneBilan(ligne)}</span>
                  {compteurLigneBilan(ligne) ? (
                    <span className="deroule-bilan-compteur">{compteurLigneBilan(ligne)}</span>
                  ) : null}
                </li>
              ))
            )}
          </ul>
        ) : null}
        {regle ? (
          <div className="deroule-regle">
            {/* Vrai bouton, pas un <span> cliquable : atteignable au Tab et a
                Entree/Espace nativement, et `aria-expanded` annonce l'etat au
                lecteur d'ecran. Meme motif que `.recap-mechant-repli`
                (RecapPhaseMechant.tsx), le seul autre dépliant du plateau. */}
            <button
              type="button"
              className="deroule-regle-bouton"
              aria-expanded={regleDepliee}
              onClick={basculerRegle}
            >
              <span aria-hidden="true">{regleDepliee ? '▾' : '▸'}</span> {t('la règle')}
            </button>
            {regleDepliee ? <p className="deroule-regle-texte">{regle}</p> : null}
          </div>
        ) : null}
        <div className="deroule-boutons">
          {/* Dire qu'on attend, sans rien bloquer : une mention grise a cote du
              bouton, qui reste cliquable. Ni modale ni bouton desactive, parce
              que l'attente dure une fraction de seconde en temps normal et
              qu'un bouton qui s'eteint puis se rallume attire l'oeil plus que
              l'etape elle-meme. Un reclic pendant l'attente est sans danger :
              il relache au plus une trame de plus. */}
          {enAttente ? (
            <span className="deroule-attente" aria-live="polite">
              {t('La suite arrive…')}
            </span>
          ) : null}
          {/* Dit pourquoi il n'y a plus rien apres, a la place meme ou l'on
              lit d'ordinaire « La suite arrive… ». Les deux ne se croisent
              jamais : une defaite ne fait plus attendre de suite. */}
          {etape.defaite ? <span className="deroule-arret">{texteArretDefaite()}</span> : null}
          {index > 0 ? (
            <button type="button" className="bh-bouton" onClick={reculer}>
              {t('Précédent')}
            </button>
          ) : null}
          {/* Sur le bilan, le bouton ne dit plus « Suivant » : il n'y a plus
              rien apres, et c'est lui qui rend la main au joueur. Sur une
              defaite, il dit « Continuer » : ce n'est pas une etape de plus
              qu'on demande, c'est le droit de reprendre la partie. */}
          <button type="button" className="bh-bouton deroule-suivant" onClick={avancer}>
            {etape.defaite
              ? t('Continuer')
              : etape.temps === 'bilan'
                ? t('À toi de jouer')
                : t('Suivant')}
          </button>
        </div>
      </section>
    </>
  )
}
