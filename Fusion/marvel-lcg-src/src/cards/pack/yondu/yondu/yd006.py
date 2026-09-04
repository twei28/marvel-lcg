from . import *

# Twirlin' and Whirlin' — evenement signature, x4 (n/15 = 6 a 9), le plus
# nombreux du deck. SUPERPOWER. Cout 0, ressource [energy].
# You may repeat this ability for each resource you overpaid for this card.
# Hero Action: Attach the Yaka Arrow upgrade to an enemy or to your identity.
#
# Cartes de reference :
#  - **`14006`** Speed Cyclone / `ho004` / `as017` pour `effect.GetCostX()` :
#    c'est ce qui compte le surpaiement. ⚠ Dans les cas de test, `surpayer:
#    True` est OBLIGATOIRE, sinon X vaut 0.
#  - `AttacherLaFleche` (helper du set), `08013` pour le ciblage dans
#    l'operation.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « You may **repeat** this ability for each resource you **overpaid** » :
#    la carte coute 0, donc TOUT ce qui est paye est du surpaiement. Une
#    ressource depensee = un deplacement de plus. C'est la carte qui fait
#    tourner le moteur du pack : quatre exemplaires, et chacun peut deplacer
#    la fleche plusieurs fois.
#  - « repeat » et non « pour chaque, faites » : les deplacements sont
#    SUCCESSIFS, chacun avec son propre choix de destination. C'est ce qui
#    permet l'aller-retour ennemi -> identite -> ennemi, et donc trois
#    declenchements du pouvoir du heros sur une seule carte.
#  - Le PREMIER deplacement est gratuit (l'abilite elle-meme), les suivants
#    sont les repetitions : X ressources surpayees = X + 1 deplacements.
#  - « to an enemy **or** to your identity » : DEUX destinations seulement.
#    Contrairement a `yd011` Tahlei et `yd012` Yaka Arrow, la main n'est PAS
#    une option ici.
#  - Sans fleche EN JEU, la carte ne fait rien : elle deplace, elle ne
#    convoque pas.
#  - Aucun libelle : ce n'est ni une attaque ni une menee, malgre les degats
#    que le pouvoir du heros va infliger derriere.


def GetAbilities() -> Sequence['Ability']:

    def twirlin_and_whirlin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # 1 deplacement de base, plus 1 par ressource surpayee.
        for _ in range(1 + max(0, effect.GetCostX())):
            if LaFleche(effect) is None:
                return
            identite = joueur.GetIdentity()
            ennemis = EnnemisEnJeu(effect)
            if not ennemis and identite is None:
                return
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Attach Yaka Arrow to an enemy",
                    lambda cibles: AttacherLaFleche(effect, cibles[0] if cibles else None),
                    condition=bool(ennemis),
                ).SetTarget(Enemy),
                AbilityFactory.ForChoiceAbility(
                    "Attach Yaka Arrow to your identity",
                    lambda cibles: AttacherLaFleche(effect, identite),
                    condition=identite is not None,
                ),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            twirlin_and_whirlin,
        ).SetPlay(),
    ]
