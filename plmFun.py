from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from plmBasic import MESSAGE, HandleLog, engine

from plmMod import (FlQtyShelfArt,FlQtyReq)

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-08-22
# description: 单元操作 数据库存相关操作 

def flQtyReq(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyReq'
    log.debug(f">>> {message['info']['fun']} 存入 更新要货数量 信息 {j_args}")

    try:
        se = Session(engine())
        stmt = select(FlQtyReq).where(FlQtyReq.state.in_(['申请','确认','']))\
            .where(FlQtyReq.pid == j_args.get('pid',0)).where(FlQtyReq.braid == j_args.get('braid',0))
        se_req = se.scalars(stmt).first()
    except Exception as e:
        message['errorMsg'] = str(e)
        log.error(message,'查询异常')
        return message
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


def flReqAudit(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flReqAudit'
    log.debug(f">>> {message['info']['fun']} 存入 审核要货数量 信息 {j_args}")

    s_state = j_args.get('state','')
    l_audit = ['申请','确认','完成','作废','驳回']
    if s_state not in l_audit:
        message['msg'] = f'状态需要在{str(l_audit)}'
        return message

    try:
        se = Session(engine())
        stmt = select(FlQtyReq).where(FlQtyReq.state.in_(['申请'])).where(FlQtyReq.id.in_(j_args.get('ids',[])) )
        se_req_audit = se.scalars(stmt).all()
    except Exception as e:
        message['errorMsg'] = str(e)
        log.error(message,'查询异常')
        return message
    
    if se_req_audit:
        try:
            i_cnt = len(se_req_audit)
            update_stmt = update(FlQtyReq).where(FlQtyReq.state == '申请').where(FlQtyReq.id.in_(j_args.get('ids',[])))\
            .values(state = s_state)
            se.execute(update_stmt)
            se.commit()

            message['success'] = True
            if i_cnt == 1:
                for a in se_req_audit:
                    message['content']['msg'] = f"{a.braid} {a.pid} {s_state} 成功"
            else:
                message['content']['msg'] = f"{s_state} {i_cnt} 成功"
            return message
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        message['errorMsg'] = f'未查询到 {s_state} 明细'
        log.warning(message,f'未查询到 {s_state} 明细')
        return message


# 存入 美陈量更新流水 信息
def flQtyShelfArt(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyShelfArt'
    log.debug(f">>> {message['info']['fun']} 存入 美陈量更新流水 信息 {j_args}")

    try:
        se = Session(engine())
        stmt = select(FlQtyShelfArt).where(FlQtyShelfArt.state.in_(['申请','确认','']))\
            .where(FlQtyShelfArt.pid == j_args.get('pid',0)).where(FlQtyShelfArt.braid == j_args.get('braid',0))
        se_art = se.scalars(stmt).first()
    except Exception as e:
        message['errorMsg'] = str(e)
        log.error(message,'查询异常')
        return message
    if se_art:
        try: # 没传的值就不更新了 如果传了0 要更新
            se_art.front_code = j_args.get('front_code','')
            se_art.dept_name = j_args.get('dept_name','')
            se_art.userid = j_args.get('userid',0)
            se_art.user_name = j_args.get('user_name','')
            se_art.qty_shelf_art_new = j_args.get('qty_shelf_art_new',-99)
            se_art.qty_shelf_art_old = j_args.get('qty_shelf_art_old',-99)
            se_art.remark = j_args.get('remark','')
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



def flArtAudit(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flArtAudit'
    log.debug(f">>> {message['info']['fun']} 存入 审核货架美陈量 信息 {j_args}")

    s_state = j_args.get('state','')
    l_audit = ['申请','确认','完成','作废','驳回']
    if s_state not in l_audit:
        message['msg'] = f'状态需要在{str(l_audit)}'
        return message

    try:
        se = Session(engine())
        stmt = select(FlQtyShelfArt).where(FlQtyShelfArt.state.in_(['申请'])).where(FlQtyShelfArt.id.in_(j_args.get('ids',[])) )
        se_art_audit = se.scalars(stmt).all()
    except Exception as e:
        message['errorMsg'] = str(e)
        log.error(message,'查询异常')
        return message
    
    if se_art_audit:
        try:
            i_cnt = len(se_art_audit)
            update_stmt = update(FlQtyShelfArt).where(FlQtyShelfArt.state == '申请').where(FlQtyShelfArt.id.in_(j_args.get('ids',[])))\
            .values(state = s_state)
            se.execute(update_stmt)
            se.commit()

            message['success'] = True
            if i_cnt == 1:
                for a in se_art_audit:
                    message['content']['msg'] = f"{a.braid} {a.pid} {s_state} 成功"
            else:
                message['content']['msg'] = f"{s_state} {i_cnt} 成功"
            return message
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        message['errorMsg'] = f'未查询到 {s_state} 明细'
        log.warning(message,f'未查询到 {s_state} 明细')
        return message