// La fenetre des reglages : quatre onglets, au centre de l'ecran.
//
// REMPLACE (14/09/2026) le menu dans le menu. Avant : la barre ouvrait un
// popover « ⚙ Reglages » qui contenait lui-meme un bouton « ⚙ Options »
// ouvrant un SECOND popover de 18 reglages a plat. Constat de l'utilisateur :
// « il y a une colonne et puis quand j'ouvre les options, il y a encore la
// colonne des options, et puis voila ainsi de suite ».
//
// ⚠ UN REGLAGE N'EST PAS UNE ACTION, ET C'EST LA COUPURE PRINCIPALE.
// L'historique, le log, le journal du heros, les sauvegardes et « quitter » ne
// sont PAS ici : ils se consultent EN JOUANT, souvent en urgence quand un bug
// vient de se produire, et ouvrir une fenetre modale pour lire un log serait
// absurde. Ils vivent dans le bouton « Partie » de la barre. La « Vue » y reste
// aussi : elle change a chaque tour en multijoueur.
//
// ⚠ UN SOUS-REGLAGE QUI APPARAIT EST UN SOUS-REGLAGE QU'ON NE DECOUVRE JAMAIS.
// « Vitesse du deroule », « Apercu d'ambiance », « Actions » ne s'inserent plus
// dans la liste quand leur parent s'allume : ils sont TOUJOURS la, en retrait,
// grises et inertes tant que le parent est coupe. Deux raisons : la liste ne
// saute plus sous le doigt, et surtout on ne peut plus ignorer qu'un reglage
// existe faute d'avoir active son parent par hasard.
//
// ⚠ AUCUN REGLAGE N'EST AJOUTE, SUPPRIME NI RENOMME. C'est un rangement, pas
// une refonte : chaque interrupteur continue d'appeler exactement la meme
// fonction qu'avant.
import { ecrireEtiquettesTable, lireEtiquettesTable } from './etiquettes-table'
import { ecrireBarreAvantage, lireBarreAvantage } from './barre-avantage-reglage'
import { ecrireCoteAmeliorations, lireCoteAmeliorations, type CoteAmeliorations } from './cote-ameliorations'
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react'
import { filtrerReglages } from './recherche-reglages'
import { choisirPolitique, lirePolitique, type PolitiqueAvance } from './avance-multi'
import { transformDecalage, useGlisserPanneau } from './placement/useGlisserPanneau'
import { ReglagesApercuAmbiance, type ApercuMeteo } from './CoucheMeteo'
import { t, langueActuelle } from './langue'
import {
  type ModeActions,
  type ModePhaseMechant,
  type DelaiAutoPhase,
  ecrireDelaiAutoPhase,
  lireDelaiAutoPhase,
  suivreDelaiAutoPhase,
  type ModeRevelation,
  type ReponseAmbiance,
  MODE_SUR_TABLE_OUVERT,
} from './moteur'
import type { ReglageMode } from './mobile/useModeMobile'
import { ecrireReglageDoigt, lireReglageDoigt, type ReglageDoigt } from './tablette/tablette'
import {
  ecrireColonnesZone,
  ecrireReglageTelephone,
  useReglagesTelephone,
  type PlateauTelephone,
  type TailleTexte,
  type ZoneAColonnes,
} from './mobile/reglages-telephone'
import type { NbColonnes } from './mobile/ronds/disposition-ronds'
import { epurePermis, type Affichage } from './affichage'
import { essaiPhaseMechant } from './essais'
import {
  PHASE_BIS_POUR_TOUS,
  PHASE_BIS_VISIBLE,
  phaseTrisUtilisable,
  PHASE_DYNAMIQUE_VISIBLE,
  PHASE_ETAPE_VISIBLE,
  ecrirePresentationPhase,
  lirePresentationPhase,
  suivrePresentationPhase,
  type PresentationPhase,
} from './phase-presentation'
import { RoueTeinte } from './RoueTeinte'
import type { Teinte } from './teinte'
import { ecrireFaconParDefaut, lireFaconParDefaut, type FaconDeJouer } from './manuel/facon-de-jouer'
import { ecrireVolumeSons, jouerSon, lireVolumeSons } from './sons'
import './reglages.css'
import type { DosCartes } from './dos-cartes'

/** Les quatre onglets, dans l'ordre ou ils s'affichent. */
// Rangement du 04/10/2026 (questions une a une) : Apparence, Son, Jeu, Avance.
export const ONGLETS = ['apparence', 'son', 'jeu', 'avance'] as const
export type Onglet = (typeof ONGLETS)[number]

export function libelleOnglet(onglet: Onglet): string {
  switch (onglet) {
    case 'apparence':
      return t('Apparence')
    case 'son':
      return t('Son')
    case 'jeu':
      return t('Jeu')
    case 'avance':
      return t('Avancé')
  }
}

/* ------------------------------------------------------------- briques -- */

/**
 * Une ligne interrupteur.
 *
 * `parent` = ce reglage depend d'un autre : il se met en retrait, et
 * `disponible: false` le grise SANS le cacher (voir l'avertissement en tete).
 */
