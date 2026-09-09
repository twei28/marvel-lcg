from . import *

# Facial Recognition Uplink — AMELIORATION, cout 3 [mental]. TECH.
# While a tracked minion is in play, your hero gets +1 THW.
# Hero Response (thwart): After a minion enters play, track it.
#
# CARTES DE REFERENCE
#  - `04125` Red Skull, `01059`, `ho015` :
#    `ThisGainKeywordForEachFaceInPlay` pour un bonus qui depend de ce qui est
#    en jeu. Ici le bonus est BINAIRE (« while a tracked minion is in play »),
#    pas « for each » : on passe donc par `ThisGainKeyword(fn, ...)` avec une
#    fonction qui rend 1 ou 0 (modele `an001b`, `dt133`).
#  - `01083` Mockingbird, `ho002` : `AfterCardEnterPlay(type, Minion, op)`.
#  - Le mot-cle maison `track` : helper `Tracer` du set, fiche
#    `docs/reference/mots-cles/track.md`.
#
# TEXTE CONTRE CODE
#  ⚠ « WHILE a tracked minion is in play » : bonus CONTINU, pas une reponse. Il
#    apparait et disparait tout seul quand le dernier sbire trace meurt — c'est
#    `change_on_event` qui le fait recalculer.
#  ⚠ « YOUR HERO gets +1 THW » : la face HEROS, pas l'identite (lecon `an002`
#    Sera, RECETTES §3). Contre-cas dans l'autre forme du.
#  ⚠ « AFTER a minion ENTERS PLAY, track IT » : le sbire a tracer est CELUI qui
#    vient d'arriver, pas un sbire au choix. Le declencheur le donne
#    (`message.trigger`), on ne le redemande pas.
#  ⚠ ⚠ Et « track » est un DEPLACEMENT : sans menace sur une manigance, il ne se
#    passe RIEN. La Response est donc conditionnee, sinon elle est proposee pour
#    rien a chaque sbire (RECETTES §1, lecon `bc010`).
#  ⚠ Le libelle imprime est « (thwart) » : `SetLabel('thwart')`, ce qui la rend
#    inutilisable sous un statut Desoriente.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def un_sbire_est_trace(effect: 'Effect') -> int:
        return 1 if SbiresTraces(effect) else 0

    def il_y_a_de_la_menace(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        Unused(message)
        return any(f is not None and getattr(f, "threat", 0)
                   for f in Worlds.GetOnFieldSchemes(effect))

    def tracer_le_nouveau(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        sbire = getattr(message, "trigger", None)
        if sbire is None:
            return
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Move 1 threat from a scheme to that minion (track)",
                lambda cibles: Tracer(effect, sbire, cibles),
            ).SetTarget(Scheme2, range=(1, 1)),
        )

    return [
        # ⚠⚠ `ex_change_on_event=OnEvent.Counter(Minion, 'threat')` : sans lui,
        # le bonus est calcule UNE fois et ne bouge plus, et « while a tracked
        # minion is in play » devient « au moment ou la carte est entree en
        # jeu ». Mesure du 08/09/2026 : le cas lisait CTR 2 au lieu de 3.
        # ⚠ Et `OnEvent.GameArea` NE SUFFIT PAS : ce qui change ici n'est pas la
        # presence d'une carte mais la pose d'un COMPTEUR sur un sbire deja en
        # jeu. `OnEvent.Counter` est l'evenement exact (modele `60053`, qui
        # emploie `OnEvent.CardInPlay(Ally)` pour sa propre condition).
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            thwart=1,
            get_new_value=lambda effect, this, attaches: un_sbire_est_trace(effect),
            ex_change_on_event=OnEvent.Counter(Minion, COMPTEUR_MENACE),
        ),

        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            Minion,
            tracer_le_nouveau,
            conditions=[il_y_a_de_la_menace],
        ).SetLabel('thwart'),
    ]
