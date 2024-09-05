import pandas as pd
import numpy as np


def pipe_newb(df):
    df_ = df.copy()
    df_['가입일시'] = (
        df['가입일시']
        .astype('str')
        .apply(lambda x: x[:4] + '-' + x[4:])
        .apply(lambda x: pd.to_datetime(x)).dt.to_period('M')
    )
    df_.drop(columns=['year'], inplace=True)
    df_.reset_index(drop=True, inplace=True)
    
    return df_


def pipe_broken(df):
    df_ = df.copy()
    df_['등록일시'] = pd.to_datetime(df_['등록일시'])
    df_.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    df_.reset_index(drop=True, inplace=True)
    
    return df_


def pipe_rental(df):
    df_ = df.copy()
    df_['대여일시'] = pd.to_datetime(df_['대여일시'])
    df_.drop(columns=['자전거구분', '성별', '대여거치대', '반납일시', '반납거치대', '대여 대여소번호', '대여 대여소명', '반납대여소번호', '반납대여소명'], inplace=True)
    df_.drop(index=df_.loc[df_['이용자종류'] == '외국인'].index, inplace=True)
    df_.replace('\\N', np.nan, inplace=True)
    df_.dropna(subset=['반납대여소ID', '생년'], how='any', axis=0, inplace=True)
    df_.drop(index=df_.loc[(df_['이용시간(분)'] < 5) | (df_['이용시간(분)'] > 60)].index, inplace=True)
    df_.drop(index=df_.loc[(df_['이용거리(M)'] < 1000) | (df_['이용거리(M)'] > 15000)].index, inplace=True)
    df_['나이(만)'] = df_['대여일시'].dt.year - df_['생년'].astype('int')
    df_.drop(index=df_.loc[(df_['나이(만)'] < 14) | (df_['나이(만)'] > 64)].index, inplace=True)
    df_.drop(columns=['생년', '이용자종류'], inplace=True)
    df_.reset_index(drop=True, inplace=True)
    
    return df_