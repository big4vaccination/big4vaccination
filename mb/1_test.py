

data1 = [('DTaP', '18 months', 'Diphtheria and tetanus toxoid with acellular pertussis vaccine'), ('DTaPHibHepBIPV', '2 4 6 months', 'Hexavalent diphtheria tetanus toxoid with acellular pertussis Hib hepatitis B and IPV vaccine'), ('DTaPIPV', '4 years', 'Diphtheria and tetanus toxoid with acellular pertussis and IPV vaccine'), ('HepA_Pediatric', '12 18 months', 'Hepatitis A pediatric dose vaccine'), ('HepB_Pediatric', 'birth', 'Hepatitis B pediatric dose vaccine'), ('HIB', '18 months', 'Haemophilus influenzae type b vaccine'), ('HPV', '12-13 years', 'Human Papillomavirus vaccine'), ('Influenza_Adult', '>=65 years', 'Influenza adult dose vaccine'), ('Influenza_Pediatric', '>=6 months', 'Influenza pediatric dose vaccine'), ('MenACWY-135 conj', '12 months', 'Meningococcal ACWY-135 conjugate vaccine'), ('MMR', '12 months', 'Measles mumps and rubella vaccine'), ('MMRV', '18 months', 'Measles mumps rubella and varicella vaccine'), ('Pneumo_conj', '2 4 6 12 months', 'Pneumococcal conjugate vaccine'), ('Pneumo_ps', '>= 65 years', 'Pneumococcal polysaccharide vaccine'), ('Rotavirus', '2 4 months', 'Rotavirus vaccine'), ('Tdap', '12-13 years', 'Tetanus and diphtheria toxoids and acellular pertussis vaccine'), ('Zoster', '70 71-79 years', 'Varicella vaccine')]
push_data = [{}]

for i in data1:
	print(i)
for i in len(data1):
	print(i)
	push_data[i]["Vaccine Code"] = data1[i][0]
	push_data[i]["AU Schedule"] = data1[i][1]
	push_data[i]["Description"] = data1[i][2]

