from qube.src.models.hello import Hello
from qube.src.commons.error import ErrorCodes, HelloServiceError
from qube.src.commons.utils import clean_nonserializable_attributes
import time


class HelloService:
    def __init__(self, context):
        self.auth_context = context

    def find_hello_by_id(self, entity_id):
        # filter with id not working,
        # unable to proceed with tenant filter
        data = Hello.query.get(entity_id)
        if data is None:
            raise HelloServiceError('hello ' +
                                    entity_id + ' not found',
                                    ErrorCodes.NOT_FOUND)

        hello_data = data.wrap()
        clean_nonserializable_attributes(hello_data)
        return hello_data

    def get_all_hellos(self):
        hello_list = []
        data = Hello.query.filter(Hello.tenantId ==
                                  self.auth_context.tenant_id)
        for hello_data_item in data:
            hello_data = hello_data_item.wrap()
            clean_nonserializable_attributes(hello_data)
            hello_list.append(hello_data)
        return hello_list

    def save_hello(self, hello_model):
        new_hello = Hello()
        for key in hello_model:
            new_hello.__setattr__(key, hello_model[key])
        hello_data = new_hello
        hello_data.tenantId = self.auth_context.tenant_id
        hello_data.orgId = self.auth_context.org_id
        hello_data.createdBy = self.auth_context.user_id
        hello_data.createdDate = str(int(time.time()))
        hello_data.modifiedBy = self.auth_context.user_id
        hello_data.modifiedDate = str(int(time.time()))
        hello_data.save()
        hello_result = hello_data.wrap()

        clean_nonserializable_attributes(hello_result)
        return hello_result

    def update_hello(self, hello_model, entity_id):

        hello_record = Hello.query.get(entity_id)  # Hello is a mongo class
        if hello_record is None:
            raise HelloServiceError('hello ' + entity_id +
                                    ' not found', ErrorCodes.NOT_FOUND)

        for key in hello_model:
            hello_record.__setattr__(key, hello_model[key])
        hello_record.modifiedBy = self.auth_context.user_id
        hello_record.modifiedDate = str(int(time.time()))
        hello_record.save()
        hello_result = hello_record.wrap()
        clean_nonserializable_attributes(hello_result)
        return hello_result

    def delete_hello(self, entity_id):
        hello = Hello.query.get(entity_id)
        if hello is None:
            raise HelloServiceError('hello ' + entity_id +
                                    ' not found', ErrorCodes.NOT_FOUND)
        hello.remove()
