# Calculateur Garg, Chaffin et Herrin

## Description

Ce projet est un calculateur web interactif permettant de calculer la dépense énergétique selon les **équations empiriques de Garg, Chaffin et Herrin (1978)**. Ces équations sont utilisées en ergonomie et en physiologie du travail pour évaluer la charge de travail physique lors de diverses activités manuelles.

## Fonctionnalités

- **31 équations implémentées** : Toutes les équations empiriques de Garg, Chaffin et Herrin (1978)
- **Calcul automatique** : Calcul de la dépense énergétique pour chaque mouvement et pour l'ensemble de la tâche
- **Paramètres personnalisables** : Poids corporel, sexe, VO2max, durée de la tâche
- **Gestion des positions** : Calcul basé sur le pourcentage de temps passé dans différentes positions
- **Tableau interactif** : Ajout, modification et suppression de tâches multiples
- **Résultats détaillés** : Affichage de la dépense énergétique en Kcal et en l O2/min, avec pourcentage du VO2max
- **Interface moderne** : Interface utilisateur intuitive avec thème sombre

## Utilisation

### Ouvrir l'application

Ouvrez simplement le fichier `Garg.html` dans votre navigateur web. Aucune installation n'est requise.

### Paramètres du sujet

Avant d'ajouter des tâches, configurez les paramètres du sujet :

1. **Poids du sujet (BW)** : Poids corporel en kilogrammes (ex: 80 kg)
2. **Sexe (S)** : 
   - Homme = 1
   - Femme = 0
3. **VO2max** : Consommation maximale d'oxygène en ml O2 / (Kg min)
   - Valeur typique : 30-50 ml O2/(Kg min)
4. **Durée de la tâche (t)** : Durée totale de la tâche en minutes
5. **Pourcentages de temps** :
   - % du temps en position assis
   - % du temps en position debout
   - % du temps en position debout-penché

### Ajouter une tâche

1. Cliquez sur **"Ajouter une tâche"**
2. Remplissez les champs :
   - **Description** : Nom de la tâche (optionnel)
   - **Technique** : Sélectionnez l'équation appropriée parmi les 31 disponibles
   - **Répétitions** : Nombre de fois que le mouvement est effectué
   - **Paramètres** : Selon l'équation choisie, remplissez les paramètres nécessaires :
     - **L** : Poids de la charge (Kg)
     - **F** : Force moyenne appliquée pour pousser ou tirer (Kg)
     - **DH** : Déplacement horizontal de la charge (m)
     - **h1** : Hauteur verticale des mains (basse) en mètres
     - **h2** : Hauteur verticale des mains (haute) en mètres
     - **G** : Inclinaison du plancher (%)
     - **t** : Durée en minutes (pour certaines équations)
     - **V** : Vitesse de marche (m/s)

3. Les résultats sont calculés automatiquement et affichés dans les colonnes "Kcal/mvt" et "Kcal total"

### Consulter les résultats

Les résultats s'affichent automatiquement dans la section "Résultats" :

- **Dépense énergétique associée aux mouvements** : Somme de toutes les dépenses énergétiques des mouvements
- **% du temps en position assis** : Dépense énergétique calculée selon le pourcentage de temps assis
- **% du temps en position debout** : Dépense énergétique calculée selon le pourcentage de temps debout
- **% du temps en position debout-penché** : Dépense énergétique calculée selon le pourcentage de temps debout penché
- **Dépense énergétique totale M** : Dépense énergétique totale en Kcal/min
- **Dépense énergétique totale M (l O2/min)** : Conversion en litres d'oxygène par minute
- **% du VO2max** : Pourcentage de la consommation maximale d'oxygène utilisée

## Équations disponibles

### Position du corps (kcal/min)
1. **Assis** : M = 0.023 × BW
2. **Debout** : M = 0.024 × BW
3. **Debout, penché** : M = 0.028 × BW

### Lever (kcal/lever)
4. **Squat** : Pour h₁ < h₂ ≤ 0.81
5. **Stoop** : Pour h₁ < h₂ ≤ 0.81
6. **Une main** : Pour h₁ < h₂ ≤ 0.81
7. **Bras** : Pour 0.81 < h₁ < h₂

### Baisser (kcal/baisser)
8. **Squat** : Pour h₁ < h₂ ≤ 0.81
9. **Stoop** : Pour h₁ < h₂ ≤ 0.81
10. **Bras** : Pour 0.81 < h₁ < h₂

### Marcher ou transporter (kcal)
11. **Sans charge** : ΔM = 10⁻² (51 + 2.54 BW × V² + 0.379 BW × G × V) × t
12. **Charge maintenue sur le côté** : ΔM = 10⁻² [80 + 2.43 BW × V² + 4.63 L × V² + 4.62 L + 0.379 (L+BW) G × V] × t
13. **Charge maintenue devant (cuisses ou ceinture)** : ΔM = 10⁻² [68 + 2.54 BW × V² + 4.08 L × V² + 11.4 L + 0.370 (L + BW) G × V] × t