export function LigneBascule({
  libelle,
  detail,
  actif,
  onBascule,
  parent = false,
  disponible = true,
  raisonIndisponible,
}: {
  libelle: string
  detail?: string
  actif: boolean
  onBascule: () => void
  parent?: boolean
  disponible?: boolean
  raisonIndisponible?: string
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={actif}
      disabled={!disponible}
      className={
        'ligne-option' +
        (actif ? ' est-actif' : '') +
        (parent ? ' est-enfant' : '') +
        (disponible ? '' : ' est-desactive')
      }
      onClick={onBascule}
      title={disponible ? detail : (raisonIndisponible ?? detail)}
    >
      <span className="ligne-option-libelle">
        {libelle}
        {detail ? <small className="ligne-option-aide">{disponible ? detail : (raisonIndisponible ?? detail)}</small> : null}
      </span>
      <span className="ligne-option-etat" aria-hidden="true">
        {actif ? t('Oui') : t('Non')}
      </span>
    </button>
  )
}

/** Une ligne « choix entre N », en pastilles. Meme regle de retrait et de gris. */
/**
 * Lot 6 (essai, multi) : la regle « qui fait avancer la phase du mechant »,
 * choisie par l'hote a la premiere phase, modifiable ici par lui seul. Lue a
 * l'ouverture ; absente tant qu'elle n'a pas ete choisie.
 */
function LigneAvancePhase() {
  const [politique, setPolitique] = useState<PolitiqueAvance | undefined>(undefined)
  useEffect(() => {
    let vivant = true
    void fetch('/get_avance_phase', { cache: 'no-store' })
      .then((r) => (r.ok ? r.json() : {}))
      .then((d: { politique?: string }) => {
        if (vivant) setPolitique(lirePolitique(d?.politique))
      })
      .catch(() => undefined)
    return () => {
      vivant = false
    }
  }, [])
  if (politique === undefined) return null
  return (
    <LigneChoix
      libelle={t('Qui fait avancer (multi)')}
      valeur={politique}
      choix={[
        { valeur: 'concerne' as PolitiqueAvance, libelle: t('Le joueur concerné') },
        { valeur: 'tous' as PolitiqueAvance, libelle: t('Tout le monde valide') },
        { valeur: 'quiconque' as PolitiqueAvance, libelle: t('N’importe qui') },
      ]}
      onChoisir={(choix) => {
        setPolitique(choix)
        void choisirPolitique(0, choix)
      }}
      detail={t('Pour toute la table, dans cette partie')}
    />
  )
}

export function LigneChoix<T extends string | number>({
  libelle,
  valeur,
  choix,
  onChoisir,
  parent = false,
  disponible = true,
  detail,
}: {
  libelle: string
  valeur: T
  choix: ReadonlyArray<{ valeur: T; libelle: string }>
  onChoisir: (valeur: T) => void
  parent?: boolean
  disponible?: boolean
  detail?: string
}) {
  return (
    <div
      className={
        'ligne-option ligne-option-choix' +
        (parent ? ' est-enfant' : '') +
        (disponible ? '' : ' est-desactive')
      }
      title={detail}
    >
      <span className="ligne-option-libelle">
        {libelle}
        {detail ? <small className="ligne-option-aide">{detail}</small> : null}
      </span>
      <span className="mode-actions" role="group" aria-label={libelle}>
        {choix.map((c) => (
          <button
            key={String(c.valeur)}
            type="button"
            disabled={!disponible}
            className={valeur === c.valeur ? 'est-actif' : ''}
            onClick={() => onChoisir(c.valeur)}
          >
            {c.libelle}
          </button>
        ))}
      </span>
    </div>
  )
}

/** Le défaut du lanceur : Automatique ou Manuel façon OCTGN. Se retient sur cet appareil. */
/**
 * Le volume des bruitages, séparé de la musique (refonte des sons, 07/10/2026).
 * Autonome comme `LigneFaconDeJouer` : il lit et écrit lui-même son réglage,
 * partagé avec le lanceur (`prepare/sons.js`). Grisé, jamais caché, quand les
 * bruitages sont coupés. Lâcher le curseur fait entendre le niveau choisi.
 */
function LigneVolumeSons({ disponible }: { disponible: boolean }) {
  const [volume, setVolume] = useState(lireVolumeSons)
  const libelle = t('Volume des bruitages')
  return (
    <div
      className={'ligne-option ligne-option-choix' + (disponible ? '' : ' est-desactive')}
      title={t('Coups, cartes, jetons, survol des menus')}
    >
      <span className="ligne-option-libelle">
        {libelle}
        <small className="ligne-option-aide">{`${volume} %`}</small>
      </span>
      <input
        type="range"
        className="ligne-option-curseur"
        min={0}
        max={100}
        step={5}
        value={volume}
        disabled={!disponible}
        aria-label={libelle}
        aria-valuetext={`${volume} %`}
        onChange={(evenement) => {
          const valeur = Number(evenement.target.value)
          setVolume(valeur)
          ecrireVolumeSons(valeur)
        }}
        onPointerUp={() => jouerSon('activate')}
        onKeyUp={() => jouerSon('activate')}
      />
    </div>
  )
}

/**
 * La phase du méchant : TROIS choix pour tout le monde (19/10/2026), dans l'ordre « Guidée »,
 * « Plateau animé », « Accéléré ». « Étape par étape » (l'ancien cartouche) et « Phase dynamique » sont cachés
 * derrière `PHASE_ETAPE_VISIBLE` et `PHASE_DYNAMIQUE_VISIBLE` (board/phase-presentation.ts) : le code reste,
 * remettre un drapeau à `true` les montre de nouveau. « bis » ne dépend plus de l'essai « nouvelle phase »
 * de /admin (`PHASE_BIS_POUR_TOUS`).
 */
function LignePhaseMechant({ p }: { p: ProprietesReglages }) {
  const [essai, setEssai] = useState(false)
  useEffect(() => {
    let vivant = true
    void essaiPhaseMechant().then((oui) => {
      if (vivant) setEssai(oui)
    })
    return () => {
      vivant = false
    }
  }, [])
  const [presentation, setPresentation] = useState(lirePresentationPhase)
  useEffect(() => suivrePresentationPhase(setPresentation), [])
  const bisOuvert = PHASE_BIS_POUR_TOUS || essai
  // Le mode `detaille` se lit par sa présentation ; `lirePresentationPhase` ne rend jamais un choix caché.
  const valeur: string = p.modePhase === 'detaille' && bisOuvert ? presentation : p.modePhase
  return (
    <LigneChoix<string>
      libelle={t('Présentation')}
      valeur={valeur}
      choix={[
        ...(PHASE_ETAPE_VISIBLE || !bisOuvert ? [{ valeur: 'detaille', libelle: t('Étape par étape') }] : []),
        ...(bisOuvert && PHASE_BIS_VISIBLE ? [{ valeur: 'bis', libelle: t('Étape par étape bis') }] : []),
        // « Guidée » (`tris`) : pour tout le monde depuis le 19/10/2026 (drapeau PHASE_TRIS_POUR_TOUS).
        ...(bisOuvert && phaseTrisUtilisable() ? [{ valeur: 'tris', libelle: t('Guidée') }] : []),
        ...(bisOuvert && PHASE_DYNAMIQUE_VISIBLE ? [{ valeur: 'dynamique', libelle: t('Phase dynamique') }] : []),
        // « Plateau animé » : OUVERT À TOUS depuis le 05/10/2026, quand la
        // fenêtre de préparation « Choisis ta phase du méchant » l'a
        // présenté à chaque joueur (décision de l'utilisateur). Un mode
        // proposé là doit pouvoir se retrouver ici.
        ...(MODE_SUR_TABLE_OUVERT ? [{ valeur: 'sur-table', libelle: t(p.libelleModePhase('sur-table')) }] : []),
        { valeur: 'instantane', libelle: t('Accéléré') },
      ]}
      onChoisir={(v) => {
        if (v === 'bis' || v === 'tris' || v === 'dynamique' || v === 'detaille') {
          if (bisOuvert) ecrirePresentationPhase(v === 'detaille' ? 'etape' : (v as PresentationPhase))
          p.changerModePhase('detaille')
          return
        }
        p.changerModePhase(v as ModePhaseMechant)
      }}
      detail={
        bisOuvert && !PHASE_ETAPE_VISIBLE
          ? t('Guidée : « Lire la suite » puis « Étape suivante » à chaque étape de la phase. Plateau animé : les cartes bougent sur la table. Accéléré : tout se joue d’un coup')
          : t('Étape par étape : un « Suivant » par étape de la phase')
      }
    />
  )
}

/** « Phase du méchant automatique : Non / 2 s / 5 s » (23/10/2026). Sans objet en « Accéléré » : rien n'y attend de clic. */
function LigneDelaiAutoPhase() {
  const [delai, setDelai] = useState<DelaiAutoPhase>(lireDelaiAutoPhase)
  useEffect(() => suivreDelaiAutoPhase(setDelai), [])
  return (
    <LigneChoix<DelaiAutoPhase>
      libelle={t('Phase du méchant automatique')}
      valeur={delai}
      choix={[
        { valeur: 0, libelle: t('Non') },
        { valeur: 2000, libelle: t('2 s') },
        { valeur: 5000, libelle: t('5 s') },
      ]}
      onChoisir={(vers) => {
        ecrireDelaiAutoPhase(vers)
        setDelai(vers)
      }}
      detail={t('Chaque étape se valide toute seule après ce délai ; un clic la passe tout de suite. Réglage personnel.')}
    />
  )
}

/** Le titre d'une section d'un onglet (« Phase du méchant », « Mon tour »...). Même style que l'ancien titre de groupe. */
function TitreSection({ children }: { children: string }) {
  return <p className="reglages-groupe">{children}</p>
}

function LigneFaconDeJouer() {
  const [facon, setFacon] = useState<FaconDeJouer>(lireFaconParDefaut)
  return (
    <LigneChoix
      libelle={t('Façon de jouer')}
      valeur={facon}
      choix={[
        { valeur: 'auto' as FaconDeJouer, libelle: t('Auto') },
        { valeur: 'manuel' as FaconDeJouer, libelle: t('Manuel') },
      ]}
      onChoisir={(valeur) => {
        ecrireFaconParDefaut(valeur)
        setFacon(valeur)
      }}
      detail={t('Choix proposé au lancement d’une nouvelle partie ; la partie en cours ne change pas')}
    />
  )
}

