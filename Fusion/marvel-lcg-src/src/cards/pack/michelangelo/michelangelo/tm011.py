from . import *

# * Michelangelo's Nunchuck — amelioration signature, x1 (14/15).
# NINJA. NUNCHUCK. WEAPON. Cout 1, ressource [energy]. Restricted.
# Each NUNCHUCK upgrade you control gains: "Hero Response: After you play an
#   event, exhaust this card -> your hero gets +1 to a basic power until the
#   end of the round."
#
# Regle de l'insert : « You may use either NUNCHUCK (or both) to get +1 to a
# basic power until the end of the round after playing an event. »
#
# Cartes de reference :
#  - « each X upgrade you control GAINS an ability » :
#    `AbilityFactory.GiveAbilityToInPlayWhenApplyThis(finder, control_by="You",
#    abilities=[...])` (environment.py:27, modele `aos/black_widow/50070`) ;
#    l'abilite donnee est enregistree PAR PORTEUR (`RegisterGiven`,
#    face_effect.py:69) ;
#  - declencheur : `jubilee/47004` —
#    `AfterPlayerPlayedCard(HeroResponse, "You", CardFinder(card_type=Event), op)` ;
#  - +1 jusqu'a la fin du round : `lady_sif/ls004` —
#    `face.GainUntilRoundEnd(effect, attack=1)` ;
#  - choix du pouvoir : `ChooseAbilities` + `ForChoiceAbility` (ls003).
#
# ⚠ Mots-pieges :
#  - « EACH NUNCHUCK upgrade you control gains » : la capacite est donnee a
#    CHAQUE Nunchuck controle, y compris CETTE carte et tm012. Sans tm011 en
#    jeu, tm012 n'a pas cette Reponse. Le « gains » est lu dans ce sens.
#  - « (or both) » : deux Nunchuck = deux exemplaires de la Reponse, chacun
#    s'epuise a part ; le bonus s'empile.
#  - « your HERO » : la face heros, pas l'identite alter-ego (Hero Response
#    exige la forme de heros).
#  - « a basic power » : ATK, THW ou DEF (REC exclu), au choix du joueur.
#  - « After you play an event » : tout evenement, `Event` seul, pas un
#    evenement de Michelangelo.
#  - Restricted : base automatique (desc), RIEN a coder.
#  - ⚠ RISQUE A TESTER (phase C) : la MEME instance d'Ability est enregistree
#    chez deux porteurs ; `Ability.Initialize` est gardee par
#    `is_initialized`. # TODO-QUESTION (question 6).

def GetAbilities() -> Sequence['Ability']:

    def bonus_de_pouvoir(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        heros = joueur.GetHero()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Your hero gets +1 ATK until the end of the round",
                lambda cibles: heros.GainUntilRoundEnd(effect, attack=1),
            ),
            AbilityFactory.ForChoiceAbility(
                "Your hero gets +1 THW until the end of the round",
                lambda cibles: heros.GainUntilRoundEnd(effect, thwart=1),
            ),
            AbilityFactory.ForChoiceAbility(
                "Your hero gets +1 DEF until the end of the round",
                lambda cibles: heros.GainUntilRoundEnd(effect, defense=1),
            ),
        )

    reponse_donnee = AbilityFactory.AfterPlayerPlayedCard(
        AbilityType.HeroResponse,
        "You",
        CardFinder(card_type=Event),
        bonus_de_pouvoir,
    ).SetCostFunc(CostFunc.Exhaust("This"))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.GiveAbilityToInPlayWhenApplyThis(
            CardFinder(trait="NUNCHUCK", card_type=Upgrade),
            control_by="You",
            abilities=[reponse_donnee],
        ),
    ]
