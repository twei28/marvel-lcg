from . import *

# * Skurge — SBIRE nemesis (N 3/5). ASGARD.
# MNG 1 / ATQ 3* / PV 5. 1 icone de boost + une icone [star].
# Teamwork (ASGARD). Toughness.
# [star] Forced Interrupt: When Skurge attacks you, he attacks the character
#   you control with the fewest remaining hit points. This attack gains
#   overkill and piercing.
# [star] Boost: Defeat an ally you control.
#
# Carte de reference : **`24026` * Crossfire**, jumeau du montage — meme
# `WhenUnitWouldAttack(ForcedInterrupt, "This", op)`, meme
# `Filter.One(..., fewest_remaining_hp=True)`, meme `message.ReplaceTarget`.
# Seuls les mots-cles gagnes different : overkill + ranged la-bas, overkill +
# **piercing** ici.
#
# ⚠ DEUX BASES AUTOMATIQUES, AUCUN SCRIPT :
#  - `Teamwork (ASGARD)` -> `desc.Teamwork = "ASGARD"`. Le moteur active
#    Skurge des qu'un AUTRE sbire ASGARD est en jeu (`can_teamwork.py`).
#    Dans ce set, l'autre sbire ASGARD est Enchantress (ls014) : les deux
#    ensemble, c'est une activation gratuite. Fiche ecrite pour ce pack :
#    docs/reference/mots-cles/teamwork.md.
#  - `Toughness` -> `desc.Toughness`. Fiche mots-cles/toughness.md.
# Les recoder ferait DOUBLER leur effet.
#
# ⚠ ECART AVEC CROSSFIRE, ET IL EST IMPRIME. Crossfire dit « the character you
# control » sans plus, et son module prend
# `Worlds.GetOnFieldFriendlyCharacters(effect)`, qui balaie TOUS les joueurs
# de la table. Skurge dit « the character YOU control » a un joueur precis —
# celui qu'il attaque. On borne donc a l'identite et aux allies de CE
# joueur-la. En solo les deux ecritures donnent le meme resultat ; a deux
# joueurs, non.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « fewest REMAINING hit points » : les PV restants, pas les PV imprimes.
#    `fewest_remaining_hp=True` le dit au moteur.
#  - « This attack gains overkill AND piercing » : les deux, contrairement au
#    « either ... or » de ls003 Impale.
#  - L'ATQ imprimee porte une etoile : elle renvoie a la capacite [star]
#    ci-dessus, ce n'est pas du degat consequent.
#  - « [star] Boost: Defeat an ALLY you control » : si le joueur n'a aucun
#    allie, rien ne se passe — et c'est correct, le texte ne prevoit pas de
#    repli. C'est la punition directe de l'aspect Leadership du deck de
#    depart.


def GetAbilities() -> Sequence['Ability']:

    def personnages_du_joueur(joueur: 'Player') -> List['CardFace']:
        faces: List['CardFace'] = []
        identite = joueur.GetIdentity()
        if identite is not None:
            faces.append(identite)
        faces += list(joueur.allies.Get())
        return faces

    def skurge(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)

        joueur = this.GetEngagedPlayer()
        if joueur is not None:
            cible = Filter.One(personnages_du_joueur(joueur), effect,
                               fewest_remaining_hp=True)
            if cible:
                message.ReplaceTarget(cible)

        message.GainOverKill(effect)
        message.GainPiercing(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        allies = list(joueur.allies.Get())
        if not allies:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Defeat an ally you control",
                lambda cibles: Faces.DefeatUnits(list(cibles), this, effect),
            ).SetTarget(Ally, from_where=["YouControlCards"]),
        )

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            skurge,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
