# Vérification des traductions : aspects A et B (Aggression, Justice, Basic, Leadership)

Lot : `aspects_a.json` + `aspects_b.json`, 136 cartes (ua, uj, ub, ul). Fichier corrigé : `ui-app/src/board/textes-fr-fanmade.ts`.
Terminologie de référence : `textes-fr-complets.ts` (officielles), `aspects-decisions.md`. Le champ `en` du JSON suit déjà les décisions
de l'utilisateur (ex. uj002 « side scheme ») ; je l'ai pris comme référence, scans vérifiés seulement sur uj002 et ul041.

Bilan : 136 relues, 16 corrigées (17 corrections), 120 laissées.

## Corrections (id, nom : AVANT -> APRÈS, raison)

1. ua030 Nerve Strike : « Remise 1 » -> « Réduction 1 » : l'officiel (60023, 60026, 60027) dit « Réduction ».
2. ua014 Daitō : « personnage allié » -> « personnage ami » : « friendly character » = « personnage ami » dans les officielles (54 occurrences, 1 seule pour « allié »).
3. uj004 Cowabunga : « soignez 2 dégâts d'un personnage allié » -> « ... d'un personnage ami » : idem.
4. uj034 Turtle Line : « personnage allié » -> « personnage ami » : idem.
5. uj034 Turtle Line : « Usages (3 jetons Corde) » -> « Utilisations (...) » : « Uses » = « Utilisations » partout dans l'officiel.
6. uj022 Move in Shadow : « (<i>contre</i>) » -> « <i>(contre)</i> » et « <i>(y compris celle-ci</i>) » -> « <i>(y compris celle-ci)</i> » : parenthèses sorties de l'italique (l'anglais les a dedans ; le texte officiel 60027 avait la même coquille, reprise ici).
7. uj024 One Way or Another : « piochez 3 cartes <i>(Mélangez le deck Rencontre)</i> » -> « piochez 3 cartes. <i>(Mélangez le deck Rencontre.)</i> » : point oublié après la phrase, point final du rappel manquant.
8. ub027 Martial Arts Training : « Starting. (<i>Vous pouvez...</i>) » -> « Départ. <i>(Vous pouvez...)</i> » : mot-clé laissé en anglais ; l'officiel (60038 etc.) traduit « Départ » ; parenthèses dans l'italique.
9. ub017 Gofu Talisman : « le Talisman Gofu » -> « Gofu Talisman » : le titre de la carte reste en anglais à l'affichage.
10. ub021 Ingenuity : « inclinez Inventivité » -> « inclinez Ingenuity » : même raison (nom de la carte inventé en français, absent partout ailleurs).
11. uj037 Watch the Exits : « après qu'un sbire s'est engagé avec vous » -> « après qu'un sbire vous a engagé » : tournure officielle, et alignement avec ua021 (même déclencheur).
12. ua026 Leatherhead : « soignez-lui 2 dégâts » -> « soignez-le de 2 dégâts » : tournure officielle (« soignez-le de 3 dégâts »).
13. ul036 Turtle Titan : « soignez-lui 2 dégâts » -> « soignez-le de 2 dégâts » : idem.
14. ua040 Ujigami : « (Limite deux fois par round.) » -> « (Limite de deux fois par round.) » : forme officielle « Limite d'une fois par round ».
15. ub037 Pepperoni : « jetons pep » / « jeton pep » -> « Pep » : nom de jeton en majuscule initiale comme « jetons Charge », « jeton Rage ».
16. ul027 Sidekick : « devient votre "acolyte" » -> « est votre « acolyte » » : l'anglais dit « is your "sidekick" » (pas « devient ») ; guillemets français.
17. uj028 Screwloose : « subit -1 dégât consécutif » -> « subit 1 dégât consécutif de moins » : aligné sur ua003 (même formule anglaise « takes -1 consequential damage »).

Test `src/board/traduction` + `textes-fr-fanmade` : 31/31 passent après régénération (fichiers générés non commités).

## À trancher (laissés tels quels)

- **Compteur ou jeton** : l'officiel écrit « jeton X » partout. Le lot mélange : ua033 Pete « 3 compteurs pistolet », ua036 Ray Fillet « 2 compteurs munitions », ua040 Ujigami « 10 compteurs dague », ub037/ul006/ub044/ub048 « jeton(s) ». Le reste des cartes TMNT et fan-made emploie surtout « compteur » (anglais « counter »). Option A : tout en « jeton » (comme l'officiel) ; option B : tout en « compteur ». Touche aussi `compteurs-fr.ts` (ammo = « munition »).
- **uj016 / ua002 / ua025, listes à puces** : l'officiel écrit « choisissez :\n• Infligez ... » (majuscule, sans ponctuation) ; ua002 et ua025 écrivent « • infligez ... ; » (minuscule, point-virgule). uj016 et ub053 suivent l'officiel. Harmoniser ?
- **ul025 Shōgun, ul041 Mushroom** : le français recopie les coquilles imprimées « Shugun » et « Musroom » (question déjà ouverte, section C de `aspects-decisions.md`). Je propose de mettre le nom correct dans le français.
- **Articles devant des titres anglais** : « le Shell Phone » (ub044), « le Sky Wagon » (ub047), « le Turtle Lair » (ub057) alors que « Party Wagon », « Mutanimal Van », « Team-Building Exercise » n'ont pas d'article. Les titres restent anglais ; garder ou retirer l'article ?
- **ub032 Mutanimal Van** : « deal 1 facedown encounter card to a player » rendu par « attribuez 1 carte Rencontre face cachée à un joueur ». Je n'ai pas trouvé d'équivalent officiel (« distribuez » absent de `textes-fr-complets.ts`). Autre option : « donnez ».
- **uj038 Wingnut** : « dépensez les ressources suivantes [energy][energy] » ; l'officiel écrit « dépensez une ressource [energy] » ou « les ressources suivantes : ». Probablement acceptable.
- **uj022** : traits « [[Artiste martial]] ou [[espion]] » (casse copiée de l'officiel 60027, sans effet à l'affichage).
- **ub002 / ub034 / ub037** : « votre taille de main augmente de +1 » : « augmente de 1 » serait plus naturel, mais l'officiel dit la même chose (« augmente de +1 »).

## Coquilles de l'anglais relevées (non corrigées)

- ul025 « Shugun » (carte Shōgun), ul041 « Musroom » (carte Mushroom), ul031 « TIme » : déjà connues (section C).
- ub055 « reducing it's resource cost » (it's pour its).
- ul010 « Each of your TURTLE allies get » (accord : gets), « cost 1 fewer resource ».
- uj016 : « After you play Inspector Ishida » sans « it » (rien de faux).
- uj017 Know Your Enemy : « Remove 1 threat from a scheme. Remove 1 threat from a scheme. » (doublon repris de l'officielle 60023, voulu).
- ub019 : « Yōjimō » sur le scan (déjà décidé).

## Non vérifié

- Je n'ai pas relu les 136 scans un par un : le champ `en` du JSON a été pris comme texte imprimé (corrigé selon les décisions). Contrôle visuel fait seulement sur uj002 et ul041.
- Les traits FR (`traits-fr.ts`) : tous les traits du lot sans entrée (NINJA, MUTANIMAL, LION, RAT, PUNK, CONDITION, RONIN, GECKO...) restent identiques en français ; je n'ai pas pu confirmer cela sur marvelcdb FR (hors ligne). Aucun trait manifestement faux.
- Noms de compteurs de `compteurs-fr.ts` : non modifiés.
