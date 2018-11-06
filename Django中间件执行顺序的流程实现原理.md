# Django中间件执行顺序的流程实现原理
>代码模拟
>> 将每个类添加一个列表中，循环列表进行实例化，如何调用类中的方法，将方法名添加到配置好的方法列表中，
>> 循环每个存放方法名的列表，依次按顺序执行，就达到了中间件5个方法的执行顺序了

        class M1(object):
            def process_request(self, request):
                print("M1_process_request")

            def process_view(self, request, view_func, *args, **kwargs):
                print("M1_process_view")

            def process_exception(self, request, exception):
                print("M1_process_exception")

            def process_template_response(self, request, response):
                print("M1_process_template")

            def process_response(self, request, response):
                print("M1_process_response")


        class M2(object):
            def process_request(self, request):
                print("M2_process_request")

            def process_view(self, request, view_func, *args, **kwargs):
                print("M2_process_view")

            def process_exception(self, request, exception):
                print("M2_process_exception")

            def process_template_response(self, request, response):
                print("M2_process_template")

            def process_response(self, request, response):
                print("M2_process_response")


        class M3(object):
            def process_request(self, request):
                print("M3_process_request")

            def process_view(self, request, view_func, *args, **kwargs):
                print("M3_process_view")

            def process_exception(self, request, exception):
                print("M3_process_exception")

            def process_template_response(self, request, response):
                print("M3_template_response")

            def process_response(self, request, response):
                print("M3_process_response")


        # 将类放入到一个列表中
        middleware = [M1, M2, M3]

        # 创建存放5种方法的列表
        process_request_list = []
        process_view_list = []
        process_response_list = []
        process_exception_list = []
        process_template_response_list = []

        # for循环，进行每个类的实例化，并将每个方法名加入到对应[方法名]的列表
        for m in middleware:
            obj = m()  # 知识点：面向对象一旦实例化就会执行类中的__call__方法
            process_request_list.append(obj.process_request)
            process_view_list.append(obj.process_view)
            process_response_list.insert(0, obj.process_response)
            process_exception_list.append(obj.process_exception)
            process_template_response_list.append(obj.process_template_response)  # 因为response是倒序执行的

        # for循环执行对应的方法，就能按各自注册顺序执行对应方法了
        for func in process_request_list:
            func("request")
        for func in process_view_list:
            func("request", "view_func")
        for func in process_response_list:
            func("request", "response")