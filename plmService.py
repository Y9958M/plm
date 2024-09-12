import time
import traceback
import datetime

from weakref import WeakKeyDictionary
from eventlet import tpool  # type: ignore
from nameko.dependency_providers import DependencyProvider  # type: ignore
from nameko.rpc import rpc, RpcProxy  # type: ignore

from plmBasic import HandleLog,msgWrapper
from plmFun import flQtyReqInsert,flQtyReqEdit,flQtyReqAudit,flQtyArtInsert,flQtyArtEdit,flQtyArtAudit

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

    # @rpc
    # def computation_bound_tpool(self):
    #     return tpool.execute(some_fun_you_can_not_control)

    @rpc
    def raise_exception(self):
        raise Exception()


    @rpc
    @msgWrapper(ldt=240907,s_func_remark='插入 要货量')
    def uQtyReqInsert(self, args):
        j_res =flQtyReqInsert(args)
        j_res['params'] = args
        log.debug(j_res)
        return j_res

    @rpc
    @msgWrapper(ldt=240907,s_func_remark='修改 要货量')
    def uQtyReqEdit(self, args):
        j_res =flQtyReqEdit(args)
        j_res['params'] = args
        log.debug(j_res)
        return j_res
    
    @rpc
    @msgWrapper(ldt=240910,s_func_remark='审核 要货量')
    def uQtyReqAudit(self, args):
        j_res =flQtyReqAudit(args)
        j_res['params'] = args
        log.debug(j_res)
        return j_res
    
    @rpc
    @msgWrapper(ldt=240905,s_func_remark='插入 美陈量')
    def uQtyArtInsert(self, args):
        j_res =flQtyArtInsert(args)
        j_res['params'] = args
        log.debug(j_res)
        return j_res
    
    @rpc
    @msgWrapper(ldt=240905,s_func_remark='更新 美陈量')
    def uQtyArtEdit(self, args):
        j_res =flQtyArtEdit(args)
        j_res['params'] = args
        log.debug(j_res)
        return j_res
    
    @rpc
    @msgWrapper(ldt=240910,s_func_remark='审核 美陈量')
    def uQtyArtAudit(self, args):
        j_res =flQtyArtAudit(args)
        j_res['params'] = args
        log.debug(j_res)
        return j_res