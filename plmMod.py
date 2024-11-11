# # 连接数据库
# DATABASE_URL = "mysql+pymysql://root:shtm2022@192.168.200.174:3306/grasp"
# engine = create_engine(DATABASE_URL, echo=True)
 
# # 创建会话
# Session = sessionmaker(bind=engine)
# session = Session()
 
# # 创建所有表
# Base.metadata.create_all(engine)

# sqlacodegen_v2 --generator declarative mysql+pymysql://root:4197@localhost:3310/plm --tables common_query

from sqlalchemy import CHAR, Column, Computed, DECIMAL, Date, DateTime, Enum, Index, String, Table, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, TINYINT,JSON
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.base import Mapped
Base = declarative_base()
metadata = Base.metadata


class BookPrdAbcLm(Base):
    __tablename__ = 'book_prd_abc_lm'
    __table_args__ = (
        Index('_idx', 'braid', 'pid'),
        {'comment': '预设-市场-商品属性'}
    )

    braid = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='门店ID')
    pid = mapped_column(BIGINT(18), nullable=False, comment='编码ID')
    pkg_dist = mapped_column(DECIMAL(10, 3), nullable=False, server_default=text("'1.000'"), comment='配送包装率')
    lv_abc = mapped_column(String(36), nullable=False, server_default=text("''"), comment='ABC等级')
    qty_shelf_art = mapped_column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='最小安全量')
    remark = mapped_column(String(36), nullable=False, comment='备注')
    from_code = mapped_column(String(36), nullable=False, comment='来源代码')
    ds_begin = mapped_column(Date, nullable=False, comment='开始日期')
    ds_end = mapped_column(Date, nullable=False, comment='结束日期')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='环境标识')
    id = mapped_column(BIGINT(20), primary_key=True, comment='序号')
    ldt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更新时间')
    cdt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')    


t_category_v = Table(
    'category_v', metadata,
    Column('sid', TINYINT(4), server_default=text("'0'")),
    Column('c1', String(255)),
    Column('cid2', INTEGER(11)),
    Column('c2_name', String(36)),
    Column('c2', String(255)),
    Column('cid', INTEGER(11)),
    Column('c3_name', String(36)),
    Column('c3', String(255)),
    Column('gpm_std', DECIMAL(10, 2), server_default=text("'-99.00'")),
    Column('gpm_ref', DECIMAL(10, 2), server_default=text("'-99.00'")),
    Column('days_expiry_def', INTEGER(11), server_default=text("'-99'")),
    Column('storage_def', Enum('常温', '低温', '冷藏', '-', '')),
    Column('model_def', Enum('工业品', '生鲜', '日清', '小百货', '散称', '短保', '服饰', '-', '')),
    Column('cnt_sku_ref', INTEGER(11), server_default=text("'-99'")),
    Column('isin', Enum('Y', 'N'), server_default=text("'N'"))
)


