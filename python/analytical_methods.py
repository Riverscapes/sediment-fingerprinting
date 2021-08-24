### Temporary script to clean up Zhen's analytical methods

import sqlite3

o_path = "/Users/philip/GISData/Mississippi/MRB_pb_edits.db"
d_path = "/Users/philip/GISData/Mississippi/test5.sqlite"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

o_con = sqlite3.connect(o_path)
# o_con.row_factory = dict_factory
o_curs = o_con.cursor()


d_con = sqlite3.connect(d_path)
# d_con.row_factory = dict_factory
d_curs = d_con.cursor()

o_curs.execute("""select
  new_id,
  analytical_method_id,
  tracer_group,
  method_description,
  method_url
  from amt""")

d_curs.executemany("""insert into analytical_methods (
  analytical_method_id,
  analytical_method_name,
  tracer_group,
  method_description,
  method_url)
  values (?, ?, ?, ?, ?)""", o_curs.fetchall())

o_curs.execute("""select
  Data_Credit_ID,
  Credit_Type,
  Credit_URL,
  Credit_Contact,
  Access_Year,
  Access_Month
from data_credit""")

d_curs.executemany("""insert into data_credits (
  Data_Credit_ID,
  Credit_Type,
  Credit_URL,
  Credit_Contact,
  Access_Year,
  Access_Month
  ) values (?, ?, ?, ?, ?, ?)""", o_curs.fetchall())

o_curs.execute("""select Citation_ID,
       Contact_Lastname,
       Contact_Firstname,
       Contact_Email,
       Source_URL,
       Pub_Year,
       Pub_Month,
       Pub_Day,
       Type,
       Tracer_Select_Statistical_Test,
       Tracer_Select_Other,
       Correction_Organics,
       Correction_Grain_Size,
       Correction_Other,
       Apportionment_Models,
       Apportionment_Statistical_Test,
       Apportionment_Other
from citation""")

