# 本demo主要是实现权限的逻辑
1. 请求过来在中间件中进行拦截，验证访问url是否在用户的权限列表中
2. 权限列表设置白名单，允许公共访问路劲，如注册、登录等等
3. 用户的权限列表在用户登录验证通过后，进行权限初始化，将用户的权限写入到session中，存入数据库，响应时同时以cookie的形式返回给用户，当用户再次访问，就有了权限列表，在中间件中通过校验，如果校验通过则继续走，经过路由系统匹配对应的视图函数，然后返回响应，如果不通过直接返回无权限。
4. 为了实现不同权限显示不通过的页面，设计了菜单表和权限表的对应关系，通过在权限表中设计url对应的菜单id，从而实现二级菜单的模型，（有菜单id，表示是二级菜单，没有id表示不是菜单，可能是按钮），菜单的信息也在初始化时，写入到session中，当为用户展示页面时，通过session拿到菜单列表，然后进行循环生成标签，然后返回给浏览器渲染。

# 权限主要采用RBAC的机制实现：角色权限访问控制

# 实现权限涉及的表，表与表之间的关系
1. 用户表
2. 角色表
3. 权限表     存放的时url
4. 菜单表
4. 用户角色表
5. 权限角色表
6. 权限菜单表

- 用户和角色    多对多关系：一个用户有多个角色，一个角色有多个用户
- 角色和权限    多对多关系
- 菜单和权限    一对多关系：一个菜单有多个子菜单，即一个菜单有多个权限


# 实现的过程中遇到的最大的坑？
1. 录入权限时，如果没在url前加上`/`，就会出现所有的权限都会没有权限，因为通过request.path_info获取到的路径为如：`/login/`,因此都会匹配不上而导致无权访问。
2. 还有就是在生成菜单时，如果因为上面的原因，在沈城二级菜单url时，会在当前路径下拼接，而不会从根开始，造成的结果为：`http://127.0.0.1/login/user_add/`,而实际想要的是：`http://127.0.0.1/user_add/`