class CtCategoryLm(Base):
    __tablename__ = 'ct_category_lm'
    __table_args__ = {'comment': '对照-算量类目（非ERP）'}

    cid_ods = mapped_column(INTEGER(11), nullable=False, comment='原品类ID')
    ods_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='原类别名称')
    cid = mapped_column(INTEGER(11), nullable=False, comment='类别ID')
    cate_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='类别名称')
    from_code = mapped_column(String(36), nullable=False, comment='来源代码')
    ds_begin = mapped_column(Date, nullable=False, comment='开始日期')
    ds_end = mapped_column(Date, nullable=False, comment='结束日期')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='环境标识')
    id = mapped_column(BIGINT(20), primary_key=True, comment='序号')
    ldt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更新时间')
    cdt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class ErpBraprdDa(Base):
    __tablename__ = 'erp_braprd_da'
    __table_args__ = {'comment': 'ERP-门店商品信息与限制'}

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    pid = mapped_column(BIGINT(20), primary_key=True, nullable=False, comment='商品ID')
    isbusiness = mapped_column(Enum('Y', 'N'), nullable=False, comment='是否经营')
    scenario = mapped_column(Enum('配送', '采购', '直流', '-', ''), nullable=False, server_default=text("''"), comment="场景 '配送','采购','直流'")
    dms_erp = mapped_column(DECIMAL(9, 3), nullable=False, server_default=text("'0.001'"), comment='日均销量')
    qty_stk = mapped_column(DECIMAL(10, 3), nullable=False, server_default=text("'0.000'"), comment='库存数量')
    cos_stk = mapped_column(DECIMAL(18, 6), nullable=False, server_default=text("'0.000000'"), comment='库存金额')
    price_sale = mapped_column(DECIMAL(12, 2), comment='售价')
    price_pur = mapped_column(DECIMAL(18, 6), comment='采购价格')
    price_prom = mapped_column(DECIMAL(12, 3), comment='促销价')
    prom_lv = mapped_column(TINYINT(4), comment='促销等级')
    ds_prom_begin = mapped_column(Date, comment='促销开始日期')
    ds_prom_end = mapped_column(Date, comment='促销结束日期')


class ErpPrdDa(Base):
    __tablename__ = 'erp_prd_da'
    __table_args__ = {'comment': 'ERP-商品信息与限制'}

    cid = mapped_column(INTEGER(11), nullable=False, server_default=text("'-99'"), comment='类目ID')
    pid = mapped_column(BIGINT(18), primary_key=True, comment='商品ID')
    barcode = mapped_column(String(36), nullable=False, server_default=text("''"), comment='商品条码')
    prd_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='商品名称')
    spec = mapped_column(String(36), nullable=False, server_default=text("''"), comment='规格')
    pcs = mapped_column(String(36), nullable=False, server_default=text("''"), comment='单位')
    brand_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='品牌')
    prd_area = mapped_column(String(36), nullable=False, server_default=text("''"), comment='产地')
    pkg = mapped_column(INTEGER(11), nullable=False, comment='包装数量')
    standard = mapped_column(Enum('标品', '称重', '计数', '虚拟', '赠品', '卡券', '-', ''), nullable=False, server_default=text("''"), comment="标品 '标品','称重','计数','虚拟','赠品','卡券','-',''")
    storage = mapped_column(Enum('常温', '低温', '冷藏', '-', ''), nullable=False, server_default=text("''"), comment=" 存储条件 '常温','低温','冷藏','-',''")
    business_model = mapped_column(Enum('自营', '联营', '代销', '-', ''), nullable=False, server_default=text("''"), comment="经营模式 '自营','联营','代销','-',''")
    days_expiry = mapped_column(INTEGER(11), nullable=False, server_default=text("'-99'"), comment='保质期')
    price_sale_hq = mapped_column(DECIMAL(8, 2), nullable=False, server_default=text("'-99.00'"), comment='参考价格')
    price_pur_ld = mapped_column(DECIMAL(18, 6), nullable=False, server_default=text("'-99.000000'"), comment='最近进价')


class FlQtyShelfArt(Base):
    __tablename__ = 'fl_qty_shelf_art'
    __table_args__ = (
        Index('_bp', 'braid', 'pid'),
        Index('_state', 'state'),
        {'comment': '流水-美陈量'}
    )

    id = mapped_column(BIGINT(20), primary_key=True, comment='自增序号')
    front_code = mapped_column(String(36), comment='来源代码')
    braid = mapped_column(INTEGER(11), comment='门店ID')
    pid = mapped_column(BIGINT(20), comment='商品ID')
    qty_shelf_art_old = mapped_column(INTEGER(11), comment='老美陈量')
    qty_shelf_art_new = mapped_column(INTEGER(11), comment='新美陈量')
    state = mapped_column(Enum('申请', '确认', '完成', '作废', '驳回', '-', ''), server_default=text("''"), comment="状 态 '申请','确认','完成','作废','驳回','-',''")
    remark = mapped_column(String(255), server_default=text("''"), comment='备注说明')
    isu = mapped_column(Enum('Y', 'N'), server_default=text("'N'"), comment='是否更新')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    empid_cdt = mapped_column(BIGINT(18))
    emp_name_cdt = mapped_column(String(36), comment='创建人')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时 间')
    emp_name_ldt = mapped_column(String(36), comment='最后更新人')


