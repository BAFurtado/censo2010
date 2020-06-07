import os
import pandas as pd


folder = r'\\sasworkspace1\publico\Bernardo Alves Furtado (Dirur)\Censo 2010\Amostra'
# OLD FILES

p2 = r'\\storage6\bases2\NINSOC\Bases\Censo_Demografico\2010\Agregados_por_Setores_Censitarios'
p3 = r'\AC_20171016\AC\Base informaçoes setores2010 universo AC\CSV'
files = os.listdir(os.path.join(p2, p3))

# Got the folder with the files, now, get the correct questions.
dom_files = [f for f in files if f.startswith('dom_')]
pes_files = [f for f in files if f.startswith('pes')]
