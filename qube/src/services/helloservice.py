from qube.src.models.hello import Hello
from qube.src.commons.error import ErrorCodes,HelloServiceError
from qube.src.commons.utils import clean_nonserializable_attributes
import time


class HelloService():

    def find_hello_by_id(self,id):
        data = Hello.query.get(id)  # filter with id not working, unable to proceed with tenant filter
        if data is None:
            raise HelloServiceError('hello '+id+' not found',ErrorCodes.NOT_FOUND)

        hello_data = data.wrap()
        clean_nonserializable_attributes(hello_data)
        return hello_data

    def get_all_hellos(self,tenantId):
        hello_list = []
        data = Hello.query.filter(Hello.tenantId == tenantId)
        for hello_data_item in data:
            hello_data = hello_data_item.wrap()
            clean_nonserializable_attributes(hello_data)
            hello_list.append(hello_data)
        return hello_list

    def save_hello(self,hello_model,tenant_id, org_id, user_id):
        new_hello = Hello();
        for key in hello_model:
            new_hello.__setattr__(key, hello_model[key])
        hello_data = new_hello
        hello_data.tenantId = tenant_id
        hello_data.orgId = org_id
        hello_data.createdBy = user_id
        hello_data.createdDate = str(int(time.time()))
        hello_data.modifiedBy = user_id
        hello_data.modifiedDate = str(int(time.time()))
        hello_data.save()
        hello_result = hello_data.wrap()

        clean_nonserializable_attributes(hello_result)
        return hello_result

    def update_hello(self,hello_model,tenant_id,user_id,id):

        hello_record = Hello.query.get(id)  # Hello is a mongo class
        if hello_record is None:
            raise HelloServiceError('hello ' + id + ' not found', ErrorCodes.NOT_FOUND)

        for key in hello_model:
            hello_record.__setattr__(key, hello_model[key])
        hello_record.modifiedBy = user_id
        hello_record.modifiedDate = str(int(time.time()))
        hello_record.save()

    def delete_hello(self,tenantId,id):
        hello = Hello.query.get(id)
        if hello is None:
            raise HelloServiceError('hello ' + id + ' not found', ErrorCodes.NOT_FOUND)
        hello.remove()