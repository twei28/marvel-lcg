#!/usr/bin/env python3
"""Pose les textes FRANCAIS du scenario Black Queen + module Darkhold (hf361-hf366, hf401-hf422) dans ui-app/src/board/textes-fr-fanmade.ts.

Fichier PARTAGE (d'autres agents l'editent) : lecture-modification-ecriture en un seul geste sous flock, uniquement entre les balises
`// DEBUT hellfire_hunt_black_queen` / `// FIN hellfire_hunt_black_queen` (idempotent). Usage : python3 textes_fr.py <racine_du_depot>
"""
import fcntl
import json
import os
import sys

RACINE = sys.argv[1]
CHEMIN = os.path.join(RACINE, "ui-app", "src", "board", "textes-fr-fanmade.ts")
DEBUT = "  // DEBUT hellfire_hunt_black_queen"
FIN = "  // FIN hellfire_hunt_black_queen"

VOL = ("<b>Réponse forcée</b> : après que Selene attaque, soignez-la d'autant de dégâts que le total des dégâts non excédentaires subis lors de "
       "cette attaque par les personnages que le joueur attaqué contrôlait.")
T_TEMPS = "<b>Réponse forcée</b> : après qu'un personnage utilise un pouvoir de base ou qu'un ennemi s'active, retirez 1 compteur de temps d'ici."
T_FIN_TEMPS = "S'il n'y a aucun compteur de temps ici, retournez cette carte."
COUT_JOUR = "et retirez 1 compteur de temps de Beneath the Sun → défaussez cette carte."

