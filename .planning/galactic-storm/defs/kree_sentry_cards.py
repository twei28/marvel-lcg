# Entrees cards.json du scenario 1 KREE SENTRY de Galactic Storm (gs076-gs090), lot GS-4 (20/10/2026).
# Texte = docs/packs/galactic-storm/transcriptions/kree-sentry.md, RELU SUR LES SCANS le 20/10/2026.
# card_id = gs + numero IMPRIME en pied de carte (« MC Custom Content By: Kajislav <n> »), 3 chiffres (+ a/b) ;
# UN card_id par numero imprime, les copies sont des exemplaires du paquet (decisions utilisateur du 20/10/2026).
#
# Lectures faites sur les scans (preuves de decoupe dans le gabarit, KREE-SENTRY-GABARITS.md) :
#  - icone « avion + croix » de Locking on Target = AMPLIFY (identique a sk252 Super-Skrull Training Program, dont
#    la fiche declare `Amplify`, et a gs133) ; icones de ressource des deux poings de l'Optic Blast Cannon =
#    [physical][physical] (comparees aux poings de sk148 / sk152, ressource R declaree).
#  - silhouette apres un nombre = « par joueur » (`*` dans desc) ; etoile a contour sous THW/ATK d'un allie =
#    degats consecutifs (une `*` par etoile) ; Y rouge = 1 icone de boost ; etoile rouge SEULE dans le coin
#    (Gotcha) = carte a « ★ Boost » sans icone (aucune cle Boost) ; etoile en exposant d'une stat = renvoi au
#    texte, sans valeur chiffree (convention Skrull Menace).
#  - badge « +1★ ATK » des deux armes = `ATK+` (comme gs129 Shi'ar Javelin, meme maquette).
#  - 1B : depart 2 / escalade +1 / objectif 7, tous PAR JOUEUR ; 2B : depart 1 / escalade +1 / objectif 10,
#    tous par joueur (lu sur les scans, la transcription avait lu « 7 et 8 superposes » : c'est le « 7 » et la
#    silhouette).
#  - 2B imprime « If this stage is completes » : coquille (question Q1 de .planning/todos/2026-10-20-gs4-questions.md,
#    recommandation « traiter comme la forme officielle »).
KS = "Kree Sentry"


def c(cid, typ, name, desc, traits, text, subtitle=""):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": subtitle, "desc": desc,
            "traits": traits, "set_name": KS, "text": text, "custom": "Kajislav"}


REPONSE_SENTRY = ("[star] <b>Forced Response</b>: After Kree Sentry attacks and damages a character, attach a set aside "
                  "copy of Sentry's Grasp to that character. If you cannot, place {n} threat on the main scheme.")
CITATION_SENTRY = ("<i>\"I am Intergalactic Sentry #372, re-activated for the first time since my posting on this "
                   "primitive planet some 250 centuries ago.\"</i>")
DEGATS_ETAPE_UN = ("[star] <b>Forced Response</b>: After resolving step one of the villain phase, deal 1 damage to each "
                   "character for each copy of Sentry's Grasp attached to it.")