class FlQtyReq(Base):
    __tablename__ = 'fl_qty_req'
    __table_args__ = (
        Index('_bp', 'braid', 'pid'),
        Index('_state', 'state'),
        {'comment': '流水-要货明细'}
    )

    id = mapped_column(BIGINT(20), primary_key=True, comment='自增序号')
    front_code = mapped_column(String(36), comment='来源代码')
    ds_validity = mapped_column(Date, comment='有效日期')
    braid = mapped_column(INTEGER(11), comment='门店ID')
    pid = mapped_column(BIGINT(20), comment='商品ID')
    qty_req = mapped_column(INTEGER(11), comment='要货数量')
    state = mapped_column(Enum('申请', '确认', '完成', '作废', '驳回', '-', ''), server_default=text("''"), comment="状 态 '申请','确认','完成','作废','驳回','-',''")
    remark = mapped_column(String(255), server_default=text("''"), comment='备注说明')
    isu = mapped_column(Enum('Y', 'N'), server_default=text("'N'"), comment='是否更新')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    empid_cdt = mapped_column(BIGINT(20), comment='用户ID')
    emp_name_cdt = mapped_column(String(36), comment='创建人')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时 间')
    emp_name_ldt = mapped_column(String(36), comment='最后更新人')


class LagDmsDa(Base):
    __tablename__ = 'lag_dms_da'
    __table_args__ = {'comment': '经营结果-日均销量'}

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    pid = mapped_column(BIGINT(20), primary_key=True, nullable=False, comment='商品ID')
    dms = mapped_column(DECIMAL(12, 3), nullable=False, comment='日均销量')
    dms_remark = mapped_column(String(255), nullable=False, comment='日均计算备注')
    dms_lv = mapped_column(TINYINT(4), nullable=False, comment='DMS计算等级')
    dms_opl = mapped_column(DECIMAL(12, 3), nullable=False, comment='日均自动订单')


class LagPriceBandDa(Base):
    __tablename__ = 'lag_price_band_da'
    __table_args__ = (
        Index('ix_tag_price_band_da_braid', 'braid'),
        Index('ix_tag_price_band_da_cateid', 'cid'),
        Index('ix_tag_price_band_da_q_tag', 'tag_q'),
        {'comment': '经营结果-价格带'}
    )

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    cid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='类目ID')
    tag_q = mapped_column(String(36), primary_key=True, nullable=False, comment='分段标签')
    qty = mapped_column(DECIMAL(12, 3), comment='数量')
    amt = mapped_column(DECIMAL(12, 2), comment='销售金额')
    fit = mapped_column(DECIMAL(12, 2), comment='门店毛利')
    cnt_prd = mapped_column(INTEGER(11), comment='品项数')
    tag_price = mapped_column(String(36), comment='价格标签')
    gpm_q = mapped_column(DECIMAL(12, 3), comment='分段毛利率')
    per_fit_q2cate = mapped_column(DECIMAL(12, 3), comment='毛利占比分段占品类群')
    per_amt_q2cate = mapped_column(DECIMAL(12, 3), comment='金额占比分段品类群')
    tag_trend_cate = mapped_column(String(36), comment='标签品类趋势')