FR = {
    "hf401": VOL + "\n<i>« Au fil des siècles… personne ne m'a jamais traquée sans que je le veuille. Malheureusement, vous ne vivrez pas assez longtemps pour "
             "raconter ce que vous avez appris… »</i>",
    "hf402": "Ténacité.\n" + VOL + "\n<i>« Des milliers d'âmes sont parties au bûcher en mon nom. Lequel de vous deux… sera le prochain ? »</i>",
    "hf403": "Solide. Ténacité.\n" + VOL + "\n<i>« C'est ici que je deviens une déesse. »</i>",
    "hf404a": "<i>Après que Sebastian a perdu tout intérêt pour le Club, Selene a tenté de reformer le Cercle intérieur avec l'aide de démons, en faisant venir "
              "Blackheart, le fils de Mephisto, comme nouveau Roi Noir.</i>\n<b>Contenu</b> : Selene (I) et Selene (II). <i>(Selene (II) et Selene (III) à la place "
              "en mode expert.)</i> Sets de rencontre Black Queen, Darkhold et Standard. Un set de rencontre modulaire <i>(Hellfire Conclave)</i>.\n"
              "<b>Mise en place</b> : mettez en jeu l'environnement Under the Moonlight. Mettez le module Darkhold de côté. Mélangez le Darkhold Dwarf mis de côté "
              "dans le deck de rencontre.",
    "hf404b": "<i>Après avoir obtenu le trône, la Reine Noire a cherché une source de pouvoir pour consolider sa position.</i>\n"
              "<b>Interruption forcée</b> : quand Darkhold Dwarf entre dans la pile de défausse, avancez à l'étape 2A.\n"
              "<b>Une fois accomplie</b> : donnez à Selene une carte d'état Tenace. Si l'environnement Beneath the Sun est en jeu, retirez-lui 2[per_hero] compteurs de temps.",
    "hf405a": "<i>Selene voulait acquérir les anciens Parchemins de Chthon, connus sous le nom de Darkhold, un livre de sorts maléfiques. En puisant dans ce savoir "
              "interdit, elle pourrait libérer de puissants sorts et rituels pour atteindre son but ultime : la divinité.</i>\n"
              "<b>Une fois révélée</b> : mélangez le set modulaire Darkhold mis de côté dans le deck de rencontre.",
    "hf405b": "<b>Une fois accomplie</b> : donnez à Selene une carte d'état Tenace. Cherchez Darkhold et attachez-le à Selene.",
    "hf406a": "<i>Avec le pouvoir du Darkhold sous son contrôle, Selene a pu accomplir un rituel obscur pour se renforcer en absorbant la force vitale de millions de "
              "créatures et accéder à la divinité.</i>\n<b>Une fois révélée</b> : cherchez la manigance annexe Immortal Moon Goddess et révélez-la. Cherchez "
              "Blackheart et mettez-le en jeu, engagé avec le premier joueur. <i>(Mélangez.)</i>",
    "hf406b": "[star] <b>Réponse forcée</b> : après l'étape 1 de la phase du méchant, placez ici 1 menace par compteur de temps sur Under the Moonlight ou "
              "Beneath the Sun.\n<b>Si cette étape est complétée, les joueurs perdent la partie.</b>",
    "hf407a": "Under the Moonlight entre en jeu avec 3[per_hero] compteurs de temps. " + T_FIN_TEMPS + "\n<b>Interruption forcée</b> : quand Black Queen "
              "s'activerait, donnez-lui 1 carte de boost supplémentaire.\n" + T_TEMPS,
    "hf407b": "Beneath the Sun entre en jeu avec 3[per_hero] compteurs de temps. " + T_FIN_TEMPS + "\nChaque identité gagne +1 à chacun de ses pouvoirs de base.\n" + T_TEMPS,
    "hf408": "Garde. Patrouille. Solide.\n<i>« Vous avez apporté l'Enfer sur Terre ! »</i>\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, "
             "cette attaque gagne Déferlement, Perçant et À distance.",
    "hf413": "Le personnage attaché ne peut pas attaquer Selene ni se défendre contre ses attaques.\n<b>Une fois révélée</b> : attachez-la à l'allié qui a le plus "
             "de points de vie restants et qui n'a pas de Hyponotic Trance attachée. Sinon, cette carte gagne Renfort.\n<b>Action de héros</b> : dépensez "
             "[mental][mental] " + COUT_JOUR,
    "hf416": "Attachez-la à Selene.\nSelene ne peut pas subir plus de 2 dégâts d'une seule attaque.\n<b>Action de héros</b> : dépensez 1 ressource [energy] "
             + COUT_JOUR + "\n<hr />\n[star] <b>Boost</b> : attachez cette carte à Selene.",
    "hf418": "Attachez-la à votre identité.\n<b>Interruption forcée</b> : quand Selene voudrait comploter contre vous, elle vous attaque à la place.\n"
             "<b>Action de héros</b> : dépensez 1 ressource [physical] " + COUT_JOUR,
    "hf419": "<b>Une fois révélée</b> : Selene vous attaque.\n<hr />\n[star] <b>Boost</b> : si cette attaque vainc un allié, placez 2 menaces sur la manigance principale.",
    "hf420": "<b>Une fois révélée</b> : retirez 1[per_hero] compteur de temps de Beneath the Sun. Si vous ne pouvez pas, placez 1[per_hero] compteur de temps sur "
             "Under the Moonlight.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
    "hf421": "Les compteurs de temps de l'environnement Under the Moonlight ne peuvent pas être retirés.\n<b>Une fois révélée</b> : retournez Beneath the Sun.",
    "hf422": "<i>« Bientôt… le monde connaîtra pour la première fois les vrais Hauts Seigneurs Extérieurs. Immortels. Invulnérables… et inarrêtables. »</i>\n"
             "Entrave 2[per_hero]. Victoire 1.\nTant que Under the Moonlight est en jeu, Black Queen ne peut pas être vaincue.",
    # ---------------------------------------------------------------- module Darkhold
    "hf361": "<b>Une fois révélé</b> : glissez sous cette carte le [[Spell of Darkhold]] du dessus de la pile de défausse de rencontre.\n<b>Une fois vaincu</b> : "
             "révélez la carte glissée ici.\n<i>« Pour faire simple, appelez-moi comme la plupart des gens que je rencontre : le Darkhold Dwarf. Ce n'est pas très "
             "délicat, je l'admets, mais à mon âge, franchement, je m'en fiche éperdument. »</i>",
    "hf362": "Attachez-le au méchant.\nUtilisations (2 compteurs de Darkspell).\n[star] <b>Interruption forcée</b> : quand le méchant attaque, retirez 1 compteur "
             "de Darkspell d'ici → donnez au personnage attaché 1 carte de boost supplémentaire pour cette activation.",
    "hf363": "Considérez l'allié attaché comme un sbire à la zone de texte vierge <i>(à l'exception de ses [[TRAITS]])</i>. Le SCH du sbire attaché est égal à son CTR "
             "imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : si Darkhold est attaché au méchant, attachez cette carte à votre allié qui "
             "a le plus de points de vie, puis retirez 1 compteur de Darkspell de Darkhold. Sinon, cherchez l'attachement Darkhold et révélez-le.",
    "hf364": "<b>Une fois révélée</b> : si Darkhold est attaché au méchant, subissez 3 dégâts indirects et retirez 1 compteur de Darkspell de Darkhold. Sinon, "
             "cherchez l'attachement Darkhold et révélez-le.",
    "hf365": "<b>Une fois révélée</b> : si Darkhold est attaché au méchant, vous êtes sonné et désorienté, et vous retirez 1 compteur de Darkspell de Darkhold. "
             "Sinon, cherchez Darkhold et révélez-le.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
    "hf366": "<b>Une fois révélée</b> : si Darkhold est attaché au méchant, défaussez des cartes du dessus du deck de rencontre jusqu'à un sbire, révélez ce "
             "sbire, et retirez 1 compteur de Darkspell de Darkhold. Sinon, cherchez Darkhold et révélez-le.",
}
# Les exemplaires multiples portent le texte de leur modele.
for n in (409, 410, 411, 412):
    FR["hf%d" % n] = ("Patrouille. Collaboration ([[Demon]]).\n<b>Réponse forcée</b> : après que Little Demon vous a attaqué et vous a infligé des dégâts, vous êtes désorienté.")
for n in (414, 415):
    FR["hf%d" % n] = FR["hf413"]
FR["hf417"] = FR["hf416"]


def bloc():
    lignes = [DEBUT + " — scénario 3 Black Queen + module Darkhold (Dipsome, préfixe hf, hf401-hf422, hf361-hf366)"]
    for k in sorted(FR):
        lignes.append("  %s: %s," % (json.dumps(k), json.dumps(FR[k], ensure_ascii=False)))
    lignes.append(FIN)
    return "\n".join(lignes) + "\n"


def main():
    with open("/tmp/cards_json.lock", "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        with open(CHEMIN, encoding="utf-8", newline="") as f:
            src = f.read()
        if DEBUT in src:
            i = src.index(DEBUT)
            j = src.index(FIN, i) + len(FIN)
            j = src.index("\n", j) + 1
            src = src[:i] + bloc() + src[j:]
        else:
            k = src.rstrip().rfind("}")
            src = src[:k] + bloc() + src[k:]
        with open(CHEMIN, "w", encoding="utf-8", newline="") as f:
            f.write(src)
        fcntl.flock(verrou, fcntl.LOCK_UN)
    print("textes FR :", len(FR))


main()
