from . import *

# Explosive Touch — AMELIORATION signature, custom « CptScorp »
# Cout 1, [energy], classe Hero, trait SUPERPOWER.
# Hero Response: After you basic attack or basic thwart an enemy or scheme
#   that has an explosive counter on it, exhaust Explosive Touch -> ready
#   Speed.
#
# ⚠ NE PAS FUSIONNER AVEC sd016 Quick Adaptation. Les deux cartes parlent des
# memes pouvoirs de base contre les memes cibles marquees, mais :
#   - sd014 est une RESPONSE (« After ») : elle agit APRES le pouvoir, s'incline
#     elle-meme et REDRESSE Speed ;
#   - sd016 est un INTERRUPT (« When ») : elle agit AVANT, ne s'incline pas, et
#     donne +1 ATQ ET +1 CTR « for that use ».
# Deux fabriques distinctes, jamais un `if`.
#
# ---------------------------------------------------------------------------
# DECLENCHEUR -> `AbilityFactory.AfterUnitUseBasicPower(AbilityType.HeroResponse,
# "You", ..., powers=["ATK", "THW"])` (factory/friend.py:373). C'est la
# fabrique du depot pour « after you basic attack / basic thwart », et elle
# couvre les deux verbes d'un coup.
#
# ⚠ `powers` prend les codes du moteur `'ATK'` / `'THW'` / `'DEF'` / `'REC'` /
# `'SCH'` — JAMAIS `'Attack'` ni `'Thwart'`. Ce piege a deja produit deux
# conditions mortes sur ce projet.
#
# `AbilityType.HeroResponse` et non `Response` nu : le texte imprime dit « Hero
# Response », et 124 des 134 cartes « Hero Response » du depot emploient bien
# le sous-type dedie (CORRECTIF 27009 Web-Bracelet).
#
# ---------------------------------------------------------------------------
# LA CONDITION « an enemy or scheme THAT HAS an explosive counter on it » est
# portee par `UneCibleDeCeMessagePorteUnCompteur` (speed/speed/__init__.py),
# qui remonte de `AfterUnitUseBasicPower` a `pre_message.would_message` puis
# lit `attacked_targets` (attaque) ou `schemes` (contre).
#
# ⚠ Le compteur est lu APRES le pouvoir de base : il est donc encore la (rien
# ne le retire avant la fin de la phase des joueurs), et un compteur POSE par
# cette attaque-la compterait aussi. C'est la lecture du texte imprime
# (« an enemy ... THAT HAS an explosive counter »), au present.
#
# ---------------------------------------------------------------------------
# COUT -> `.SetCostFunc(CostFunc.Exhaust("This"))` : « exhaust Explosive
# Touch ». Modele 27009 Web-Bracelet, meme forme.
#
# EFFET -> `Faces.ReadyAll([message.trigger], effect)`. `message.trigger` est
# l'unite qui vient d'employer le pouvoir de base, c'est-a-dire l'identite du
# joueur : « ready Speed », mot pour mot. On ne cherche PAS « Speed » par nom
# (`CardFinder(name="Speed")`) : le catalogue contient deja un allie officiel
# `15010` « * Speed » et un sbire `57060` « * Speed », une recherche par nom
# non bornee les toucherait.
#
# La boucle est finie : le redressement de Speed ne redeclenche pas la
# Response (aucun pouvoir de base n'est employe par le redressement), et la
# carte est desormais inclinee.


def GetAbilities() -> Sequence['Ability']:

    def cible_marquee(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> bool:
        Unused(effect)
        return UneCibleDeCeMessagePorteUnCompteur(message)

    def explosive_touch(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.ReadyAll([message.trigger], effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            explosive_touch,
            powers=["ATK", "THW"],
            conditions=[cible_marquee],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