function LigneEtiquettesTable() {
  const [actif, setActif] = useState(lireEtiquettesTable)
  return (
    <LigneBascule
      libelle={t('Étiquettes de type sur la table')}
      detail={t('« Allié », « Soutien »… au-dessus des cartes en jeu ; toujours visibles dans la main')}
      actif={actif}
      onBascule={() => {
        ecrireEtiquettesTable(!actif)
        setActif(!actif)
      }}
    />
  )
}

function LigneBarreAvantage() {
  const [actif, setActif] = useState(lireBarreAvantage)
  return (
    <LigneBascule
      libelle={t('Barre d’avantage (estimation)')}
      detail={t('Une fine barre au bord gauche : elle monte quand les héros dominent. Une estimation, pas une probabilité')}
      actif={actif}
      onBascule={() => {
        ecrireBarreAvantage(!actif)
        setActif(!actif)
      }}
    />
  )
}

function LigneCoteAmeliorations() {
  const [cote, setCote] = useState<CoteAmeliorations>(lireCoteAmeliorations)
  return (
    <LigneChoix
      libelle={t('Améliorations')}
      valeur={cote}
      choix={[
        { valeur: 'gauche' as CoteAmeliorations, libelle: t('À gauche') },
        { valeur: 'droite' as CoteAmeliorations, libelle: t('À droite') },
      ]}
      onChoisir={(valeur) => {
        ecrireCoteAmeliorations(valeur)
        setCote(valeur)
      }}
      detail={t('De quel côté de la carte qui les porte (héros, alliés, méchant, sbires)')}
    />
  )
}

/* ---------------------------------------------------------- telephone -- */
// Zone 3 de la refonte (10/10/2026) : trois reglages du TELEPHONE, montres sur
// telephone seulement (`telephone`). Autonomes comme `LigneEtiquettesTable` :
// ils lisent et ecrivent eux-memes leur valeur (mobile/reglages-telephone.ts),
// et le plateau ouvert suit sans rechargement.

function LignePlateauTelephone() {
  const { plateau } = useReglagesTelephone()
  return (
    <LigneChoix
      libelle={t('Plateau')}
      valeur={plateau}
      choix={[
        { valeur: 'ronds' as PlateauTelephone, libelle: t('Ronds') },
        { valeur: 'cartes' as PlateauTelephone, libelle: t('Cartes') },
      ]}
      onChoisir={(valeur) => ecrireReglageTelephone('plateau', valeur)}
      detail={t('La forme de la table au téléphone (les ronds sont plus adaptés au téléphone)')}
    />
  )
}

// LA TABLETTE (24/10/2026, decision 10) : Auto suit l'appareil (tactile sans
// souris), Oui / Non le forcent (PC a ecran tactile, iPad avec une souris).
function LigneJeuAuDoigt() {
  const [reglage, setReglage] = useState<ReglageDoigt>(lireReglageDoigt)
  return (
    <LigneChoix<ReglageDoigt>
      libelle={t('Jeu au doigt')}
      valeur={reglage}
      choix={[
        { valeur: 'auto', libelle: t('Auto') },
        { valeur: 'oui', libelle: t('Oui') },
        { valeur: 'non', libelle: t('Non') },
      ]}
      onChoisir={(valeur) => {
        ecrireReglageDoigt(valeur)
        setReglage(valeur)
      }}
      detail={t('Tablette : aperçu au toucher, gros boutons, glisser les cartes')}
    />
  )
}

function LigneDemanderLePlateau() {
  const { plateauMemorise } = useReglagesTelephone()
  return (
    <LigneBascule
      libelle={t('Demander le plateau à chaque partie')}
      detail={t('Cartes ou ronds, au début de chaque partie sur téléphone')}
      actif={!plateauMemorise}
      onBascule={() => ecrireReglageTelephone('plateauMemorise', !plateauMemorise)}
    />
  )
}

function LigneAideDebut() {
  const { aideDebut } = useReglagesTelephone()
  return (
    <LigneBascule
      libelle={t('Aide au début de la partie')}
      detail={t('La visite guidée des ronds, à la prochaine partie sur téléphone')}
      actif={aideDebut}
      onBascule={() => ecrireReglageTelephone('aideDebut', !aideDebut)}
    />
  )
}

function LigneTailleTexte() {
  const { tailleTexte } = useReglagesTelephone()
  return (
    <LigneChoix
      libelle={t('Taille du texte')}
      valeur={tailleTexte}
      choix={[
        { valeur: 'normal' as TailleTexte, libelle: t('Normale') },
        { valeur: 'grand' as TailleTexte, libelle: t('Grande') },
        { valeur: 'tres-grand' as TailleTexte, libelle: t('Très grande') },
      ]}
      onChoisir={(valeur) => ecrireReglageTelephone('tailleTexte', valeur)}
      detail={t('Bandeau, titres, menus et boutons du plateau')}
    />
  )
}

