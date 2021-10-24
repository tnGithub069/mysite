"""
ビュークラス
V010_TopPageProcess
トップページ用View
エラーフラグ：0(正常終了),1(業務エラー),2(システムエラー)
flg_return：0(render),1(redirect)

flg_return==0の時、「template」「context」必須
flg_return==1の時、「path_name」必須

"""

from django.urls import reverse
from . import S001_TaskIchrnshtk,D010_Index_SetDisp,S006_GetKeibaNews

def main(request):
    #--View共通----------------------------------------------
    #戻り値用の変数宣言
    flg_return = ""
    template = ''
    context = {}
    path_name = ''
    #-------------------------------------------------------
    #try:
    if request.method == 'POST':
        #POSTの場合
        """
        POST時の処理を書く。
        パターンに応じてflg_returnの値を設定する。
        bottunパターンによって処理を分けたりもするかも。
        例は、redirect
        """
        flg_return = "1"
        path_name = 'sample_url2'
    else:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #POST以外の場合
        """
        POST以外時の処理を書く。
        パターンに応じてflg_returnの値を設定する。
        bottunパターンによって処理を分けたりもするかも。
        例は、render
        """
        #サービスを利用する場合は呼び出す
        #--S060-------------------------------------------------------------------------
        #サービス呼び出し
        #表示クラスを呼び出し、表示用のコンテキストを作成する
        list_msg=[]
        json_setDisp = D010_Index_SetDisp.main(list_msg)
        #コンテキストにセット
        context = {**context,**json_setDisp["context"]}
        #-------------------------------------------------------------------------------
        #戻り値にセット
        flg_return = "0"
        template = 'TaskManagement/taskTable.html'
    
    #戻り値用のjsonを作成
    json_view = {'flg_return':flg_return, 'template':template, 'context':context, 'path_name':path_name}
    return json_view
    #==例外処理==========================================================================================
    """
    except Exception as e :
        #システムエラー共通処理
        C030_MessageUtil.systemErrorCommonMethod()
        raise
    """
    #====================================================================================================

