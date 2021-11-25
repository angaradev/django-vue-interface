"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union, overload
from ..conf.urls import IncludedURLConf
from ..http.response import HttpResponseBase
from .resolvers import URLPattern, URLResolver

def include(arg: Any, namespace: Optional[str] = ...) -> Tuple[Sequence[Union[URLResolver, URLPattern]], Optional[str], Optional[str]]:
    ...

@overload
def path(route: str, view: Callable[..., HttpResponseBase], kwargs: Dict[str, Any] = ..., name: str = ...) -> URLPattern:
    ...

@overload
def path(route: str, view: IncludedURLConf, kwargs: Dict[str, Any] = ..., name: str = ...) -> URLResolver:
    ...

@overload
def path(route: str, view: Sequence[Union[URLResolver, str]], kwargs: Dict[str, Any] = ..., name: str = ...) -> URLResolver:
    ...

@overload
def re_path(route: str, view: Callable[..., HttpResponseBase], kwargs: Dict[str, Any] = ..., name: str = ...) -> URLPattern:
    ...

@overload
def re_path(route: str, view: IncludedURLConf, kwargs: Dict[str, Any] = ..., name: str = ...) -> URLResolver:
    ...

@overload
def re_path(route: str, view: Sequence[Union[URLResolver, str]], kwargs: Dict[str, Any] = ..., name: str = ...) -> URLResolver:
    ...

