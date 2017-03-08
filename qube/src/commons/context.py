
class AuthContext:
    def __init__(self, tenant_id, org_id, user_id, is_system_user):
        self.tenant_id = tenant_id
        self.org_id = org_id
        self.user_id = user_id
        self.is_system_user = is_system_user
