from tortoise import Model, fields


class RequestLog(Model):
    path = fields.CharField(max_length=200)
    method = fields.CharField(max_length=10)
    time = fields.FloatField()
    status_code = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        indexes = [("created_at", "path", "method", "status_code")]
        ordering = ["-id"]
