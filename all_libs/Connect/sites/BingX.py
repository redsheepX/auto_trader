import os
import sys
rootPath=os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.append(rootPath)

from all_libs.Connect.sites import Base_class
import configparser
import requests





class BingX(Base_class.Connection):
    def __init__(self) -> None:
        super().__init__()
        config=configparser.ConfigParser()
        config.read(f"{rootPath}/Setting/Connect/ConnectSetup")
        self.api_key=config["BingX"]["ApiKey"]
        self.secret_key=config["BingX"]["SecretKey"]
        self.api_url="https://api-swap-rest.bingbon.pro"
        
    def getRequestUrl(self,param:dict,meth:str,type:str="post") -> str:
        newP={}
        output=""
        if api_path[0] !="/":
            api_path="/"+api_path  
        for i in sorted(param.keys()):
            newP[i]=param[i]
        if type!="post":
            print(self.api_url+api_path+"?"+self.getParamString(newP))
            output= self.api_url+api_path+"?"+self.getParamString(newP)
        else:
            newP["sign"]=getSignature(self.secret_key,getOriginString(meth,api_path,self.getParamString(newP)))
            output= self.api_url+api_path+"?"+self.getParamString(newP)
        return output

    def getParamString(self,dict):
        output=""
        for key in dict:
            output+=(key+"=")
            output+=str(dict[key])
            output+="&"
        output=output[:-1]
        return output



if __name__ == '__main__':
    a=BingX()


#region bingXapi定義區
def setMarginMode(symbol:str,marginMode:str):

    meth="POST"
    path="api/v1/user/setMarginMode"

    param={
        'symbol': symbol,
        'marginMode' : marginMode,
        'apiKey':apikey,
        'timestamp':timenow()
        }

    requesturl=getrequesturl(apiurl,meth,path,param,secret,True)
    r=requests.post(requesturl)
    a=loads(r.text)
    if a["code"]==0:
        logging.info("切換逐倉成功")
        return 0
    else:
        print(a)
        logging.info(f'切換逐倉失敗，{a["data"]}')
        return 1

def getOriginString(method,path,paramssign):
    if path[0] !="/":
        path="/"+path    
    output=method+path+paramssign
    return output

def timenow():
    meth="POST"
    path="/api/v1/common/server/time"
    param={
    }
    requesturl=getrequesturl(apiurl,meth,path,param,secret)
    r=requests.get(requesturl)
    return str(loads(r.text)["data"]["currentTime"])

def getSignature(secret,data):
    return urllib.parse.quote_plus(str(base64.b64encode(hmac.new(secret.encode('utf-8'),data.encode('utf-8'),digestmod=sha256).digest()),"utf-8"))




def finalurl(apiurl,path,param):
    if path[0] !="/":
        path="/"+path
    return apiurl+path+param

def getrequesturl(apiurl,meth,path,param,secret,post=True):
    newp={}
    if path[0] !="/":
        path="/"+path  
    for i in sorted(param.keys()):
        newp[i]=param[i]
    if not post:
        print(apiurl+path+"?"+getParamString(newp))
        return apiurl+path+"?"+getParamString(newp)
    else:
        newp["sign"]=getSignature(secret,getOriginString(meth,path,getParamString(newp)))
        return apiurl+path+"?"+getParamString(newp)

def getbalance():
    """獲得帳戶數據

    Returns:
        回傳: 帳戶資訊
    """
    #ex: a=getbalance()
    meth="POST"
    path="/api/v1/user/getBalance"
    param={
        "apiKey":apikey,
        "timestamp":timenow(),
        "currency":"USDT"
    }
    requesturl=getrequesturl(apiurl,meth,path,param,secret)
    r=requests.post(requesturl)
    a=loads(r.text)
    if a["code"]==0:
        print("資料抓取成功")
        return a["data"]
    else:
        print(f'抓取資料失敗，錯誤訊息:{a["msg"]}')



def getccsize():
    requesturl='https://api-swap-rest.bingbon.pro/api/v1/market/getAllContracts'
    r=requests.get(requesturl)
    a=loads(r.text)
    if a["code"]==0:
        for i in a["data"]['contracts']:
            if adddash(cc) == i['symbol']:
                ccsize=i['size']
        return ccsize
    else:
        print(f'抓取資料失敗，錯誤訊息:{a["msg"]}')






    
