from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from plmBasic import MESSAGE, SID, HandleLog, engine

from plmMod import (FlQtyShelfArt,)

log = HandleLog(__name__,i_c_level=10,i_f_level=20)

# author  :don
# date    :2024-08-22
# description: 单元操作 数据库存相关操作 

# 存入 美陈量更新流水 信息
def flQtyShelfArt(j_args)-> dict:
    message = MESSAGE.copy()
    message['info']['fun'] = 'flQtyShelfArt'
    log.debug(f">>> {message['info']['fun']} 存入 美陈量更新流水 信息 {j_args}")

    se = Session(engine())
    stmt = select(FlQtyShelfArt).where(FlQtyShelfArt.isapprove == 'N').where(FlQtyShelfArt.pid == j_args.get('pid',0))
    se_prd = se.scalars(stmt).first()
    if se_prd:
        try: # 没传的值就不更新了 如果传了0 要更新
            se_prd.from_code = j_args.get('front_code','')
            se_prd.deptid = j_args.get('deptid',0)
            se_prd.dept_name = j_args.get('dept_name','')
            se_prd.userid = j_args.get('userid',0)
            se_prd.work_code = j_args.get('work_code','')
            se_prd.user_name = j_args.get('user_name','')
            se_prd.qty_shelf_art_new = j_args.get('qty_shelf_art_new',-99)
            se_prd.qty_shelf_art_old = j_args.get('qty_shelf_art_old',-99)
            se_prd.remark = j_args.get('remark','')
            se.commit()
        except Exception as e:
            message.update({'msg':str(e)})
            log.warning(message,'更新异常')
    else:
        si = insert(FlQtyShelfArt).values(
            from_code = j_args.get('front_code'),
            deptid = j_args.get('deptid'),
            dept_name = j_args.get('dept_name'),
            work_code = j_args.get('work_code',''),
            userid = j_args.get('userid'),
            user_name = j_args.get('user_name'),
            pid = j_args.get('pid'),
            qty_shelf_art_new = j_args.get('qty_shelf_art_new'),
            qty_shelf_art_old = j_args.get('qty_shelf_art_old'),
            remark = j_args.get('remark',''))

        try:
            se.execute(si)
            se.commit()
        except Exception as e:
            message.update({'msg':str(e)})
            log.warning(message,'插入异常')
    message.update({'code':200,'msg':f"申请更新 {j_args.get('pid')} 数量为 {j_args.get('qty_shelf_art_new',-99)} 提交成功"})
    return message

