from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# ========== 原有模型 ==========

class Tag(models.Model):
    """文章标签模型"""
    name = models.CharField(_("标签名称"), max_length=50, unique=True)
    slug = models.SlugField(_("URL别名"), max_length=50, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = _("标签")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class MainCategory(models.Model):
    """主分类模型"""
    name = models.CharField(_("主分类名称"), max_length=100, unique=True)
    slug = models.SlugField(_("URL别名"), max_length=100, unique=True, allow_unicode=True)
    order = models.PositiveIntegerField(_("排序权重"), default=0, help_text=_("数字越大，排序越靠后"))
    is_enabled = models.BooleanField(_("是否启用"), default=True)
    icon = models.CharField(_("图标类名"), max_length=50, blank=True, null=True, help_text=_("例如：fas fa-book"))
    description = models.TextField(_("描述"), blank=True, null=True)

    class Meta:
        verbose_name = _("主分类")
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """子分类模型"""
    parent = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories', verbose_name=_("所属主分类"))
    name = models.CharField(_("子分类名称"), max_length=100)
    slug = models.SlugField(_("URL别名"), max_length=100, allow_unicode=True)
    is_enabled = models.BooleanField(_("是否启用"), default=True)
    icon = models.CharField(_("图标类名"), max_length=50, blank=True, null=True)
    description = models.TextField(_("描述"), blank=True, null=True)

    class Meta:
        verbose_name = _("子分类")
        verbose_name_plural = verbose_name
        unique_together = ('parent', 'name') # 同一主分类下，子分类名称不能重复
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} -> {self.name}"

class Article(models.Model):
    """文章模型"""
    class ContentType(models.TextChoices):
        GRAMMAR = 'GR', _('语法')
        DATA_STRUCTURE = 'DS', _('数据结构')
        AI_PROGRAMMING = 'AI', _('AI编程')

    title = models.CharField(_("文章标题"), max_length=200)
    subtitle = models.CharField(_("副标题"), max_length=200, blank=True, null=True)
    summary = models.TextField(_("摘要"))
    content_type = models.CharField(_("内容类型"), max_length=2, choices=ContentType.choices, default=ContentType.GRAMMAR)
    read_time_minutes = models.PositiveIntegerField(_("预计阅读时间"), default=5)
    
    content_html = models.TextField(_("富文本内容"), help_text=_("用于存储TinyMCE编辑器的HTML内容"))
    content_code = models.TextField(_("代码内容"), blank=True, null=True, help_text=_("用于存储Monaco编辑器的代码"))
    code_language = models.CharField(_("代码语言"), max_length=50, default='python')

    category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("所属分类"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("标签"))

    is_published = models.BooleanField(_("是否发布"), default=False)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("文章")
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def clean(self):
        """模型验证"""
        if self.is_published:
            if not self.title or self.title.strip() == '':
                raise ValidationError(_('发布时文章标题不能为空'))
            if not self.category:
                raise ValidationError(_('发布时必须选择文章分类'))
            if not self.summary or self.summary.strip() == '':
                raise ValidationError(_('发布时文章摘要不能为空'))
            if not self.content_html or self.content_html.strip() == '':
                raise ValidationError(_('发布时文章内容不能为空'))
            
    def save(self, *args, **kwargs):
        """保存前的验证"""
        if self.is_published:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# ========== 函数库相关模型 ==========

class Library(models.Model):
    """库信息模型"""
    library_id = models.AutoField(_("库ID"), primary_key=True)
    library_name = models.CharField(_("库名称"), max_length=100, unique=True)
    library_name_cn = models.CharField(_("库中文名称"), max_length=100)
    description = models.TextField(_("描述"), blank=True, null=True)
    version = models.CharField(_("版本"), max_length=50, blank=True, null=True)
    category = models.CharField(_("分类"), max_length=100, blank=True, null=True)
    is_builtin = models.BooleanField(_("是否内置"), default=False)
    is_standard = models.BooleanField(_("是否标准库"), default=False)
    library_type = models.CharField(_("库类型"), max_length=100, default="standard")
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("库信息")
        verbose_name_plural = verbose_name
        db_table = 'function_library'

    def __str__(self):
        return f"{self.library_name} ({self.library_name_cn})"

