
# SCRIPTS D'AIDE A L'INVESTISSEMENT FINANCIER


## Avertissements

Ces scripts Python ont pour but de résoudre le problème d'algorithmie proposé par OpenClassrooms dans le cadre du projet 7 de la formation Développeur Python.
Les scripts permettent de résoudre une variation du problème du sac à dos, où la solution d'investissement optimale doit être trouvée en prenant en compte les prix et les profits de différentex actions, dans la limite d'une somme maximum.

## Mise en place et exécution des scripts

1. Téléchargez le projet depuis Github. Soit directement (format zip), soit en clonant le projet en utilisant la commande suivante dans Git Bash :  
```
git clone <URL du repo>
```
2. Vous pouvez ensuite procéder à la création d'un environnement virtuel et à l'installation des requirements. (En l'occurence, les scripts ne nécessitant aucun requirements particuliers, ces 2 étapes n'est pas nécessaire.)
```
python -m venv <environment name>
```
Puis, toujours dans le terminal, activez votre environnement avec la commande suivante si vous êtes sous Linux :
```
source env/bin/activate
```
Ou bien celle-ci si vous êtes sous Windows
```
env/Scripts/activate.bat
```
3. Téléchargez les packages Python nécessaires à la bonne exécution du script à l'aide de la commande suivante :
```
pip install -r requirements.txt
```
4. Vous pouvez maintenant exécuter les scripts, soit à l'aide de l'IDE de votre choix, soit directement depuis le Terminal, à l'aide de commandes prenant la forme suivante :
```		
python script.py --arg1=valeur --arg2=valeur
```
Pour le script de force brute, les arguments sont le fichier en entrée et le fichier en sortie. Ainsi la commande peut être :
```		
python brute_force.py --in_file="../data/demo_dataset.csv" --out_file="results/brute_force_results.csv" 
```
Pour le script de Dynamic programing, les arguments sont le fichier en entrée et le fichier en sortie, et le traitement des données négatives. Ainsi la commande peut être :
```		
python dynamic_programing.py --in_file="../data/dataset1.csv" --out_file="results/dp_results.csv" --include_neg=True
```
Pour le script de Greedy Algorithm, les arguments sont le fichier en entrée et le fichier en sortie, et le traitement des données négatives. Ainsi la commande peut être :
```		
python greedy_algorithm.py --in_file="../data/dataset1.csv" --out_file="results/ga_results.csv" --include_neg=True
```