### Maintenir (kcal)
14. **Charge sur le côté ou sur les cuisses (2 mains)** : ΔM = 0.037 × L × t
15. **Charge devant au niveau ceinture (2 mains)** : ΔM = 0.062 × L × t
16. **Charge (une main)** : ΔM = 0.088 × L × t

### Pousser / tirer (kcal/mouvement)
17. **Hauteur 0.8 m** : ΔM = 10⁻² × DH (0.112 × BW + 1.15 × F + 0.505 × S × F)
18. **Hauteur 1.5 m** : ΔM = DH (0.086 + 0.036 × F)

### Mouvement latéral des bras (kcal/mouvement)
19. **180° debout (2 mains)** : ΔM = 10⁻² (0.11 × BW + 0.726 × L)
20. **180° debout (1 main)** : ΔM = 10⁻² (0.097 × BW + 0.946 × L)
21. **90° debout (1 ou 2 mains)** : ΔM = 10⁻² (3.31 + 0.629 × L + 0.143 × S × L)
22. **90° assis (1 main)** : ΔM = 10⁻² (3.5 + 0.682 × L + 0.321 × S × L)
23. **90° assis (2 mains)** : ΔM = 10⁻² (2.54 + 1.1 × L + 0.248 × S × L)

### Mouvement avant / arrière des bras (kcal/mouvement)
24. **Assis (1 ou 2 mains)** : ΔM = 10⁻² × DH (6.3 + 2.71 × L)
25. **Debout (1 ou 2 mains)** : ΔM = 10⁻² × DH (3.57 + 1.23 × L)

### Travail général des membres supérieurs (kcal)
26. **Travail de la main Léger** : ΔM = 0.2 × t
27. **Travail de la main Lourd** : ΔM = 0.6 × t
28. **Travail d'un seul bras Léger** : ΔM = 0.7 × t
29. **Travail d'un seul bras Lourd** : ΔM = 1.5 × t
30. **Travail des deux bras Léger** : ΔM = 1.2 × t
31. **Travail des deux bras Lourd** : ΔM = 2.2 × t

## Paramètres de calcul

| Paramètre | Description | Unité |
|-----------|-------------|-------|
| **BW** | Poids corporel | Kg |
| **F** | Force moyenne appliquée pour pousser ou tirer | Kg |
| **G** | Inclinaison du plancher | % |
| **h1** | Hauteur verticale des mains (basse) | m |
| **h2** | Hauteur verticale des mains (haute) | m |
| **L** | Poids de la charge | Kg |
| **S** | Sexe (homme = 1, femme = 0) | - |
| **V** | Vitesse de marche | m/s |
| **DH** | Déplacement horizontal de la charge | m |
| **t** | Durée | minutes |

## Gestion des tâches

- **Ajouter une tâche** : Cliquez sur "Ajouter une tâche"
- **Modifier une tâche** : Modifiez directement les valeurs dans le tableau
- **Supprimer une tâche** : Cliquez sur le bouton "Suppr." à côté de la tâche
- **Réinitialiser** : Cliquez sur "Réinitialiser" pour supprimer toutes les tâches

## Calculs

### Dépense énergétique des mouvements
Pour chaque tâche, la dépense énergétique par mouvement est calculée selon l'équation sélectionnée, puis multipliée par le nombre de répétitions.

### Dépense énergétique des positions
Les dépenses énergétiques des positions (assis, debout, debout-penché) sont calculées selon les pourcentages de temps spécifiés :
- Dépense position = (Équation position × durée totale × % temps) / 100

### Dépense énergétique totale
La dépense énergétique totale en Kcal/min est calculée comme suit :
```
M total = (Dépense mouvements + Dépense positions) / Durée totale
```

### Conversion en l O2/min
La conversion utilise le facteur : 1 Kcal/min ≈ 0.208 l O2/min

### Pourcentage du VO2max
```
% VO2max = (Dépense en l O2/min / VO2max en l O2/min) × 100
```
où VO2max en l O2/min = VO2max (ml O2/(Kg min)) × BW (Kg) / 1000

## Technologies utilisées

- HTML5
- CSS3 (avec thème sombre moderne)
- JavaScript (vanilla, sans dépendances)

## Compatibilité

L'application fonctionne sur tous les navigateurs web modernes :
- Chrome
- Firefox
- Edge
- Safari
- Opera

## Références

Garg, A., Chaffin, D. B., & Herrin, G. D. (1978). Prediction of metabolic rates for manual materials handling jobs. *American Industrial Hygiene Association Journal*, 39(8), 661-674.

## Notes importantes

- Les calculs sont basés sur les équations empiriques de Garg, Chaffin et Herrin (1978)
- Les équations sont valides pour des conditions spécifiques (voir les contraintes dans les descriptions)
- Les résultats sont donnés à titre indicatif et doivent être interprétés par un professionnel qualifié
- Pour des évaluations précises, consultez un ergonome ou un spécialiste en santé au travail
- Certaines équations ont des contraintes sur les hauteurs (h₁ < h₂ ≤ 0.81 ou 0.81 < h₁ < h₂) - respectez ces contraintes pour des résultats valides

## Licence

Ce projet est fourni tel quel, sans garantie. Utilisez-le à vos propres risques.

