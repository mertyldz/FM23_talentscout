import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform, pdist
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

#* PLAYERS => 
df = pd.read_excel(r"FM_2023_final.xlsx")
df.head()

def grab_col_names(dataframe, cat_th=10,  car_th=20):
    """
    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.

    Parameters
    ----------
    dataframe: dataframe
        değişken isimleri alınmak istenen dataframe'dir.
    cat_th: int, float
        numerik fakat kategorik olan değişkenler için sınıf eşik değeri
    car_th: int, float
        kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    -------
    cat_cols: list
        Kategorik değişken listesi
    num_cols: list
        Numerik değişken listesi
    cat_but_car: list
        Kategorik görünümlü kardinal değişken listesi

    Notes
    ------
    cat_cols + num_cols + cat_but_car = toplam değişken sayısı
    num_but_cat cat_cols'un içerisinde.

    """
    # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]

    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and dataframe[col].dtypes in ["int64", "float64"]]

    cat_but_car = [col for col in dataframe.columns if
                   dataframe[col].nunique() > car_th and str(dataframe[col].dtypes) in ["category", "object"]]

    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes in ["int64", "float64"]]
    num_cols = [col for col in num_cols if col not in cat_cols]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')

    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df)

player_columns = ["Age", "Last_Player_Value", "Salary", "Nationality"]

df.head()

#? Oyuncu kıyaslama
pedri = df.loc[df["Name"] == "Pedri" , player_columns]
kane = df.loc[df["Name"] == "Harry Kane" , player_columns]

#? Radar Graph


Techn = ['Crossing',  'Dribbling', 'First Touch', 'Corners', 'Free Kick Taking', 'Technique', 'Passing', 'Left Foot', 'Right Foot']
Attack = ['Finishing', 'Heading', 'Long Shots', 'Penalty Taking', 'Jumping Reach']
Power = ['Strength', 'Natural Fitness']
Speed = ['Acceleration', 'Agility', 'Balance', 'Pace', 'Stamina']
Defence = ['Marking', 'Tackling', 'Aggressiion', 'Long Throws', 'Foul']
Mentality = ['Emotional control', 'Sportsmanship', 'Resistant to stress', 'Professional', 'Bravery', 'Anticipation', 'Composure', 'Concentration', 'Decision', 'Determination', 'Flair', 'Leadership', 'Work Rate', 'Teamwork', 'Stability', 'Ambition', 'Argue', 'Loyal', 'Adaptation', 'Vision', 'Off The Ball']
GoalK = ['Reflexes', 'Kicking', 'Handling', 'One On Ones',  'Command Of Area', 'Communication', 'Eccentricity', 'Rushing Out', 'Punching', 'Throwing', 'Aerial Reach']

df["Techn"] = df[Techn].apply(lambda x: x.mean(), axis=1)
df["Attack"] = df[Attack].apply(lambda x: x.mean(), axis=1)
df["Power"] = df[Power].apply(lambda x: x.mean(), axis=1)
df["Speed"] = df[Speed].apply(lambda x: x.mean(), axis=1)
df["Mentality"] = df[Mentality].apply(lambda x: x.mean(), axis=1)
df["GoalK"] = df[GoalK].apply(lambda x: x.mean(), axis=1)

grouped_attributes = ["Techn","Attack","Power", "Speed", "Mentality" ,"GoalK"]
radar_plot = ["Name"] + grouped_attributes
df_radar = df[radar_plot]
df_radar.to_excel("radar_plot.xlsx")
df.drop(grouped_attributes, inplace=True, axis=1)

#! Bar Plot
barplot_attributes =["Name"] + Techn + Attack + Power + Speed + Defence + Mentality
len(barplot_attributes)
barplot = df[barplot_attributes]
barplot.to_excel("barplot.xlsx")
df[Speed]

#! Similarity
position = ["DL", "DC", "DR", "WBL", "WBR", "DM", "ML", "MC", "MR", "AML", "AMC", "AMR", "ST", "GK"]
similarity_cols =["Name"] + Techn + Attack + Power + Speed + Defence + Mentality + GoalK + position
similarity_df = df[similarity_cols]

df2 = similarity_df.copy()
df2.set_index("Name", inplace=True)

#STANDARD SCALER UYGULA!!!!!!!!!

# En benzeyen 5 kişi
def most_similar(dataframe, number=5):
    euc_list={}
    for i in list(dataframe.columns):
        euc_list.update({i:list(dataframe[i].sort_values(ascending=True)[1:number+1].index)})
    ec=pd.DataFrame(euc_list)
    return ec

#* Euclidean Distance
distances = pdist(df2, metric="euclidean")
dist_matrix = squareform(distances)
euclidean_distance = pd.DataFrame(dist_matrix, columns=df2.index, index=df2.index)
euclidean_distance.to_excel("euclidean_distance.xlsx")
euclidean_distance.iloc[0:5, 0:5]


#* Canberra Distance
canberra_distances = pdist(df2, metric="canberra")
canberradist_matrix = squareform(canberra_distances)
canberradistance = pd.DataFrame(canberradist_matrix, columns=df2.index, index=df2.index)
canberradistance.to_excel("canberradistance.xlsx")
euclidean_distance.iloc[0:5, 0:5]


#* Minkowski Distance
minkowski_distance = pdist(df2, metric="minkowski")
minkowski_matrix = squareform(minkowski_distance)
minkowskidistance = pd.DataFrame(minkowski_matrix, columns=df2.index, index=df2.index)
minkowskidistance.to_excel("minkowskidistance.xlsx")


#* Correlation Distance
correlation_distance = pdist(df2, metric="correlation")
correlation_matrix = squareform(correlation_distance)
correlationdistance = pd.DataFrame(correlation_matrix, columns=df2.index, index=df2.index)
correlationdistance.to_excel("correlationdistance.xlsx")


#* cityblock(manhattan) distance
cityblock_distance = pdist(df2, metric="cityblock")
cityblock_matrix = squareform(cityblock_distance)
cityblockdistance = pd.DataFrame(cityblock_matrix, columns=df2.index, index=df2.index)
cityblockdistance.to_excel("cityblockdistance.xlsx")


#* jaccard distance
jaccard_distance = pdist(df2, metric="jaccard")
jaccard_matrix = squareform(jaccard_distance)
jaccarddistance = pd.DataFrame(jaccard_matrix, columns=df2.index, index=df2.index)
jaccarddistance.to_excel("jaccarddistance.xlsx")

#* dice's distance
dice_distance = pdist(df2, metric="dice")
dice_matrix = squareform(dice_distance)
dicedistance = pd.DataFrame(dice_matrix, columns=df2.index, index=df2.index)
dicedistance.to_excel("dicedistance.xlsx")
