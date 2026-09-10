from . import *

# Fighting a Friend — TRAITRISE de nemesis (5/5). Boost 2.
# When Revealed (Alter-Ego): Place 3 threat on Superhuman Registration Act.
# When Revealed (Hero): Deal damage to a friendly character equal to your ATK.
#
# ⚠ LA FACE HEROS EST LA PLUS DURE DU SET pour Spider-Woman, dont l'ATQ monte
# avec ses toiles : plus elle frappe fort, plus elle blesse les siens.
#
# CARTES DE REFERENCE
#  - `50142` Psychological Manipulation : DEUX `WhenThisRevealed`, l'une
#    « Alter-Ego », l'autre « Hero », et cote heros exactement
#    `Worlds.GetOnFieldFriendlyCharacters` + `this.DealDamage([unite], ATQ)`.
#    Elle, elle DESIGNE la cible (« the fewest remaining hit points ») ;
#    ici le texte ne designe rien, donc on demande.
#  - `60064` Pawn of the Kingpin : le patron du choix quand la carte laisse
#    choisir — `ChooseAbilities` + `ForChoiceAbility(...).SetTarget(...)`, avec
#    le raccourci « une seule cible possible, pas de question ».
#    ⚠ `.SetTarget()` est licite ici : l'interdiction (`ability.py:168`) ne
#    frappe que les faces ENNEMIES, et une traitrise n'en est pas une.
#
# TEXTE CONTRE CODE
#  ⚠ « your ATK » : l'ATQ du HEROS qui revele, pas celle d'un ennemi. Cote
#    alter ego la question ne se pose pas, l'autre moitie du texte s'applique.
#  ⚠ « a FRIENDLY CHARACTER » : identite ou allie, de N'IMPORTE QUEL joueur,
#    et pas seulement de celui qui revele. C'est ce que rend
#    `GetOnFieldFriendlyCharacters` (worlds.py:289).
#  ⚠ ATQ de zero : on ne demande rien et on n'inflige rien.
#  ⚠ Cote alter ego, Acte d'Enregistrement absent : rien. Pas de repli sur le
#    complot principal.


def GetAbilities() -> Sequence['Ability']:

    def cote_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        PoserSurLActe(effect.this, 3, effect)

    def cote_heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is None:
            return
        valeur = heros.attack
        if valeur <= 0:
            return

        amis = Worlds.GetOnFieldFriendlyCharacters(effect)
        if not amis:
            return
        if len(amis) == 1:
            this.DealDamage(list(amis), valeur, effect)
            return

        def infliger(choisis: Sequence['CardFace']) -> None:
            this.DealDamage(list(choisis), valeur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                'Deal the damage to a friendly character', infliger
            ).SetTarget(amis, range=(1, 1), not_move=True))

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", cote_alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", cote_heros),
    ]
