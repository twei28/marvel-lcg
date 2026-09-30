/* Sélecteur d'interface partagé par les écrans V2.

   Le serveur pose `ui_version=v2` uniquement après validation de la clé du
   siège hôte du compte d'essai. Ce script ne donne aucun droit : il expose
   seulement la préférence à CSS et aux futurs points d'entrée V2.

   Chargé sans `defer` dans <head> pour que l'attribut existe avant le premier
   calcul de style et éviter un éclair de V1. */
(function () {
    "use strict";

    var v2 = document.cookie.split(";").some(function (morceau) {
        return morceau.trim() === "ui_version=v2";
    });
    if (v2) document.documentElement.dataset.uiVersion = "v2";
})();
