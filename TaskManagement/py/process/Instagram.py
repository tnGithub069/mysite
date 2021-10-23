# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 10:36:24 2021

@author: 洋貴
"""


""
#==参考サイト====================================================================
"""
Instagramにプログラムで自動ログインする【Python + Selenium】
https://self-development.info/instagram%E3%81%AB%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%81%A7%E8%87%AA%E5%8B%95%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3%E3%81%99%E3%82%8B%E3%80%90python-selenium%E3%80%91/
PythonでChromeDriverによりSelenium操作
https://self-development.info/python%e3%81%a7chromedriver%e3%81%ab%e3%82%88%e3%82%8aselenium%e6%93%8d%e4%bd%9c/
Seleniumの最下部スクロールコマンド(window.scrollTo)が効かない場合の代替方法
https://qiita.com/tmhknkmr12/items/f1e5da44c5a33010d25d
【Python】send_keys・・・キーボード入力をする(特殊キー)
https://www.seleniumqref.com/api/python/element_set/Python_special_send_keys.html
Selenium webdriverよく使う操作メソッドまとめ
https://qiita.com/mochio/items/dc9935ee607895420186
Selenium API(逆引き)・・・Selenium APIを利用目的から検索できます
https://www.seleniumqref.com/api/webdriver_gyaku.html
no such elementが出たときにページが移行できるプログラム
https://teratail.com/questions/226721
"""
#==============================================================================

#インポート======================================================================
import Account as Account
import common.SC_LINE as SC_LINE
import common.SC_DBAccess as SC_DBAccess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import sys
import datetime
#==============================================================================

#定数宣言======================================================================
fancID = 'AI04'
sourceID = 'S0001'
#==============================================================================

DOMAIN_BASE = "https://www.instagram.com/"
#CHROMEDRIVER = "C:\Project_AI_Dev\pkgs\chromedriver-binary-2.38-0\Library\bin\chromedriver.exe"
ACCOUNT_NO = '0000001'
LOGIN_ID = Account.getLoginInfo(ACCOUNT_NO)[0][0]
PASSWORD = Account.getLoginInfo(ACCOUNT_NO)[0][1]
DATETIME_FFB = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

def test():
    #pydb_OK = Account.getOKList()
    #print(pydb_OK)
    #list_OK = Account.getOKList_bk()
    #dbUpdate_Follower(list_OK)
    #dbUpdate_Follower_Black(list_OK)
    #dbUpdate_Following(list_OK)
    
    #休憩
    time.sleep(3)
    

def get_driver():
       
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    #options.add_argument('--headless')
    # ブラウザーを起動
    #CS 2020/01/09
    #driver = webdriver.Chrome(CHROMEDRIVER, options=options)
    driver = webdriver.Chrome(executable_path=r'C:\Project_AI_Dev\pkgs\chromedriver-binary-2.38-0\Library\bin\chromedriver.exe', options=options)
    #CE 2020/01/09
    
    return driver

 
# Instagramログイン
def do_login(driver):
    # ログインURL
    login_url = DOMAIN_BASE + "accounts/login/"
    driver.get(login_url)
     
    # 電話、メールまたはユーザー名のinput要素が読み込まれるまで待機（最大10秒）
    elem_id = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
      
    try:
        # パスワードのinput要素
        elem_password = driver.find_element_by_name("password")
    
        if elem_id and elem_password:
            # ログインID入力
            elem_id.send_keys(LOGIN_ID)
          
            # パスワード入力
            elem_password.send_keys(PASSWORD)
              
      
            # ログインボタンクリック
            elem_btn = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))
            )
             
            actions = ActionChains(driver)
            actions.move_to_element(elem_btn)
            actions.click(elem_btn)
            actions.perform()
 
            # 適当（3秒間待つように対応しています）
            time.sleep(3)
 
            # 遷移
            # 遷移後のURLでログイン可否をチェック
            perform_url = driver.current_url
              
            if perform_url.find(login_url) == -1:
                # ログイン成功
                return True
            else:
                # ログイン失敗
                return False
               
        else:
            return False
    except:
        return False 


def clickBottun(xPATH,waittime):
    errCount = 0
    while True:
        try:
            if not bs_exist(getBS(driver), "このページは動作していません"):
                # ボタンクリック
                print(xPATH,'ボタンクリック処理スタート')
                elem_btn = WebDriverWait(driver, waittime).until(
                    EC.visibility_of_element_located((By.XPATH, xPATH))
                )
                print(xPATH,'WebDriverWait完了')
                
                actions = ActionChains(driver)
                print(xPATH,'ActionChains完了')
                actions.move_to_element(elem_btn)
                print(xPATH,'move_to_element完了')
                actions.click(elem_btn)
                print(xPATH,'click完了')
                actions.perform()
                print(xPATH,'perform完了')
             
                # 適当（3秒間待つように対応しています）
                time.sleep(3)
                
                #問題なく処理を完了した場合、ループを抜ける
                break
            else:
                
                print('「このページは動作していません」画面のリロード処理')
                
                elem_btn = WebDriverWait("//*[@id='reload-button']", 3).until(
                    EC.visibility_of_element_located((By.XPATH, xPATH))
                )
                 
                actions = ActionChains(driver)
                actions.move_to_element(elem_btn)
                actions.click(elem_btn)
                actions.perform()
                
                time.sleep(5)
                
                #再度、目的のボタン押下処理を実行する
                continue
                               
        except TimeoutException as e:
            #エラーカウントを + 1
            errCount = errCount + 1
            time.sleep(5)
            #タイムアウトとなった場合、再度処理を実施する
            if errCount <= 3:
                print('エラーカウント：',errCount)
                #2回やってダメだった場合、ボディクリックを試す
                if errCount == 2:
                    driver.find_element_by_tag_name('body').click()
                continue
            else:
                #エラーカウントが10を超えた場合、処理をあきらめる
                print()
                return e

def getBS(driver):
    pageSource = driver.page_source
    bs = BeautifulSoup(pageSource, 'html.parser')
    #print(bs)
    return bs


def getfollow(driver):
    bs = getBS(driver)
    list_class = bs.find_all('',{'class':'PZuss'})
    list_follow = []
    for _class_ in list_class:
        list_a = _class_.find_all('a')
        for a in list_a:
            follow = a.get('title')
            if follow is not None:
                list_follow.append(follow)
    return list_follow


def bs_exist(bs,keyWord):
    flg = True
    elems = bs.find_all(text=re.compile(keyWord))
    if len(elems) == 0:
        flg = False
    return flg


def getNotExists(list_A,list_B):
    list_NotExist = []
    for obj_A in list_A:
        if obj_A not in list_B:
            list_NotExist.append(obj_A)
    return list_NotExist

def removeOKList(list_NotExist):
    list_OK = Account.getOKList()
    for obj_OK in list_OK:
        if obj_OK in list_NotExist:
            list_NotExist.remove(obj_OK)
    return list_NotExist

def calculatePageDowns(kensu):
    #1回のPageDownでスクロールされる件数（現状：6）
    kensu_1PageDown = 5.0
    #何スクロールに1回画面がロードされるか(3回に1回)
    load_bunb = 3.0
    load_bunsh = 1.0
    #ページロードのブロック（件数）（n回に1回ロードする）
    #本来なら「block_load = round(load_bunb/load_bunsh) +1」とした方が安全
    block_load = load_bunb/load_bunsh
    #ページ下部までのロード回数（最後の+1は確実に繰り上げするための処理,安全方向に期待値を取った）
    int_total_load = round(kensu/(kensu_1PageDown*block_load)) + 1
    #ページ下部までのスクロール回数
    scrollCount = round(kensu/kensu_1PageDown)+1
    scrollCount = scrollCount + int_total_load
    
    return scrollCount

def calculatePageEnds(kensu):
    #1回のロードで表示されるフォローの件数
    kensu_load = 12.0
    #全件表示するまでに十分な「PAGE_END」操作数
    scrollCount = (round(kensu/kensu_load) + 1) * 2
    return scrollCount

def scrollPageEnd(kensu_follows):
    scrollCount = calculatePageEnds(kensu_follows)
    print('スクロール回数',scrollCount)
    i = 0
    for i in range(scrollCount):
        i = i + 1
        try:
            #driver.find_element_by_tag_name('body').click()
            #driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            #driver.find_element_by_xpath("//*[@class='PZuss']").click()
            #driver.find_element_by_xpath("//*[@class='PZuss']").send_keys(Keys.PAGE_DOWN)
            driver.find_element_by_xpath("//*[@class='PZuss']").click()
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            print('スクロール中',i)
            time.sleep(2)

        except NoSuchElementException:
            if i != 0:
                print('引き算前',i)
                i = i-1
                print('引き算後',i)
            print('NoSuchElementException',i+1)
            time.sleep(5)
            continue
  
def sendLineMessage(list_NotExist):
    
    #メッセージを定義
    message = '非フォロワーリスト'
    
    #非フォロワーをメッセージに格納
    for notFollower in list_NotExist:       
        message = message + "\n" + notFollower

    SC_LINE.LINE.sendMessage(message)



def dbUpdate_FFB(list_follower,list_following,list_NotExist):
    
    DATETIME_FFB = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    #フォロワーを更新する
    dbUpdate_Follower(list_follower)
    #フォローを更新する
    dbUpdate_Following(list_following)
    #ブラックリストを更新する
    dbUpdate_Follower_Black(list_NotExist)

def dbUpdate_Follower(list_follower):
    #フォロワーの数だけループ
    for followerID in list_follower:
        #M001を参照し、followerIDが存在するかを確認する
        int_countM001 =len(SC_DBAccess.getAll_FromM001_byUSR_ID(followerID))
        
        #M001に登録されていない場合
        if int_countM001 == 0:
            #M001に新規登録
            SC_DBAccess.insertM001(followerID,"","","R",fancID+sourceID,DATETIME_FFB,fancID+sourceID,DATETIME_FFB,"0")
        #M001からフォロワーのアカウントNOを取得する
        follower_M001 = SC_DBAccess.getAll_FromM001_byUSR_ID(followerID)
        account_NO = follower_M001[0][0]
        
        #更新用変数に値のセット
        EDBN = ""
        USRNAME = follower_M001[0][3]
        USRSHUBTS = follower_M001[0][4]
        CRTUSR = fancID + "_" + sourceID
        CRTDATE = DATETIME_FFB
        UPDUSR = fancID + "_" + sourceID
        UPDDATE = DATETIME_FFB
        SAKJKBN = "0"
        
        #T001を参照し、account_NOが存在するかを確認する
        int_countT001 =len(SC_DBAccess.getAll_FromT001orT002_byOneColumn("T001_FOLLOWER","ACCOUNT_NO",account_NO))
         #T001に登録されていない場合
        if int_countT001 == 0:
            #T001に新規登録
            EDBN = "001"
            SC_DBAccess.insertT001orT002("T001_FOLLOWER",account_NO,followerID,EDBN,USRNAME,USRSHUBTS,CRTUSR,CRTDATE,UPDUSR,UPDDATE,SAKJKBN)
        else:
            #枝番の最大値を取得する
            EDBN = SC_DBAccess.getMaxEDBNFromT001orT002_byPKey("T001_FOLLOWER",account_NO,followerID)[0][0]
            #T001の更新日付を更新する
            SC_DBAccess.updateT001orT002_ByPKey("T001_FOLLOWER",account_NO,followerID,EDBN,USRNAME,USRSHUBTS,UPDUSR,UPDDATE,SAKJKBN)
        

def dbUpdate_Follower_Black(list_NotExist):
    #フォロワーの数だけループ
    for followerID in list_NotExist:
        #M001を参照し、followerIDが存在するかを確認する
        int_countM001 =len(SC_DBAccess.getAll_FromM001_byUSR_ID(followerID))
        
        #M001に登録されていない場合
        if int_countM001 == 0:
            #M001に新規登録
            SC_DBAccess.insertM001(followerID,"","","B",fancID+sourceID,DATETIME_FFB,fancID+sourceID,DATETIME_FFB,"0")
        
        #M001からフォロワーのアカウントNOを取得する
        follower_M001 = SC_DBAccess.getAll_FromM001_byUSR_ID(followerID)
        account_NO = follower_M001[0][0]        
        
        #更新用変数に値のセット
        EDBN = ""
        USRNAME = follower_M001[0][3]
        USRSHUBTS = "B"
        CRTUSR = fancID + "_" + sourceID
        CRTDATE = DATETIME_FFB
        UPDUSR = fancID + "_" + sourceID
        UPDDATE = DATETIME_FFB
        SAKJKBN = "0"
        
        #アカウント種別をブラックに更新する
        SC_DBAccess.updateM001_byPKey(account_NO,followerID,"","",USRSHUBTS,fancID+sourceID,DATETIME_FFB,"0")

        
        #T001を参照し、account_NOが存在するかを確認する
        int_countT001 =len(SC_DBAccess.getAll_FromT001orT002_byOneColumn("T001_FOLLOWER","ACCOUNT_NO",account_NO))
         #T001に登録されていない場合
        if int_countT001 == 0:
            #T001に新規登録
            EDBN = "001"
            SC_DBAccess.insertT001orT002("T001_FOLLOWER",account_NO,followerID,EDBN,USRNAME,USRSHUBTS,CRTUSR,CRTDATE,UPDUSR,UPDDATE,SAKJKBN)
        else:
            #枝番の最大値を取得する
            EDBN = SC_DBAccess.getMaxEDBNFromT001orT002_byPKey("T001_FOLLOWER",account_NO,followerID)[0][0]
            #T001の更新日付を更新する
            SC_DBAccess.updateT001orT002_ByPKey("T001_FOLLOWER",account_NO,followerID,EDBN,USRNAME,USRSHUBTS,UPDUSR,UPDDATE,SAKJKBN)
    

def dbUpdate_Following(list_following):
    #フォロワーの数だけループ
    for followingID in list_following:
        #M001を参照し、followerIDが存在するかを確認する
        int_countM001 =len(SC_DBAccess.getAll_FromM001_byUSR_ID(followingID))
        
        #M001に登録されていない場合
        if int_countM001 == 0:
            #M001に新規登録
            SC_DBAccess.insertM001(followingID,"","","R",fancID+sourceID,DATETIME_FFB,fancID+sourceID,DATETIME_FFB,"0")
        #M001からフォロワーのアカウントNOを取得する
        follower_M001 = SC_DBAccess.getAll_FromM001_byUSR_ID(followingID)
        account_NO = follower_M001[0][0]
        
        #更新用変数に値のセット
        EDBN = ""
        USRNAME = follower_M001[0][3]
        USRSHUBTS = follower_M001[0][4]
        CRTUSR = fancID + "_" + sourceID
        CRTDATE = DATETIME_FFB
        UPDUSR = fancID + "_" + sourceID
        UPDDATE = DATETIME_FFB
        SAKJKBN = "0"
        
        #T002を参照し、account_NOが存在するかを確認する
        int_countT002 =len(SC_DBAccess.getAll_FromT001orT002_byOneColumn("T002_FOLLOWING","ACCOUNT_NO",account_NO))
         #T001に登録されていない場合
        if int_countT002 == 0:
            #T001に新規登録
            EDBN = "001"
            SC_DBAccess.insertT001orT002("T002_FOLLOWING",account_NO,followingID,EDBN,USRNAME,USRSHUBTS,CRTUSR,CRTDATE,UPDUSR,UPDDATE,SAKJKBN)
        else:
            #枝番の最大値を取得する
            EDBN = SC_DBAccess.getMaxEDBNFromT001orT002_byPKey("T002_FOLLOWING",account_NO,followingID)[0][0]
            #T001の更新日付を更新する
            SC_DBAccess.updateT001orT002_ByPKey("T002_FOLLOWING",account_NO,followingID,EDBN,USRNAME,USRSHUBTS,UPDUSR,UPDDATE,SAKJKBN)


if __name__ == "__main__":
    
    #テスト
    test()
    
    # Driver
    driver = get_driver()
    # ログイン
    login_flg = do_login(driver)
    print(login_flg)

    #ログイン情報の記録＞後でボタンをクリック
    if bs_exist(getBS(driver), "ログイン情報を保存"):
        clickBottun('//*[@id="react-root"]/section/main/div/div/div/div/button',3)
    
    #「お知らせをオンにする」＞後でボタンをクリック
    if bs_exist(getBS(driver), "お知らせをオンにする"):
        #clickBottun('//html/body/div[3]/div/div/div/div[3]/button[2]',3)
        clickBottun('//*[@class="aOOlW   HoLwm "]',5)
        #getBS(driver)    
    
    #ヘッダ部の「人マーク」画像をクリック
    #clickBottun('//*[@class="_47KiJ"]/div[5]/span/img',3)
    clickBottun('//*[@alt="'+LOGIN_ID+'のプロフィール写真"]',5)
    
    #プロフィールボタンをクリック
    clickBottun('//*[@href="/'+LOGIN_ID+'/"]',5)
       
    #プロフィール画面のフォロワー数・フォロー数を取得
    bs = getBS(driver)
    #正規表現において、ワイルドカードは「.*」
    elem = bs.find('a',{'href':re.compile('.*followers.*')})
    kensu_follower = float(elem.span.get_text())
    elem = bs.find('a',{'href':re.compile('.*following.*')})
    kensu_following = float(elem.span.get_text())
    
    #プロフィール画面のフォロワーをクリック
    clickBottun('//*[@href="/'+LOGIN_ID+'/followers/"]',5)
    
    #最下部までスクロール
    scrollPageEnd(kensu_follower)
    
    #プロフィール画面のフォロワーリストを取得
    list_follower = getfollow(driver)
    print("フォロワーTOP5",list_follower[:5])
              
    #閉じるボタン
    driver.find_element_by_tag_name('body').click()
    clickBottun('//*[@class="wpO6b "]', 5)
    
    #プロフィール画面のフォロー
    clickBottun('//*[@href="/'+LOGIN_ID+'/following/"]',5)
    
    #最下部までスクロール
    scrollPageEnd(kensu_following)

    #プロフィール画面のフォローリストを取得
    list_following = getfollow(driver)
    print("フォローTOP5",list_following[:5])
       
    #フォローリストからフォロワーでないアカウントリストを取得する
    list_NotExist = getNotExists(list_following, list_follower)
    #NotExistリストから、OKリストを除く
    list_NotExist = removeOKList(list_NotExist)
    

    print("フォロワー",list_follower)
    print("フォロー",list_following) 
    print("非フォロワー",list_NotExist)
    
    #閉じるボタン
    clickBottun('//*[@class="wpO6b "]', 5)
    
    #結果をLINEで送信する
    sendLineMessage(list_NotExist)
    
    #DB登録====================================================================
    
    #フォロワー、フォロー、ブラックリストのDBを更新する
    dbUpdate_FFB(list_follower,list_following,list_NotExist)
    
    #==========================================================================
    
    driver.quit()
    
