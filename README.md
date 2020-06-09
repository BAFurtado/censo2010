# Geração População Artificial por Áreas de Ponderação Censo 2010 IBGE
This is just a documented script. We gather official data and use generator at 
https://github.com/BAFurtado/home_violence to come up with a random artificial population with gender, age and years 
of study at the level of census tracts.

It acquires data from Brazilian official statistics bureau (ibge.gov.br) and organizes the data for the format needed 
at https://github.com/BAFurtado/home_violence

1. We download census tract data
2. Extract information from tables
3. Output, organized by weighted areas, counting people by gender and age
4. Output as a single file

memoire-aide about handling large files with python

https://towardsdatascience.com/how-to-process-a-dataframe-with-billions-of-rows-in-seconds-c8212580f447

1. Numero people por idade por genero por AP

Still needs doing:
2. Percentual de anos de estudo por AP
3. Etnia
4. Salario da família