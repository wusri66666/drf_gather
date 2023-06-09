from rest_framework.renderers import JSONRenderer


class Response(JSONRenderer):
    """ 自定义返回数据 Json格式
    {
        "code": 0,
        "msg": "success",
        "data": { ... }
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            response = renderer_context['response']
            code = 0 if int(response.status_code / 100) == 2 else -1
            msg = 'success'
            if isinstance(data, dict):
                msg = data.pop('msg', msg)
                code = data.pop('code', code)
                if data.get("page_size"):
                    data = data
                else:
                    data = data.pop('data', data)
            if code != 0 and data:
                try:
                    msg = data.pop('detail', 'failed')
                except Exception as e:
                    msg = 'failed'
            res = {
                'code': code,
                'msg': msg,
                'data': data,
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