CARDS = [
    # --- Mechant ------------------------------------------------------------------------------------------
    c("gs076", "Villain", "Kree Sentry", {"HP": "16*", "ATK": "1", "SCH": "2", "Stage": "1"}, ["KREE", "ROBOT"],
      REPONSE_SENTRY.format(n=1) + "\n" + CITATION_SENTRY),
    c("gs077", "Villain", "Kree Sentry", {"HP": "18*", "ATK": "2", "SCH": "2", "Stage": "2"}, ["KREE", "ROBOT"],
      "<b>When Revealed</b>: Attach a set aside copy of Sentry's Grasp to Rick Jones.\n"
      + REPONSE_SENTRY.format(n=2) + "\n" + CITATION_SENTRY),
    c("gs078", "Villain", "Kree Sentry", {"HP": "21*", "ATK": "3", "SCH": "2", "Stage": "3"}, ["KREE", "ROBOT"],
      "<b>When Revealed</b>: Attach each set aside copy of Sentry's Grasp to Rick Jones.\n"
      + REPONSE_SENTRY.format(n=3)),
    # --- Manigances principales ---------------------------------------------------------------------------
    c("gs079a", "MainScheme", "Sentry Awakens", {"Stage": "1"}, [],
      "<b>Contents</b>: Kree Sentry (I) and Kree Sentry (II) <i>(Kree Sentry (II) and Kree Sentry (III) instead for "
      "expert mode)</i>. Kree Sentry, and Standard encounter sets. One modular encounter set <i>(Imperial Guard)</i>.\n"
      "<b>Setup</b>: Put Rick Jones into play under the first player's control. Set 1 copy of Sentry's Grasp aside and "
      "attach the other to Rick Jones."),
    c("gs079b", "MainScheme", "Sentry Awakens",
      {"Stage": "1", "TargetThreat": "7*", "EscalationThreat": "1*", "StartingThreat": "2*"}, [],
      "<i>Buried deep within an abandoned Kree outpost, the Psyche Magnitron remained dormant—until the vault was "
      "breached. Now, Sentry #372 has awakened, programmed to eliminate all intruders and protect its ancient charge at "
      "all costs.</i>\n" + DEGATS_ETAPE_UN),
    c("gs080a", "MainScheme", "Self-Destruct Sequence", {"Stage": "2"}, [],
      "<i>Realizing the Psyche Magnitron's value, the Kree Sentry redirected all power to its self-destruct "
      "sequence.</i>\n<b>When Revealed</b>: If the Outpost Collapse Protocol side scheme is in play, place 2[per_hero] "
      "threat and 1 acceleration token on it. Otherwise, search the encounter deck and discard pile for the Outpost "
      "Collapse Protocol side scheme and reveal it."),
    c("gs080b", "MainScheme", "Self-Destruct Sequence",
      {"Stage": "2", "TargetThreat": "10*", "EscalationThreat": "1*", "StartingThreat": "1*"}, [],
      DEGATS_ETAPE_UN + "\n<b>If this stage is completed, the players lose the game.</b>"),
    # --- Allie de scenario et condition ---------------------------------------------------------------------
    c("gs081", "Ally", "* Rick Jones", {"HP": "5", "THW": "1", "ATK": "2**", "Class": "Encounter"}, ["CIVILIAN"],
      "The first player controls Rick Jones. He does not count against your ally limit.\n"
      "<b>Forced Interrupt</b>: When Kree Sentry attacks you, it attacks Rick Jones instead.\n"
      "<b>If Rick Jones leaves play, the players lose the game.</b>"),
    c("gs082", "Attachment", "Sentry's Grasp", {}, ["CONDITION"],
      "Attached character cannot thwart or scheme and can only attack Kree Sentry or this card.\n"
      "Any player can attack this card as if it were a minion. If there is 3 or more damage here, set Sentry's Grasp "
      "aside.\n<b>Forced Interrupt</b>: When this card would leave play, set it aside instead."),
    # --- Armes de Kree Sentry ---------------------------------------------------------------------------------
    c("gs083", "Attachment", "Optic Blast Cannon", {"Boost": "1", "ATK+": "1"}, ["WEAPON"],
      "Attach to Kree Sentry.\n[star] Kree Sentry's attacks gain piercing and ranged.\n"
      "<b>Hero Action</b>: Spend [physical][physical] resources → discard this card.\n<hr />\n"
      "[star] <b>Boost</b>: If this activation is an attack, it gains piercing and ranged."),
    c("gs084", "Attachment", "Repulsor Blast Unit", {"Boost": "1", "ATK+": "1"}, ["WEAPON"],
      "Attach to Kree Sentry.\n[star] Kree Sentry's attacks gain overkill and ranged.\n"
      "<b>Forced Interrupt</b>: When Sentry's Grasp would be set aside, if there is 5 or more damage on it, discard "
      "Repulsor Blast Unit.\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, it gains overkill."),
    # --- Manigances annexes -----------------------------------------------------------------------------------
    c("gs085", "SideScheme", "Death Grip", {"StartingThreat": "3*", "Boost": "1"}, [],
      "<i>Determined to hold the line, his grip tightens with deadly intent. Every move you make only brings his "
      "massive hand closer, ready to end the fight in an instant.</i>\nSentry's Grasp is set aside when there is 5 or "
      "more damage on it instead of 3."),
    c("gs086", "SideScheme", "Locking on Target",
      {"StartingThreat": "3", "Hinder": "1*", "Amplify": "1", "Boost": "2"}, [],
      "<i>\"A sentry can never surrender. A sentry must be true to its programming.\" —Kree Sentry</i>\n"
      "Hinder 1[per_hero]."),
    c("gs087", "SideScheme", "Outpost Collapse Protocol", {"StartingThreat": "1", "Hinder": "2*", "Boost": "2"}, [],
      "<i>As the battle rages, the outpost begins to collapse and falling debris threatens everyone inside.</i>\n"
      "Hinder 2[per_hero].\n<b>Forced Response</b>: After resolving step one of the villain phase, the first player "
      "deals 1 damage to each character they control."),
    # --- Traitrises ---------------------------------------------------------------------------------------------
    c("gs088", "Treachery", "\"Gotcha!\"", {}, [],
      "<b>When Revealed</b>: Attach a set aside copy of Sentry's Grasp to Rick Jones. If you cannot, this card gains "
      "surge.\n<hr />\n[star] <b>Boost</b>: Attach a set aside copy of Sentry's Grasp to Rick Jones.\n"
      "<i>\"The sentry is programmed to destroy you — and destroy you I shall!\" —Kree Sentry</i>"),
    c("gs089", "Treachery", "Caught in Its Sights", {"Boost": "1"}, [],
      "<b>When Revealed</b>: You may spend 2 resources of any type. If you do not, Kree Sentry attacks Rick Jones.\n"
      "<i>\"Prioritizing threat matrix... Targets acquired. Execute primary.\" —Kree Sentry</i>"),
    c("gs090", "Treachery", "Intruder Elimination", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Choose a non-[[KREE]] character. Kree Sentry attacks that character <i>(even if that "
      "character is an alter-ego)</i>. If an enemy was attacked this way, this card gains surge.\n"
      "<i>\"All intruders are to be destroyed!\" —Kree Sentry</i>"),
]

# Paquet rencontre propre du scenario (13 cartes, numeros 9 a 21 de « KREE SENTRY (n/21) »).
ENCOUNTERS = (["gs083"] + ["gs084"] * 2 + ["gs085"] + ["gs086"] * 2 + ["gs087"] + ["gs088"] * 2 + ["gs089"] * 2
              + ["gs090"] * 2)
# Cartes mises de cote : Rick Jones (mis en jeu par 1A) et les DEUX exemplaires de Sentry's Grasp.
SET_ASIDE = ["gs081", "gs082", "gs082"]
