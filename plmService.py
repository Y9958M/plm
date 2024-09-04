import time
import traceback
import datetime
import json

from weakref import WeakKeyDictionary
from eventlet import tpool  # type: ignore
from nameko.dependency_providers import DependencyProvider  # type: ignore
from nameko.rpc import rpc, RpcProxy  # type: ignore

from plmBasic import HandleLog,msgWrapper,MESSAGE,msgJson
from plmFun import flQtyShelfArt

log = HandleLog('plm-service')

class LoggingDependency(DependencyProvider):

    def __init__(self):
        self.timestamps = WeakKeyDictionary()

    def worker_setup(self, worker_ctx):

        self.timestamps[worker_ctx] = datetime.datetime.now()

        service_name = worker_ctx.service_name
        method_name = worker_ctx.entrypoint.method_name

        log.info("%s.%s starting"%(service_name, method_name))

    def worker_result(self, worker_ctx, result=None, exc_info=None):

        service_name = worker_ctx.service_name
        method_name = worker_ctx.entrypoint.method_name

        if exc_info is None:
            status = "completed"
        else:
            status = "errored"
            log.error(traceback.print_tb(exc_info[2]))

        now = datetime.datetime.now()
        worker_started = self.timestamps.pop(worker_ctx)
        elapsed = (now - worker_started).seconds

        log.info("%s.%s %s after %ds"%(service_name, method_name, status, elapsed))

def some_fun_you_can_not_control():
    start = time.time()
    while True:
        if time.time() - start > 300:
            break

class PLMService(object):
    log = LoggingDependency()
    name = "PLM"              # 定义微服务名称 
    YM = RpcProxy("YM")

    @rpc
    @msgWrapper(ldt=240814,s_func_remark='测试连接用')
    def hello_world(self, msg):
        res_ym = self.YM.hello_world(msg)
        j_res = {'code':200,'msg':f'Hello World!I Am {self.name}: {msg} from Platform producer! 确认已连接','pf_msg':res_ym,'service':self.name}
        log.debug(j_res)
        return j_res
    
    @rpc
    def computation_bound(self):
        start = time.time()
        while True:
            if time.time() - start > 300:
                break

    @rpc
    def computation_bound_sleep(self):
        start = time.time()
        while True:
            if int(time.time() - start) % 5 == 0:
                time.sleep(0.2)

            if time.time() - start > 300:
                break

    @rpc
    def computation_bound_tpool(self):
        return tpool.execute(some_fun_you_can_not_control)

    @rpc
    def raise_exception(self):
        raise Exception()

    @rpc
    @msgWrapper(ldt=240822,s_func_remark='更新美陈量')
    def uQtyShelfArt(self, args):
        j_res =flQtyShelfArt(args)
        log.debug(j_res)
        return j_res
    
    @rpc
    @msgWrapper(ldt=240902,s_func_remark='查询商品条码返回编码')
    def cPrdBarcode(self, args):
        message = MESSAGE.copy()
        log.debug(args,'cPrdBarcode 入参')
        # 输入一个条码或编码 回你一个编码 一码多品 情况下，默认按联营
        barcode = args.get('barcode','')
        ln = len(barcode)
        # permission_braid = args.get('permission_braid',[])
        # permission_purid = args.get('permission_purid',[])
        if ln > 5 and ln < 21:
            res_ym = json.loads(self.YM.cQ({'sqlid':'plm_barcode','barcode':barcode}))
            ds = res_ym.get('data',{})
            total = ds.get('total',0)
            if total > 1:
                message.update({'msg':'一码多品'})
            elif total == 1:
                message.update(ds)
            elif total == 0:
                message.update({'msg':'库内无对应条码'})
            else:
                message.update({'msg':'异常 结果为负数'})
            log.debug(res_ym)
        else:
            message.update({'msg':'条码长度不符'})
        return msgJson(message)