class LagSaleDa(Base):
    __tablename__ = 'lag_sale_da'
    __table_args__ = {'comment': '经营结果-门店单品'}

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, index=True, comment='门店ID')
    pid = mapped_column(BIGINT(20), primary_key=True, nullable=False, index=True, comment='商品ID')
    qty_stk = mapped_column(DECIMAL(12, 3), nullable=False, comment='期末数量')
    qty_s15h = mapped_column(DECIMAL(12, 3), nullable=False, comment='15点前销量')
    qty_yd = mapped_column(DECIMAL(12, 3), nullable=False, comment='昨天销售数量')
    qty_s1d = mapped_column(DECIMAL(12, 3), nullable=False, comment='销量1天')
    qty_last = mapped_column(DECIMAL(12, 3), nullable=False, comment='最后销售数量')
    amt_yd = mapped_column(DECIMAL(12, 2), nullable=False, comment='昨天销售金额')
    fit_yd = mapped_column(DECIMAL(12, 2), nullable=False, comment='昨天销售毛利')
    qty_s7d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前7天销量')
    qty_x7d = mapped_column(DECIMAL(12, 3), nullable=False, comment='7天最大销量')
    c7d = mapped_column(INTEGER(11), nullable=False, comment='7天次数')
    amt_s7d = mapped_column(DECIMAL(12, 2), nullable=False, comment='销售7天')
    fit_s7d = mapped_column(DECIMAL(12, 2), nullable=False, comment='毛利7天')
    agio_s7d = mapped_column(DECIMAL(12, 2), nullable=False, comment='前7天折扣金额')
    cnt_prom_s7d = mapped_column(INTEGER(11), nullable=False, comment='计数促销7天')
    qty_prom_s7d = mapped_column(DECIMAL(12, 3), nullable=False, comment='销量促销7天')
    amt_prom_s7d = mapped_column(DECIMAL(12, 2), nullable=False, comment='促销销售额7天')
    fit_prom_s7d = mapped_column(DECIMAL(12, 2), nullable=False, comment='促销毛利7天')
    qty_future_s7d_y = mapped_column(DECIMAL(12, 3), nullable=False, comment='去年未来7天销量')
    qty_prom_s28d = mapped_column(DECIMAL(12, 3), nullable=False, comment='28天促销销量')
    qty_s28d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前28天销量')
    qty_x28d = mapped_column(INTEGER(11), nullable=False, comment='最大量28天')
    qty_n28d = mapped_column(INTEGER(11), nullable=False, comment='最小量28天')
    qty_rec_s28d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前28天收货合计')
    qty_stk_x28d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前28天最大库存数量')
    qty_stk_n28d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前28天最小库存数量')
    c28d = mapped_column(INTEGER(11), nullable=False, comment='前28天次数')
    cnt_sale_s28d = mapped_column(INTEGER(11), nullable=False, comment='前28天销售次数')
    cnt_stk_s28d = mapped_column(INTEGER(11), nullable=False, comment='次数28天有库存')
    cnt_rec_s28d = mapped_column(INTEGER(11), nullable=False, comment='前28天收货次数')
    cnt_prom_s28d = mapped_column(INTEGER(11), nullable=False, comment='前28天促销次数')
    agio_s28d = mapped_column(DECIMAL(12, 2), nullable=False, comment='前28天折扣金额')
    fit_prom_s28d = mapped_column(DECIMAL(12, 2), nullable=False, comment='毛利促销28天')
    fit_s28d = mapped_column(DECIMAL(12, 2), nullable=False, comment='毛利28天')
    amt_s28d = mapped_column(DECIMAL(12, 2), nullable=False, comment='金额28天')
    amt_prom_s28d = mapped_column(DECIMAL(12, 2), nullable=False, comment='促销28天金额')
    cos_lf_s28d = mapped_column(DECIMAL(18, 6), nullable=False, comment='前28天生鲜损耗成本')
    qty_s84d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前91天数量')
    qty_x84d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前91天最大数量')
    qty_n84d = mapped_column(DECIMAL(12, 3), nullable=False, comment='前91天最小数量')
    c84d = mapped_column(INTEGER(11), nullable=False, comment='前91天次数')
    amt_s84d = mapped_column(DECIMAL(12, 2), nullable=False, comment='前91天金额')
    fit_s84d = mapped_column(DECIMAL(12, 2), nullable=False, comment='前91天毛利')
    agio_s84d = mapped_column(DECIMAL(12, 2), nullable=False, comment='前91折让金额')
    std_7d = mapped_column(INTEGER(11), nullable=False, comment='前7天标准差')
    std_28d = mapped_column(INTEGER(11), nullable=False, comment='前28天标准差')
    std_84d = mapped_column(INTEGER(11), nullable=False, comment='前91天标准差')
    days_unsale = mapped_column(INTEGER(11), nullable=False, comment='未销天数')
    days_rec_last = mapped_column(INTEGER(11), nullable=False, comment='最后收货天数')
    days_rec_first = mapped_column(INTEGER(11), nullable=False, comment='第一次收货天数')
    days_cal_in = mapped_column(INTEGER(11), nullable=False, comment='进目录天数')
    days_ws_last = mapped_column(INTEGER(11), nullable=False, comment='状态变更天数')
    days_build = mapped_column(INTEGER(11), nullable=False, comment='建档天数')


