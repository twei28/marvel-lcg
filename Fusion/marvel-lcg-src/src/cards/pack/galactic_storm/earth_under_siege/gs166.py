from . import *

# Annihilus (I) — MECHANT, stade 1. NEGATIVE ZONE. SCH 1, ATK 2, PV 6.
# [star] Forced Response: After Annihilus activates against you, discard cards from the top of your deck
#   until you discard an identity-specific card.
#
# Cartes de reference :
#  - « After Annihilus activates against you » : `AbilityFactory.AfterEnemyActivatesAgainstYou` (modele
#    sm/venom_goblin/27114.py, `message.GetAgainstPlayer()`).
#  - « discard cards from the top of your deck until you discard an identity-specific card » :
#    `DefausserJusquaCarteIdentitaire` (earth_under_siege/__init__.py), partagee avec gs167 (meme texte) et
#    gs169 Annihilation Wave (meme mecanique, + degats indirects).
#
# ⚠ Mots-pieges : « activates AGAINST YOU » = le joueur vise par l'activation (pas forcement celui qui a
# revele la carte qui l'a declenchee) ; le texte ne dit PAS « if you cannot », la defausse s'arrete
# simplement quand le deck est vide (aucun effet si aucune carte identitaire n'est trouvee).
#
# ⚠ NON PROUVE PAR CAS (20/10/2026) : construit sans erreur (test_cards), modele IDENTIQUE a des cartes
# deja shippees et presumees testees (nt013 Terrax the Tamer, sm/venom_goblin/27114-27115), mais dans ce
# harnais `Puzzle.Attack('gs166')` ne declenche jamais `AfterEnemyActivatesAgainstYou` malgre de nombreuses
# variantes testees (inline vs helper partage, avec/sans SetVillainRule, avec/sans Rhino en jeu, forme
# heros/alter-ego, avec .SetName()). Hypothese non tranchee : limite du harnais de test specifique a ce
# message, OU defaut latent du moteur jamais exerce par un cas existant (nt013 n'a pas de preuve negative
# independante). A signaler a l'utilisateur et verifier en partie reelle / autoplay avant de clore le lot.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesAnnihilus()
