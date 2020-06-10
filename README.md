## Dados para Geração População Artificial por Áreas de Ponderação Censo 2010 IBGE

This is just a documented script. We gather official data and use generator at 
https://github.com/BAFurtado/home_violence to come up with a random artificial population with gender, age and years 
of study and color at the level of census tracts.

It acquires data from Brazilian official statistics bureau (ibge.gov.br) and organizes the data for the format needed 
at https://github.com/BAFurtado/home_violence

1. We download census tract data and sampled weighted areas data 
2. Extract information from tables and from text-like data (pd.read_fwf)
3. Output, organized by weighted areas, counting people by gender and age, by qualification status
4. Output as a single files, for both

#### This is all restricted to metropolitan areas of interest (ACPs, IBGE/2015)

memoire-aide about handling large files with python (not used here, though)

https://towardsdatascience.com/how-to-process-a-dataframe-with-billions-of-rows-in-seconds-c8212580f447

1. Numero pessoas por idade por genero por AP
2. Percentual de grau de instrução por AP
3. Cor por AP
4. Salario da família (média, variância)
5. Número médio pessoas na família (média, variância)