/** Le nombre de colonnes d'une zone de la table en ronds (26/10/2026) : 1, 2, 3, 4 ou Auto. */
function LigneColonnesZone({ zone, titre }: { zone: ZoneAColonnes; titre: string }) {
  const { colonnesZones } = useReglagesTelephone()
  return (
    <LigneChoix
      libelle={`${t('Colonnes')} : ${titre}`}
      valeur={colonnesZones[zone] as number}
      choix={[
        { valeur: 1, libelle: '1' },
        { valeur: 2, libelle: '2' },
        { valeur: 3, libelle: '3' },
        { valeur: 4, libelle: '4' },
        { valeur: 0, libelle: t('Auto') },
      ]}
      onChoisir={(valeur) => ecrireColonnesZone(zone, valeur as NbColonnes)}
    />
  )
}

function LignesColonnesZones() {
  return (
    <>
      <LigneColonnesZone zone="manigances" titre={t('Manigances')} />
      <LigneColonnesZone zone="allies" titre={t('Alliés')} />
      <LigneColonnesZone zone="sbires" titre={t('Sbires')} />
      <LigneColonnesZone zone="enJeu" titre={t('Cartes en jeu')} />
    </>
  )
}

function LigneVerrouPortrait() {
  const { verrouPortrait } = useReglagesTelephone()
  return (
    <LigneBascule
      libelle={t('Verrou portrait')}
      detail={t('Garde le plateau debout quand le téléphone se couche')}
      actif={verrouPortrait}
      onBascule={() => ecrireReglageTelephone('verrouPortrait', !verrouPortrait)}
    />
  )
}

function LigneVibrations() {
  const { vibrations } = useReglagesTelephone()
  return (
    <LigneBascule
      libelle={t('Vibrations')}
      detail={t('Ton tour, attaque subie, action validée')}
      actif={vibrations}
      onBascule={() => ecrireReglageTelephone('vibrations', !vibrations)}
    />
  )
}

/* -------------------------------------------------------------- fenetre -- */

export type ProprietesReglages = {
  affichage: Affichage
  changerAffichage: (affichage: Affichage) => void
  /** La teinte du fond (RoueTeinte) ; `undefined` = couleur d'origine. */
  teinte?: Teinte
  changerTeinte?: (teinte: Teinte) => void
  reinitialiserTeinte?: () => void
  /** « Modifier la table » (table personnalisable) ; absent sur telephone. */
  modifierLaTable?: () => void
  animations: boolean
  basculerAnimations: () => void
  sons: boolean
  basculerSons: () => void
  musique: boolean
  basculerMusique: () => void
  scansFr: boolean
  basculerScansFr: () => void
  /** Dos de cartes : officiels Marvel ou NarwhalChampions (dos-cartes.ts). */
  dosCartes?: DosCartes
  changerDosCartes?: (choix: DosCartes) => void
  textesCdb: boolean
  basculerTextesCdb: () => void
  basculerLangue: () => void | Promise<void>

  modePhase: ModePhaseMechant
  changerModePhase: (mode: ModePhaseMechant) => void
  /** Lot 6 (essai, multi) : l'hote peut changer qui fait avancer la phase du mechant. */
  avancePhaseHote?: boolean
  libelleModePhase: (mode: ModePhaseMechant) => string
  /** « Temps par decision » du moteur, en secondes ; 0 = sans limite. */
  tempsParDecision: number
  texteTempsParDecision: () => string
  validationCourte: boolean
  basculerValidationCourte: () => void
  autoCible: boolean
  basculerAutoCible: () => void
  finTourAuto: boolean
  basculerFinTourAuto: () => void
  paiementAuto: boolean
  basculerPaiementAuto: () => void
  sauvegardeAuto: boolean
  basculerSauvegardeAuto: () => void
  revelation: ModeRevelation
  cyclerRevelation: () => void

  meteo: boolean
  basculerMeteo: () => void
  apercuMeteo: ApercuMeteo
  reglerApercuMeteo: (valeur: ApercuMeteo) => void
  reponseAmbiance: ReponseAmbiance
  cyclerReponseAmbiance: () => void

  designEssai: boolean
  basculerDesignEssai: () => void
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
  curseurs: boolean
  basculerCurseurs: () => void
  montrerDisposition: boolean
  reglageMode: ReglageMode
  cyclerReglageMode: () => void
  /** Sur telephone : taille du texte, verrou portrait, vibrations (zone 3). */
  telephone?: boolean
  /** Le plateau PC joue au doigt (board/tablette/tablette.ts). Le reglage s'affiche hors telephone. */
  tablette?: boolean
}

