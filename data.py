import pandas as pd
import re

df = pd.read_csv('crimedata.csv')
suffixes = ['township', 'city', 'borough', 'village']
racePop = ['blackPop', 'whitePop', 'asianPop', 'hispanicPop']
crimes = ['murders', 'rapes', 'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons']

df = df.fillna(0)
df['blackPop'] = df['population'] * df['racepctblack'] / 100
df['whitePop'] = df['population'] * df['racePctWhite'] / 100
df['asianPop'] = df['population'] * df['racePctAsian'] / 100
df['hispanicPop'] = df['population'] * df['racePctHisp'] / 100


column = []
for t in df.communityName:
    result = re.findall(r'(town|township|city|borough|village)', t)
    if len(result) == 0:
        result = '-'
    else:
        result = result[0]
    column.append(result)

ty = pd.Series(column)


df['typeC'] = ty

for suffix in suffixes:
    df['communityName'] = df['communityName'].str.replace(suffix, '')

townsPerSt = df[df['typeC'] == 'town'].groupby('state')[
    'blackPop', 'whitePop', 'asianPop', 'hispanicPop', 'population', 'murders', 'rapes', 'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons', 'ViolentCrimesPerPop', 'nonViolPerPop', 'medIncome', 'perCapInc', 'NumUnderPov'].aggregate(
    'sum').reset_index()

citiesPerSt = df[df['typeC'] == 'city'].groupby('state')[
    'blackPop', 'whitePop', 'asianPop', 'hispanicPop', 'population', 'murders', 'rapes', 'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons', 'ViolentCrimesPerPop', 'nonViolPerPop', 'medIncome', 'perCapInc', 'NumUnderPov'].aggregate(
    'sum').reset_index()

boroughsPerSt = df[df['typeC'] == 'borough'].groupby('state')[
    'blackPop', 'whitePop', 'asianPop', 'hispanicPop', 'population', 'murders', 'rapes', 'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons', 'ViolentCrimesPerPop', 'nonViolPerPop', 'medIncome', 'perCapInc', 'NumUnderPov'].aggregate(
    'sum').reset_index()

villagesPerSt = df[df['typeC'] == 'village'].groupby('state')[
    'blackPop', 'whitePop', 'asianPop', 'hispanicPop', 'population', 'murders', 'rapes', 'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons', 'ViolentCrimesPerPop', 'nonViolPerPop', 'medIncome', 'perCapInc', 'NumUnderPov'].aggregate(
    'sum').reset_index()

PerSt = df.groupby('state')[
    'blackPop', 'whitePop', 'asianPop', 'hispanicPop', 'population', 'murders', 'rapes', 'robberies', 'assaults', 'burglaries', 'larcenies', 'autoTheft', 'arsons', 'ViolentCrimesPerPop', 'nonViolPerPop', 'medIncome', 'perCapInc', 'NumUnderPov'].aggregate(
    'sum').reset_index()

townsPerSt[
    'overall'] = townsPerSt.murders + townsPerSt.rapes + townsPerSt.robberies + townsPerSt.assaults + townsPerSt.burglaries + townsPerSt.larcenies + townsPerSt.autoTheft + townsPerSt.arsons
citiesPerSt[
    'overall'] = citiesPerSt.murders + citiesPerSt.rapes + citiesPerSt.robberies + citiesPerSt.assaults + citiesPerSt.burglaries + citiesPerSt.larcenies + citiesPerSt.autoTheft + citiesPerSt.arsons
boroughsPerSt[
    'overall'] = boroughsPerSt.murders + boroughsPerSt.rapes + boroughsPerSt.robberies + boroughsPerSt.assaults + boroughsPerSt.burglaries + boroughsPerSt.larcenies + boroughsPerSt.autoTheft + boroughsPerSt.arsons
villagesPerSt[
    'overall'] = villagesPerSt.murders + villagesPerSt.rapes + villagesPerSt.robberies + villagesPerSt.assaults + villagesPerSt.burglaries + villagesPerSt.larcenies + villagesPerSt.autoTheft + villagesPerSt.arsons
PerSt[
    'overall'] = PerSt.murders + PerSt.rapes + PerSt.robberies + PerSt.assaults + PerSt.burglaries + PerSt.larcenies + PerSt.autoTheft + PerSt.arsons

for race in racePop:
    townsPerSt[race] = 100 * townsPerSt[race] / townsPerSt.population
    citiesPerSt[race] = 100 * citiesPerSt[race] / citiesPerSt.population
    boroughsPerSt[race] = 100 * boroughsPerSt[race] / boroughsPerSt.population
    villagesPerSt[race] = 100 * villagesPerSt[race] / villagesPerSt.population
    PerSt[race] = 100 * PerSt[race] / PerSt.population
for crime in crimes:
    townsPerSt[crime] = 100 * townsPerSt[crime] / townsPerSt.overall
    citiesPerSt[crime] = 100 * citiesPerSt[crime] / citiesPerSt.overall
    boroughsPerSt[crime] = 100 * boroughsPerSt[crime] / boroughsPerSt.overall
    villagesPerSt[crime] = 100 * villagesPerSt[crime] / villagesPerSt.overall
    PerSt[crime] = 100 * PerSt[crime] / PerSt.overall

choose_dataset = {'All': PerSt, 'towns': townsPerSt, 'cities': citiesPerSt, 'boroughs': boroughsPerSt,
                  'villages': villagesPerSt}
