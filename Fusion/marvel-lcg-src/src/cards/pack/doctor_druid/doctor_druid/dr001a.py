from . import *

# * Doctor Druid (face heros) — AVENGER. MYSTIC. THW 1 / ATK 1 / DEF 2, main 5, PV 9.
# Druidic Ritual - Action: Take 1 damage -> play the topmost event with an
#   "Action", or "Hero Action" ability in your discard pile (paying its cost).
#   (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `05018` * Lockjaw pour « jouer depuis la defausse en payant son cout » :
#    le moteur n'a AUCUNE operation « joue cette carte », l'idiome est
#    `YouMayPlayCardLikeInHand(from_where="YourDiscardPile")`, qui rend la
#    carte JOUABLE, le joueur la jouant ensuite normalement.
#  - `aoa/45043` et `core/she_hulk/01027` pour `CostFunc.TakeDamage`.
#
# TEXTE CONTRE CODE
#  « Take 1 damage » -> DANS LE COUT (`CostFunc.TakeDamage(1, "YourIdentity")`),
#    jamais dans le corps : sinon le degat tomberait meme si la suite echoue.
#  « the TOPMOST event » -> le DESSUS de la defausse, donc la DERNIERE carte
#    posee : on parcourt `discard_pile` a l'ENVERS.
#  « with an "Action", or "Hero Action" ability » -> `EvenementRejouable`.
#    ⚠ MOT-PIEGE : `dr008` Mystical Protection est une Hero INTERRUPT, donc
#    PAS rejouable, alors qu'elle est bien un evenement du set.
#  « (Limit once per round.) » -> `.LimitOncePerRound()`. ⚠ Cette limite
#    n'etait rendue INERTE que jusqu'au correctif moteur du 03/09/2026
#    (once_per.py / GetForDelayAbility) ; ici elle porte sur une Action
#    ordinaire, donc elle mordait deja.
#
# ⚠ ECART ASSUME : le texte dit « play », le moteur ne sait que RENDRE
# JOUABLE. La permission est donc posee en temporaire jusqu'a la fin de la
# phase, sur la seule carte designee. Le joueur paie le cout de l'evenement
# comme le texte l'exige ; il peut en revanche renoncer, ce que le texte
# imprime ne prevoit pas.


def GetAbilities() -> Sequence['Ability']:

    def rituel_druidique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # Le DESSUS de la defausse est la DERNIERE carte posee.
        for face in reversed(list(joueur.discard_pile.Get(True))):
            if not EvenementRejouable(face):
                continue
            for permission in AbilityFactory.YouMayPlayCardLikeInHand(
                AbilityType.Rule,
                CardFinder(name=face.name, card_type=Event),
                from_where="YourDiscardPile",
            ):
                # ⚠ `unregister_after_exec` est OBLIGATOIRE (mot-cle sans
                # defaut, face_effect.py:98). Sans lui : « RegisterTemp()
                # missing 1 required keyword-only argument », exception AVALEE
                # par le moteur — la capacite ne faisait donc RIEN, et le cas
                # de test passait quand meme parce qu'il ne mesurait que le
                # COUT, paye avant le crash. Sorti par l'autoplay, 338 fois.
                this.effect.RegisterTemp(
                    permission,
                    unregister_after_exec=False,
                    until_phase_end=True,
                )
            return

    return [
        # LES SEPT BONUS « TANT QUE CETTE CARTE EST DANS VOTRE MAIN ».
        # Ils sont portes ICI et non par les cartes elles-memes : voir le long
        # commentaire de `__init__.py`, qui donne les trois montages essayes et
        # la raison de fond (aucune carte du depot ne fait porter un
        # modificateur CONTINU par une carte en main).
        BonusSelonLaMain("Fellow Druid", hand_size=1),
        BonusSelonLaMain("Astral Travel", thwart=1),
        BonusSelonLaMain("Awaken Nature", retaliate=1),
        BonusSelonLaMain("Elemental Control", attack=1),
        BonusSelonLaMain("Practice of Druidry",
                         attack=1, thwart=1, defense=1, recover=1),
        BonusSelonLaMain("Mystical Protection", stalwart=1),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            rituel_druidique,
        ).SetName("Druidic Ritual")
        .SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .LimitOncePerRound(),
    ]
