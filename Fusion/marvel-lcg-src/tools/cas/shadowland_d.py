# Cas test_capacites de l'agent D du chantier SHADOWLAND : sets NINJA SWARM (sl028-sl036) et BLACK FLOWER (sl072-sl078). Prefixe de nom `[sld]`.
# Cas montes sur `rhino` (Spider-Man) comme tools/cas/shadowland.py, ou sur le scenario REEL `shadows_in_the_night` (graine 42 = vilain Elektra sl014a).
HEROS = "spider_man"
RIEN = ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]
FORME_HEROS = "Puzzle.ChangeForm('01001b')"
CC = "Puzzle.PutIntoPlay('sl072a,sl072b', under_control=True)"          # la Creeping Corruption du joueur 1, face A (paire visible,verso)
CC_B = "Puzzle.PutIntoPlay('sl072b,sl072a', under_control=True)"        # face B visible


def _r(nom, pourquoi, mise, declencher, attendu, forme_heros=True, **cle):
    """Cas du scenario REEL d'essai (voir plus bas) : le deck de rencontre est vide puis rempli de trois « I'm Tough » (zero icone de boost)."""
    cas = {"nom": "[sld] " + nom, "pourquoi": pourquoi, "scenario": "sl_essai_ninja_black_flower", "heros": HEROS,
           "mise_en_place": [*([] if cle.pop("deck_reel", False) else ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"]), *([FORME_HEROS] if forme_heros else []), *mise],
           "declencher": declencher, "verifier": "sld_etat", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"]), "regles": ["v16_all", "v18_all"]}
    cas.update(cle)
    return cas


def _s(nom, pourquoi, mise, declencher, attendu, verifier="sld_etat", forme_heros=True, deck=None, **cle):
    avant = cle.pop("avant_forme", [])   # ⚠ PIEGE : `ChangeForm` remet la menace du complot a 0 -> poser la menace AVANT
    # `deck` = cartes du deck de rencontre, LA DERNIERE AU DESSUS (comme 60201 de tools/test_capacites.py) ; par defaut trois « I'm Tough » inoffensifs
    rien = RIEN if deck is None else ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(" + ", ".join(repr(c) for c in deck) + ")"]
    cas = {"nom": "[sld] " + nom, "pourquoi": pourquoi, "scenario": "rhino", "heros": HEROS,
           "mise_en_place": [*rien, *avant, *([FORME_HEROS] if forme_heros else []), *mise],
           "declencher": declencher, "verifier": verifier, "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    # ------------------------------------------------------------------------------------------------------ sl072a : Creeping Corruption, face A
    _s("sl072a Action : epuise la carte, pose 1 compteur corruption ICI et pioche 1 carte", "« Exhaust Creeping Corruption and place 1 corruption counter here -> draw 1 card »",
       [CC], ["Puzzle.Action('sl072a', 'Action')"], {"compteurs": [["sl072a", "corruption", 1]], "exhausted": ["sl072a"], "taille_main": 2}),
    _s("sl072a Action, TEMOIN : sans l'Action, ni compteur ni pioche", "la mesure suit l'Action",
       [CC], [], {"compteurs": [["sl072a", "corruption", 0]], "taille_main": 1}),
    _s("sl072a, 5e compteur POSE PAR L'ACTION (4 -> 5) : les compteurs partent, la carte se retourne (face B), la pioche a quand meme lieu", "« If there are at least 5 corruption counters here, remove each of them from here and flip this card »",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)"], ["Puzzle.Action('sl072a', 'Action')"],
       {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]], "taille_main": 2}),
    _s("sl072a, pose de 2 d'un coup (4 -> 6) : TOUS les compteurs partent (pas seulement 5) et la carte se retourne", "« remove EACH of them from here »",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)", "Puzzle.Counter('sl072a', 'corruption', 2)"], [],
       {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]]}),
    _s("sl072a, TEMOIN : 4 compteurs seulement, la carte reste face A", "le seuil est de 5",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)"], [], {"compteurs": [["sl072a", "corruption", 4]], "face_visible": [["sl072", "sl072a"]]}),
    # ------------------------------------------------------------------------------------------------------ sl072b : Creeping Corruption, face B
    _s("sl072b Action : epuise la carte, pose 1 compteur, pioche 2 cartes puis defausse 1 carte de la main (choisie)", "« draw 2 cards, then discard 1 card from your hand »",
       [CC_B], ["Puzzle.Action('sl072b', 'Action')"], {"compteurs": [["sl072b", "corruption", 1]], "exhausted": ["sl072b"], "taille_main": 2}),
    _s("sl072b, 5e compteur : le joueur est vaincu (la partie est perdue : seul joueur elimine)", "« If there are at least 5 corruption counters here, you are defeated »",
       [CC_B, "Puzzle.Counter('sl072b', 'corruption', 5)"], [], {"partie_finie": True}),
    _s("sl072b, TEMOIN : 4 compteurs, le joueur n'est pas vaincu", "le seuil est de 5",
       [CC_B, "Puzzle.Counter('sl072b', 'corruption', 4)"], [], {"partie_finie": False, "compteurs": [["sl072b", "corruption", 4]]}),
    _s("sl072b, 5e compteur POSE PAR L'ACTION (4 -> 5) : defaite", "le cout pose le 5e compteur",
       [CC_B, "Puzzle.Counter('sl072b', 'corruption', 4)"], ["Puzzle.Action('sl072b', 'Action')"], {"partie_finie": True}),
    _s("sl072a/b : le trait OVERPOWERING est sur la face B seulement", "le trait est imprime sur la face B",
       [CC_B], [], {"traits_de": [["sl072b", "OVERPOWERING"]]}),
]

