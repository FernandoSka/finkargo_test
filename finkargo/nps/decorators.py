import httpagentparser



def add_meta_info(func):

    def inner(view_func, request, *args, **kwargs):
        try:
            agent = request.META["HTTP_USER_AGENT"]
            operative_sistem = httpagentparser.detect(agent)["os"]
            browser = httpagentparser.detect(agent)["browser"]
            request.data._mutable=True
            request.data.update({
                "operative_sistem": f'{operative_sistem["name"]} {operative_sistem["version"]}',
                "browser": f'{browser["name"]} {browser["version"]}'
            })
        except Exception:
            pass
        return func(view_func, request, *args,*kwargs)
    return inner