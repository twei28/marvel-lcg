from . import *

# * Spider-Woman (Veranke) II — MECHANT, face A (CAMOUFLAGED). SKRULL. PV 18[per_hero], MNG 3, ATQ 2 (etoile).
# Spider-Woman cannot take damage.
# ★ Forced Response: After Spider-Woman attacks you, place 1 suspicion counter on "Who Do You Trust?".
# You are a Skrull! — Hero Action: Exhaust a hero and spend 1[per_hero] resources of any type → flip Spider-Woman.
#   (The players can pay this ability's costs as a group.)
#
# Cartes de reference (une par capacite) :
#  - « cannot take damage » : **`mojo 39012a`** * Spiral (`ThisCannotTakeDamageWhile(conditions=True)`) et
#    `60131` The Getaway (`*UnitCannotTakeDamage(Villain)`, liste a deballer) : la fabrique `UnitCannotTakeDamage`
#    pose aussi le marqueur d'affichage ; meme texte, meme famille.
#  - ★ Reponse forcee « After the villain attacks you » : **`sk150`** Ice Control (`AfterUnitAttackYou(ForcedResponse,
#    "AttachedEnemy", ...)`), ici l'attaquant est « This ».
#  - Action de heros a cout composite : **`rainy 90131`** (`CostFunc.Exhaust("YourHero")` + `SetCost`) et
#    **`sk086`** Skrull Empire (Hero Action portee par une carte de RENCONTRE). Le paiement en groupe n'est pas
#    le mot-cle Alliance (reserve aux evenements, `25036`) : la capacite est marquee `cout_en_groupe`, lu par
#    `CheckAnyPlayerMayHelpPay` (resources.py, modification de moteur documentee dans defs/secret_invasion_moteur.md).
#  - « flip » : **`mojo 39012b`** Spiral et **`60110a`** Typhoid Mary (`this.card.Flip(effect)` sur un mechant
#    recto-verso : attachements, statuts, boosts et degats restent).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After Spider-Woman attacks YOU » : le joueur attaque, pas un allie ; le jeton va sur l'environnement
#    sk194 (par son card_id : son nom porte des guillemets). Sans environnement en jeu, rien.
#  - « Exhaust A hero » (n'importe quel heros, avec le paiement en groupe) et « 1[per_hero] resources of ANY
#    type » : Cost("1") x nombre de joueurs. Sans le groupe (Mistrust and Paranoia), seulement le heros de
#    celui qui agit.
#  - « flip Spider-Woman » retourne la CARTE (elle passe sur Queen Veranke), jamais « inflige » quoi que ce soit.
#  - L'etoile du badge ATQ renvoie au texte (convention validee 15/10/2026), aucune valeur a ajouter.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesSpiderWoman()
