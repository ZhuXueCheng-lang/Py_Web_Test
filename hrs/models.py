from django.db import models


class Dept(models.Model):
    def __str__(self):
        return self.name
    """部门类"""

    no = models.IntegerField(primary_key=True, db_column='dno', verbose_name='部门编号')
    name = models.CharField(max_length=20, db_column='dname', verbose_name='部门名称')
    location = models.CharField(max_length=10, db_column='dloc', verbose_name='部门所在地')

    class Meta:
        db_table = 'tb_dept'


class Emp(models.Model):
    def __str__(self):
        return self.name
    """员工类"""

    no = models.IntegerField(primary_key=True, db_column='eno', verbose_name='员工编号')
    name = models.CharField(max_length=20, db_column='ename', verbose_name='员工姓名')
    job = models.CharField(max_length=10, verbose_name='职位')
    # 多对一外键关联(自参照)
    mgr = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='主管')
    sal = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='月薪')
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='补贴')
    # 多对一外键关联(参照部门模型)
    dept = models.ForeignKey(Dept, db_column='dno', on_delete=models.PROTECT, verbose_name='所在部门')

    class Meta:
        db_table = 'tb_emp'

class Film(models.Model):
    def __str__(self):
        return self.name
    """资源类"""

    id = models.IntegerField(primary_key=True, db_column='id', verbose_name='主键id')
    name = models.CharField(max_length=50, db_column='name', verbose_name='资源名字')
    type = models.CharField(max_length=50, db_column='type', verbose_name='资源类型')
    Torrent = models.CharField(max_length=50, db_column='torrent', verbose_name='种子地址')
    FilmURL= models.CharField(max_length=50, db_column='FilmURL', verbose_name='网页URL')
    # 多对一外键关联(自参照)

    big = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='大小')

    class Meta:
        db_table = 'h_film'
class Img (models.Model):
    def __str__(self):
        return self.imgURL
    id = models.AutoField(primary_key=True, db_column='img_id', verbose_name='主键id')
    FilmID=models.ForeignKey(Film, db_column='id', on_delete=models.PROTECT, verbose_name='所属资源')
    imgURL=models.CharField(max_length=50, db_column='img', verbose_name='图片地址')
    class Meta:
        db_table = 'img'