d_curs.executemany("""insert into citations (
  Citation_ID,
  Contact_Last_name,
  Contact_First_name,
  Contact_Email,
  Source_URL,
  Pub_Year,
  Pub_Month,
  Pub_Day,
  Type,
  Tracer_Select_Statistical_Test,
  Tracer_Select_Other,
  Correction_Organics,
  Correction_Grain_Size,
  Correction_Other,
  Apportionment_Models,
  Apportionment_Statistical_Test,
  Apportionment_Other)
  values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", o_curs.fetchall())

o_curs.execute("select category_id, category_type from sample_category")
d_curs.executemany("insert into sample_categories (category_id, category_type) values (?, ?)", o_curs.fetchall())


o_curs.execute("select tracer_type_id, tracer_type_name from tracer_types")
d_curs.executemany("insert into tracer_types (tracer_type_id, tracer_type_name) values (?, ?)", o_curs.fetchall())

o_curs.execute("""select Sample_ID,
       Citation_ID,
       DataCredit_ID,
       Category_ID,
       Location_Latitude,
       Location_Longitude,
       Location_Description,
       Drainage_sqkm,
       Sample_Type,
       Grain_Size_Range_µm,
       Grain_Size_Median_µm,
       Collection_Year,
       Collection_Month,
       Collection_Tool,
       Chronology_Year,
       Sampling_Period_Day,
       Created_Date,
       Updated_Date
from sample""")

d_curs.executemany("""insert into samples (
  Sample_ID,
  Citation_ID,
  Data_Credit_ID,
  Category_ID,
  Location_Latitude,
  Location_Longitude,
  Location_Description,
  Drainage_sq_km,
  Sample_Type,
  Grain_Size_Range_micro_m,
  Grain_Size_Median_micro_m,
  Collection_Year,
  Collection_Month,
  Collection_Tool,
  Chronology_Year,
  Sampling_Period_Day,
  Created_Date,
  Updated_Date) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", o_curs.fetchall())

d_curs.execute('select analytical_method_name, analytical_method_id from analytical_methods')
analytical_methods = {row[0]: row[1] for row in d_curs.fetchall()}

d_curs.execute('select tracer_type_name, tracer_type_id from tracer_types')
tracer_types = {row[0]: row[1] for row in d_curs.fetchall()}


o_curs.execute("select AnalyticalMethod_ID, sample_id, POC_pc, TOC_pc, TON_pc, Lignin_mg_100mgOC from tracer_organic")
for row in o_curs.fetchall():
  sample_id = int(row[1])
  analytical_method = row[0]
  analytical_method_id = analytical_methods[analytical_method]
  tracer_type_id = tracer_types['organic']

  new_data = [None if val == '' else val for val in row[1:]]


  d_curs.execute("insert into tracer_organic (Sample_ID, POC_pc, TOC_pc, TON_pc, Lignin_mg_100mgOC) values (?, ?, ?, ?, ?)", new_data)
  d_curs.execute("insert into sample_analytical_methods (sample_id, analytical_method_id, tracer_type_id) values (?, ?, ?)", [sample_id, analytical_method_id, tracer_type_id])

o_curs.execute("""
select AnalyticalMethod_ID,
       Sample_ID,
       Ag_mg_kg,
       Al_mg_kg,
       As_mg_kg,
       Au_ppb,
       B_mg_kg,
       Ba_mg_kg,
       Be_mg_kg,
       Bi_mg_kg,
       Br_mg_kg,
       Ca_mg_kg,
       Cd_mg_kg,
       Ce_mg_kg,
       Co_mg_kg,
       Cr_mg_kg,
       Cs_mg_kg,
       Cu_mg_kg,
       Dy_mg_kg,
       Er_mg_kg,
       Eu_mg_kg,
       Fe_mg_kg,
       Ga_mg_kg,
       Gd_mg_kg,
       Ge_mg_kg,
       Hf_mg_kg,
       Hg_mg_kg,
       Ho_mg_kg,
       In_mg_kg,
       K_mg_kg,
       La_mg_kg,
       Li_mg_kg,
       Lu_mg_kg,
       Mg_mg_kg,
       Mn_mg_kg,
       Mo_mg_kg,
       Na_mg_kg,
       Nb_mg_kg,
       Nd_mg_kg,
       Ni_mg_kg,
       P_mg_kg,
       Pb_mg_kg,
       Pd_mg_kg,
       Pr_mg_kg,
       Pt_mg_kg,
       Rb_mg_kg,
       Re_mg_kg,
       S_mg_kg,
       Sb_mg_kg,
       Sc_mg_kg,
       Se_mg_kg,
       Si_mg_kg,
       Sm_mg_kg,
       Sn_mg_kg,
       Sr_mg_kg,
       Ta_mg_kg,
       Tb_mg_kg,
       Te_mg_kg,
       Th_mg_kg,
       Ti_mg_kg,
       Tl_mg_kg,
       Tm_mg_kg,
       U_mg_kg,
       V_mg_kg,
       W_mg_kg,
       Y_mg_kg,
       Yb_mg_kg,
       Zn_mg_kg,
       Zr_mg_kg,
       Al2O3_ppm,
       CaO_ppm,
       Fe2O3_ppm,
       K2O_ppm,
       MgO_ppm,
       MnO_ppm,
       Na2O_ppm,
       P2O5_ppm,
       SiO2_ppm,
       TiO2_ppm
from tracer_inorganic""")

for row in o_curs.fetchall():
  sample_id = int(row[1])
  tracer_type_id = tracer_types['inorganic']
  new_data = [None if val == '' else val for val in row[1:]]

  d_curs.execute("""insert into tracer_inorganic (
       Sample_ID,
       Ag_mg_kg,
       Al_mg_kg,
       As_mg_kg,
       Au_ppb,
       B_mg_kg,
       Ba_mg_kg,
       Be_mg_kg,
       Bi_mg_kg,
       Br_mg_kg,
       Ca_mg_kg,
       Cd_mg_kg,
       Ce_mg_kg,
       Co_mg_kg,
       Cr_mg_kg,
       Cs_mg_kg,
       Cu_mg_kg,
       Dy_mg_kg,
       Er_mg_kg,
       Eu_mg_kg,
       Fe_mg_kg,
       Ga_mg_kg,
       Gd_mg_kg,
       Ge_mg_kg,
       Hf_mg_kg,
       Hg_mg_kg,
       Ho_mg_kg,
       In_mg_kg,
       K_mg_kg,
       La_mg_kg,
       Li_mg_kg,
       Lu_mg_kg,
       Mg_mg_kg,
       Mn_mg_kg,
       Mo_mg_kg,
       Na_mg_kg,
       Nb_mg_kg,
       Nd_mg_kg,
       Ni_mg_kg,
       P_mg_kg,
       Pb_mg_kg,
       Pd_mg_kg,
       Pr_mg_kg,
       Pt_mg_kg,
       Rb_mg_kg,
       Re_mg_kg,
       S_mg_kg,
       Sb_mg_kg,
       Sc_mg_kg,
       Se_mg_kg,
       Si_mg_kg,
       Sm_mg_kg,
       Sn_mg_kg,
       Sr_mg_kg,
       Ta_mg_kg,
       Tb_mg_kg,
       Te_mg_kg,
       Th_mg_kg,
       Ti_mg_kg,
       Tl_mg_kg,
       Tm_mg_kg,
       U_mg_kg,
       V_mg_kg,
       W_mg_kg,
       Y_mg_kg,
       Yb_mg_kg,
       Zn_mg_kg,
       Zr_mg_kg,
       Al2O3_ppm,
       CaO_ppm,
       Fe2O3_ppm,
       K2O_ppm,
       MgO_ppm,
       MnO_ppm,
       Na2O_ppm,
       P2O5_ppm,
       SiO2_ppm,
       TiO2_ppm
       ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", new_data)
  
  val_list = []
  if row[0] in analytical_methods:
    val_list.append(row[0])
  else:
    for raw in row[0].split(','):
      raw = raw.replace(' ', '')
      if ';' in raw:
        left = raw.split('-')[0]
        semis = raw.split(';')
        # add the first one
        val_list.append(semis[0])
        for semi in semis[1:]:
          val_list.append(left + '-' + semi)
      else:
        val_list.append(raw)

  for val in val_list:
    id = analytical_methods[val]
    d_curs.execute("insert into sample_analytical_methods (sample_id, analytical_method_id, tracer_type_id) values (?, ?, ?)", [sample_id, id, tracer_type_id])

o_curs.execute("""select
       AnalyticalMethod_ID,
       Sample_ID,
       "210Pb_pCi_g",
       "210Pbex_pCi_g",
       "7Be_mBq_g",
       "10Be_atoms_g",
       "137Cs_pCi_g",
       "226Ra_pCi_g",
       "238U_pCi_g",
       "238Pu_pCi_g",
       "239_240Pu_pCi_g",
       "212Bi_pCi_g",
       "214Bi_pCi_g",
       "212Pb_pCi_g",
       "214Pb_pCi_g",
       "228Ac_pCi_g",
       "40K_pCi_g"
from tracer_fallout_radionuclide""")
for row in o_curs.fetchall():
  sample_id = int(row[1])
  analytical_method = row[0]
  new_data = [None if val == '' else val for val in row[1:]]

  analytical_method_id = analytical_methods[analytical_method]
  tracer_type_id = tracer_types['fallout radionuclide']

  d_curs.execute("""INSERT into tracer_fallout_radionuclide (
    Sample_ID,
       "210Pb_pCi_g",
       "210Pbex_pCi_g",
       "7Be_mBq_g",
       "10Be_atoms_g",
       "137Cs_pCi_g",
       "226Ra_pCi_g",
       "238U_pCi_g",
       "238Pu_pCi_g",
       "239_240Pu_pCi_g",
       "212Bi_pCi_g",
       "214Bi_pCi_g",
       "212Pb_pCi_g",
       "214Pb_pCi_g",
       "228Ac_pCi_g",
       "40K_pCi_g") values (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", new_data)
  
  d_curs.execute("insert into sample_analytical_methods (sample_id, analytical_method_id, tracer_type_id) values (?, ?, ?)", [sample_id, analytical_method_id, tracer_type_id])

o_curs.execute('select AnalyticalMethod_ID, Sample_ID, TC_pc, TN_pc, C_N_Molar_Ratio from tracer_other')
for row in o_curs.fetchall():
  sample_id = int(row[1])
  analytical_method = row[0]
  analytical_method_id = analytical_methods[analytical_method]
  tracer_type_id = tracer_types['other']
  new_data = [None if val == '' else val for val in row[1:]]

  d_curs.execute('insert into tracer_other (Sample_ID, TC_pc, TN_pc, C_N_Molar_Ratio) values (?, ?, ?, ?)', new_data)
  d_curs.execute("insert into sample_analytical_methods (sample_id, analytical_method_id, tracer_type_id) values (?, ?, ?)", [sample_id, analytical_method_id, tracer_type_id])

o_curs.execute("""select
       AnalyticalMethod_ID, 
       Sample_ID,
       "87Sr_86Sr",
       "144Nd_143Nd",
       "206Pb_204Pb",
       "206Pb_207Pb",
       "206Pb_208Pb",
       "207Pb_204Pb",
       "208Pb_204Pb",
       D13C_permil,
       D15N_permil
from tracer_isotope""")

for row in o_curs.fetchall():
  sample_id = int(row[1])
  analytical_method = row[0]
  analytical_method_id = analytical_methods[analytical_method]
  tracer_type_id = tracer_types['isotope']
  new_data = [None if val == '' else val for val in row[1:]]


  d_curs.execute("""insert into tracer_isotope (
    Sample_ID,
    "87Sr_86Sr",
    "144Nd_143Nd",
    "206Pb_204Pb",
    "206Pb_207Pb",
    "206Pb_208Pb",
    "207Pb_204Pb",
    "208Pb_204Pb",
    D13C_permil,
    D15N_permil)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", new_data)

  d_curs.execute("insert into sample_analytical_methods (sample_id, analytical_method_id, tracer_type_id) values (?, ?, ?)", [sample_id, analytical_method_id, tracer_type_id])

d_con.commit()
print("got to here")
  




