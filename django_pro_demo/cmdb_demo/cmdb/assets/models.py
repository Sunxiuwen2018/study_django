from django.db import models
from django.contrib.auth.models import User

__all__ = ['Asset', 'Server', 'SecurityDevice',
           'StorageDevice', 'NetworkDevice', 'Software',
           'IDC', 'ManuFacturer', 'BusinessUnit', 'Contract',
           'Tag', 'Cpu', 'Ram', 'Disk', 'NIC', 'EventLog', ]

asset_type_choice = (
    ('server', '服务器'),
    ('networkdevice', '网络设备'),
    ('storagedevice', '存储设备'),
    ('securitydevice', '安全设备'),
    ('software', '软件资产'),
)


# Create your models here.
class Asset(models.Model):
    """所有资产的共有数据表"""

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, verbose_name='资产类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产序列号')
    business = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线')
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')
    manufacturer = models.ForeignKey('ManuFacturer', null=True, blank=True, verbose_name='制造商')
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理ip')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员')
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房')
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='合同')
    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买时间')
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保时间')
    price = models.FloatField(null=True, blank=True, verbose_name='价格')
    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='资产上线批准人', related_name='approved_by')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')

    def __str__(self):
        """<server> db服务器"""
        return '<%s> %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        ordering = ['-c_time']
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'


class Server(models.Model):
    """服务器设备"""
    sub_asset_type_choice = (
        (0, 'pc服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入')
    )

    asset = models.OneToOneField('Asset', verbose_name='资产类型')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='服务器类型')
    created_by = models.SmallIntegerField(choices=created_by_choice, default=0, verbose_name='添加方式')
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server',
                                  null=True, blank=True, verbose_name='宿主机')  # 虚拟机专有字段
    model = models.CharField(max_length=512, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')
    os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('发行版本', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)

    def __str__(self):
        """显示服务器信息
        资产名称--服务器类型--服务器型号 <sn:xxxxx>
        """
        return '%s--%s--%s <sn:%s>' % (self.asset.name,
                                       self.get_sub_asset_type_display(),
                                       self.model,
                                       self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name


class SecurityDevice(models.Model):
    """安全设备"""
    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '运维审计系统'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='安全设备类型')

    def __str__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display() + "id:%s" % self.id

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = verbose_name


class StorageDevice(models.Model):
    """存储设备"""
    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (4, '磁带机'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='存储设备类型')

    def __str__(self):
        return self.asset.name + '--' + self.get_sub_asset_type_display() + "id:%s" % self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = verbose_name


class NetworkDevice(models.Model):
    """网络设备"""
    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (3, 'vpn设备'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='网络设备类型')

    vlan_ip = models.GenericIPAddressField('VLanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField('内网IP', blank=True, null=True)

    model = models.CharField('网络设备型号', max_length=128, null=True, blank=True)
    firmware = models.CharField('设备固件版本', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.TextField('详细配置', null=True, blank=True)

    def __str__(self):
        return '%s--%s--%s <sn: %s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = verbose_name


class Software(models.Model):
    """只保存付费购买软件"""

    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField('软件类型', choices=sub_asset_type_choice, default=0)
    license_num = models.IntegerField(default=1, verbose_name='授权数量')
    version = models.CharField('软件/系统版本', max_length=64, unique=True, help_text='例如：CentOs release 6.7(final)')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = verbose_name


class IDC(models.Model):
    """机房"""
    name = models.CharField('机房名称', unique=True, max_length=64)
    memo = models.CharField('备注', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = verbose_name


class ManuFacturer(models.Model):
    """厂商"""
    name = models.CharField('厂商名称', unique=True, max_length=64)
    telephone = models.CharField('支持电话', max_length=30, blank=True, null=True)
    memo = models.CharField('备注', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = verbose_name


class BusinessUnit(models.Model):
    """业务线"""
    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level')
    name = models.CharField('业务线', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = verbose_name


class Contract(models.Model):
    """合同"""
    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=64)
    memo = models.TextField('备注', blank=True, null=True)
    price = models.IntegerField('合同金额')
    detail = models.TextField('合同详细', blank=True, null=True)
    start_day = models.DateField('开始日期', blank=True, null=True)
    end_day = models.DateField('失效日期', blank=True, null=True)
    license_num = models.DateField('license数量', blank=True, null=True)
    c_day = models.DateField('创建日期', auto_now_add=True)
    m_day = models.DateField('修改日期', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """资产标签"""
    name = models.CharField('标签名', max_length=32, unique=True)
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Cpu(models.Model):
    """cpu组件"""
    asset = models.OneToOneField('Asset')

    cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('物理cpu个数', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('cpu核数', default=1)

    def __str__(self):
        return self.asset.name + ": " + self.cpu_model

    class Meta:
        verbose_name = 'cpu'
        verbose_name_plural = verbose_name


class Ram(models.Model):
    """内存组件"""
    asset = models.OneToOneField('Asset')
    sn = models.CharField('sn号', max_length=128, blank=True, null=True)
    model = models.CharField('内存型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('内存制造商', max_length=128, blank=True, null=True)
    slot = models.CharField('插槽', max_length=64)
    capacity = models.IntegerField('内存大小(GB)', blank=True, null=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一


class Disk(models.Model):
    """硬盘"""
    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('UNKNOWN', 'UNKNOWN'),
    )

    asset = models.ForeignKey('Asset')
    sn = models.CharField('硬盘sn号', max_length=128)
    slot = models.CharField('所在槽位', max_length=64, blank=True, null=True)
    model = models.CharField('磁盘型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('磁盘制造商', max_length=128, blank=True, null=True)
    capacity = models.FloatField('磁盘容量(GB', blank=True, null=True)
    interface_type = models.CharField('接口类型', max_length=16, choices=disk_interface_type_choice, default='UNKNOWN')

    def __str__(self):
        return '{}: {}: {}GB'.format(self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'sn')


class NIC(models.Model):
    """网卡组件"""
    asset = models.ForeignKey('Asset')
    name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
    model = models.CharField('网卡型号', max_length=128)
    mac = models.CharField('MAC地址', max_length=64)
    ip_address = models.GenericIPAddressField('ip地址', blank=True, null=True)
    net_mask = models.CharField('子网掩码', max_length=64, blank=True, null=True)
    bonding = models.CharField('绑定地址', max_length=64, blank=True, null=True)

    def __str__(self):
        return f'{self.asset.name}: {self.model}: {self.mac}'

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'model', 'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。


class EventLog(models.Model):
    """
    日志
    在关联对象被删除的时候，不能一并删除，需保留日志
    因此，on_delete = models.SET_NULL
    """
    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
    )
    name = models.CharField('事件名称', max_length=128)
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True,
                                  on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=4)
    component = models.CharField('事件子项', max_length=256, blank=True, null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    # 自动更新资产数据时没有执行人
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人', on_delete=models.SET_NULL)
    memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = verbose_name


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    sn = models.CharField('资产sn号', max_length=128, unique=True)
    asset_type = models.CharField("资产类型", choices=asset_type_choice,
                                  default='server',
                                  max_length=64, null=True, blank=True)

    manufacturer = models.CharField('生产厂商', max_length=64, blank=True, null=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    ram_size = models.PositiveSmallIntegerField('内存大小', blank=True, null=True)
    cpu_model = models.CharField('cpu型号', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('物理cpu个数', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField('cpu核数', blank=True, null=True)
    os_distribution = models.CharField('系统厂商', max_length=64, blank=True, null=True)
    os_type = models.CharField('系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField('系统发行版', max_length=64, blank=True, null=True)

    data = models.TextField('资产数据')

    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']