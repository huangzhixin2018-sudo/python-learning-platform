#!/usr/bin/env python
"""
Python学习平台性能监控脚本
用于检测和优化项目性能问题
"""

import os
import sys
import time
import psutil
import requests
from django.core.management import execute_from_command_line
from django.conf import settings
from django.db import connection
from django.test import RequestFactory
from django.core.cache import cache

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.memory_usage = []
        self.cpu_usage = []
        
    def monitor_system_resources(self):
        """监控系统资源使用情况"""
        print("🔍 系统资源监控...")
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"   CPU使用率: {cpu_percent}%")
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        print(f"   内存使用: {memory.percent}% ({memory.used // 1024 // 1024}MB / {memory.total // 1024 // 1024}MB)")
        
        # 磁盘使用情况
        disk = psutil.disk_usage('/')
        print(f"   磁盘使用: {disk.percent}% ({disk.used // 1024 // 1024 // 1024}GB / {disk.total // 1024 // 1024 // 1024}GB)")
        
        return {
            'cpu': cpu_percent,
            'memory': memory.percent,
            'disk': disk.percent
        }
    
    def check_database_connections(self):
        """检查数据库连接情况"""
        print("\n🗄️  数据库连接检查...")
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"   数据库版本: {version[0]}")
                
                # 检查连接数
                cursor.execute("SELECT count(*) FROM pg_stat_activity;")
                connections = cursor.fetchone()
                print(f"   当前连接数: {connections[0]}")
                
                # 检查慢查询
                cursor.execute("""
                    SELECT query, mean_time, calls 
                    FROM pg_stat_statements 
                    ORDER BY mean_time DESC 
                    LIMIT 5;
                """)
                slow_queries = cursor.fetchall()
                if slow_queries:
                    print("   🐌 慢查询TOP5:")
                    for query, mean_time, calls in slow_queries:
                        print(f"      {mean_time:.2f}ms ({calls}次): {query[:50]}...")
                else:
                    print("   ✅ 未发现慢查询")
                    
        except Exception as e:
            print(f"   ❌ 数据库检查失败: {e}")
    
    def check_cache_performance(self):
        """检查缓存性能"""
        print("\n💾 缓存性能检查...")
        
        # 测试缓存写入
        start_time = time.time()
        cache.set('test_key', 'test_value', 60)
        write_time = time.time() - start_time
        
        # 测试缓存读取
        start_time = time.time()
        value = cache.get('test_key')
        read_time = time.time() - start_time
        
        print(f"   缓存写入时间: {write_time*1000:.2f}ms")
        print(f"   缓存读取时间: {read_time*1000:.2f}ms")
        
        # 清理测试数据
        cache.delete('test_key')
    
    def check_static_files(self):
        """检查静态文件加载"""
        print("\n📁 静态文件检查...")
        
        static_dir = os.path.join(settings.BASE_DIR, 'static')
        if os.path.exists(static_dir):
            total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                           for dirpath, dirnames, filenames in os.walk(static_dir)
                           for filename in filenames)
            print(f"   静态文件总大小: {total_size // 1024}KB")
        else:
            print("   ⚠️  静态文件目录不存在")
    
    def generate_performance_report(self):
        """生成性能报告"""
        print("\n📊 性能优化建议:")
        
        recommendations = [
            "1. 数据库优化:",
            "   - 为频繁查询的字段添加索引",
            "   - 使用select_related和prefetch_related减少查询",
            "   - 考虑使用数据库连接池",
            "",
            "2. 缓存优化:",
            "   - 启用Redis缓存替代内存缓存",
            "   - 为热点数据设置合理的缓存时间",
            "   - 使用缓存版本控制",
            "",
            "3. 前端优化:",
            "   - 压缩和合并CSS/JS文件",
            "   - 使用CDN加速静态资源",
            "   - 实现图片懒加载",
            "   - 优化字体加载",
            "",
            "4. 服务器优化:",
            "   - 启用Gzip压缩",
            "   - 配置适当的worker进程数",
            "   - 使用负载均衡",
            "",
            "5. 代码优化:",
            "   - 避免N+1查询问题",
            "   - 使用分页减少数据传输",
            "   - 优化模板渲染",
            "   - 使用异步处理耗时操作"
        ]
        
        for rec in recommendations:
            print(rec)
    
    def run_full_check(self):
        """运行完整性能检查"""
        print("🚀 Python学习平台性能监控开始...\n")
        
        # 系统资源检查
        resources = self.monitor_system_resources()
        
        # 数据库检查
        self.check_database_connections()
        
        # 缓存检查
        self.check_cache_performance()
        
        # 静态文件检查
        self.check_static_files()
        
        # 生成报告
        self.generate_performance_report()
        
        print(f"\n⏱️  检查完成，耗时: {time.time() - self.start_time:.2f}秒")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == 'monitor':
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        
        import django
        django.setup()
        
        # 运行性能监控
        monitor = PerformanceMonitor()
        monitor.run_full_check()
    else:
        print("使用方法: python performance_monitor.py monitor")

if __name__ == '__main__':
    main()
