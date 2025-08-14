#!/usr/bin/env python
"""
生产环境数据导入脚本
从Excel文件导入函数库数据到生产数据库
"""

import os
import sys
import django
import pandas as pd

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings_production')
django.setup()

from Pythonfun.models import Library, Module, OperationType, Function, Parameter

def import_excel_data():
    """从Excel文件导入数据到生产数据库"""
    try:
        # 读取Excel文件
        xl = pd.ExcelFile('templates/OS模块函数数据库_最终版.xlsx')
        print("🚀 开始导入Excel数据到生产环境...")
        
        # 1. 导入库信息
        print("\n=== 导入库信息 ===")
        df_library = pd.read_excel(xl, '库信息')
        for _, row in df_library.iterrows():
            library, created = Library.objects.get_or_create(
                library_id=row['library_id'],
                defaults={
                    'library_name': row['library_name'],
                    'library_name_cn': row['library_name_cn'],
                    'description': row.get('description', ''),
                    'version': row.get('version', ''),
                    'category': row.get('category', ''),
                    'is_builtin': row.get('is_builtin', False),
                    'is_standard': row.get('is_standard', False),
                }
            )
            if created:
                print(f"✅ 创建库: {library.library_name}")
            else:
                print(f"ℹ️  库已存在: {library.library_name}")
        
        # 2. 导入模块信息
        print("\n=== 导入模块信息 ===")
        df_module = pd.read_excel(xl, '模块信息')
        for _, row in df_module.iterrows():
            library = Library.objects.get(library_id=row['library_id'])
            module, created = Module.objects.get_or_create(
                module_id=row['module_id'],
                defaults={
                    'library': library,
                    'module_name': row['module_name'],
                    'description': row.get('description', ''),
                    'is_builtin': row.get('is_builtin', False),
                }
            )
            if created:
                print(f"✅ 创建模块: {module.module_name}")
            else:
                print(f"ℹ️  模块已存在: {module.module_name}")
        
        # 3. 导入操作类型
        print("\n=== 导入操作类型 ===")
        df_operation = pd.read_excel(xl, '操作类型')
        for _, row in df_operation.iterrows():
            operation, created = OperationType.objects.get_or_create(
                operation_type_id=row['operation_type_id'],
                defaults={
                    'operation_name': row['operation_name'],
                    'operation_name_cn': row['operation_name_cn'],
                    'description': row.get('description', ''),
                }
            )
            if created:
                print(f"✅ 创建操作类型: {operation.operation_name}")
            else:
                print(f"ℹ️  操作类型已存在: {operation.operation_name}")
        
        # 4. 导入函数信息
        print("\n=== 导入函数信息 ===")
        df_function = pd.read_excel(xl, '函数信息')
        for _, row in df_function.iterrows():
            module = Module.objects.get(module_id=row['module_id'])
            operation_type = None
            if pd.notna(row.get('operation_type_id')):
                operation_type = OperationType.objects.get(operation_type_id=row['operation_type_id'])
            
            function, created = Function.objects.get_or_create(
                function_id=row['function_id'],
                defaults={
                    'module': module,
                    'function_name': row['function_name'],
                    'function_name_cn': row.get('function_name_cn', ''),
                    'description': row.get('description', ''),
                    'description_cn': row.get('description_cn', ''),
                    'operation_type': operation_type,
                    'syntax': row.get('syntax', ''),
                    'parameters_text': row.get('parameters', ''),
                    'return_value': row.get('return_value', ''),
                    'return_value_cn': row.get('return_value_cn', ''),
                    'example': row.get('example', ''),
                    'example_cn': row.get('example_cn', ''),
                    'availability': row.get('availability', ''),
                    'version_added': row.get('version_added', ''),
                }
            )
            if created:
                print(f"✅ 创建函数: {function.function_name}")
            else:
                print(f"ℹ️  函数已存在: {function.function_name}")
        
        # 5. 导入参数信息
        print("\n=== 导入参数信息 ===")
        df_parameter = pd.read_excel(xl, '参数信息')
        for _, row in df_parameter.iterrows():
            function = Function.objects.get(function_id=row['function_id'])
            parameter, created = Parameter.objects.get_or_create(
                parameter_id=row['parameter_id'],
                defaults={
                    'function': function,
                    'parameter_name': row['parameter_name'],
                    'parameter_name_cn': row.get('parameter_name_cn', ''),
                    'data_type': row.get('data_type', ''),
                    'is_required': row.get('is_required', True),
                    'default_value': row.get('default_value', ''),
                    'description': row.get('description', ''),
                    'description_cn': row.get('description_cn', ''),
                }
            )
            if created:
                print(f"✅ 创建参数: {parameter.parameter_name}")
            else:
                print(f"ℹ️  参数已存在: {parameter.parameter_name}")
        
        print("\n🎉 数据导入完成！")
        print(f"📊 数据库统计:")
        print(f"   - 库数量: {Library.objects.count()}")
        print(f"   - 模块数量: {Module.objects.count()}")
        print(f"   - 操作类型数量: {OperationType.objects.count()}")
        print(f"   - 函数数量: {Function.objects.count()}")
        print(f"   - 参数数量: {Parameter.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入数据时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = import_excel_data()
    sys.exit(0 if success else 1)
