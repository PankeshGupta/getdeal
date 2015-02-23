"use strict";

(function($){
	// Module permettant la filtration des deals
	var filtrationDeal = {

		filtres: $("ul.nav-filtration li > a.slide-plug"), // Tous les liens déclencheurs du déroulement des sous-menus
		listeInputs: $('.categories-filtres li input'), // Toutes les "checkboxes" des catégories "voyages, High-tech....."
		controleurPlugin: $("#controleur-plugin i"), // Les trois icônes du haut + - & reset
		linkCocherDecocher: $("#control-select a"), // les liens Tout cocher/ Tout décocher
		resetActive: false, // Si l'utilisateur a cliqué sur le bouton reset

		// Objet contenant les valeurs initiales de tous les tous les filtres (servant à l'appel AJAX)
		initialValue: {
			"check-beaute": 1, // 1 <=> (équivaut) la checkbox est active
			"check-restauration": 1,
			"check-shopping": 1,
			"check-voyage": 1,
			"check-sorties-losiris": 1,
			"check-high-tech": 1,
			score: 70,
			minPrice: 100,
			maxPrice: 700,
			reduction: 46,
			destination: 'all'
		},// Fin objet contenant les valeurs initiales de tous les tous les filtres (servant à l'appel AJAX)


		// Toutes les catégories ("Attribut servant à mettre à jour l'objet: (@obj initialValue)  plus tard
		categoriesName: ["check-beaute", "check-restauration", "check-shopping", "check-voyage", "check-sorties-losiris", "check-high-tech"],// Fin // Toutes les catégories ("Attribut servant à mettre à jour l'objet: (@obj initialValue)  plus tard


		// Les déclencheurs des sliders
		sliderScore: $("#slide-score"),
		sliderPrix: $("#slide-prix"),
		sliderReduction: $("#slide-reduction"),// Fin les déclencheurs des sliders

		// Initialisateur du module
		init: function() {
			this.initialValueModified = $.extend({}, this.initialValue); // @attr : copie superficielle des valeurs initiales de l'objet: (@obj initialValue); Ce dernier sera utilisé lors du reset
			this.iconFiltresExpand = this.filtres.children("span");	 // @attr : Toutes les icônes (plus, minus) de chaque filtre
			this.initialiseSlider(); // Appel de la méthode initialiseSlider pour initialiser les sliders
			this.filtres.on("click", this.slideTog); // Gestionnaire de clic sur les les liens déclencheurs du déroulement des sous-menus
			this.initialiserCheckbox();	// Initialiser les checkbox (plugin iCheck)
			this.controleurPlugin.on("click", this.gestionClicControleur); // Gestionnaire de clic sur les trois icônes du haut + - & reset
			this.linkCocherDecocher.on("click", this.majAllCheckedUnchekced); // Gestionnaire de clic sur les checkboxes des catégories

			// S'il y'a des voyages càd le menu  Destination est affiché
			if ($('#conteneur-destination').length !== 0) {
    			this.caretBoutonDest = $("#caret-destination"); // @attr La flèche en bas
    			this.boutonDest = $("#caret-destination").prev(); // @attr Le bouton
    			this.destinationsVoyages = $("#destination-voyages a"); // @attr les liens des destinations Londres, Mardrid....
    			this.destinationsPresentes = true; // @attr la zone destination existe càd des voyages existent dans la bdd
    			this.destinationsVoyages.on("click", this.clicLiensDestination);
			} else {
				this.destinationsPresentes = false;
			} // Fin s'il y'a des voyages càd le menu  Destination est affiché
		},// Fin  initialisateur du module


		// slideUp / slideDown
		slideTog: function(e) {
			e.preventDefault();

			var fD = filtrationDeal,
				$this = $(this),
				divDropDown = $this.next(),
				clicAux;

			if (! divDropDown.is(':visible') ) {
				$this.next().slideDown(200, function() {
					clicAux = false;
					fD.setIconAfterClic($this.children("span"), clicAux);
				});
			} else {
				$this.next().slideUp(200, function() {
					clicAux = true;
					fD.setIconAfterClic($this.children("span"), clicAux);
				});
			}

		}, // Fin slideUp / slideDown


		// Reset module
		resetAll: function() {

			filtrationDeal.listeInputs.off("ifChecked").iCheck('check')
									.on("ifChecked", filtrationDeal.majInitValObjCheck);

			filtrationDeal.resetActive = true; // L'utilisateur a cliqué sur le bouton Reset

			filtrationDeal.sliderScore.slider( "value", 70);
			filtrationDeal.sliderReduction.slider( "value", 46);
			filtrationDeal.sliderPrix.slider( "values", [ 100, 700 ] );

			filtrationDeal.resetActive = false; // Ré-initialiser

			if (filtrationDeal.destinationsPresentes) {
				filtrationDeal.enableButtonDestination();
			}


			filtrationDeal.getDataWithAjax(filtrationDeal.initialValue);

			this.initialValueModified = $.extend({}, this.initialValue); // Ré-initialiser l'objet servant à Ajax

		}, // Fin reset Module


		// Gestionnaire des clics sur +, - et Reset
		gestionClicControleur: function(e) {
			var $targetClick = $(e.target);
			var fD = filtrationDeal;
			if ($targetClick.is('.icon-minus') ) {
				fD.slideUpAll();
			} else if ($targetClick.is('.icon-plus') ) {
				fD.slideDownAll();
			} else {
				fD.resetAll();

			}
		}, // Fin gestionnaire des clics sur +, - et Reset


		// Activer le bouton destination s'il existe
		enableButtonDestination: function() {
			filtrationDeal.caretBoutonDest.removeAttr("disabled"); // On supprime l'état disabled
			filtrationDeal.boutonDest.removeAttr("disabled"); // On supprime l'état disabled
			filtrationDeal.majInitValDestination("all");
		}, // Fin activer le bouton destination s'il existe


		// Désactiver le bouton destination s'il existe
		disableButtonDestination: function() {
			filtrationDeal.caretBoutonDest.attr("disabled", "disabled"); // On ajoute l'état disabled
			filtrationDeal.boutonDest.attr("disabled", "disabled"); // On ajoute l'état disabled
			filtrationDeal.majInitValDestination("none");
		}, // Fin désactiver le bouton destination s'il existe


		// Gestionnaire des clics sur les liens de destination Londres, Madrid....
		clicLiensDestination: function(e) {
			e.preventDefault();
			filtrationDeal.majInitValDestination(this.id); 	// this fait référence au lien cliqué
			filtrationDeal.getDataWithAjax(filtrationDeal.initialValueModified);
		},// Fin Gestionnaire des clics sur les liens de destination Londres, Madrid....



		// Initialiser les Sliders
		initialiseSlider: function() {
			var that = this;
			this.sliderScore.slider({
				orienation: 'horizontal',
				min: 0,
			    max: 100,
				range: "min",
				animate: true,
				value: 70,
				create: function (e, ui) {
					that.labelScore = $("<span class='label-value-slide'>70%</span>"); // La valeur initiale
        			that.sliderScore.children(".ui-slider-handle:first").append(that.labelScore);
        		},
        		slide: function (e, ui) {
        			that.setLabelValue(that.labelScore, ui.value, '%');
    			},
    			change: function(e, ui) {
    				that.majInitValObjScore(ui.value);
    				that.setLabelValue(that.labelScore, ui.value, '%');
    			}

    		});
			this.sliderPrix.slider({
				orienation: 'horizontal',
				min: 10,
			    max: 1000,
			    values: [ 100, 700 ],
			    animate: true,
				range: true,
				create: function (e, ui) {
					that.labelPrixMin = $("<span class='label-value-slide'>100</span>"); // La valeur initiale
        			that.sliderPrix.children("a:first").append(that.labelPrixMin);
        			that.labelPrixMax = $("<span class='label-value-slide'>700</span>"); // La valeur initiale
        			that.sliderPrix.children(".ui-slider-handle").eq(1).append(that.labelPrixMax);
        		},
        		slide: function (e, ui) {
        			that.setLabelValuesPrice(that.labelPrixMin, that.labelPrixMax, ui.values, 'Dhs');
    			},
    			change: function(e, ui) {
    				that.majInitValObjPrix(ui.values);
    				that.setLabelValuesPrice(that.labelPrixMin, that.labelPrixMax, ui.values, 'Dhs');
    			}
			});
			this.sliderReduction.slider({
				orienation: 'horizontal',
				min: 0,
			    max: 100,
			    value: 46,
				range: "min",
				animate: true,
				create: function (e, ui) {
					that.labelReduction = $("<span class='label-value-slide'>46%</span>"); // La valeur initiale
        			that.sliderReduction.children(".ui-slider-handle:first").append(that.labelReduction);
        		},
        		slide: function (e, ui) {
        			that.setLabelValue(that.labelReduction, ui.value, '%');
    			},
    			change: function(e, ui) {
    				that.majInitValObjReduction(ui.value);
    				that.setLabelValue(that.labelReduction, ui.value, '%');
    			}
			});
		}, // Fin Initialiser les Sliders


		// Initialiser les Checkboxes des catégories
		initialiserCheckbox: function() {
			this.listeInputs.iCheck({
	    		checkboxClass: 'icheckbox_square'
			}).on("ifChecked", filtrationDeal.majInitValObjCheck)
			  .on("ifUnchecked", filtrationDeal.majInitValObjUncheck);
		},// Fin initialiser les Checkboxes des catégories


		// Set + ou -
		setIconAfterClic: function($spanIcon, clicSurLuimeme) {
			if (! clicSurLuimeme) {
				$spanIcon.attr("class", "icon-minus");
			} else {
				$spanIcon.attr("class", "icon-plus");
			}
		},// Fin set + ou -


		// Set + ou - pour le controleur du haut
		majIconPlusMinusAll: function(signe) {
			if (signe === "-") {
				this.iconFiltresExpand.attr("class", "icon-plus");
			} else {
				this.iconFiltresExpand.attr("class", "icon-minus");
			}
		},// Fin set + ou - pour le controleur du haut



		// slideDownAll
		slideDownAll: function() {
			filtrationDeal.filtres.next().slideDown(200, function() {
				filtrationDeal.majIconPlusMinusAll("+");
			});
		}, // Fin // slideDownAll


		// slideUpAll
		slideUpAll: function() {
			filtrationDeal.filtres.next().slideUp(200, function() {
				filtrationDeal.majIconPlusMinusAll("-");
			});
		}, // Fin slideUpAll


		// Mettre à jour les étiquettes du slider score & réduction
		setLabelValue: function(label, value, unite) {
			label.text(value + ' ' + unite)
		}, // Fin Mettre à jour les étiquettes du slider score & réduction


		// Mettre à jour l'étiquette du slider Tranche du prix
		setLabelValuesPrice: function(labelMin, labelMax, values, unite) {
			labelMin.text(values[0] + ' ');
			labelMax.text(values[1] + ' ');
		}, // Fin Mettre à jour l'étiquette du slider Tranche du prix


		/*=============Partie Maj de l'objet servant à Ajax ==================
		  ===================================================================*/

		majInitValObjScore: function(newValue) {
			if (!filtrationDeal.resetActive) {
				filtrationDeal.initialValueModified.score = newValue;
				filtrationDeal.getDataWithAjax(filtrationDeal.initialValueModified);
			}
		},

		majInitValDestination: function(newValue) {
			filtrationDeal.initialValueModified.destination = newValue;
		},


		majInitValObjPrix: function(newValues) {
			if (!filtrationDeal.resetActive) {
				filtrationDeal.initialValueModified.minPrice = newValues[0];
				filtrationDeal.initialValueModified.maxPrice = newValues[1];
				filtrationDeal.getDataWithAjax(filtrationDeal.initialValueModified);
			}
		},

		majInitValObjReduction: function(newValue) {
			if (!filtrationDeal.resetActive) {
				filtrationDeal.initialValueModified.reduction = newValue;
				filtrationDeal.getDataWithAjax(filtrationDeal.initialValueModified);
			}
		},


		majInitValObjCheck: function() {
			filtrationDeal.initialValueModified[this.id] = 1;
			if (this.id === "check-voyage") {
				if (filtrationDeal.destinationsPresentes) {
					filtrationDeal.enableButtonDestination();
				}
			}
			filtrationDeal.getDataWithAjax(filtrationDeal.initialValueModified);
		},

		majInitValObjUncheck: function() {
			filtrationDeal.initialValueModified[this.id] = 0;
			if (this.id === "check-voyage") {
				if (filtrationDeal.destinationsPresentes) {
					filtrationDeal.disableButtonDestination();
				}
			}
			filtrationDeal.getDataWithAjax(filtrationDeal.initialValueModified);
		},


		// Gestion des lien tout cocher/ tou décocher
		majvalInitObjCat: function(checkUnchek) {
			var i;
			if (checkUnchek === 1) {
				for (i=0; i<filtrationDeal.categoriesName.length; i++) {
					filtrationDeal.initialValueModified[ filtrationDeal.categoriesName[i] ] = 1;
				}

				if (filtrationDeal.destinationsPresentes) {
					filtrationDeal.enableButtonDestination();
				}

			} else {
				for (i=0; i<filtrationDeal.categoriesName.length; i++) {
					filtrationDeal.initialValueModified[ filtrationDeal.categoriesName[i] ] = 0;
				}

				if (filtrationDeal.destinationsPresentes) {
					filtrationDeal.disableButtonDestination();
				}
			}
			filtrationDeal.getDataWithAjax(filtrationDeal.initialValueModified);

		},


		majAllCheckedUnchekced: function(e) { // Callback de "Tout cocher/Tout décocher"
			var $this =  $(this);
			if ($this.attr("class") === "tout-cocher") {
				filtrationDeal.listeInputs
										.off("ifChecked").iCheck('check')
										.on("ifChecked", filtrationDeal.majInitValObjCheck);
				filtrationDeal.majvalInitObjCat(1);

			} else {
				filtrationDeal.listeInputs
										.off("ifUnchecked").iCheck('uncheck')
										.on("ifUnchecked", filtrationDeal.majInitValObjUncheck);
				filtrationDeal.majvalInitObjCat(0);
			}
			e.preventDefault();
		}, // Fin Gestion des lien tout cocher/ tou décocher
		 //=============Fin Partie Maj de l'objet servant à Ajax ==================



		 // Obtenir les données avec Ajax Enfin :P !
		 getDataWithAjax: function(objParam) {
		 	console.log(objParam)
		 }


	};

	filtrationDeal.init(); // Initialisation du module Filtration des deals
})(jQuery);
