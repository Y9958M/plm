from datetime import date
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from plmBasic import MESSAGE, HandleLog, engine

from plmMod import (FlQtyShelfArt,FlQtyReq,SetBraprdDi)

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-08-22
# description: 单元操作 数据库存相关操作 

def flQtyReqInsert(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyReqInsert'
    log.debug(f">>> {message['info']['fun']} 存入 更新要货数量 信息 {j_args}")

    qty_req = j_args.get('qty_req',-99)
    if isinstance(qty_req,int):
        if qty_req <0 or qty_req > 999999:
            message['errorMsg'] = f'申请数量不对 {qty_req} '
            return message
    else:
        message['errorMsg'] = f'{qty_req} 不是数字'
        return message
    
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
        try: # 员工可以可接更新要货量
            se_req.qty_req = j_args.get('qty_req',-99)
            se_req.ds_validity = date.today().strftime('%Y-%m-%d')
            se_req.remark = j_args.get('remark','')
            se_req.emp_name_ldt = j_args.get('user_name'),
            se.commit()
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        si = insert(FlQtyReq).values(
            front_code = j_args.get('front_code'),
            ds_validity = date.today().strftime('%Y-%m-%d'),
            empid_cdt = j_args.get('userid'),
            emp_name_cdt = j_args.get('user_name'),
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
    message['msg'] = f"{j_args.get('prd_name','')} 数量:{j_args.get('qty_req',-99)} 提交成功"
    return message


def flQtyReqEdit(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyReqEdit'
    log.debug(f">>> {message['info']['fun']} 存入 修改要货数量 信息 {j_args}")

    i = j_args.get('id','')
    qty_req = j_args.get('qty_req',-99)
    emp_name = j_args.get('user_name','')

    try:
        se = Session(engine())
        stmt = select(FlQtyReq).where(FlQtyReq.state.in_(['申请','确认'])).where(FlQtyReq.id == i)
        se_req_edit = se.scalars(stmt).first()
    except Exception as e:
        message['errorMsg'] = str(e)
        log.error(message,'查询异常')
        return message
    
    if se_req_edit:
        try:
            update_stmt = update(FlQtyReq).where(FlQtyReq.id == i)\
            .values(qty_req = qty_req,
                    emp_name_ldt= emp_name,
                    remark= f"{se_req_edit.remark} {emp_name} 变更:{qty_req}")
            se.execute(update_stmt)
            se.commit()

            message['msg'] = f"{se_req_edit.braid} {se_req_edit.pid} {se_req_edit.qty_req} 变更 {qty_req} 成功"
            message['success'] = True    
            return message
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        message['success'] = True
        message['msg'] = '未更新 请重新查询'
        return message


def flQtyReqAudit(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyReqAudit'
    log.debug(f">>> {message['info']['fun']} 存入 审核要货数量 信息 {j_args}")

    s_state = j_args.get('state','')
    l_audit = ['申请','确认','完成','作废','驳回']
    if s_state not in l_audit:
        message['errorMsg'] = f'状态需要在{str(l_audit)}'
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
            .values(state = s_state,emp_name_ldt=j_args.get('user_name',''))
            se.execute(update_stmt)
            se.commit()

            if i_cnt == 1:
                for a in se_req_audit:
                    message['msg'] = f"{a.braid} {a.pid} {s_state} 成功"
            else:
                message['msg'] = f"{s_state} {i_cnt} 成功"
            message['success'] = True    
            return message
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        message['success'] = True
        message['msg'] = f'无 {s_state} 明细 请重新查询'
        return message


# 存入 美陈量更新流水 信息
def flQtyArtInsert(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyArtInsert'
    log.debug(f">>> {message['info']['fun']} 存入 美陈量更新流水 信息 {j_args}")

    qty_art = j_args.get('qty_shelf_art_new',-99)
    if isinstance(qty_art,int):
        if qty_art <0 or qty_art > 999999:
            message['errorMsg'] = f'数量不对 {qty_art} '
            return message
    else:
        message['errorMsg'] = f'{qty_art} 不是数字'
        return message
    
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
        try:
            se_art.front_code = j_args.get('front_code','')
            se_art.emp_name_ldt = j_args.get('user_name','')
            se_art.qty_shelf_art_new = qty_art
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
            braid = j_args.get('braid'),
            pid = j_args.get('pid'),
            empid_cdt = j_args.get('userid'),
            emp_name_cdt = j_args.get('user_name'),
            qty_shelf_art_new = qty_art,
            qty_shelf_art_old = j_args.get('qty_shelf_art_old'),
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
    message['msg'] = f"{j_args.get('prd_name','')} 数量: {qty_art} 提交成功"
    return message


def flQtyArtEdit(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyArtEdit'
    log.debug(f">>> {message['info']['fun']} 存入 修改要货数量 信息 {j_args}")

    i = j_args.get('id','')
    qty_art = j_args.get('qty_art',-99)
    emp_name = j_args.get('user_name','')

    try:
        se = Session(engine())
        stmt = select(FlQtyShelfArt).where(FlQtyShelfArt.state.in_(['申请','确认'])).where(FlQtyShelfArt.id == i)
        se_art_edit = se.scalars(stmt).first()
    except Exception as e:
        message['errorMsg'] = str(e)
        log.error(message,'查询异常')
        return message
    
    if se_art_edit:
        try:
            update_stmt = update(FlQtyShelfArt).where(FlQtyShelfArt.id == i)\
            .values(qty_shelf_art_new = qty_art,
                    emp_name_ldt= emp_name,
                    remark= f"{se_art_edit.remark} {emp_name} 变更:{qty_art}")
            se.execute(update_stmt)
            se.commit()

            message['msg'] = f"{se_art_edit.braid} {se_art_edit.pid} {se_art_edit.qty_shelf_art_new} 变更 {qty_art} 成功"
            message['success'] = True    
            return message
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        message['success'] = True
        message['msg'] = '未更新 请重新查询'
        return message


def flQtyArtAudit(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyArtAudit'
    log.debug(f">>> {message['info']['fun']} 存入 审核货架美陈量 信息 {j_args}")
    ids = j_args.get('ids',[])
    s_state = j_args.get('state','')
    l_audit = ['申请','确认','完成','作废','驳回']
    if s_state not in l_audit:
        message['msg'] = f'状态需要在{str(l_audit)}'
        return message

    try:
        se = Session(engine())
        stmt = select(FlQtyShelfArt).where(FlQtyShelfArt.state.in_(['申请'])).where(FlQtyShelfArt.id.in_(ids) )
        se_art_audit = se.scalars(stmt).all()
    except Exception as e:
        message['errorMsg'] = str(e)
        log.error(message,'查询异常')
        return message
    
    if se_art_audit:
        try:
            i_cnt = len(se_art_audit)
            update_stmt = update(FlQtyShelfArt).where(FlQtyShelfArt.state == '申请').where(FlQtyShelfArt.id.in_(ids))\
            .values(state = s_state)
            se.execute(update_stmt)
            se.commit()
            if s_state == '确认':
                with engine().connect() as conn:
                    s_sql = """UPDATE set_braprd_di a 
    INNER JOIN fl_qty_shelf_art b ON a.braid = b.braid AND a.pid = b.pid
    SET a.qty_shelf_art = b.qty_shelf_art_new,b.state = '完成',b.isu = 'Y'
    WHERE b.state = '确认' AND a.iscovered = 'Y'
    """
                    conn.exec_driver_sql(s_sql)
            message['success'] = True
            if i_cnt == 1:
                for a in se_art_audit:
                    message['msg'] = f"{a.braid} {a.pid} {s_state} 成功"
            else:
                message['msg'] = f"{s_state} {i_cnt}条 成功"
            return message
        except Exception as e:
            message['errorMsg'] = str(e)
            log.warning(message,'更新异常')
            return message
    else:
        message['success'] = True
        message['msg'] = f'无 {s_state} 明细 请重新查询'
        return message