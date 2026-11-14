from . import *

# Annihilation Wave — TRAITRISE (ensemble Annihilus), x3 exemplaires.
# When Revealed: Discard cards from the top of your deck until you discard an identity-specific card.
#   Take 1 indirect damage (to a maximum of 3) for each card discarded this way.
#
# Cartes de reference :
#  - Defausse jusqu'a carte identitaire : `DefausserJusquaCarteIdentitaire` (earth_under_siege/__init__.py),
#    partagee avec gs166/gs167 Annihilus (meme texte).
#  - « Take 1 indirect damage ... for each card discarded this way » : `identite.TakeIndirectDamage`
#    (modele sm/venom/27080.py).
#
# ⚠ Mots-pieges : « for EACH CARD discarded this way » = toutes les cartes parties pendant la boucle
# (celles avant ET la carte identitaire elle-meme qui arrete la boucle), pas seulement celle-ci ; « to a
# MAXIMUM of 3 » plafonne le TOTAL de degats, pas le nombre de cartes defaussees (la defausse continue
# normalement meme si elle depasse 3 cartes, seul le degat est plafonne).
#
# ⚠ NON PROUVE PAR CAS (20/10/2026) : construit sans erreur (test_cards), suit le modele exact de gs165
# (meme pack, meme AbilityFactory.WhenThisRevealed(None, ..) via Puzzle.Reveal, gs165 PROUVE par cas), mais
# Puzzle.Reveal('gs169') dans le harnais ne declenche jamais son operation (confirme par des print() de
# diagnostic jamais affiches ; cause non identifiee apres investigation approfondie). A verifier en partie
# reelle / autoplay avant de clore le lot.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        trouvee, autres = DefausserJusquaCarteIdentitaire(effect, joueur)
        total = len(autres) + (1 if trouvee is not None else 0)
        if total > 0:
            joueur.GetIdentity().TakeIndirectDamage(effect.this, min(total, 3), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
