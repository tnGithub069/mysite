# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 09:53:37 2019

@author: Naoya
Webページを解析し、url（シンザン記念）の馬名およびリンク先を取得
"""
#urllib→Webページ取得
#beautifulSoup→Webページ解析

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import Calculate
import Check
import Constant
#import datetime

#処理名
_処理名_ = "【urlからcsv作る処理】"

_csv格納パス_インプットデータ_ = Constant._csv格納パス_インプットデータ_
_csv格納パス_過去10年分のレースデータ_ = Constant._csv格納パス_過去10年分のレースデータ_
_csv格納パス_予想対象レースの出馬情報_ = Constant._csv格納パス_予想対象レースの出馬情報_

_URL_ネット競馬_DBトップ_ = Constant._URL_ネット競馬_DBトップ_

#メインメソッド============================================================================
    
def main(list_msg):
   
    #csv読み込み
    df_InputData = pd.read_csv(_csv格納パス_インプットデータ_, sep=",",encoding="shift-jis")
    
    #インプットフォーマット読み込み
    inputFormat = df_InputData.iloc[0,1]
    
    #フォーマット：A00の場合
    if inputFormat == "A00":
        #インプット情報
        getRecordNo = int(df_InputData.iloc[1,1])
        getPasts = int(df_InputData.iloc[2,1])
        #float_zahyo = float(df_InputData.iloc[3,1])
        url_thisYearRace = df_InputData.iloc[4,1]
        url_PastRaceDataBase = df_InputData.iloc[5,1]
        
        const_RaceName = "https://db.netkeiba.com"
        indexer_RaceName = "/race/2"
        df_links_PastRace = get_identfiedLinks(url_PastRaceDataBase,const_RaceName,indexer_RaceName)
        
        const_Date = "https://db.netkeiba.com"
        indexer_Date = "/race/list/"
        df_links_Date = get_identfiedLinks(url_PastRaceDataBase,const_Date,indexer_Date)
        
        df_urls = pd.DataFrame( columns=["URL"] )
        
        df_temp = pd.Series( [url_thisYearRace], index = df_urls.columns )
        df_urls = df_urls.append( df_temp, ignore_index=True ) 
        
        df_temp = df_links_PastRace.loc[0:getPasts-1,['URL']]
        df_urls = df_urls.append( df_temp, ignore_index=True )

    #フォーマット：A01の場合（現状、エラーが起きます）
    elif inputFormat == "A01":
        #インプット情報
        getRecordNo = int(df_InputData.iloc[1,1])
        getPasts = int(df_InputData.iloc[2,1])
        float_zahyo = float(df_InputData.iloc[3,1])
        df_urls = df_InputData.iloc[4:,1]
    
    #urlのDataFrameのインデックスを振り直す（必要ないかも？）
    df_urls = df_urls.reset_index(drop=True)

    size_df_urls = len(df_urls)
    int_rootFlag = 0
    for int_roop_01 in range(size_df_urls):
        #今年のレースか、過去のレースかのルートを判定するためのflagを立てる
        if int_roop_01 == 0:
            int_rootFlag = 1
        else: 
            int_rootFlag = 2
               
        #urlを取得
        url = df_urls.iloc[int_roop_01,0]
        
        #htmlを取得
        html = urllib.request.urlopen(url)
        #BeautifulSoupで使える形に変換
        soup = BeautifulSoup(html, "html.parser")
        #title取得
        title = soup.title.string
        
        print(title)
        
        #htmlタグから<a>(リンク)のものを全てlist(links)に取得
        #linksから"https://db.netkeiba.com/horse/"を含むものを取得し、馬名とともに表示
        links = soup.find_all("a")
        
        
        #今年のレースか、過去のレースかのルートを判定する 
        #判定前の共通パラメータ宣言
        horseURL =""
        pass_csv = ""
        conf_hoseName = ""
        zahyo = 0.0
        float_zahyo = float(df_InputData.iloc[3,1])
        raceDate = ""
        
        #今年のレースの場合
        if int_rootFlag == 1:
            
            raceDate = "9999/99/99"
            
            counter = 0
            for link in links:
                
                if "https://db.netkeiba.com/horse/" in (str(link)):
                    horseURL = link.get("href")
                    pass_csv =  _csv格納パス_予想対象レースの出馬情報_
                    outputHoseCsv(list_msg,int_rootFlag,counter,link,horseURL,pass_csv,conf_hoseName,zahyo,getRecordNo,raceDate)       
                    
                    counter = counter + 1
                else:
                    pass
        
        #過去のレースの場合
        elif int_rootFlag == 2:
            
            raceDate = df_links_Date.iloc[int_roop_01-1,0]
            
            df_pastRaceResult = get_pastRaceResult(url)
            #「座標」列を追加
            df_pastRaceResult = df_pastRaceResult.assign(座標 = 0)
            
            #列の番号を取得
            columnsNo_CHAKUSA = df_pastRaceResult.columns.get_loc("着差")
            columnsNo_ZAHYO = df_pastRaceResult.columns.get_loc("座標")
            columnsNo_BAMEI = df_pastRaceResult.columns.get_loc("馬名")
            columnsNo_CHAKUJUN = df_pastRaceResult.columns.get_loc("着順")
            
            #「座標」を計算し、DFに格納する
            size_df_pastRaceResult = len(df_pastRaceResult)
            
            for i in range(size_df_pastRaceResult):
                #着差・着順を取得
                str_chakusa =   str(df_pastRaceResult.iloc[i,columnsNo_CHAKUSA])
                str_chakujun =   str(df_pastRaceResult.iloc[i,columnsNo_CHAKUJUN])
                #座標を計算
                if not '+' in str_chakusa:    
                    float_zahyo_temp = Calculate.Calculate.calculate_zahyo(list_msg,title,str_chakusa,str_chakujun)
                else:
                    
                    float_zahyo_temp = Calculate.Calculate.calculate_zahyo_inPlus(list_msg,title,str_chakusa,str_chakujun)
                    
                float_zahyo = float_zahyo - float_zahyo_temp
                #座標を格納
                df_pastRaceResult.iloc[i,columnsNo_ZAHYO] = float_zahyo
            
            counter = 0
            for link in links:
                
                if "/horse/" in (str(link)):
                    conf_hoseName = df_pastRaceResult.iloc[counter,columnsNo_BAMEI]
                    zahyo = df_pastRaceResult.iloc[counter,columnsNo_ZAHYO]
                    horseURL = "https://db.netkeiba.com" + link.get("href")
                    pass_csv = _csv格納パス_過去10年分のレースデータ_
                    outputHoseCsv(list_msg,int_rootFlag,counter,link,horseURL,pass_csv,conf_hoseName,zahyo,getRecordNo,raceDate)
                    
                    counter = counter + 1
                else:
                    pass




#関数定義============================================================================

def outputHoseCsv(list_msg,int_rootFlag,counter,link,horseURL,pass_csv,conf_hoseName,zahyo,getRecordNo,raceDate):
    
    #馬名の取得
    horseName = link.string
    #print(horseName + " " + link.get("href"))
    
    #horseURL：引数
    horse_html = urllib.request.urlopen(horseURL)
    #データフレーム型リストの準備
    df = pd.read_html(horse_html, header=0)
    
    #表の番号を特定する
    int_allColumsNo = 3
    df_flag = (df[int_allColumsNo].dropna(how="all").dropna(how="all", axis=1))
    int_flag = len(df_flag.columns)
    
    if int_flag == 25:
        pass
    elif int_flag == 1:
        int_allColumsNo = 4
    else:
        list_msg.append('【エラー】' + _処理名_ + '：馬ページの表の番号がイレギュラーパターンな気がしますよ、あららぎさん。　馬名：' + horseName)
    
    #カラムを明記
    df[int_allColumsNo].columns = ["日付", "開催", "天気", "R", "レース名", "映像", "頭数", "枠番", "馬番", "オッズ", "人気", "着順", "騎手", "斤量", "距離", "馬場", "馬場指数", "タイム","着差","タイム指数", "通過", "ペース", "上り", "馬体重", "厩舎コメント", "備考", "勝ち馬(2着馬)", "賞金"]
    #全てNULLとなる行列を削除
    df_temp = (df[int_allColumsNo].dropna(how="all").dropna(how="all", axis=1))
    
    df_temp["馬名"]= horseName
    
    #df_horseName = pd.DataFrame([[horseName]] ,columns=["馬名"])
    df_temp = df_temp.ix[:,["馬名","日付", "開催", "天気", "R", "レース名", "映像", "頭数", "枠番", "馬番", "オッズ", "人気", "着順", "騎手", "斤量", "距離", "馬場", "馬場指数", "タイム","着差","タイム指数", "通過", "ペース", "上り", "馬体重", "厩舎コメント", "備考", "勝ち馬(2着馬)", "賞金"]]
    #正しい位置に座標を格納したかを確認するための、「確認用馬名」列を追加
    df_temp = df_temp.assign(確認用馬名 = conf_hoseName)
    #「座標」列を追加
    df_temp = df_temp.assign(座標 = zahyo)
    
    #馬名と確認用馬名が一致しているかのチェック
    if int_rootFlag == 2:
        columnsNo_BAMEI = df_temp.columns.get_loc("馬名")
        columnsNo_ConfBAMEI = df_temp.columns.get_loc("確認用馬名")
        str1_BAMEI_link = df_temp.iloc[0,columnsNo_BAMEI]
        str_BAMEI_byZAHYO =  df_temp.iloc[0,columnsNo_ConfBAMEI]
        flag_conf = Check.Check.isEquals(str1_BAMEI_link,str_BAMEI_byZAHYO)
        if flag_conf == False:
            list_msg.append("【エラー】" + _処理名_ + "：馬名と確認用馬名が一致していません。正しく分析できませんよ、あららぎさん")
       
    #近走成績から、該当するレコードをn取得する
    df_temp = df_temp[df_temp.日付 < raceDate]
    base = 0
    #getRecordNo = 引数
    #近走成績がgetRecordNo行未満の場合、取得行数を変更
    recordNo_temp = len(df_temp)
    if recordNo_temp < getRecordNo:
        getRecordNo = recordNo_temp
    df_csv = df_temp[base:getRecordNo]
    
    #pass_csv = 引数
    if counter == 0:
        df_csv.to_csv(pass_csv, index=False, encoding="utf-8", mode='a', header=True)
    else:
        df_csv.to_csv(pass_csv, index=False, encoding="utf-8", mode='a', header=False)


    
def get_pastRaceResult(receURL):
    horse_html = urllib.request.urlopen(receURL)
    #データフレーム型リストの準備
    df = pd.read_html(horse_html, header=0)
    int_allColumsNo = 0
    df[int_allColumsNo].columns = ["着順","枠番","馬番","馬名","年齢","斤量","騎手","タイム","着差","タイム指数","通過","上り","単勝","人気","馬体重","調教タイム","厩舎コメント","備考","調教師","馬主","賞金"]
    
    #全てNULLとなる行列を削除
    df_pastRaceResult = (df[int_allColumsNo].dropna(how="all").dropna(how="all", axis=1))
    
    return df_pastRaceResult

#指定したurl上の全てのリンクを取得するメソッド
def get_ALLlinks(url):
    #htmlを取得
    html = urllib.request.urlopen(url)
    #BeautifulSoupで使える形に変換
    soup = BeautifulSoup(html, "html.parser")
    #title取得
    title = soup.title.string
    
    print(title)
    
    #htmlタグから<a>(リンク)のものを全てlist(links)に取得
    #linksから"https://db.netkeiba.com/horse/"を含むものを取得し、馬名とともに表示
    links = soup.find_all("a")
    
    return links

#指定したurl上の特定のリンクを取得するメソッド
def get_identfiedLinks(str_url,str_const,str_indexer):
    df_links = pd.DataFrame( columns=['リンク名','URL'] )
    list_ALLLinks = get_ALLlinks(str_url)
    counter = 0
    for link in list_ALLLinks:
        if str_indexer in (str(link)):
            link_name = link.string
            link_url = str_const + link.get("href")
            df_temp = pd.Series( [ link_name, link_url ], index = df_links.columns )
            df_links = df_links.append( df_temp, ignore_index=True )            
            counter = counter + 1
    return df_links

#ネット競馬データベースURLから、n年分の出馬情報リンクを取得するメソッド
def get_url_nYearsRaceData(n,url_PastRaceDB):
    
    #DB検索結果ページを読み込み、該当リンクを全て取得する
    const_RaceName = _URL_ネット競馬_DBトップ_
    indexer_RaceName = "/race/2"
    df_links_PastRace = get_identfiedLinks(url_PastRaceDB,const_RaceName,indexer_RaceName)
    
    #n年分に絞る
    df_urls = pd.DataFrame( columns=["URL"] )
    df_temp = df_links_PastRace.loc[0:n-1,['URL']]
    df_urls = df_urls.append( df_temp, ignore_index=True )
    
    return df_urls

    
    