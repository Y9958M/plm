from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from plmBasic import MESSAGE, SID, HandleLog, engine

from plmMod import (FlQtyShelfArt,FlQtyReq)

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-08-22
# description: 单元操作 数据库存相关操作 

def flQtyReq(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyReq'
    log.debug(f">>> {message['info']['fun']} 存入 更新要货数量 信息 {j_args}")

    se = Session(engine())
    stmt = select(FlQtyReq).where(FlQtyReq.state.in_(['申请','确认','']))\
        .where(FlQtyReq.pid == j_args.get('pid',0)).where(FlQtyReq.braid == j_args.get('braid',0))
    se_req = se.scalars(stmt).first()
    if se_req:
        try: # 没传的值就不更新了 如果传了0 要更新
            se_req.qty_req = j_args.get('qty_req',-99)
            se_req.remark = j_args.get('remark','')
            se.commit()
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        si = insert(FlQtyReq).values(
            front_code = j_args.get('front_code'),
            dept_name = j_args.get('dept_name'),
            userid = j_args.get('userid'),
            user_name = j_args.get('user_name'),
            pid = j_args.get('pid'),
            braid = j_args.get('braid'),
            qty_req = j_args.get('qty_req'),
            remark = j_args.get('remark',''),
            isu = 'N',
            state = '申请')
            
        try:
            se.execute(si)
            se.commit()
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'插入异常')
            return message
    message['success'] = True
    message['content']['msg'] = f"申请更新 {j_args.get('pid')} 数量为 {j_args.get('qty_req',-99)} 提交成功"
    return message



# 存入 美陈量更新流水 信息
def flQtyShelfArt(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyShelfArt'
    log.debug(f">>> {message['info']['fun']} 存入 美陈量更新流水 信息 {j_args}")

    se = Session(engine())
    stmt = select(FlQtyShelfArt).where(FlQtyShelfArt.state.in_(['申请','确认','']))\
        .where(FlQtyShelfArt.pid == j_args.get('pid',0)).where(FlQtyShelfArt.braid == j_args.get('braid',0))
    se_prd = se.scalars(stmt).first()
    if se_prd:
        try: # 没传的值就不更新了 如果传了0 要更新
            se_prd.front_code = j_args.get('front_code','')
            se_prd.dept_name = j_args.get('dept_name','')
            se_prd.userid = j_args.get('userid',0)
            se_prd.user_name = j_args.get('user_name','')
            se_prd.qty_shelf_art_new = j_args.get('qty_shelf_art_new',-99)
            se_prd.qty_shelf_art_old = j_args.get('qty_shelf_art_old',-99)
            se_prd.remark = j_args.get('remark','')
            se.commit()
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        si = insert(FlQtyShelfArt).values(
            front_code = j_args.get('front_code'),
            dept_name = j_args.get('dept_name'),
            userid = j_args.get('userid'),
            user_name = j_args.get('user_name'),
            pid = j_args.get('pid'),
            braid = j_args.get('braid'),
            qty_shelf_art_new = j_args.get('qty_shelf_art_new'),
            qty_shelf_art_old = j_args.get('qty_shelf_art_old'),
            remark = j_args.get('remark',''),
            state = '申请')
            
        try:
            se.execute(si)
            se.commit()
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'插入异常')
            return message
    message['success'] = True
    message['content']['msg'] = f"申请更新货架美陈 {j_args.get('pid')} 数量为 {j_args.get('qty_shelf_art_new',-99)} 提交成功"
    return message

