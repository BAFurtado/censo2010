### Geração Famílias Artificiais por Áreas de Ponderação Censo 2010 IBGE

### Áreas de ponderação do IBGE, dissolvidos dos setores censitários originais. Completa

#### This repository downloads data from Brazilian census 2010, including census tracts. 
#### Then, it generates artificial populations by census block (which are constructed from original sectors)

## Objeto

1. Este repositório gera dados de população artificial, a partir dos dados do censo 2010.
2. Adicionalmente, contém as funcionalidades para 
    
    2.1 Download, extração e junção dos shapes de setores censitários de todas as UFs, e os une (dissolve) 
    por áreas de ponderação.
    
    2.2 Os resultados são apresentados apenas para as 46 Áreas de Concentração de População do IBGE. 
    Porém, as funcionalidades para gerar populações para qualquer município também esté presente. 
    Para fazê-lo, comente a linha #53 do arquivo `sectors_into_APs.py`
    
    2.3 Os dados estão separados por código de uf. O código porém também gera o Brasil completo 72 MB.
 
Originally, this was constructed to be used at https://github.com/BAFurtado/home_violence. 
However, it might be useful on its own.

####  Cite as: Furtado, Bernardo Alves (2020). Gerando Famílias Artificiais Intraurbanas: censo 2010. Brasília, Ipea.

## Output

1. pandas.DataFrame com um indivíduo por linha, contendo:

    a. AREAP: área de ponderação
    
    b. gender
    
    c. age
    
    d. years_study (anos de instrução)
    
    e. color
    
    f. salário 
    
    g. category (se criança ou adulto e genero) 
    
2. Adicionalmente, uma lista de listas contendo os **indexes** do DataFrame de indivíduos referentes às famílias de 
cada um. 


# How to run

1. `clone` the repository 
2. `import generator`
3. Create a `dict` that includes at least


    metro = 'CAMPINAS'
    params = dict()
    params['PROCESSING_ACPS'] = [metro]
    params['INITIAL_FAMILIES'] = 1000
    params['DATA_YEAR'] = 2010
    people, families = generator.main(params)`


##### Possible metropolises include:

`
metropolis = ["MANAUS", "BELEM", "MACAPA", "SAO LUIS", "TERESINA", "FORTALEZA", "CRAJUBAR", "NATAL", "JOAO PESSOA",
              "CAMPINA GRANDE", "RECIFE", "MACEIO", "ARACAJU", "SALVADOR", "FEIRA DE SANTANA",
              "ILHEUS - ITABUNA", "PETROLINA - JUAZEIRO", "BELO HORIZONTE", "JUIZ DE FORA", "IPATINGA", "UBERLANDIA",
              "VITORIA", "VOLTA REDONDA - BARRA MANSA", "RIO DE JANEIRO", "CAMPOS DOS GOYTACAZES", "SAO PAULO",
              "CAMPINAS", "SOROCABA", "SAO JOSE DO RIO PRETO", "SANTOS", "JUNDIAI", "SAO JOSE DOS CAMPOS",
              "RIBEIRAO PRETO", "CURITIBA", "LONDRINA", "MARINGA", "JOINVILLE", "FLORIANOPOLIS", "PORTO ALEGRE",
              "NOVO HAMBURGO - SAO LEOPOLDO", "CAXIAS DO SUL", "PELOTAS - RIO GRANDE", "CAMPO GRANDE", "CUIABA",
              "GOIANIA", "BRASILIA"]`