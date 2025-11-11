# Calculateur RSST - Évaluation de la Charge de Travail

## Description

Ce projet est un calculateur web interactif permettant d'évaluer la charge de travail physique selon les normes de la **Table RSST** (Réglementation Suisse de Sécurité au Travail). Il calcule le métabolisme et le travail moyen en fonction des activités effectuées, de leur position, du type de travail et de leur durée.

## Fonctionnalités

- **Ajout d'activités multiples** : Créez une liste d'activités avec leurs caractéristiques
- **Calcul automatique** : Calcul du métabolisme basal, de la sommation pondérée et du travail moyen
- **Classification RSST** : Classification automatique selon les normes RSST (Travail léger, moyen, lourd, très lourd)
- **Classification AIHA** : Classification détaillée selon les normes AIHA (American Industrial Hygiene Association)
- **Interface moderne** : Interface utilisateur intuitive avec thème sombre

## Utilisation

### Ouvrir l'application

Ouvrez simplement le fichier `RSSTcalculator.html` dans votre navigateur web. Aucune installation n'est requise.

### Ajouter une activité

1. **Titre de l'activité** (optionnel) : Donnez un nom à votre activité (ex: "Assemblage pièces")

2. **Position et mouvement du corps** : Sélectionnez la position :
   - Assis (18 kcal/h)
   - Debout (36 kcal/h)
   - Marche - Lente (120 kcal/h)
   - Marche - Normale (150 kcal/h)
   - Marche - Rapide (180 kcal/h)
   - Marche en montant (120 kcal/h + 48 kcal/h par mètre)

3. **Type de travail** : Sélectionnez le type d'effort :
   - Aucun travail supplémentaire
   - Travail léger/lourd impliquant la main, un bras, les deux bras ou le corps
   - Différents niveaux d'intensité (léger, moyen, lourd, très lourd)

4. **Durée** : Entrez la durée de l'activité en minutes ou en secondes

5. Cliquez sur **"Ajouter l'activité"**

### Consulter les résultats

Une fois des activités ajoutées, les résultats s'affichent automatiquement :

- **Métabolisme basal moyen** : 1 kcal/min (60 kcal/h)
- **Sommation pondérée moyenne (Σ)** : Moyenne pondérée de toutes les activités
- **Durée totale de la tâche** : Somme de toutes les durées
- **Travail moyen de la tâche** : Charge de travail moyenne en kcal/min

### Classification

L'application classe automatiquement votre travail selon deux systèmes :

#### Classification RSST (simplifiée)
- **Travail léger** : jusqu'à 3.3 kcal/min (200 kcal/h)
- **Travail moyen** : de 3.3 à 5.8 kcal/min (200 à 350 kcal/h)
- **Travail lourd** : de 5.8 à 8.3 kcal/min (350 à 500 kcal/h)
- **Travail très lourd** : > 8.3 kcal/min (> 500 kcal/h)

#### Classification AIHA (détaillée)
- **Repos (assis)** : 1.5 kcal/min
- **Travail très léger** : 1.6-2.5 kcal/min
- **Travail léger** : 2.5-5.0 kcal/min
- **Travail modéré** : 5.0-7.5 kcal/min
- **Travail lourd** : 7.5-10.0 kcal/min
- **Travail très lourd** : 10.0-12.5 kcal/min
- **Travail excessivement lourd** : > 12.5 kcal/min

## Calculs

### Métabolisme basal
Le métabolisme basal est fixé à **60 kcal/h** (1 kcal/min), représentant la quantité minimale d'énergie calorique dépensée lorsque le corps humain est au repos complet.

### Calcul du travail moyen
Pour chaque activité :
- **Métabolisme total** = Position + Type de travail + Métabolisme basal (60 kcal/h)
- **Conversion en kcal/min** = Métabolisme total / 60
- **Travail moyen** = Sommation pondérée (Σ) / Durée totale

La sommation pondérée est calculée comme suit :
```
Σ = Σ (kcal/min × durée en minutes) pour toutes les activités
```

## Gestion des activités

- **Supprimer une activité** : Cliquez sur le bouton "Supprimer" à côté de l'activité
- **Supprimer toutes les activités** : Cliquez sur "Supprimer toutes les activités"

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

## Notes importantes

- Les calculs sont basés sur les normes RSST (Réglementation Suisse de Sécurité au Travail)
- Le métabolisme basal de 60 kcal/h est une valeur standard pour un adulte moyen
- Les résultats sont donnés à titre indicatif et doivent être interprétés par un professionnel qualifié
- Pour des évaluations précises, consultez un ergonome ou un spécialiste en santé au travail

## Licence

Ce projet est fourni tel quel, sans garantie. Utilisez-le à vos propres risques.