export function ContenuOnglet({
  onglet,
  p,
}: {
  onglet: Onglet
  p: ProprietesReglages
}) {
  if (onglet === 'apparence') {
    const sobre = p.affichage === 'sobre'
    return (
      <>
        <TitreSection>{t('Affichage')}</TitreSection>
        {/* Trois affichages au choix (18/10/2026) : Normal (valeur `epure`, celui de depart), Colore (valeur
            `normal`), Sobre. Sans droit a l'epure (ancienne reserve), Normal n'est pas propose. */}
        <LigneChoix
          libelle={t('Style d’affichage')}
          valeur={p.affichage}
          choix={[
            ...(epurePermis() ? [{ valeur: 'epure' as Affichage, libelle: t('Normal') }] : []),
            { valeur: 'normal' as Affichage, libelle: t('Coloré') },
            { valeur: 'sobre' as Affichage, libelle: t('Sobre') },
          ]}
          onChoisir={p.changerAffichage}
          detail={t('Coloré : couleurs du héros et halo vif. Sobre : fond gris, sans couleurs ni animations')}
        />
        {/* La couleur du fond (04/10/2026) : la table change en direct. */}
        {p.changerTeinte && p.reinitialiserTeinte ? (
          <div className="reglage-teinte">
            <span className="reglage-teinte-titre">{t('Couleur de la table')}</span>
            <RoueTeinte valeur={p.teinte} changer={p.changerTeinte} reinitialiser={p.reinitialiserTeinte} />
          </div>
        ) : null}
        <LigneBascule
          libelle={t('Animations')}
          detail={t('Cartes qui bougent, secousses, halos')}
          actif={p.animations && !sobre}
          onBascule={p.basculerAnimations}
          parent
          disponible={!sobre}
          raisonIndisponible={t('Coupées par l’affichage sobre')}
        />
        <LigneBascule
          libelle={t('Météo et décor')}
          detail={t('Selon les cartes en jeu (pluie de Storm…)')}
          actif={p.meteo}
          onBascule={p.basculerMeteo}
        />
        {/* Deja ecrit pour se griser tout seul quand l'ambiance est coupee. */}
        <ReglagesApercuAmbiance
          meteo={p.meteo}
          apercuMeteo={p.apercuMeteo}
          reglerApercuMeteo={p.reglerApercuMeteo}
          reponseAmbiance={p.reponseAmbiance}
          cyclerReponseAmbiance={p.cyclerReponseAmbiance}
        />
        <TitreSection>{t('Sur la table')}</TitreSection>
        {/* La table personnalisable (04/10/2026). PC seulement. */}
        {p.modifierLaTable ? (
          <div className="reglage-teinte reglage-table">
            <span className="reglage-teinte-titre">{t('Placement des zones')}</span>
            <button type="button" className="bh-bouton" onClick={p.modifierLaTable}>
              {t('Modifier la table')}
            </button>
          </div>
        ) : null}
        <LigneEtiquettesTable />
        <LigneBarreAvantage />
        {p.telephone ? null : <LigneJeuAuDoigt />}
        {p.telephone ? (
          <>
            <LignePlateauTelephone />
            <LigneDemanderLePlateau />
            <LigneAideDebut />
            <LigneTailleTexte />
            <LignesColonnesZones />
            <LigneVerrouPortrait />
          </>
        ) : null}
        <TitreSection>{t('Langue et cartes')}</TitreSection>
        {/* La langue n'est pas un interrupteur oui/non : deux pastilles nommees,
            pour qu'on lise ou on va avant de cliquer. */}
        <LigneChoix
          libelle={t('Langue')}
          valeur={langueActuelle() === 'fr' ? 'fr' : 'en'}
          choix={[
            { valeur: 'fr', libelle: 'Français' },
            { valeur: 'en', libelle: 'English' },
          ]}
          onChoisir={(vers) => {
            if (vers !== (langueActuelle() === 'fr' ? 'fr' : 'en')) void p.basculerLangue()
          }}
          // ⚠ CE QUE LA LANGUE NE PEUT PAS FAIRE, DIT AU MOMENT DU CHOIX
          // (16/09/2026) : une carte sans scan dans cette langue reste en
          // anglais, et l'infobulle prend le relais.
          detail={t('Langue de l’interface et de la narration. Une carte sans scan dans cette langue reste en anglais : agrandie, sa traduction est posée sur son texte.')}
        />
        <LigneBascule
          libelle={t('Cartes en français')}
          detail={t('Images des cartes en français quand elles existent')}
          actif={p.scansFr}
          onBascule={p.basculerScansFr}
        />
        {p.dosCartes && p.changerDosCartes ? (
          <LigneChoix
            libelle={t('Dos de cartes')}
            valeur={p.dosCartes}
            choix={[
              { valeur: 'officiels' as DosCartes, libelle: t('Officiels Marvel') },
              { valeur: 'narwhal' as DosCartes, libelle: 'NarwhalChampions' },
            ]}
            onChoisir={p.changerDosCartes}
            detail={t('Le dos des cartes face cachée : decks, boosts, cartes rencontre')}
          />
        ) : null}
        <LigneBascule
          libelle={t('Texte des cartes en français')}
          detail={t('Sous l’aperçu agrandi (chargé depuis fr.marvelcdb.com)')}
          actif={p.textesCdb}
          onBascule={p.basculerTextesCdb}
        />
      </>
    )
  }

  if (onglet === 'son') {
    return (
      <>
        <TitreSection>{t('Sons')}</TitreSection>
        <LigneBascule
          libelle={t('Bruitages')}
          detail={t('Coups, cartes jouées, menaces')}
          actif={p.sons}
          onBascule={p.basculerSons}
        />
        <LigneVolumeSons disponible={p.sons} />
        {p.telephone ? <LigneVibrations /> : null}
        <TitreSection>{t('Musique')}</TitreSection>
        <LigneBascule
          libelle={t('Musique de fond')}
          detail={t('Si un fichier de musique est installé')}
          actif={p.musique}
          onBascule={p.basculerMusique}
        />
      </>
    )
  }

  if (onglet === 'jeu') {
    return (
      <>
        <TitreSection>{t('Phase du méchant')}</TitreSection>
        {/* SUR TELEPHONE la presentation est d'office « Guidee » (26/10/2026, demande de l'utilisateur : pas d'autres
            choix) : pas de ligne « Presentation ». Le delai automatique ci-dessous reste : il vaut pour la Guidee. */}
        {p.telephone ? (
          <p className="ligne-option-note">{t('Guidée sur téléphone : « Lire la suite » puis « Étape suivante » à chaque étape de la phase')}</p>
        ) : (
          <LignePhaseMechant p={p} />
        )}
        {p.modePhase !== 'instantane' ? <LigneDelaiAutoPhase /> : null}
        {p.avancePhaseHote ? <LigneAvancePhase /> : null}
        {/* L'hypothese du mode, dite la ou on le choisit : un « Temps par
            decision » regle a la preparation fait expirer les attentes du
            moteur, qui poursuit sans nous. */}
        {p.modePhase === 'detaille' && p.tempsParDecision > 0 ? (
          <p className="ligne-option-note">{p.texteTempsParDecision()}</p>
        ) : null}
        <LigneChoix
          libelle={t('Carte révélée en grand')}
          valeur={p.revelation}
          choix={[
            { valeur: 'off' as ModeRevelation, libelle: t('Non') },
            { valeur: 'court' as ModeRevelation, libelle: t('2,6 s') },
            { valeur: 'long' as ModeRevelation, libelle: t('5 s') },
          ]}
          onChoisir={(vers) => {
            // Le reglage se cycle (un seul geste cote moteur) : on avance
            // jusqu'a tomber sur la valeur demandee, au plus deux fois.
            if (vers === p.revelation) return
            p.cyclerRevelation()
            if (vers !== suivantRevelation(p.revelation)) p.cyclerRevelation()
          }}
          // D42 (04/10/2026) : en « Étape par étape », la carte révélée se montre
          // en grand DANS le cartouche du bas. La ligne reste, grisée, et dit
          // pourquoi ; les deux autres modes la gardent.
          disponible={p.modePhase !== 'detaille'}
          detail={
            p.modePhase === 'detaille'
              ? t('Le cartouche s’en charge')
              : t('Au centre de l’écran, le temps de la lire')
          }
        />
        <TitreSection>{t('Mon tour')}</TitreSection>
        <LigneFaconDeJouer />
        <LigneCoteAmeliorations />
        <TitreSection>{t('Le jeu agit pour moi quand il n’y a qu’un choix')}</TitreSection>
        <LigneBascule
          libelle={t('Choisir la seule cible possible')}
          actif={p.autoCible}
          onBascule={p.basculerAutoCible}
        />
        <LigneBascule
          libelle={t('Valider sans demander')}
          detail={t('Cible unique et coût couvert')}
          actif={p.validationCourte}
          onBascule={p.basculerValidationCourte}
        />
        <LigneBascule
          libelle={t('Payer avec la seule carte possible')}
          actif={p.paiementAuto}
          onBascule={p.basculerPaiementAuto}
        />
        <LigneBascule
          libelle={t('Finir mon tour quand je ne peux plus rien jouer')}
          actif={p.finTourAuto}
          onBascule={p.basculerFinTourAuto}
        />
        <TitreSection>{t('Partie')}</TitreSection>
        <LigneBascule
          libelle={t('Sauvegarde à chaque phase')}
          detail={t('En plus des trois emplacements')}
          actif={p.sauvegardeAuto}
          onBascule={p.basculerSauvegardeAuto}
        />
      </>
    )
  }

  return (
    <>
      <TitreSection>{t('Plateau')}</TitreSection>
      <LigneBascule
        libelle={t('Nouveau plateau')}
        detail={t('Non : l’ancien plateau (avant septembre)')}
        actif={p.designEssai}
        onBascule={p.basculerDesignEssai}
      />
      <LigneChoix
        libelle={t('Aide quand je joue une carte')}
        valeur={p.modeActions}
        choix={[
          { valeur: 'simple' as ModeActions, libelle: t('Courte') },
          { valeur: 'detailed' as ModeActions, libelle: t('Détaillée') },
        ]}
        onChoisir={p.changerModeActions}
        parent
        disponible={p.designEssai}
        detail={t('Ce que dit le panneau quand tu joues une carte')}
      />
      {/* Montre UNIQUEMENT sur un appareil mobile : sur un PC le plateau est de
          toute facon rendu en mode PC, le reglage n'aurait aucun effet et c'est
          lui qui a un jour enferme l'utilisateur. */}
      {p.montrerDisposition ? (
        <LigneChoix
          libelle={t('Table complète comme sur PC')}
          valeur={p.reglageMode === 'pc' ? 'pc' : 'auto'}
          choix={[
            { valeur: 'auto', libelle: t('Non') },
            { valeur: 'pc', libelle: t('Oui') },
          ]}
          onChoisir={(vers) => {
            if (vers !== (p.reglageMode === 'pc' ? 'pc' : 'auto')) p.cyclerReglageMode()
          }}
          detail={t('Non : la vue téléphone, adaptée à l’écran')}
        />
      ) : null}
      <TitreSection>{t('Multijoueur')}</TitreSection>
      <LigneBascule
        libelle={t('Curseurs des autres joueurs')}
        detail={t('En multijoueur, voir le curseur des autres joueurs')}
        actif={p.curseurs}
        onBascule={p.basculerCurseurs}
      />
      <p className="options-raccourcis">
        {t(
          'Raccourcis : E ou Espace = fin du tour, Entrée ou Espace = étape suivante pendant le déroulé d’une phase, U = annuler, Échap = annuler l’action en cours'
        )}
      </p>
    </>
  )
}

