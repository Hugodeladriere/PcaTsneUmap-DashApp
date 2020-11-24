import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from rdkit import Chem
from rdkit.Chem import Descriptors,Crippen, AllChem


from sklearn.preprocessing import StandardScaler
#PCA
from sklearn.decomposition import PCA
#TSNE
from sklearn.manifold import TSNE
#UMAP
import umap.umap_ as umap


def morgan_finger(df): 
    df['mol'] = df['smiles'].apply(lambda x: Chem.MolFromSmiles(x)) #Create a rdkit object that allow more manipulation
    
    #Get Morgan Fingerprint transforamtion here with 4 in radius and 4096 bits
    df_morgan = [AllChem.GetMorganFingerprintAsBitVect(x, radius=4, nBits=4096) for x in df['mol']]
    print(len(df_morgan))
    df_morgan_lists = [list(l) for l in df_morgan]
    print(len(df_morgan_lists))
    df_morgan_name = [f'Bit_{i}' for i in range(4096)]
    print(len(df_morgan_name))
    df_data= pd.DataFrame(df_morgan_lists, index = df['smiles'], columns=df_morgan_name)
    
        
    return df_data


def make_pca(df):
    print("make pca")
    pca = PCA(n_components=2)
    df_data_std = StandardScaler().fit_transform(df)
    df_data_2d = pca.fit_transform(df_data_std)

    df_pca= pd.DataFrame(df_data_2d)
    df_pca.index = df.index
    df_pca.columns = ['PC{}'.format(i+1) for i in df_pca.columns]
    df_pca = df_pca.set_index(df.index)

    return df_pca


def make_tsne(df):
    print("make tsne")
    tsne = TSNE(n_components=2)
    df_data_std = StandardScaler().fit_transform(df)
    df_data_2d = tsne.fit_transform(df_data_std)

    df_tsne= pd.DataFrame(df_data_2d)
    df_tsne.index = df.index
    df_tsne.columns = ['PC{}'.format(i+1) for i in df_tsne.columns]
    df_tsne = df_tsne.set_index(df.index)

    return df_tsne



def make_umap(df):
    print("make umap")
    model_umap = umap.UMAP(n_components=2)
    df_data_std = StandardScaler().fit_transform(df)
    df_data_2d = model_umap.fit_transform(df_data_std)

    df_umap= pd.DataFrame(df_data_2d)
    df_umap.index = df.index
    df_umap.columns = ['PC{}'.format(i+1) for i in df_umap.columns]
    df_umap = df_umap.set_index(df.index)

    return df_umap




def loc_value(df,value_min,value_max):
    cond_min = df.value > value_min
    cond_max = df.value < value_max
    df = df.loc[cond_max & cond_min]
    return df