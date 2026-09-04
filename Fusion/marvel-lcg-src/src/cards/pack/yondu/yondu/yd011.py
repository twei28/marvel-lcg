from . import *

# Tahlei — amelioration signature, x1 (n/15 = 14). TECH.
# Cout 0, DEUX ressources [mental].
# Hero Action: Exhaust Tahlei -> if the Yaka Arrow upgrade is in play, attach
#   it to an enemy, to your identity, or add it to your hand.
#
# ⚠ NOM : la carte s'appelle « Tahlei » — c'est le nom de l'aileron de Yondu.
# Le fichier du zip s'appelle bien `14. Tahlei.png`, pas de piege ici,
# contrairement au pack night_thrasher.
#
# Cartes de reference :
#  - `AttacherLaFleche` (helper du set) : SEUL point d'entree pour deplacer la
#    fleche, parce que c'est `AttachTo2` qui emet les messages dont vit le
#    pouvoir du heros.
#  - **`08013`** Stealth Strike pour le choix a trois branches DANS
#    l'operation : les trois destinations n'ont pas le meme type de cible.
#  - `17022` * Knowhere / `as010` pour `CostFunc.Exhaust("This")`.
#  - `yd012` Yaka Arrow, dont la `Forced Interrupt` offre EXACTEMENT les memes
#    trois destinations : les deux textes sont jumeaux, et les deux modules
#    doivent le rester.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **if the Yaka Arrow upgrade is in play** » : condition, pas un cout.
#    Fleche absente du terrain (en main, en defausse, hors jeu), l'Action
#    resout sans rien faire — et Tahlei est quand meme inclinee, puisque le
#    cout est paye avant.
#  - Trois destinations, jamais deux : un ennemi, l'identite, ou LA MAIN.
#  - « **Hero** Action » : rien en forme civile, alors que c'est l'alter-ego
#    qui la convoque (yd001b Crew Cut). Le pack force donc l'aller-retour.
#  - DEUX ressources [mental] imprimees : `RES: "BB"`. L'icone a ete croisee
#    avec `yd010` Ravage, du meme pack, qui porte une seule [mental] (leçon
#    Lockjaw : une icone ne se nomme jamais a vue).
#  - Cout 0 : elle entre en jeu gratuitement, et c'est ce qui rend le moteur
#    du pack fiable — la fleche a toujours un pilote.


def GetAbilities() -> Sequence['Ability']:

    def tahlei(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        fleche = LaFleche(effect)
        if fleche is None:
            return

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        ennemis = EnnemisEnJeu(effect)

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
            AbilityFactory.ForChoiceAbility(
                "Add Yaka Arrow to your hand",
                lambda cibles: RappelerLaFlecheEnMain(effect),
            ),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tahlei,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
