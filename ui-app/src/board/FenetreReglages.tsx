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
import { useCallback, useEffect, useRef, useState } from 'react'
import { ReglagesApercuAmbiance, type ApercuMeteo } from './CoucheMeteo'
import { t, langueActuelle } from './langue'
import {
  DELAI_PAS_A_PAS_MAX,
  DELAI_PAS_A_PAS_MIN,
  type ModeActions,
  type ModePhaseMechant,
  type ModeRevelation,
  type ReponseAmbiance,
  MODE_SUR_TABLE_OUVERT,
} from './moteur'
import type { ReglageMode } from './mobile/useModeMobile'

/** Les quatre onglets, dans l'ordre ou ils s'affichent. */
export const ONGLETS = ['image', 'deroule', 'ambiance', 'avance'] as const
export type Onglet = (typeof ONGLETS)[number]

export function libelleOnglet(onglet: Onglet): string {
  switch (onglet) {
    case 'image':
      return t('Image et son')
    case 'deroule':
      return t('Déroulé de partie')
    case 'ambiance':
      return t('Ambiance')
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
      <span className="ligne-option-libelle">{libelle}</span>
      <span className="ligne-option-etat" aria-hidden="true">
        {actif ? t('Oui') : t('Non')}
      </span>
    </button>
  )
}

/** Une ligne « choix entre N », en pastilles. Meme regle de retrait et de gris. */
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
      <span className="ligne-option-libelle">{libelle}</span>
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

/* -------------------------------------------------------------- fenetre -- */

export type ProprietesReglages = {
  animations: boolean
  basculerAnimations: () => void
  sons: boolean
  basculerSons: () => void
  musique: boolean
  basculerMusique: () => void
  succes: boolean
  basculerSucces: () => void
  scansFr: boolean
  basculerScansFr: () => void
  textesCdb: boolean
  basculerTextesCdb: () => void
  basculerLangue: () => void | Promise<void>

  modePhase: ModePhaseMechant
  changerModePhase: (mode: ModePhaseMechant) => void
  libelleModePhase: (mode: ModePhaseMechant) => string
  /**
   * Les ESSAIS sont-ils ouverts pour ce client (`board/essais.ts`) ?
   *
   * Le mode « Sur la table » n'est proposé qu'à ce moment-là, le temps que
   * l'utilisateur le valide à l'usage. Les autres joueurs continuent de voir
   * deux modes, et rien ne change pour eux.
   *
   * ⚠ UN MODE ABSENT DE LA LISTE RESTE CHOISI S'IL EST DÉJÀ ÉCRIT. `LigneChoix`
   * n'affiche que les choix reçus : quelqu'un dont le stockage porterait
   * « sur-table » sans être en essais verrait une liste où aucun bouton n'est
   * actif, et le mode resterait actif sans être visible. D'où la liste
   * construite ci-dessous, qui l'ajoute AUSSI dans ce cas-là.
   */
  essais: boolean
  /** « Temps par decision » du moteur, en secondes ; 0 = sans limite. */
  tempsParDecision: number
  texteTempsParDecision: () => string
  avanceAuto: boolean
  basculerAvanceAuto: () => void
  delaiPasAPas: number
  reglerDelaiPasAPas: (ms: number) => void
  validationCourte: boolean
  basculerValidationCourte: () => void
  autoCible: boolean
  basculerAutoCible: () => void
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
}