class Module(models.Model):
    """模块信息模型"""
    module_id = models.AutoField(_("模块ID"), primary_key=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='modules', verbose_name=_("所属库"))
    module_name = models.CharField(_("模块名称"), max_length=100)
    module_name_cn = models.CharField(_("模块中文名称"), max_length=100, default="")
    description = models.TextField(_("描述"), blank=True, null=True)
    source_file = models.CharField(_("源文件"), max_length=200, blank=True, null=True)
    is_builtin = models.BooleanField(_("是否内置"), default=False)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("模块信息")
        verbose_name_plural = verbose_name
        db_table = 'function_module'
        unique_together = ('library', 'module_name')

    def __str__(self):
        return f"{self.library.library_name}.{self.module_name}"

class OperationType(models.Model):
    """操作类型模型"""
    operation_type_id = models.AutoField(_("操作类型ID"), primary_key=True)
    operation_name = models.CharField(_("操作类型名称"), max_length=100, unique=True)
    operation_name_cn = models.CharField(_("操作类型中文名称"), max_length=100)
    description = models.TextField(_("描述"), blank=True, null=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("操作类型")
        verbose_name_plural = verbose_name
        db_table = 'function_operation_type'

    def __str__(self):
        return f"{self.operation_name} ({self.operation_name_cn})"

class Function(models.Model):
    """函数信息模型"""
    function_id = models.AutoField(_("函数ID"), primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='functions', verbose_name=_("所属模块"))
    function_name = models.CharField(_("函数名称"), max_length=200)
    function_name_cn = models.CharField(_("函数中文名称"), max_length=200, blank=True, null=True)
    description = models.TextField(_("描述"), blank=True, null=True)
    description_cn = models.TextField(_("中文描述"), blank=True, null=True)
    operation_type = models.ForeignKey(OperationType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("操作类型"))
    syntax = models.TextField(_("语法"), blank=True, null=True)
    parameters_text = models.TextField(_("参数"), blank=True, null=True)
    return_value = models.TextField(_("返回值"), blank=True, null=True)
    return_value_cn = models.TextField(_("返回值中文"), blank=True, null=True)
    example = models.TextField(_("示例"), blank=True, null=True)
    example_cn = models.TextField(_("中文示例"), blank=True, null=True)
    availability = models.CharField(_("可用性"), max_length=100, blank=True, null=True)
    version_added = models.CharField(_("添加版本"), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("函数信息")
        verbose_name_plural = verbose_name
        db_table = 'function_info'
        unique_together = ('module', 'function_name')

    def __str__(self):
        return f"{self.module}.{self.function_name}"

class Parameter(models.Model):
    """参数信息模型"""
    parameter_id = models.AutoField(_("参数ID"), primary_key=True)
    function = models.ForeignKey(Function, on_delete=models.CASCADE, related_name='parameters', verbose_name=_("所属函数"))
    parameter_name = models.CharField(_("参数名称"), max_length=100)
    parameter_name_cn = models.CharField(_("参数中文名称"), max_length=100, blank=True, null=True)
    data_type = models.CharField(_("数据类型"), max_length=100, blank=True, null=True)
    is_required = models.BooleanField(_("是否必需"), default=True)
    default_value = models.CharField(_("默认值"), max_length=200, blank=True, null=True)
    description = models.TextField(_("描述"), blank=True, null=True)
    description_cn = models.TextField(_("中文描述"), blank=True, null=True)
    constraints = models.TextField(_("约束条件"), blank=True, null=True)
    parameter_type = models.CharField(_("参数类型"), max_length=100, default="positional")
    position = models.IntegerField(_("位置"), default=0)
    example_usage = models.TextField(_("使用示例"), blank=True, null=True)

    class Meta:
        verbose_name = _("参数信息")
        verbose_name_plural = verbose_name
        db_table = 'function_parameter'
        unique_together = ('function', 'parameter_name')

    def __str__(self):
        return f"{self.function.function_name}.{self.parameter_name}"