class SetBraMl(Base):
    __tablename__ = 'set_bra_ml'
    __table_args__ = {'comment': '设置-门店'}

    braid = mapped_column(INTEGER(11), primary_key=True, comment='门店ID')
    bra_name = mapped_column(String(30), nullable=False, comment='门店名称')
    bra_sname = mapped_column(String(30), nullable=False, comment='门店简称')
    bra_type = mapped_column(Enum('物流', '卖场', '社区', '便利', '总部', '-', ''), nullable=False, comment='门店类型')
    city = mapped_column(String(36), nullable=False, comment='城市')
    city_code = mapped_column(String(36), nullable=False, comment='城市代码')
    tag_bra_lv = mapped_column(String(36), nullable=False, server_default=text("''"), comment='门店等级标签')
    bra_area = mapped_column(DECIMAL(12, 3), nullable=False, server_default=text("'0.000'"), comment='门店面积')
    tag_region = mapped_column(String(36), nullable=False, server_default=text("''"), comment='区域标签')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='生效标记')
    ds_begin = mapped_column(Date, nullable=False, comment='开始日期')
    ds_end = mapped_column(Date, nullable=False, comment='结束日期')
    bra = mapped_column(String(255), Computed("(concat(`braid`,' ',`bra_sname`))", persisted=False), comment='门店')
    from_code = mapped_column(String(36), comment='数据来源')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class SetBracateM(Base):
    __tablename__ = 'set_bracate_m'
    __table_args__ = (
        Index('_idx', 'braid', 'cid', unique=True),
        {'comment': '设置-门店品类补货门店'}
    )

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    cid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='类目ID')
    dcid_def = mapped_column(INTEGER(11), nullable=False, server_default=text("'-99'"), comment='默认配送物流中心')
    isopl = mapped_column(Enum('Y', 'N'), nullable=False, server_default=text("'N'"), comment='是否自动补货')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='生效标记')
    ldt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更新时间')