export function ContenuOnglet({
  onglet,
  p,
}: {
  onglet: Onglet
  p: ProprietesReglages
}) {
  if (onglet === 'image') {
    return (
      <>
        <LigneBascule
          libelle={t('Animations')}
          detail={t('Déplacements de cartes, secousse d’impact, halo de statut')}
          actif={p.animations}
          onBascule={p.basculerAnimations}
        />
        <LigneBascule
          libelle={t('Sons')}
          detail={t('Effets sonores du moteur')}
          actif={p.sons}
          onBascule={p.basculerSons}
        />
        <LigneBascule
          libelle={t('Musique')}
          detail={t('Musique de fond (nécessite un fichier dans assets/sounds)')}
          actif={p.musique}
          onBascule={p.basculerMusique}
        />
        <LigneBascule
          libelle={t('Succès')}
          detail={t('Bannière quand un exploit est réalisé (Premier sang, Double K.O. ...)')}
          actif={p.succes}
          onBascule={p.basculerSucces}
        />
        <LigneBascule
          libelle={t('Scans en français')}
          detail={t('Images des cartes en français quand elles existent')}
          actif={p.scansFr}
          onBascule={p.basculerScansFr}
        />
        <LigneBascule
          libelle={t('Textes marvelcdb (réseau)')}
          detail={t('Texte officiel FR sous l’aperçu des cartes, via fr.marvelcdb.com')}
          actif={p.textesCdb}
          onBascule={p.basculerTextesCdb}
        />
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
          // (16/09/2026). Tous les scans n'existent pas dans les deux
          // langues. Sans cette phrase, une carte restee en anglais au milieu
          // d'une partie francaise ressemble a un defaut ; avec elle, c'est
          // une regle connue d'avance, et l'infobulle prend le relais.
          detail={t('Langue de l’interface et de la narration. Une carte sans scan dans cette langue reste en anglais : sa traduction s’affiche dans l’infobulle.')}
        />
      </>
    )
  }

  if (onglet === 'deroule') {
    return (
      <>
        <LigneChoix
          libelle={t('Phase du méchant')}
          valeur={p.modePhase}
          choix={[
            { valeur: 'detaille' as ModePhaseMechant, libelle: t(p.libelleModePhase('detaille')) },
            // « Sur la table » : réservé aux essais, ou déjà choisi (voir la
            // prop `essais`). Un mode actif mais absent de la liste laisserait
            // un écran de réglages où plus rien n'est coché.
            ...(MODE_SUR_TABLE_OUVERT && (p.essais || p.modePhase === 'sur-table')
              ? [{ valeur: 'sur-table' as ModePhaseMechant, libelle: t(p.libelleModePhase('sur-table')) }]
              : []),
            { valeur: 'instantane' as ModePhaseMechant, libelle: t(p.libelleModePhase('instantane')) },
          ]}
          onChoisir={p.changerModePhase}
        />
        {/* L'hypothese du mode, dite la ou on le choisit : un « Temps par
            decision » regle a la preparation fait expirer les attentes du
            moteur, qui poursuit sans nous. Le mode Instantane ne retient rien,
            l'hypothese ne lui sert a rien. */}
        {p.modePhase === 'detaille' && p.tempsParDecision > 0 ? (
          <p className="ligne-option-note">{p.texteTempsParDecision()}</p>
        ) : null}
        <LigneBascule
          libelle={t('Avance toute seule')}
          detail={t('Chaque étape se termine seule après un délai, sans attendre un clic')}
          actif={p.avanceAuto}
          onBascule={p.basculerAvanceAuto}
          parent
          disponible={p.modePhase === 'detaille'}
          raisonIndisponible={t('Seulement en phase du méchant détaillée')}
        />
        <label
          className={
            'ligne-option ligne-option-curseur est-enfant' +
            (p.modePhase === 'detaille' && p.avanceAuto ? '' : ' est-desactive')
          }
        >
          <span className="ligne-option-libelle">{t('Vitesse du déroulé')}</span>
          <input
            type="range"
            min={DELAI_PAS_A_PAS_MIN}
            max={DELAI_PAS_A_PAS_MAX}
            step={100}
            value={p.delaiPasAPas}
            disabled={!(p.modePhase === 'detaille' && p.avanceAuto)}
            onChange={(e) => p.reglerDelaiPasAPas(Number(e.target.value))}
            title={t('Temps d’affichage de chaque étape')}
          />
          <span className="ligne-option-etat" aria-hidden="true">
            {(p.delaiPasAPas / 1000).toFixed(1).replace('.', ',')} s
          </span>
        </label>
        <LigneBascule
          libelle={t('Validation courte')}
          detail={t('Supprime le « Valider » quand la cible est unique et le coût couvert')}
          actif={p.validationCourte}
          onBascule={p.basculerValidationCourte}
        />
        <LigneBascule
          libelle={t('Auto-ciblage')}
          detail={t('Sélectionne d’office la cible quand une seule est légale')}
          actif={p.autoCible}
          onBascule={p.basculerAutoCible}
        />
        <LigneChoix
          libelle={t('Cartes révélées')}
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
          detail={t('Présentation au centre des cartes révélées par la Rencontre')}
        />
      </>
    )
  }

  if (onglet === 'ambiance') {
    return (
      <>
        <LigneBascule
          libelle={t('Ambiance')}
          detail={t('Météo, décor ou traitement de l’image, selon les cartes en jeu')}
          actif={p.meteo}
          onBascule={p.basculerMeteo}
        />
        {/* Deja ecrit pour se griser tout seul quand l'ambiance est coupee :
            on le reprend tel quel plutot que de le reecrire ici. */}
        <ReglagesApercuAmbiance
          meteo={p.meteo}
          apercuMeteo={p.apercuMeteo}
          reglerApercuMeteo={p.reglerApercuMeteo}
          reponseAmbiance={p.reponseAmbiance}
          cyclerReponseAmbiance={p.cyclerReponseAmbiance}
        />
      </>
    )
  }

  return (
    <>
      <LigneBascule
        libelle={t('Nouveau design')}
        detail={t('Barre, bandeau et assistant d’action. Décoche pour revenir à l’ancien plateau.')}
        actif={p.designEssai}
        onBascule={p.basculerDesignEssai}
      />
      <LigneChoix
        libelle={t('Actions')}
        valeur={p.modeActions}
        choix={[
          { valeur: 'simple' as ModeActions, libelle: 'Simple' },
          { valeur: 'detailed' as ModeActions, libelle: t('Détaillé') },
        ]}
        onChoisir={p.changerModeActions}
        parent
        disponible={p.designEssai}
        detail={t('Niveau de détail de l’assistant d’action')}
      />
      <LigneBascule
        libelle={t('Curseurs des autres joueurs')}
        detail={t('En multijoueur, montre où pointent les autres')}
        actif={p.curseurs}
        onBascule={p.basculerCurseurs}
      />
      {/* Montre UNIQUEMENT sur un appareil mobile : sur un PC le plateau est de
          toute facon rendu en mode PC, le reglage n'aurait aucun effet et c'est
          lui qui a un jour enferme l'utilisateur. */}
      {p.montrerDisposition ? (
        <LigneChoix
          libelle={t('Disposition')}
          valeur={p.reglageMode === 'pc' ? 'pc' : 'auto'}
          choix={[
            { valeur: 'auto', libelle: t('Automatique') },
            { valeur: 'pc', libelle: t('Ordinateur') },
          ]}
          onChoisir={(vers) => {
            if (vers !== (p.reglageMode === 'pc' ? 'pc' : 'auto')) p.cyclerReglageMode()
          }}
          detail={t('Rendu du plateau : automatique selon l’appareil, ou forcer la table complète')}
        />
      ) : null}
      <p className="options-raccourcis">{t('Raccourcis : E = fin du tour, U = annuler')}</p>
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
  ...p
}: { ouvert: boolean; fermer: () => void } & ProprietesReglages) {
  const [onglet, setOnglet] = useState<Onglet>('image')
  const boite = useRef<HTMLDivElement | null>(null)

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
        className="reglages-fenetre"
        role="dialog"
        aria-modal="true"
        aria-label={t('Réglages')}
        ref={boite}
      >
        <header className="reglages-tete">
          <h2>{t('Réglages')}</h2>
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
              aria-selected={onglet === o}
              className={`reglages-onglet${onglet === o ? ' est-actif' : ''}`}
              onClick={() => setOnglet(o)}
            >
              {libelleOnglet(o)}
            </button>
          ))}
        </nav>
        <div className="reglages-contenu" role="tabpanel" aria-label={libelleOnglet(onglet)}>
          <ContenuOnglet onglet={onglet} p={p} />
        </div>
      </div>
    </div>
  )
}