def trade(symbol:str , apikey:str , side:str , price:float , cost:float , tradetype:str , action:str, times:float=1000000 , lever:int = 5,leverchanged=False,amountmode=False):
    """交易用

    Args:
        symbol (str): 交易對 ex: BTC-USDT
        apikey (str): 介面密鑰
        side (str): (Bid/Ask 買/賣)
        price (float): 價格
        cost (float): 實際投資金額
        tradetype (str): Market/Limit 市價/限價
        action (str): Open/Close 開倉/平倉
        times(float): 不需填寫
        lever(int): 槓桿倍數

        範例: a=trade("BTC-USDT",apikey,side="Bid",price=40000,cost=50,tradetype="Limit",action="Open",lever=5)
    Returns:
        _type_: 成功訊息
    """
    meth="POST"
    path="/api/v1/user/trade"
    if amountmode:
        amount=floor(cost*times)/times
    else:    
        amount=floor(cost*lever/price*times)/times

    if action == 'Close':
        if side=='Long':
            side='Ask'
        elif side == 'Short':
            side='Bid'
    else:
        if side=='Long':
            side='Bid'
        elif side == 'Short':
            side='Ask'
    param={
        "symbol":symbol,
        "apiKey":apikey,
        "timestamp":timenow(),
        "side":side,
        "entrustPrice":price,
        "entrustVolume":amount,
        "tradeType" : tradetype,
        "action" : action
    }
    if side=='Bid':
        leverside='Long'
    elif side == 'Ask':
        leverside='Short'
    if leverchanged == False:
        a=changelever(symbol,leverside,lever)
    else:
        a=0
    if a == 0:
        leverchanged=True
        setMarginMode(adddash(cc),'Isolated')
        requesturl=getrequesturl(apiurl,meth,path,param,secret,True)
        r=requests.post(requesturl)
        b=loads(r.text)
        print(b)
        print(f"預計交易量:{amount}，預計預計交易額:{price}")
        if b["code"]==0:
            logging.error(f"交易成功，本次交易金額:{price} ，本次交易數量{amount}。")
            return int(0),str(b['data']['orderId']),amount
        elif "The quantity entered is incorrect" in b["msg"]:
            times=float(b["msg"][b["msg"].find('times of')+9:])
            status,b,amount=trade(symbol,apikey,side,price,amount,tradetype,action,1/times,lever=lever,leverchanged=True,amountmode=True)
            return int(status),str(b),amount
        elif "Error:Field validation for 'EntrustVolume'" in b["msg"]:
            logging.error(f'交易數量不足，請增加下注額')
            return int(2),str(b),0
        else:
            logging.error(f'交易失敗，錯誤訊息:{b["msg"]}')
            return int(1),str(b),0
    else:
        logging.error("槓桿調整失敗，未進行交易。")
        return int(3),str(a['msg']),0

def changelever(symbol:str,side:str,lever:int):
    """修改槓桿倍率

    Args:
        symbol (str): 合約名稱中需有"-"，如BTC-USDT
        side (str): 多倉或者空倉的槓桿，Long表示多倉，Short表示空倉
        lever (int): 槓桿倍數

    Returns:
        _type_: _description_
    """
    meth="POST"
    path="api/v1/user/setLeverage"

    param={
        'symbol': symbol,
        'side' : side,
        'leverage':lever,
        'apiKey':apikey,
        'timestamp':timenow()
        }

    requesturl=getrequesturl(apiurl,meth,path,param,secret,True)
    r=requests.post(requesturl)
    a=loads(r.text)
    if a["code"]==0:
        logging.error(f"修改槓桿成功，目前{symbol}的{side}，槓桿為 {lever} 倍")
        return 0
    elif "the account has positions or pending orders" in a['msg']:
        logging.error(f"目前有持倉，不進行調整槓桿")
        return 0
    else:
        logging.error(f'修改槓桿失敗，錯誤訊息:{a["msg"]}')
        return 1

def closeposition(symbol:str,apikey,side,amount,price):

    meth="POST"
    path="/api/v1/user/trade"
    if side == 'Long':
        apiside='Ask'
    elif side == 'Short':
        apiside='Bid'
    param={
        "symbol":symbol,
        "apiKey":apikey,
        "timestamp":timenow(),
        "side":apiside,
        "entrustPrice":price,
        "entrustVolume":amount,
        "tradeType" : 'Market',
        "action" : 'Close'
    }

    requesturl=getrequesturl(apiurl,meth,path,param,secret,True)
    r=requests.post(requesturl)
    b=loads(r.text)
    print(b)
    if b["code"]==0:
        logging.error("交易成功")
        return 0,str(b['data']['orderId'])
    elif "Error:Field validation for 'EntrustVolume'" in b["msg"]:
        logging.error("交易數量不足，請增加下注額")
        return 2,b["msg"]
    else:
        logging.error(f'交易失敗，錯誤訊息:{b["msg"]}')
        return 1,b["msg"]


def cancelorderapi(symbol:str,orderid:str):
    meth="POST"
    path="api/v1/user/cancelOrder"

    param={
        'orderId' : orderid,
        'symbol': symbol,
        'apiKey':apikey,
        'timestamp':timenow()
        }

    requesturl=getrequesturl(apiurl,meth,path,param,secret,True)
    r=requests.post(requesturl)
    a=loads(r.text)
    if a["code"]==0:
        logging.error(f"取消開倉成功，目前{orderid}，已取消")
        return 0
    elif 'Insufficient position' in a['msg']:
        logging.error(f"取消開倉失敗，目前{orderid}")
        return 0
    else:
        print(a)
        logging.error(f'取消開倉失敗，{orderid}尚未被取消')
        return 1
    
def checkcancelorder(symbol:str,orderid:str):
    meth="POST"
    path="api/v1/user/queryOrderStatus"

    param={
        'apiKey' : apikey,
        'timestamp': timenow(),
        'symbol':symbol,
        'orderId':orderid
        }

    requesturl=getrequesturl(apiurl,meth,path,param,secret,True)
    r=requests.post(requesturl)
    a=loads(r.text)
    print(a)
    if a["code"]==0:
        logging.error(f"訂單:{orderid}狀態查詢成功，狀態為:{a['data']['status']}。")
        return a['data']['status'] , a['data']['filledVolume']

    else:
        logging.error(f'訂單:{orderid}狀態查詢失敗')
        return 1 , 0

def getfullcost(symbol:str,orderid:str):
    meth="POST"
    path="api/v1/user/queryOrderStatus"

    param={
        'apiKey' : apikey,
        'timestamp': timenow(),
        'symbol':symbol,
        'orderId':orderid
        }

    requesturl=getrequesturl(apiurl,meth,path,param,secret,True)
    r=requests.post(requesturl)
    a=loads(r.text)
    print(a)
    if a["code"]==0:
        price=float(a['data']['avgFilledPrice'])
        volume=float(a['data']['filledVolume'])
        fullcost=price*volume
        return  fullcost

    else:
        logging.error(f'訂單:{orderid}狀態查詢失敗')
        return 1 , 0



#endregion bingXapi定義區