class SetBraprdDi(Base):
    __tablename__ = 'set_braprd_di'
    __table_args__ = (
        Index('_idx', 'pid'),
        {'comment': '设置-门店商品'}
    )

    braid = mapped_column(INTEGER(11), nullable=False, comment='门店ID')
    dcid = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='配送部门ID')
    supid = mapped_column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='供应商ID')
    pid = mapped_column(BIGINT(20), nullable=False, comment='商品ID')
    model = mapped_column(Enum('工业品', '粮油', '生鲜', '日清', '小百货', '散称', '短保', '服饰', '-', ''), nullable=False, server_default=text("''"), comment="模式 '工业品','生鲜','日清','小百货','散称','短保'")
    sign_opl = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='补货标识1手工，2自动')
    pkg_sup = mapped_column(DECIMAL(12, 3), nullable=False, server_default=text("'0.000'"), comment='供应商整件数量')
    pkg_dist = mapped_column(DECIMAL(12, 3), nullable=False, server_default=text("'0.000'"), comment='配送整件数量')
    qty_shelf_art = mapped_column(DECIMAL(12, 3), nullable=False, server_default=text("'0.000'"), comment='货架美陈量')
    qty_shelf_max = mapped_column(DECIMAL(12, 3), nullable=False, server_default=text("'0.000'"), comment='货架满陈量')
    iscovered = mapped_column(Enum('Y', 'N'), nullable=False, server_default=text("'Y'"), comment='是否覆盖')
    remark = mapped_column(String(255), nullable=False, server_default=text("''"), comment='备注')
    shelf_code = mapped_column(String(36), nullable=False, server_default=text("''"), comment='货架码')
    shelf_type = mapped_column(String(36), comment='货架类型')
    shelf_deep = mapped_column(INTEGER(11), comment='货架深')
    shelf_stack = mapped_column(INTEGER(11), comment='货架堆叠层数')
    shelf_vertical = mapped_column(INTEGER(11), comment='陈列几层')
    shelf_count = mapped_column(INTEGER(11), comment='单层排面数')
    qty_shelf = mapped_column(INTEGER(11), Computed('((((`shelf_vertical` * `shelf_count`) * `shelf_stack`) * `shelf_deep`))', persisted=False), comment='基础排面量')
    id = mapped_column(BIGINT(20), primary_key=True, comment='序号ID')
    sid = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='数据标识 0不生效，1生效，2 测试，3假删除')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')

class SetCategoryLm(Base):
    __tablename__ = 'set_category_lm'
    __table_args__ = (
        Index('_cid', 'cid'),
        {'comment': '设置-算量类目（非ERP）'}
    )

    parentid = mapped_column(INTEGER(11), nullable=False, comment='父ID')
    cid = mapped_column(INTEGER(11), nullable=False, comment='类别ID')
    cate_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='类别名称')
    gpm_std = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'-99.00'"), comment='毛利率标准（报表统计预警）')
    gpm_ref = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'-99.00'"), comment='参考毛利率（过渡期如联营）')
    days_expiry_def = mapped_column(INTEGER(11), nullable=False, server_default=text("'-99'"), comment='默认保质期')
    storage_def = mapped_column(Enum('常温', '低温', '冷藏', '-', ''), nullable=False, server_default=text("''"), comment="默认存储条件 '常温','低温','冷藏','-',''")
    model_def = mapped_column(Enum('工业品', '生鲜', '日清', '小百货', '散称', '短保', '服饰', '-', ''), nullable=False, comment='算量模式')
    cnt_sku_ref = mapped_column(INTEGER(11), nullable=False, server_default=text("'-99'"), comment='参考品项数')
    isin = mapped_column(Enum('Y', 'N'), nullable=False, server_default=text("'N'"), comment='算量时是否包含')
    from_code = mapped_column(String(36), nullable=False, comment='来源代码')
    ds_begin = mapped_column(Date, nullable=False, comment='开始日期')
    ds_end = mapped_column(Date, nullable=False, comment='结束日期')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='环境标识')
    id = mapped_column(BIGINT(20), primary_key=True, comment='序号')
    ldt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更新时间')
    cdt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    cate = mapped_column(String(255), Computed("(concat(`cid`,' ',`cate_name`))", persisted=False), comment='类别')


