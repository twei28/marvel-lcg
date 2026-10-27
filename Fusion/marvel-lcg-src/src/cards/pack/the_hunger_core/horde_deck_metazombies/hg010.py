from . import *

# Zombie Spider-Man — METAZOMBIE (Horde deck). WEB-SLINGER. SCH 2. ATK 2. PV 9[per_hero].
# Web — Forced Response: After Zombie Spider-Man deals damage to a hero, that hero is stunned.
#
# Cartes de reference :
#  - « After ... deals damage to a hero, that hero is stunned » : `AbilityFactory.AfterUnitAttackAndDamageUnit(
#    ForcedResponse, "This", Hero, op, target_in_play=True)`, modele `60166` Kingpin's Cane (« After Kingpin
#    attacks and damages a hero, stun that hero »), qui cible deja `Hero` (pas `Character` ni `Identity` nu)
#    -- meme restriction imprimee « a hero » que sur CETTE carte. `60166` passe un `CardFinder` en attaquant
#    parce que c'est une AMELIORATION attachee a Kingpin (pas Kingpin lui-meme) ; ici l'attaquant EST la carte
#    qui porte la capacite, donc `"This"`, modele `hg009` Zombie Hulk (`WhenUnitWouldAttackUnit(..., "This",
#    ...)`). Variante sans la restriction au heros, meme fabrique : `21086` Supergiant (`Character`), `02038`
#    Scorpion (`None`, tout personnage).
#
# ⚠ Mots-pieges :
#  - « Web » est un NOM D'AMBIANCE propre a cette carte, pas un mot-cle officiel (absent de
#    `docs/reference/mots-cles/README.md`, aucune autre carte du moteur ne le reprend comme mot-cle) : rien a
#    ouvrir avant de coder, le texte qui suit EST la regle complete.
#  - « Stunned » (Etourdi) est un statut DE BASE du moteur (comme Confused), pas un mot-cle maison ni officiel
#    a ficher : lu/pose nativement par `Faces.GiveStatus(cibles, "Stunned", effect)` / `face.IsStunned()`
#    (`can_status.py`), au meme titre que Toughness/Restricted -- heuristique du README (`mots-cles/README.md`
#    §"Officiels") : seuls les termes imprimes EN GRAS sur la carte sont catalogues, « stunned » ne l'est pas
#    ici (seul « Web » l'est).
#  - « deals damage to a hero » SANS le mot « attacks » explicite dans le texte transcrit (a la difference de
#    `60166` « attacks and damages a hero ») : arbitrage technique, pas une question de regle -- Zombie
#    Spider-Man n'a NI manigance, NI capacite de degats indirects (`desc` ne porte que SCH/ATK/HP, `text` ne
#    contient que cette seule ligne) : la SEULE source possible de degats qu'il inflige a un heros est son
#    attaque. `AfterUnitAttackAndDamageUnit` (declencheur = l'attaque de CETTE carte qui blesse la cible) est
#    donc rigoureusement equivalent a « chaque fois qu'il inflige des degats a un heros » pour cette carte
#    precise, et colle au modele officiel `60166` qui porte le MEME mot « hero » (pas « character »). Pas de
#    question posee a l'utilisateur : les deux lectures produisent exactement le meme comportement en jeu.
#  - « that hero is stunned » : la cible qui subit le statut est celle qui a ete ATTAQUEE/BLESSEE
#    (`message.attacked`), jamais Zombie Spider-Man lui-meme.
#  - `target_in_play=True` (modele `60166`) : si le heros est deja hors jeu au moment du Forced Response (cas
#    limite, ex. vaincu entre-temps par un autre effet simultane), on ne pose pas le statut sur une carte
#    sortie.


def GetAbilities() -> Sequence['Ability']:

    def web(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Unused(effect)
        cible = message.attacked
        Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            Hero,
            web,
            target_in_play=True,
        ),
    ]
