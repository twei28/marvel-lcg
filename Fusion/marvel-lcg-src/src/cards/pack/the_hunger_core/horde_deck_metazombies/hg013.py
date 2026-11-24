from . import *

# Zombie Black Widow — METAZOMBIE (Horde deck). AVENGER. SPY. SCH 1. ATK 1. PV 9[per_hero]. Stalwart 1.
# Ambush. Allies cannot defend against Zombie Black Widow's attacks.
#
# Cartes de reference :
#  - « Allies cannot defend against X's attacks » : `AbilityFactory.UnitCannotDefend(Ally, "This",
#    cannot_trigger_defense_ability=True)`, modele `ap305` Clan Yautja / The Hunt Begins (« Allies cannot
#    defend against enemy attacks » -> `UnitCannotDefend(Ally, Enemy, cannot_trigger_defense_ability=True)`,
#    meme restriction au cote defenseur, Ally seulement) croise avec `ip034` Molecule Man / `gs190` Veranke
#    (« [Character|Players] cannot defend against [This]'s attacks » -> `UnitCannotDefend(Unit2, "This",
#    cannot_trigger_defense_ability=True)`, meme restriction a l'ATTAQUANT, "This" seulement). Les deux
#    cartes different sur un seul axe chacune (ap305 : generique cote attaquant, specifique "This" cote
#    defenseur -- Ally ; ip034/gs190 : specifique "This" cote attaquant, generique cote defenseur -- Unit2) ;
#    hg013 cumule les DEUX restrictions imprimees (« ALLIES », pas Unit2 ; « ZOMBIE BLACK WIDOW's attacks »,
#    pas un ennemi quelconque), d'ou `UnitCannotDefend(Ally, "This", cannot_trigger_defense_ability=True)`.
#
# ⚠ Mots-pieges :
#  - « Ambush » est un NOM D'AMBIANCE propre a cette carte, pas un mot-cle officiel ni une mecanique a coder
#    (arbitrage utilisateur, 27/10/2026) : meme statut que « Storm » (hg012), « Devour » (hg009), « Web »
#    (hg010), « Absorption » (hg011) -- aucune fiche `mots-cles/ambush.md` a creer, rien a ouvrir avant de
#    coder, seule la phrase qui suit (« Allies cannot defend... ») porte une regle.
#  - « ALLIES cannot defend » : Ally SEULEMENT (pas Unit2, pas Character) -- le heros/l'identite attaquee
#    PEUT toujours defendre normalement (il n'y a d'ailleurs personne d'autre a defendre pour lui). Si ce
#    texte avait dit « Character » ou « Players », le modele aurait ete Unit2 (ip034/gs190) ; ici il nomme
#    explicitement Ally, modele ap305.
#  - « against ZOMBIE BLACK WIDOW's attacks » : seule CETTE carte est concernee (`who_attacker="This"`), pas
#    n'importe quel ennemi/Metazombie de la table (a la difference d'ap305, qui vise TOUT ennemi YAUTJA) --
#    si un autre Metazombie ou le Coeur attaque, les allies peuvent defendre normalement.
#  - `cannot_trigger_defense_ability=True` (modele ap305/ip034/gs190, pas `UnitCannotMakeBasicDefense` qui
#    passe `False`) : aucune des trois cartes de reference ne distingue « defense de base » et « capacite de
#    defense », le texte imprime « cannot defend » est generique sans restriction -> bloque toute defense,
#    base ou declenchee par une capacite.
#  - Stalwart (desc.Stalwart = "1") est une BASE NATIVE, aucun script requis (fiche `mots-cles/stalwart.md`).


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.UnitCannotDefend(Ally, "This", cannot_trigger_defense_ability=True),
    ]