class SetMatrxM(Base):
    __tablename__ = 'set_matrx_m'
    __table_args__ = {'comment': '设置-算法矩阵'}

    braid = mapped_column(INTEGER(11), nullable=False, server_default=text("'100'"), comment='门店 100总部 ')
    scenario = mapped_column(Enum('配送', '采购', '直流', '-', ''), nullable=False, comment='ERP业务场景')
    model = mapped_column(Enum('工业品', '粮油', '生鲜', '日清', '小百货', '散称', '短保', '服饰', '-', ''), nullable=False, comment="算量模式 '工业品','生鲜','日清','小百货','散称','短保'")
    level = mapped_column(Enum('主销', '畅销', '普销', '慢销', '滞销', '分货', '报货', '-', ''), nullable=False, comment="算量等级 '主销','畅销','普销','慢销','滞销','分货','报货'")
    days_interval = mapped_column(INTEGER(3), nullable=False, server_default=text("'0'"), comment='下单到收货的间隔天数T+N')
    formula_trigger = mapped_column(Enum('YES', 'NO', '安全量', '大仓量', '货架量', '报货量', '-', ''), nullable=False, comment="触发公式 'YES','NO','安全量','大仓量','货架量'")
    rat_trigger = mapped_column(INTEGER(3), nullable=False, server_default=text("'100'"), comment='触发修正系数%')
    formula_alg = mapped_column(Enum('均销', '货架', '定量', '先知', '-', ''), nullable=False, comment="计算公式 '日均','货架','定量','先知'")
    rat_alg = mapped_column(INTEGER(3), nullable=False, server_default=text("'100'"), comment='计算修正系数%')
    formula_merge = mapped_column(Enum('场景规则', '-', ''), nullable=False, comment="拟合公式 'PKG','NO'")
    rat_merge = mapped_column(INTEGER(3), nullable=False, server_default=text("'50'"), comment='拟合修正系数%')
    remark = mapped_column(String(255), nullable=False, server_default=text("''"), comment='备注')
    id = mapped_column(BIGINT(20), primary_key=True, comment='序号')
    sid = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='数据标识 0不生效，1生效，2 测试，3假删除')
    ldt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class SetPrdDi(Base):
    __tablename__ = 'set_prd_di'
    __table_args__ = (
        Index('_idx_brand', 'brand_name'),
        Index('_idx_cid', 'cid'),
        Index('_idx_name', 'prd_name'),
        {'comment': '设置-商品清单'}
    )

    cid = mapped_column(INTEGER(11), nullable=False, server_default=text("'-99'"), comment='类目ID')
    pid = mapped_column(BIGINT(18), primary_key=True, comment='商品ID')
    barcode = mapped_column(String(36), nullable=False, server_default=text("''"), comment='商品条码')
    prd_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='商品名称')
    spec = mapped_column(String(36), nullable=False, server_default=text("''"), comment='规格')
    pcs = mapped_column(String(36), nullable=False, server_default=text("''"), comment='单位')
    brand_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='品牌')
    prd_area = mapped_column(String(36), nullable=False, server_default=text("''"), comment='产地')
    pkg = mapped_column(INTEGER(11), nullable=False, comment='包装数量')
    standard = mapped_column(Enum('标品', '称重', '计数', '虚拟', '赠品', '卡券', '-', ''), nullable=False, server_default=text("''"), comment="标品 '标品','称重','计数','虚拟','赠品','卡券','-',''")
    storage = mapped_column(Enum('常温', '低温', '冷藏', '-', ''), nullable=False, server_default=text("''"), comment=" 存储条件 '常温','低温','冷藏','-',''")
    business_model = mapped_column(Enum('自营', '联营', '代销', '-', ''), nullable=False, server_default=text("''"), comment="经营模式 '自营','联营','代销','-',''")
    days_expiry = mapped_column(INTEGER(11), nullable=False, server_default=text("'-99'"), comment='保质期')
    price_sale_hq = mapped_column(DECIMAL(8, 2), nullable=False, server_default=text("'-99.00'"), comment='参考价格')
    price_pur_ld = mapped_column(DECIMAL(18, 6), nullable=False, server_default=text("'-99.000000'"), comment='最近进价')
    dio_safe_ref = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='参考安全周转天数(门店售卖时间)')
    pkg_dist_ref = mapped_column(DECIMAL(11, 3), nullable=False, server_default=text("'1.000'"), comment='参考配送数量')
    remark = mapped_column(String(255), nullable=False, server_default=text("''"), comment='备注')
    sid = mapped_column(SMALLINT(6), nullable=False, server_default=text("'0'"), comment='数据标识 0不生效 1生产 2测试 3作废')
    ldt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更新时间')
    qty_art_ref = mapped_column(DECIMAL(11, 3), comment='参考陈列量')
    tag_abc = mapped_column(String(36), comment='ABC标签')
    shelf_deep_ref = mapped_column(INTEGER(11), server_default=text("'1'"), comment='货架深')
    shelf_count_ref = mapped_column(INTEGER(11), comment='单层排面数')
    shelf_stack_ref = mapped_column(INTEGER(11), comment='货架堆叠层数')
    shelf_vertical_ref = mapped_column(INTEGER(11), comment='陈列几层')
    qty_shelf_ref = mapped_column(INTEGER(11), Computed('((((`shelf_deep_ref` * `shelf_count_ref`) * `shelf_stack_ref`) * `shelf_vertical_ref`))', persisted=False), comment='陈列量')