/** L'ordre du cycle de `cyclerRevelation`, pour viser une valeur en un ou deux pas. */
export function suivantRevelation(actuel: ModeRevelation): ModeRevelation {
  return actuel === 'off' ? 'court' : actuel === 'court' ? 'long' : 'off'
}

export function FenetreReglages({
  ouvert,
  fermer,
  lectureSeule,
  ...p
}: { ouvert: boolean; fermer: () => void; lectureSeule?: boolean } & ProprietesReglages) {
  const [onglet, setOnglet] = useState<Onglet>('apparence')
  const boite = useRef<HTMLDivElement | null>(null)
  // La recherche (23/10/2026) : non vide, les quatre onglets se rendent a la suite et le filtre cache ce qui ne correspond pas.
  const [recherche, setRecherche] = useState('')
  const [aucunResultat, setAucunResultat] = useState(false)
  const enRecherche = recherche.trim() !== ''
  const contenu = useRef<HTMLDivElement | null>(null)
  // A CHAQUE rendu : une ligne recreee par React (un reglage qui change) doit retrouver son etat cache ou montre.
  useLayoutEffect(() => {
    const racine = contenu.current
    if (!racine) return
    const visibles = filtrerReglages(racine, recherche)
    setAucunResultat(enRecherche && visibles === 0)
  })
  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »).
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(ouvert ? 'reglages-ouvert' : 'reglages-ferme')

  // ⚠ Echap ferme, et le clic sur le fond aussi : une modale qu'on ne peut
  // fermer que par un bouton precis est une modale dont on se sent prisonnier,
  // ce qui est exactement le reproche fait a l'ancien empilement de menus.
  const surTouche = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === 'Escape') fermer()
    },
    [fermer]
  )
  useEffect(() => {
    if (!ouvert) return
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [ouvert, surTouche])

  if (!ouvert) return null

  return (
    <div
      className="reglages-fond"
      role="presentation"
      onClick={(e) => {
        if (e.target === e.currentTarget) fermer()
      }}
    >
      <div
        className="reglages-fenetre est-reglages"
        role="dialog"
        aria-modal="true"
        aria-label={t('Réglages')}
        ref={boite}
        style={transformDecalage(decalage)}
      >
        <header className="reglages-tete">
          <h2
            className="poignee-glisser"
            onPointerDown={gestesGlisser.onPointerDown}
            onPointerMove={gestesGlisser.onPointerMove}
            onPointerUp={gestesGlisser.onPointerUp}
            onPointerCancel={gestesGlisser.onPointerCancel}
          >
            {t('Réglages')}
          </h2>
          <input
            type="search"
            className="reglages-recherche"
            value={recherche}
            placeholder={t('Chercher un réglage…')}
            aria-label={t('Chercher un réglage')}
            onChange={(e) => setRecherche(e.target.value)}
            onKeyDown={(e) => {
              // Échap efface d'abord la recherche ; une seconde fois, il ferme la fenêtre.
              if (e.key === 'Escape' && recherche !== '') {
                e.stopPropagation()
                setRecherche('')
              }
            }}
          />
          <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
            ×
          </button>
        </header>
        {/* Sur ordinateur cette liste est une colonne a gauche ; sur telephone
            elle passe en bandeau horizontal qui glisse du doigt. Un seul
            balisage, c'est la CSS qui bascule (board.css, .reglages-onglets). */}
        <nav className="reglages-onglets" role="tablist" aria-label={t('Réglages')}>
          {ONGLETS.map((o) => (
            <button
              key={o}
              type="button"
              role="tab"
              aria-selected={onglet === o && !enRecherche}
              className={`reglages-onglet${onglet === o && !enRecherche ? ' est-actif' : ''}`}
              onClick={() => {
                setRecherche('')
                setOnglet(o)
              }}
            >
              {libelleOnglet(o)}
            </button>
          ))}
        </nav>
        <div className="reglages-contenu" role="tabpanel" aria-label={enRecherche ? t('Résultats de la recherche') : libelleOnglet(onglet)} ref={contenu}>
          {lectureSeule ? <p className="reglages-lecture-seule">{t('Réglages du joueur, en lecture seule.')}</p> : null}
          <div {...(lectureSeule ? { inert: true } : {})}>
            {enRecherche ? (
              ONGLETS.map((o) => (
                <div key={o} data-onglet={o}>
                  <ContenuOnglet onglet={o} p={p} />
                </div>
              ))
            ) : (
              <div data-onglet={onglet}>
                <ContenuOnglet onglet={onglet} p={p} />
              </div>
            )}
          </div>
          {aucunResultat ? <p className="reglages-aucun-resultat">{t('Aucun réglage ne correspond à cette recherche.')}</p> : null}
        </div>
      </div>
    </div>
  )
}
