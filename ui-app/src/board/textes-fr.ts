// Genere par tools/importer_scans_fr.py — NE PAS EDITER A LA MAIN.
//
// Texte francais des cartes qui n'ont PAS de scan francais : c'est le seul
// cas ou le plateau l'affiche, sous l'apercu. Les cartes fan-made n'y sont
// pas, marvelcdb ne les connait pas.
//
// Le type dit « string | undefined » parce que la plupart des codes sont
// ABSENTS : sans cela le plateau croirait tenir un texte pour chaque carte.
export const TEXTES_FR: Readonly<Record<string, string | undefined>> = {
  '01043b': "<b>Action de héros</b> : résolvez la capacité \"<b>Spéciale</b>\" de chaque amélioration [[BLACK PANTHER]] que vous contrôlez, dans n'importe quel ordre. <i>(La résolution de chaque capacité est une étape de cette séquence.)</i>",
  '01043c': "<b>Action de héros</b> : résolvez la capacité \"<b>Spéciale</b>\" de chaque amélioration [[BLACK PANTHER]] que vous contrôlez, dans n'importe quel ordre. <i>(La résolution de chaque capacité est une étape de cette séquence.)</i>",
  '01043d': "<b>Action de héros</b> : résolvez la capacité \"<b>Spéciale</b>\" de chaque amélioration [[BLACK PANTHER]] que vous contrôlez, dans n'importe quel ordre. <i>(La résolution de chaque capacité est une étape de cette séquence.)</i>",
  '01144b': "<b>Une fois révélée</b> : chaque joueur met en jeu la carte du dessus de notre deck, face cachée, engagée avec lui en tant que sbire [[Drone]].\n\n[star] <b>Boost</b>: choisissez : soit vous dépensez une ressource [mental], soit vous mettez en jeu la carte du dessus de votre deck, face cachée, engagée avec vous en tant que sbire [[Drone]].",
  '01144c': "<b>Une fois révélée</b> : chaque joueur met en jeu la carte du dessus de notre deck, face cachée, engagée avec lui en tant que sbire [[Drone]].\n\n[star] <b>Boost</b>: choisissez : soit vous dépensez une ressource [physical], soit vous mettez en jeu la carte du dessus de votre deck, face cachée, engagée avec vous en tant que sbire [[Drone]].",
  '47007b': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si vous avez payé cette carte en utilisant 2 types de ressources différents, sonnez cet ennemi.",
  '47007c': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si vous avez payé cette carte en utilisant 2 types de ressources différents, sonnez cet ennemi.",
  '47008b': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous avez payé cette carte en utilisant 2 types de ressources différents, désorientez un ennemi.",
  '47008c': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous avez payé cette carte en utilisant 2 types de ressources différents, désorientez un ennemi.",
}