class SetRouterM(Base):
    __tablename__ = 'set_router_m'
    __table_args__ = {'comment': '设置-供应商路由'}

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    scenario = mapped_column(Enum('配送', '采购', '直流', '-', ''), primary_key=True, nullable=False, server_default=text("''"), comment='供应链模式 1直送大仓 2直送门店 3补货配送 4越库')
    dcid = mapped_column(INTEGER(11), primary_key=True, nullable=False, server_default=text("'0'"), comment='大仓ID')
    supid = mapped_column(BIGINT(20), primary_key=True, nullable=False, server_default=text("'0'"), comment='供应商ID')
    order_cycle = mapped_column(CHAR(7), nullable=False, server_default=text("'1234567'"), comment='自动订货周期')
    days_order = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='订单处理天数')
    remark = mapped_column(String(255), nullable=False, server_default=text("''"), comment='备注')
    sid = mapped_column(INTEGER(1), nullable=False, server_default=text("'0'"), comment='环境标识 0不生效 1生产 2测 试 3删除 4UAT 5本地')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class ShelfBraprdMa(Base):
    __tablename__ = 'shelf_braprd_ma'
    __table_args__ = {'comment': '货架-门店商品陈列信息'}

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    pid = mapped_column(BIGINT(20), primary_key=True, nullable=False, comment='商品ID')
    qty_shelf_max = mapped_column(DECIMAL(12, 3), comment='货架满陈量')
    qty_shelf_art = mapped_column(DECIMAL(12, 3), comment='货架美陈量')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class TagLevelDa(Base):
    __tablename__ = 'tag_level_da'
    __table_args__ = {'comment': '标签-算量用等级'}

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    pid = mapped_column(BIGINT(20), primary_key=True, nullable=False, comment='商品ID')
    level = mapped_column(Enum('主销', '畅销', '普销', '慢销', '滞销', '分货', '报货', '-', ''), nullable=False, comment="等级标签 '主销','畅销','普销','慢销','滞销','分配','-',''")


class TagLifecycleDa(Base):
    __tablename__ = 'tag_lifecycle_da'
    __table_args__ = {'comment': '标签-商品生命周期'}

    braid = mapped_column(INTEGER(11), primary_key=True, nullable=False, comment='门店ID')
    pid = mapped_column(BIGINT(20), primary_key=True, nullable=False, comment='商品ID')
    tag_lifecycle = mapped_column(Enum('导入期', '成长期', '成熟期', '衰退期', '-', ''), nullable=False, comment="商品生命周期 '导入期','成长期','成熟期','衰退期'")


class LogsPlm(Base):
    __tablename__ = 'logs_plm'
    __table_args__ = (
        Index('_idx', 'key_code'),
        {'comment': '日志-操作'}
    )

    key_code = mapped_column(String(36), nullable=False, server_default=text("'0'"), comment='关键字代码')
    args_in = mapped_column(JSON, nullable=False, comment='入参')
    args_out = mapped_column(JSON, nullable=False, comment='出参')
    id = mapped_column(BIGINT(20), primary_key=True, comment='自增序号')
    front_code = mapped_column(String(36), comment='来源代码')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时 间')