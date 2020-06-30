import generator
import geopandas as gpd
import os


def main(ppl, fams, shp):
    db = dict()
    for f in fams:
        for j, i in enumerate(f):
            ppl.loc[i, 'family'] = j + 1
    db['females_c'] = ppl.loc[ppl.gender == 'female', :].groupby('AREAP')['gender'].agg('count').reset_index()
    db['males_c'] = ppl.loc[ppl.gender == 'male', :].groupby('AREAP')['gender'].agg('count').reset_index()
    db['age_study_wage_mean'] =  ppl.groupby('AREAP')[['age', 'years_study', 'wage']].agg('mean').reset_index()
    db['num_families_mean'] = ppl.groupby('AREAP')['family'].agg('mean').reset_index()
    db['children'] = ppl.loc[ppl.category == 'child', :].groupby('AREAP')['category'].agg('count').reset_index()

    file = r'\\storage1\carga\modelo dinamico de simulacao\aps_violence'
    for key in db:
        db[key] = shp.merge(db[key], on='AREAP')
        db[key].to_file(os.path.join(file, f'{key}.shp'))
    return db


if __name__ == '__main__':
    metro = 'CAMPINAS'
    # Necessary parameters to generate data
    prms = dict()
    prms['PROCESSING_ACPS'] = [metro]
    prms['INITIAL_FAMILIES'] = 2500
    prms['DATA_YEAR'] = 2010
    people, families = generator.main(prms)
    shape = gpd.read_file('data/areas/35.shp')
    final_shps = main(people, families, shape)
