"""
性能优化装饰器
"""
import hashlib
import json
from functools import wraps
from django.core.cache import cache
from django.conf import settings

def cache_view(timeout=300, key_prefix='view'):
    """
    视图缓存装饰器
    
    Args:
        timeout: 缓存超时时间（秒）
        key_prefix: 缓存键前缀
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 管理员不使用缓存
            if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff:
                return view_func(request, *args, **kwargs)
            
            # 生成缓存键
            cache_key_parts = [
                key_prefix,
                request.path,
                request.GET.urlencode(),
                request.user.id if request.user.is_authenticated else 'anonymous'
            ]
            cache_key = hashlib.md5('|'.join(cache_key_parts).encode()).hexdigest()
            
            # 尝试从缓存获取
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # 执行视图函数
            response = view_func(request, *args, **kwargs)
            
            # 缓存响应（只缓存成功的响应）
            if response.status_code == 200:
                cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator

def cache_method_result(timeout=300, key_prefix='method'):
    """
    方法结果缓存装饰器
    
    Args:
        timeout: 缓存超时时间（秒）
        key_prefix: 缓存键前缀
    """
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # 生成缓存键
            cache_key_parts = [
                key_prefix,
                method.__name__,
                str(args),
                str(sorted(kwargs.items()))
            ]
            cache_key = hashlib.md5('|'.join(cache_key_parts).encode()).hexdigest()
            
            # 尝试从缓存获取
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行方法
            result = method(self, *args, **kwargs)
            
            # 缓存结果
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator

def cache_query_result(timeout=300, key_prefix='query'):
    """
    查询结果缓存装饰器
    
    Args:
        timeout: 缓存超时时间（秒）
        key_prefix: 缓存键前缀
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key_parts = [
                key_prefix,
                func.__name__,
                str(args),
                str(sorted(kwargs.items()))
            ]
            cache_key = hashlib.md5('|'.join(cache_key_parts).encode()).hexdigest()
            
            # 尝试从缓存获取
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行查询
            result = func(*args, **kwargs)
            
            # 缓存结果
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator
