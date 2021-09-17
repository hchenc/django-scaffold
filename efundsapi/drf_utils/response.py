from rest_framework import response


class APIResponse(response.Response):
    def __init__(self, data=None, status=200,
                 success=None, extra=None, **kwargs):
        _data = {
            "data": data,
            "success": success if success is not None else status < 400,
            "status": status,
        }
        if isinstance(extra, dict):
            _data.update(extra)
        super(APIResponse, self).__init__(data=_data, status=status, **kwargs)

    def render(self):
        return super(APIResponse, self).render()