CAS += [
    # ------------------------------------------------------------------------------------------------------ sl028 : Black Mountain
    _s("sl028 Black Mountain engage : un AUTRE sbire NINJA engage avec le meme joueur (Ghost Maker) ne peut pas etre attaque", "« each other NINJA minion engaged with you cannot be attacked »",
       ["Puzzle.PutIntoPlay('sl028')", "Puzzle.PutIntoPlay('sl006')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl006", 0]], "en_jeu": ["sl006"]}, cibles=["sl006"]),
    _s("sl028, TEMOIN : sans Black Mountain, Ghost Maker prend les 2 degats de l'attaque de base", "la protection vient de Black Mountain",
       ["Puzzle.PutIntoPlay('sl006')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl006", 2]]}, cibles=["sl006"]),
    _s("sl028 : Black Mountain lui-meme reste attaquable (« each OTHER »)", "c'est ainsi qu'on leve son Guard",
       ["Puzzle.PutIntoPlay('sl028')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl028", 2]]}, cibles=["sl028"]),
    _s("sl028 : un sbire NON-NINJA engage (Whirlwind) reste attaquable", "« each other NINJA minion »",
       ["Puzzle.PutIntoPlay('sl028')", "Puzzle.PutIntoPlay('01130')"], ["Puzzle.Attack('01001a')"], {"degats": [["01130", 2]]}, cibles=["01130"]),
    _s("sl028 : un sbire NINJA engage avec un AUTRE joueur reste attaquable (« engaged with YOU »)", "Black Mountain est engage avec le joueur 1, Ghost Maker avec le joueur 2",
       ["Puzzle.PutIntoPlay('sl028')", "Puzzle.PutIntoPlay('sl006')", "Puzzle.Engage('sl006', player=1)"], ["Puzzle.Attack('01001a')"], {"degats": [["sl006", 2]]}, cibles=["sl006"], heros2="spider_man"),
    _s("sl028 Boost, un ALLIE defend (Black Widow) : Black Mountain est revelee et entre en jeu", "« If an ally is defending against this attack, reveal this minion »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Attack('01094', defender='01075')"], {"en_jeu": ["sl028"]}, deck=["sl028"]),
    _s("sl028 Boost, TEMOIN : c'est le HEROS qui defend -> Black Mountain n'est pas revelee", "le defenseur doit etre un allie",
       [], ["Puzzle.Attack('01094', defender='01001a')"], {"hors_jeu": ["sl028"]}, deck=["sl028"]),
    # ------------------------------------------------------------------------------------------------------ sl029 : Kirigi
    _s("sl029 Kirigi vaincu, choix « melanger » : il retourne dans le deck de rencontre (et n'est pas en defausse)", "« either spends 2 resources of any type or shuffles Kirigi into the encounter deck »",
       ["Puzzle.PutIntoPlay('sl029')"], ["Puzzle.Damage('sl029', 99)"], {"dans_deck_rencontre": ["sl029"], "hors_jeu": ["sl029"]}, choisir_option="Shuffle_Kirigi_into_the_encounter_deck"),
    _s("sl029 Kirigi vaincu, choix « depenser 2 ressources » : les ressources sont payees et Kirigi reste defausse", "la 1re branche",
       ["Puzzle.PutIntoPlay('sl029')"], ["Puzzle.Damage('sl029', 99)"], {"defausse": ["01088"], "defausse_rencontre": ["sl029"], "hors_jeu": ["sl029"]},
       preferer_option="Spend", payer_avec=["01088"], main_exclusive=["01088"]),
    _s("sl029 Kirigi vaincu, 2 ressources IMPAYABLES (1 seule ressource en main) : la branche n'est pas offerte, il retourne dans le deck", "le moteur reduirait sinon la branche payante au plus gros morceau payable",
       ["Puzzle.PutIntoPlay('sl029')"], ["Puzzle.Damage('sl029', 99)"], {"dans_deck_rencontre": ["sl029"], "en_main": ["01093"]}, main_exclusive=["01093"], preferer_option="Spend"),
    _s("sl029 Boost, un ALLIE defend : +2 icones de boost ET overkill -> Black Widow (2 PV) subit 4, l'excedent de 2 passe sur l'identite", "« this card gains [boost][boost] and this attack gains overkill »",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Attack('01094', defender='01075')"], {"degats_identite": 2, "defausse": ["01075"]}, deck=["sl029"]),
    _s("sl029 Boost, TEMOIN : le heros defend (DEF 3) -> aucun effet (ni icones ni overkill), l'identite ne prend rien", "le defenseur doit etre un allie",
       [], ["Puzzle.Attack('01094', defender='01001a')"], {"degats_identite": 0}, deck=["sl029"]),
    # ------------------------------------------------------------------------------------------------------ sl030-sl034 : Teamwork (NINJA), « When Defeated » commun
    # ⚠ le deck de rencontre se liste DU DESSOUS VERS LE DESSUS (la derniere carte est la 1re defaussee) ; Teamwork se joue en vraie partie (v16_teamwork) : seul le sbire qui ARRIVE s'active
    _s("sl030 Bo Staff Ninja vaincu : defausse les 2 cartes du dessus du deck de rencontre et revele le PREMIER sbire Teamwork (Katana, dessus) ; Kusarigama defaussee reste en defausse",
       "« discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way » (Toughness : un 1er coup retire le statut Tough)",
       ["Puzzle.PutIntoPlay('sl030')"], ["Puzzle.Damage('sl030', 99)", "Puzzle.Damage('sl030', 99)"], {"en_jeu": ["sl032"], "hors_jeu": ["sl033", "sl030"], "defausse_rencontre": ["sl033", "sl030"]},
       deck=["01105", "sl033", "sl032"], regles=["v16_all", "v18_all"]),
    _s("sl031 Fukiya Ninja vaincu : la 1re carte defaussee est un sbire SANS Teamwork (Weapons Runner) -> on passe a la 2e, Shuriken, qui est revelee",
       "« the first minion with the teamwork keyword » : un sbire sans le mot-cle ne compte pas",
       ["Puzzle.PutIntoPlay('sl031')"], ["Puzzle.Damage('sl031', 99)"], {"en_jeu": ["sl034"], "hors_jeu": ["01121"], "defausse_rencontre": ["01121"]},
       deck=["01105", "sl034", "01121"], regles=["v16_all", "v18_all"]),
    _s("sl032 Katana Ninja vaincu : un sbire Teamwork en TROISIEME position n'est pas touche (seules les 2 du dessus sont defaussees)", "« the top 2 cards »",
       ["Puzzle.PutIntoPlay('sl032')"], ["Puzzle.Damage('sl032', 99)"], {"dans_deck_rencontre": ["sl033"], "hors_jeu": ["sl033"], "defausse_rencontre": ["01105"]},
       deck=["sl033", "01105", "01105"], regles=["v16_all", "v18_all"]),
    _s("sl033 Kusarigama Ninja vaincu, aucun sbire Teamwork parmi les 2 cartes : les 2 sont defaussees et rien n'est revele", "pas de sbire = pas de revelation",
       ["Puzzle.PutIntoPlay('sl033')"], ["Puzzle.Damage('sl033', 99)"], {"defausse_rencontre": ["01105"], "defausse_rencontre_taille": 3, "hors_jeu": ["sl033"]},
       deck=["01105", "01105", "01105"], regles=["v16_all", "v18_all"]),
    _s("sl034 Shuriken Ninja vaincu, SEUL NINJA en jeu : il est encore en jeu pendant son « When Defeated » (RR), donc Fukiya, revele, trouve un autre NINJA et s'active (1 degat)", "decision DECISIONS-d.md n°2 : une carte vaincue ne quitte le jeu qu'APRES ses « When Defeated »",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sl034')"], ["Puzzle.Damage('sl034', 99)"], {"en_jeu": ["sl031"], "degats_identite": 1}, deck=["01105", "sl031"], regles=["v16_all", "v18_all"]),
    _s("sl034 Shuriken Ninja vaincu AVEC un autre NINJA en jeu (Ghost Maker) : Fukiya, revele, s'active (Teamwork) et attaque : ATQ 1 -> 1 degat a l'identite", "Teamwork (NINJA) : un autre sbire NINJA en jeu",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sl034')", "Puzzle.PutIntoPlay('sl006')"], ["Puzzle.Damage('sl034', 99)"], {"en_jeu": ["sl031", "sl006"], "degats_identite": 1}, deck=["01105", "sl031"], regles=["v16_all", "v18_all"]),
    _s("sl030 Bo Staff Ninja vaincu, le sbire revele est le DERNIER arrive : si le sbire revele n'a pas Teamwork (2 cartes defaussees sans NINJA), le joueur n'est pas attaque", "temoin du cas precedent",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sl030')", "Puzzle.PutIntoPlay('sl006')"], ["Puzzle.Damage('sl030', 99)", "Puzzle.Damage('sl030', 99)"], {"degats_identite": 0, "hors_jeu": ["sl032"]}, deck=["01105", "01105", "01105"], regles=["v16_all", "v18_all"]),
    _s("sl030 Teamwork a l'ENTREE EN JEU : Bo Staff Ninja arrive avec Ghost Maker (NINJA) deja la -> il s'active et attaque (ATQ 1 -> 1 degat), Ghost Maker NON (v16_teamwork)", "Teamwork (NINJA) natif : le sbire qui arrive s'active, pas les autres",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sl006')"], ["Puzzle.PutIntoPlay('sl030')"], {"degats_identite": 1}, regles=["v16_all", "v18_all"]),
    _s("sl030 Teamwork, TEMOIN : arrive SEUL, aucun autre NINJA -> pas d'activation", "il faut un AUTRE sbire du trait",
       ["Puzzle.Exhaust('01001a')"], ["Puzzle.PutIntoPlay('sl030')"], {"degats_identite": 0}, regles=["v16_all", "v18_all"]),
    _s("sl030 Teamwork, TEMOIN : arrive avec un sbire NON-NINJA (Whirlwind) -> pas d'activation", "le trait cite est NINJA",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('01130')"], ["Puzzle.PutIntoPlay('sl030')"], {"degats_identite": 0}, regles=["v16_all", "v18_all"]),
    _s("sl032 Teamwork : Kusarigama (Teamwork) deja en jeu avec Ghost Maker, Katana arrive : SEUL Katana s'active (1 degat ; Kusarigama a deja eu ses degats, soignes avant)", "regle 1.6+ : seul le sbire qui arrive s'active",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sl006')", "Puzzle.PutIntoPlay('sl033')", "Puzzle.Heal('01001a', 5)"], ["Puzzle.PutIntoPlay('sl032')"], {"degats_identite": 1}, regles=["v16_all", "v18_all"]),
    _s("sl033 Kusarigama Ninja (Patrol) engage : le joueur ne peut pas contrecarrer le complot principal", "Patrol natif (desc)",
       ["Puzzle.PutIntoPlay('sl033')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["01097b", 5]]}, avant_forme=["Puzzle.SetThreat('01097b', 5)"]),
    _s("sl033 Patrol, TEMOIN : sans Kusarigama, le meme contre retire 2 menaces (5 -> 3)", "le blocage vient de Patrol",
       ["Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["01097b", 3]]}, avant_forme=["Puzzle.SetThreat('01097b', 5)"]),
    _s("sl032 Katana Ninja (Guard) engage : le joueur ne peut pas attaquer le vilain", "Guard natif (desc)",
       ["Puzzle.PutIntoPlay('sl032')"], ["Puzzle.Attack('01001a')"], {"degats": [["01094", 0]]}, cibles=["01094"]),
    _s("sl030 Bo Staff Ninja entre en jeu avec un statut Tough (Toughness)", "Toughness natif (desc)",
       ["Puzzle.PutIntoPlay('sl030')"], [], {"statuts": [["sl030", "Tough"]]}),
    _s("sl031 Fukiya Ninja (ranged) attaque Black Panther (Retaliate 1) : la riposte est IGNOREE, Fukiya ne prend rien", "« This minion's attacks gain ranged »",
       [], ["Puzzle.PutIntoPlay('sl031')", "Puzzle.Attack('sl031')"], {"degats": [["sl031", 0]]}, heros="black_panther", forme_heros=False,
       avant_forme=["Puzzle.ChangeForm('01040b')"]),
    _s("sl032 Katana Ninja attaque Black Panther (Retaliate 1) : TEMOIN, la riposte frappe (1 degat sur Katana)", "sans ranged, Retaliate s'applique",
       [], ["Puzzle.PutIntoPlay('sl032')", "Puzzle.Attack('sl032')"], {"degats": [["sl032", 1]]}, heros="black_panther", forme_heros=False,
       avant_forme=["Puzzle.ChangeForm('01040b')"]),
    _s("sl034 Shuriken Ninja (piercing) attaque un heros Tough : le statut Tough est defausse ET les degats passent (1)", "« This minion's attacks gain piercing »",
       ["Puzzle.Exhaust('01001a')", "Puzzle.Tough('01001a')"], ["Puzzle.PutIntoPlay('sl034')", "Puzzle.Attack('sl034')"], {"degats_identite": 1, "statuts_absents": [["01001a", "Tough"]]}),
    _s("sl032 Katana Ninja attaque un heros Tough : TEMOIN, le Tough absorbe (0 degat)", "sans piercing, Tough bloque",
       ["Puzzle.Exhaust('01001a')", "Puzzle.Tough('01001a')"], ["Puzzle.PutIntoPlay('sl032')", "Puzzle.Attack('sl032')"], {"degats_identite": 0, "statuts_absents": [["01001a", "Tough"]]}),
    # ------------------------------------------------------------------------------------------------------ sl035 : Dancing Shadows
    _s("sl035 Dancing Shadows : chaque sbire NINJA a +1 PV (Ghost Maker 4 -> 5)", "« Each NINJA minion gets +1 hit point »",
       ["Puzzle.PutIntoPlay('sl035')", "Puzzle.PutIntoPlay('sl006')"], [], {"pv_max": [["sl006", 5]]}),
    _s("sl035, TEMOIN : sans Dancing Shadows, Ghost Maker garde 4 PV", "le bonus vient de la manigance",
       ["Puzzle.PutIntoPlay('sl006')"], [], {"pv_max": [["sl006", 4]]}),
    _s("sl035 : un sbire NON-NINJA (Whirlwind) ne gagne rien (6 PV)", "« each NINJA minion »",
       ["Puzzle.PutIntoPlay('sl035')", "Puzzle.PutIntoPlay('01130')"], [], {"pv_max": [["01130", 6]]}),
    _s("sl035 : tant qu'un sbire NINJA est en jeu, la menace ne peut pas etre retiree de la manigance (3 reste 3)", "« Threat cannot be removed from this scheme while at least 1 NINJA minion is in play »",
       ["Puzzle.PutIntoPlay('sl035')", "Puzzle.PutIntoPlay('sl006')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["sl035", 3]]}, cibles=["sl035"]),
    _s("sl035, TEMOIN : sans aucun sbire NINJA en jeu, la menace se retire normalement (3 - 2 = 1)", "la contrainte tombe sans NINJA",
       ["Puzzle.PutIntoPlay('sl035')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"menace": [["sl035", 1]]}, cibles=["sl035"]),
    _s("sl035 : le dernier sbire NINJA vaincu, la menace redevient retirable (3 - 2 = 1)", "la condition est reevaluee en cours de partie",
       ["Puzzle.PutIntoPlay('sl035')", "Puzzle.PutIntoPlay('sl006')", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.Damage('sl006', 99)"], ["Puzzle.Thwart('01075')"], {"menace": [["sl035", 1]]}, cibles=["sl035"]),
    _s("sl035 Boost : « Reveal this card » -> Dancing Shadows entre en jeu quand elle sert de boost", "[star] Boost : Reveal this card",
       [], ["Puzzle.Attack('01094')"], {"en_jeu": ["sl035"]}, deck=["sl035"]),
    # ------------------------------------------------------------------------------------------------------ sl036 : Countless Numbers
    _s("sl036 Countless Numbers revelee : les sbires NINJA de la defausse de rencontre retournent dans le deck, le sbire non-NINJA reste en defausse",
       "« Shuffle each NINJA minion in the encounter discard pile into the encounter deck »",
       ["Puzzle.CreateEncounterDiscardPile('sl006', 'sl030', '01121')"], ["Puzzle.Reveal('sl036')"], {"defausse_rencontre": ["01121"], "absents_defausse_rencontre": ["sl006", "sl030"]}, deck=["01105", "01105", "01105", "01105", "01105"]),
    _s("sl036 Countless Numbers : TEMOIN, la traitrise seule (rien de NINJA en defausse) laisse la defausse a l'identique", "la regle n'agit que sur les sbires NINJA",
       ["Puzzle.CreateEncounterDiscardPile('01121')"], ["Puzzle.Reveal('sl036')"], {"defausse_rencontre": ["01121"]}, deck=["01105", "01105", "01105", "01105"]),
    _s("sl036 Countless Numbers en BOOST : « Resolve this card's When Revealed ability » -> les sbires NINJA de la defausse retournent aussi dans le deck", "[star] Boost",
       ["Puzzle.CreateEncounterDiscardPile('sl006', '01121')"], ["Puzzle.Boost('sl036')"], {"defausse_rencontre": ["01121"], "absents_defausse_rencontre": ["sl006"]}, deck=["01105", "01105", "01105", "01105"]),
    _s("sl036 Surge (natif) : apres sa revelation, une carte de rencontre SUPPLEMENTAIRE est revelee puis defaussee (01105)", "desc : Surge 1",
       [], ["Puzzle.Reveal('sl036')"], {"defausse_rencontre": ["sl036", "01105"]}, deck=["01105", "01105", "01105", "01105"]),
    # ======================================================================================================== BLACK FLOWER
    # Le heros est EPUISE quand une attaque doit faire des degats (sinon le pilote defend avec Spider-Man, DEF 3) ; la Creeping Corruption se pose face A (CC) ou face B (CC_B).
    # ------------------------------------------------------------------------------------------------------ sl073 : Aka
    _s("sl073 Aka entre en jeu (Quickstrike) : l'Interruption est offerte, le joueur place 1 compteur et l'attaque est ANNULEE (identite intacte)", "« you may place 1 corruption counter on your Creeping Corruption. If you do, cancel that attack »",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.PutIntoPlay('sl073')"], {"compteurs": [["sl072a", "corruption", 1]], "degats_identite": 0}),
    _s("sl073, refus (« you MAY ») : pas de compteur et l'attaque a lieu (ATQ 3)", "l'Interruption est facultative",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.PutIntoPlay('sl073')"], {"compteurs": [["sl072a", "corruption", 0]], "degats_identite": 3}, passer_sur_option="Interrupt"),
    _s("sl073, sans Creeping Corruption : aucune annulation possible, l'attaque a lieu (ATQ 3)", "« If you do » : sans compteur pose, pas d'annulation",
       ["Puzzle.Exhaust('01001a')"], ["Puzzle.PutIntoPlay('sl073')"], {"degats_identite": 3}),
    _s("sl073, 5e compteur pose par l'Interruption (4 -> 5) : la carte se retourne (face B, 0 compteur) ET l'attaque est annulee", "le seuil se franchit pendant le cout, l'annulation suit",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)", "Puzzle.Exhaust('01001a')"], ["Puzzle.PutIntoPlay('sl073')"], {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]], "degats_identite": 0}),
    _s("sl073 Boost, branche 1 : place 1 compteur sur la Creeping Corruption (Rhino attaque : ATQ 2 + 1 icone = 3 degats)", "« Choose: Either place 1 corruption counter on your Creeping Corruption, or discard 1 random card »",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 1]], "degats_identite": 3, "en_main": ["01088"]}, deck=["sl073"]),
    _s("sl073 Boost, branche 2 : defausse 1 carte AU HASARD de la main (la seule) et AUCUN compteur (Black Panther : sa main ne se remplit pas pendant l'attaque)", "« or discard 1 random card from your hand »",
       [CC, "Puzzle.Exhaust('01040a')"], ["Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01088')", "Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 0]], "main_exacte": []}, deck=["sl073"], preferer_option="Discard 1 random", heros="black_panther", forme_heros=False, avant_forme=["Puzzle.ChangeForm('01040b')"]),
    _s("sl073 Boost, main VIDE : la branche « defausser » est masquee, il reste la branche compteur", "echappatoire a la corruption refusee (DECISIONS-d.md n°8)",
       [CC, "Puzzle.Exhaust('01040a')"], ["Puzzle.EmptyHand()", "Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 1]]}, deck=["sl073"], preferer_option="Discard 1 random", heros="black_panther", forme_heros=False, avant_forme=["Puzzle.ChangeForm('01040b')"]),
    _s("sl073 Boost, SANS Creeping Corruption : seule la branche « defausser » existe (la carte de la main est defaussee)", "la branche compteur est impossible",
       ["Puzzle.Exhaust('01040a')"], ["Puzzle.EmptyHand()", "Puzzle.CreateHandCards('01088')", "Puzzle.Attack('01094')"], {"main_exacte": []}, deck=["sl073"], heros="black_panther", forme_heros=False, avant_forme=["Puzzle.ChangeForm('01040b')"]),
    # ------------------------------------------------------------------------------------------------------ sl074 : Tongue of the Beast
    _s("sl074 Tongue of the Beast vaincue : le joueur qui l'a vaincue place 2 compteurs sur sa Creeping Corruption", "« The defeating player places 2 corruption counters on their Creeping Corruption »",
       [CC, "Puzzle.PutIntoPlay('sl074')"], ["Puzzle.Damage('sl074', 99)"], {"compteurs": [["sl072a", "corruption", 2]]}),
    _s("sl074 vaincue avec 4 compteurs : 2 d'un coup (4 -> 6) -> TOUS les compteurs partent et la carte se retourne", "seuil franchi par une pose de 2",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)", "Puzzle.PutIntoPlay('sl074')"], ["Puzzle.Damage('sl074', 99)"], {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]]}),
    _s("sl074 vaincue SANS Creeping Corruption : rien ne se passe (pas d'erreur)", "pas de carte, pas de compteur",
       ["Puzzle.PutIntoPlay('sl074')"], ["Puzzle.Damage('sl074', 99)"], {"hors_jeu": ["sl074"]}),
    _s("sl074 vaincue par le joueur 2 (Black Panther) : les 2 compteurs vont sur LA Creeping Corruption de CE joueur", "« their Creeping Corruption » (une par joueur)",
       [CC, "Puzzle.PutIntoPlay('sl072a,sl072b', under_control=True, player=1)", "Puzzle.PutIntoPlay('sl074')"], ["Puzzle.Damage('sl074', 99, Puzzle.FindFaceInPlay('01040a'))"],
       {"corruption_joueurs": [[0, 0, "sl072a"], [1, 2, "sl072a"]]}, heros2="black_panther"),
    _s("sl074 Boost, branche 1 : 1 compteur (Rhino attaque : ATQ 2, aucune icone sur cette carte)", "« Choose: Either place 1 corruption counter ... or this card gains [boost][boost][boost] »",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 1]], "degats_identite": 2}, deck=["sl074"]),
    _s("sl074 Boost, branche 2 : la carte gagne 3 icones -> ATQ 2 + 3 = 5 et AUCUN compteur", "la 2e branche",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 0]], "degats_identite": 5}, deck=["sl074"], preferer_option="gains"),
    # ------------------------------------------------------------------------------------------------------ sl075 : Binding Ritual
    _s("sl075 Binding Ritual revelee, branche 1 : le joueur place 1 compteur (menace de depart 1 par joueur = 1, rien d'ajoute)", "« Each player chooses: Place 1 corruption counter on their Creeping Corruption »",
       [CC], ["Puzzle.Reveal('sl075')"], {"compteurs": [["sl072a", "corruption", 1]], "menace": [["sl075", 1]]}),
    _s("sl075 revelee, branche 2 : 3 menaces ici (1 + 3 = 4), aucun compteur", "« Place 3 threat here »",
       [CC], ["Puzzle.Reveal('sl075')"], {"compteurs": [["sl072a", "corruption", 0]], "menace": [["sl075", 4]]}, preferer_option="Place 3 threat"),
    _s("sl075 revelee SANS Creeping Corruption : seule la branche menace existe (4)", "la branche compteur est impossible",
       [], ["Puzzle.Reveal('sl075')"], {"menace": [["sl075", 4]]}),
    _s("sl075 revelee a DEUX joueurs : chacun place le compteur sur SA Creeping Corruption (menace de depart 2)", "« each player chooses »",
       [CC, "Puzzle.PutIntoPlay('sl072a,sl072b', under_control=True, player=1)"], ["Puzzle.Reveal('sl075')"],
       {"corruption_joueurs": [[0, 1, "sl072a"], [1, 1, "sl072a"]], "menace": [["sl075", 2]]}, heros2="black_panther"),
    _s("sl075 revelee a DEUX joueurs, les deux choisissent la menace : 2 + 3 + 3 = 8", "chaque joueur choisit pour lui",
       [CC, "Puzzle.PutIntoPlay('sl072a,sl072b', under_control=True, player=1)"], ["Puzzle.Reveal('sl075')"],
       {"corruption_joueurs": [[0, 0, "sl072a"], [1, 0, "sl072a"]], "menace": [["sl075", 8]]}, heros2="black_panther", preferer_option="Place 3 threat"),
    _s("sl075 : icone Crisis (desc)", "Crisis 1",
       [], ["Puzzle.Reveal('sl075')"], {"icones": [["Crisis", 1]]}, preferer_option="Place 3 threat"),
    # ------------------------------------------------------------------------------------------------------ sl076 : Roots of a Black Flower
    _s("sl076 Roots of a Black Flower revelee : menace de depart 1 (fixe) et 2 icones Acceleration", "desc : StartingThreat 1, Acceleration 2",
       [], ["Puzzle.Reveal('sl076')"], {"menace": [["sl076", 1]], "icones": [["Acceleration", 2]]}),
    _s("sl076 vaincue par le joueur : 2 compteurs sur sa Creeping Corruption", "« The defeating player places 2 corruption counters on their Creeping Corruption »",
       [CC, "Puzzle.Reveal('sl076')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"], {"compteurs": [["sl072a", "corruption", 2]]}, cibles=["sl076"]),
    _s("sl076 vaincue avec 4 compteurs (4 -> 6) : la Creeping Corruption se retourne et se vide", "seuil franchi par 2 compteurs d'un coup",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)", "Puzzle.Reveal('sl076')", "Puzzle.PutIntoPlay('01075', under_control=True)"], ["Puzzle.Thwart('01075')"],
       {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]]}, cibles=["sl076"]),
    _s("sl076, TEMOIN : en jeu mais PAS vaincue, aucun compteur n'est pose (le compteur ne part qu'a la defaite)", "« When Defeated »",
       [CC, "Puzzle.PutIntoPlay('sl076')"], [], {"compteurs": [["sl072a", "corruption", 0]], "menace": [["sl076", 1]]}),
    _s("sl076 Boost, branche 1 : 1 compteur (Rhino : ATQ 2, aucune icone)", "« Choose: Either place 1 corruption counter ... or place 4 threat on the main scheme »",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 1]], "menace": [["01097b", 0]], "degats_identite": 2}, deck=["sl076"]),
    _s("sl076 Boost, branche 2 : 4 menaces sur le complot PRINCIPAL, aucun compteur", "la 2e branche",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 0]], "menace": [["01097b", 4]]}, deck=["sl076"], preferer_option="Place 4 threat"),
    # ------------------------------------------------------------------------------------------------------ sl077 : Malediction
    _s("sl077 Malediction revelee en ALTER-EGO, accepte : 2 compteurs et le vilain ne manigance pas", "« You may place 2 corruption counters on your Creeping Corruption. If you do not, the villain schemes with +2 SCH »",
       [CC], ["Puzzle.Reveal('sl077')"], {"compteurs": [["sl072a", "corruption", 2]], "menace": [["01097b", 0]]}, forme_heros=False),
    _s("sl077 en ALTER-EGO, refuse : aucun compteur et le vilain manigance avec +2 SCH (Rhino SCH 1 + 2 = 3 menaces)", "« If you do not »",
       [CC], ["Puzzle.Reveal('sl077')"], {"compteurs": [["sl072a", "corruption", 0]], "menace": [["01097b", 3]]}, forme_heros=False, choisir_option="Cancel"),
    _s("sl077 en ALTER-EGO, SANS Creeping Corruption : impossible d'accepter -> le vilain manigance avec +2 SCH (3 menaces)", "refus par impossibilite",
       [], ["Puzzle.Reveal('sl077')"], {"menace": [["01097b", 3]]}, forme_heros=False),
    _s("sl077 en ALTER-EGO, accepte avec 4 compteurs (4 -> 6) : la Creeping Corruption se retourne et se vide, le vilain ne manigance pas", "deux compteurs d'un coup",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)"], ["Puzzle.Reveal('sl077')"], {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]], "menace": [["01097b", 0]]}, forme_heros=False),
    _s("sl077 revelee en HEROS, Creeping Corruption face A (sans OVERPOWERING) : le vilain ATTAQUE (Rhino ATQ 2), pas de manigance", "« otherwise, the villain attacks you »",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('sl077')"], {"degats_identite": 2, "menace": [["01097b", 0]]}),
    _s("sl077 en HEROS, Creeping Corruption face B (OVERPOWERING) : le vilain MANIGANCE avec +1 SCH (1 + 1 = 2 menaces), pas d'attaque", "« the villain schemes with +1 SCH »",
       [CC_B, "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('sl077')"], {"degats_identite": 0, "menace": [["01097b", 2]]}),
    _s("sl077 en HEROS, SANS Creeping Corruption : « otherwise », le vilain attaque (2)", "pas de trait OVERPOWERING",
       ["Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('sl077')"], {"degats_identite": 2, "menace": [["01097b", 0]]}),
    _s("sl077 a DEUX joueurs : Spider-Man (revele) a la face A, Black Panther la face B -> c'est SA Creeping Corruption qui compte : le vilain ATTAQUE", "« YOUR Creeping Corruption »",
       [CC, "Puzzle.PutIntoPlay('sl072b,sl072a', under_control=True, player=1)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('sl077')"], {"degats_identite": 2, "menace": [["01097b", 0]]}, heros2="black_panther"),
    _s("sl077 a DEUX joueurs : Spider-Man (revele) a la face B, Black Panther la face A -> le vilain MANIGANCE avec +1 SCH (2 menaces)", "le trait est lu sur la Creeping Corruption du joueur qui revele",
       [CC_B, "Puzzle.PutIntoPlay('sl072a,sl072b', under_control=True, player=1)", "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('sl077')"], {"degats_identite": 0, "menace": [["01097b", 2]]}, heros2="black_panther"),
    _s("sl077 : icone de boost 1 (desc)", "desc : Boost 1",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"degats_identite": 3}, deck=["sl077"], preferer_option="Place 2"),
    # ------------------------------------------------------------------------------------------------------ sl078 : Invasive Thoughts
    _s("sl078 Invasive Thoughts revelee, Creeping Corruption face A : 1 compteur puis, sans OVERPOWERING, 1 degat a l'identite", "« place 1 corruption counter ... otherwise, take 1 damage »",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Reveal('sl078')"], {"compteurs": [["sl072a", "corruption", 1]], "degats_identite": 1, "menace": [["01097b", 0]]}),
    _s("sl078 revelee, Creeping Corruption face B (OVERPOWERING) : 1 compteur puis 1 menace sur le complot principal, pas de degat", "« If it has the OVERPOWERING trait, place 1 threat on the main scheme »",
       [CC_B], ["Puzzle.Reveal('sl078')"], {"compteurs": [["sl072b", "corruption", 1]], "degats_identite": 0, "menace": [["01097b", 1]]}),
    _s("sl078 revelee avec 4 compteurs sur la face A : le 5e la retourne (face B) PUIS le test lit OVERPOWERING -> 1 menace, pas de degat", "« If IT has the trait » : lu APRES la pose",
       [CC, "Puzzle.Counter('sl072a', 'corruption', 4)"], ["Puzzle.Reveal('sl078')"], {"compteurs": [["sl072b", "corruption", 0]], "face_visible": [["sl072", "sl072b"]], "degats_identite": 0, "menace": [["01097b", 1]]}),
    _s("sl078 revelee SANS Creeping Corruption : pas de compteur, pas d'OVERPOWERING -> 1 degat (DECISIONS-d.md n°9)", "« otherwise, take 1 damage »",
       [], ["Puzzle.Reveal('sl078')"], {"degats_identite": 1, "menace": [["01097b", 0]]}),
    _s("sl078 Boost, branche 1 : 1 compteur (Rhino : ATQ 2 sans icone)", "« Choose: Either place 1 corruption counter ... or take 4 indirect damage »",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 1]], "degats_identite": 2}, deck=["sl078"]),
    _s("sl078 Boost, branche 2 : 4 degats INDIRECTS (2 + 4 = 6), aucun compteur", "la 2e branche",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.Attack('01094')"], {"compteurs": [["sl072a", "corruption", 0]], "degats_identite": 6}, deck=["sl078"], preferer_option="Take 4 indirect"),
    # ======================================================================================================== PARTIE REELLE : scenario Shadows in the Night + modulaires Ninja Swarm et Black Flower
    # Scenario d'essai `sl_essai_ninja_black_flower` (data/scenarios) : `shadows_in_the_night` + `modular_sets: [ninja_swarm, black_flower]`. La Creeping Corruption se pose a la main (CC), car son Setup
# ne s'execute que pour un exemplaire du deck JOUEUR (voir DECISIONS-d.md n°10).
    # Graine 42 = vilain Elektra (sl014a). Le deck de rencontre est vide puis rempli de traitrises inoffensives (zero icone de boost) avant les cas qui mesurent des degats ou de la menace.
    _r("[reel] les 9 cartes Ninja Swarm et les 9 cartes Black Flower entrent dans le deck de rencontre par `modular_sets`, la Creeping Corruption (Setup, exemplaire du deck JOUEUR) n'est pas dans le deck de rencontre",
       "chargement des sets data/encounter_sets/ninja_swarm.json et black_flower.json",
       [], [], {"dans_deck_rencontre": ["sl028", "sl029", "sl030", "sl031", "sl032", "sl033", "sl034", "sl035", "sl036", "sl073", "sl074", "sl075", "sl076", "sl077", "sl078"], "hors_jeu": ["sl072a", "sl072b"]}, forme_heros=False, deck_reel=True),
    _r("[reel] Teamwork en chaine : Kirigi seul (aucune activation), Bo Staff arrive (Kirigi present) -> s'active (ATQ 1 + 1 = 2 degats), Fukiya arrive -> s'active (2 degats) : 4 au total, pas de double activation (Kirigi, ATQ 2 + 1, ajouterait 3)",
       "regle de jeu reelle v16 : seul le sbire qui ARRIVE s'active ; la position des deux cartes sl003a/sl004a est identique au depart : +1 ATQ a chaque personnage",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sl029')"], ["Puzzle.PutIntoPlay('sl030')", "Puzzle.PutIntoPlay('sl031')"], {"en_jeu": ["sl029", "sl030", "sl031"], "degats_identite": 4}),
    _r("[reel] Black Mountain, Kirigi et Bo Staff engages : Kirigi (NINJA, autre que Black Mountain) ne peut pas etre attaque, Black Mountain si",
       "Black Mountain en partie reelle, avec Teamwork des deux autres",
       ["Puzzle.Exhaust('01001a')", "Puzzle.PutIntoPlay('sl028')", "Puzzle.PutIntoPlay('sl029')", "Puzzle.PutIntoPlay('sl030')"], ["Puzzle.Attack('01001a')"], {"degats": [["sl029", 0], ["sl030", 0], ["sl028", 0]]}, cibles=["sl029"]),
    _r("[reel] la Creeping Corruption posee : Aka (Quickstrike) entre en jeu (Quickstrike) -> Interruption, 1 compteur et attaque annulee",
       "Creeping Corruption du Setup + Aka (Black Flower) en partie reelle",
       [CC, "Puzzle.Exhaust('01001a')"], ["Puzzle.PutIntoPlay('sl073')"], {"compteurs": [["sl072a", "corruption", 1]], "degats_identite": 0}),
    _r("[reel] Malediction (alter-ego, refus) : Elektra manigance avec +2 SCH -> 2 de depart + 3 = 5 menaces sur le complot",
       "« If you do not, the villain schemes with +2 SCH » dans le vrai scenario",
       [CC], ["Puzzle.Reveal('sl077')"], {"menace": [["sl001b", 5]], "compteurs": [["sl072a", "corruption", 0]]}, forme_heros=False, choisir_option="Cancel"),
    # ======================================================================================================== interactions avec le scenario 1 (agent A) : une carte PERMANENTE ne se defausse jamais
    # Trouve en autoplay (22/10/2026) : « discard an ally or upgrade you control » (sl004b) pouvait cibler la Creeping Corruption, et le moteur plantait (assert `is_eliminated`).
    _s("sl004b, branche « defausser un allie ou une amelioration » avec la Creeping Corruption (Permanent) ET un allie : l'allie est defausse, la Creeping Corruption RESTE", "une carte Permanent n'est jamais une cible de defausse",
       [CC, "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('sl003a,sl003b')", "Puzzle.PutIntoPlay('sl004b,sl004a')"], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"],
       {"defausse": ["01075"], "en_jeu": ["sl072a"], "face_visible": [["sl004", "sl004a"]]}, preferer_option="Discard an ally"),
    _s("sl004b avec la seule Creeping Corruption en jeu : la branche « defausser » n'est PAS offerte (aucune cible), le pilote prend la premiere (3 degats) ; pas de plantage, la carte reste", "meme regle",
       [CC, "Puzzle.PutIntoPlay('sl003a,sl003b')", "Puzzle.PutIntoPlay('sl004b,sl004a')"], ["Puzzle.Action('sl004b', 'FirstPlayerAction')"],
       {"en_jeu": ["sl072a"], "degats_identite": 3, "face_visible": [["sl004", "sl004a"]]}, preferer_option="Discard an ally"),
    _s("sl006 Ghost Maker vaincu, vilain aux Streets -> Atop the Tenshu : « discard 1 card you control » avec la seule Creeping Corruption : rien n'est defausse (Permanent), pas de plantage", "meme regle",
       [CC, "Puzzle.PutIntoPlay('sl003a,sl003b')", "Puzzle.PutIntoPlay('sl004a,sl004b')", "Puzzle.PutIntoPlay('sl006')"], ["Puzzle.Damage('sl006', 99)"],
       {"en_jeu": ["sl072a"], "face_visible": [["sl003", "sl003b"]]}),
]


VERIFICATIONS = r'''
def sld_etat(monde, aides):
    """etat_attendu + les cles de l'agent D :
         face_visible        [[prefixe, card_id]] la face MONTREE de la carte (deux faces = un prefixe)
         partie_finie        bool
         corruption_joueurs  [[indice_joueur, n_compteurs, card_id_visible]] la Creeping Corruption de CHAQUE joueur (deux heros : meme card_id)"""
    cas = aides["cas"]
    attendu = cas.get("attendu") or {}
    soucis = []
    for prefixe, voulu in attendu.get("face_visible") or []:
        vues = []
        for objet in monde.object_manager.card_dict.values():
            face = getattr(objet, "face", None)
            cid = str(getattr(getattr(face, "paper", None), "card_id", ""))
            if cid.startswith(prefixe) and cid not in vues:
                vues.append(cid)
        if vues != [voulu]:
            soucis.append(f"faces montrees pour {prefixe} : {vues} (attendu {voulu})")
    if "partie_finie" in attendu and bool(monde.is_game_over) != attendu["partie_finie"]:
        soucis.append(f"partie finie = {bool(monde.is_game_over)} (attendu {attendu['partie_finie']})")
    for indice, n, voulu in attendu.get("corruption_joueurs") or []:
        joueur = monde.const_players[indice]
        cc = [f for f in joueur.GetControlUpgrade() if str(f.paper.card_id) in ("sl072a", "sl072b")]
        if len(cc) != 1:
            soucis.append(f"joueur {indice} : {len(cc)} Creeping Corruption (attendu 1)")
            continue
        vu = cc[0].GetCounters("corruption")
        if vu != n or str(cc[0].paper.card_id) != voulu:
            soucis.append(f"joueur {indice} : {cc[0].paper.card_id} avec {vu} compteurs (attendu {voulu} avec {n})")
    if attendu.get("absents_defausse_rencontre") or "defausse_rencontre_taille" in attendu:
        from game.operate.worlds import Worlds as _W
        ids_def = [str(f.paper.card_id) for f in _W.GetEncounterDiscardPileCards(monde)]
        for cid in attendu.get("absents_defausse_rencontre") or []:
            if cid in ids_def:
                soucis.append(f"{cid} est encore dans la defausse de rencontre {ids_def}")
        if "defausse_rencontre_taille" in attendu and len(ids_def) != attendu["defausse_rencontre_taille"]:
            soucis.append(f"defausse de rencontre de {len(ids_def)} cartes {ids_def} (attendu {attendu['defausse_rencontre_taille']})")
    if "main_exacte" in attendu:
        ids_main = sorted(str(f.paper.card_id) for f in monde.players[0].hand_cards.Get())
        if ids_main != sorted(attendu["main_exacte"]):
            soucis.append(f"main {ids_main} (attendu {sorted(attendu['main_exacte'])})")
    propres = ("main_exacte", "face_visible", "partie_finie", "corruption_joueurs", "absents_defausse_rencontre", "defausse_rencontre_taille")
    reste = {k: v for k, v in attendu.items() if k not in propres}
    cas["attendu"] = reste
    try:
        ok, msg = etat_attendu(monde, aides)
    finally:
        cas["attendu"] = attendu
    if not ok:
        soucis.append(msg)
    return (False, " ; ".join(soucis)) if soucis else (True, "etat conforme")
'''
